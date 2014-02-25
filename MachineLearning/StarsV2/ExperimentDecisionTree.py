'''
Created on 02/12/2013

@author: thiagocastroferreira
'''

import numpy as np
import Assurance as ass
import ParserStars as parser
import DecisionTree2 as tree

def run(dominios, targets, folds, atributos, participantes, incluirParticipante):
    featureVector = parser.parseFeatureVector(dominios, targets)
    
    inputs = {}
    frequencias = {}
    for fold in folds:
        frequencias[fold] = countAttributeFrequency(folds, fold)
        participantes[fold] = parser.descriptionsMeans(folds, fold, dominios)
        inputs[fold] = parser.parseSVMInput(folds[fold], featureVector, participantes[fold], frequencias[fold], incluirParticipante)
    
    resultadoTotal = []
    dice = []
    masi = []
    acuracia = 0.0
    
#     print 10 * "*"
#     if incluirParticipante == True:
#         print "SVM com o id do participante"
#     else:
#         print "SVM sem o id do participante"
#     print 10 * "*"
    
    for fold in ["1","2","3","4","5","6"]:
#         print "FOLD: " + fold
        resultados = tree.run(inputs, fold)
        resultadoTotal.append(resultados)
        acertos = resultados[0]
        total = resultados[1]
        expressoes = resultados[2]
        
        tp = resultados[3]
        tn = resultados[4]
        fp = resultados[5]
        fn = resultados[6]
        
        for expressao in expressoes:
            contexto = expressao["anotacao"]["caracteristicas"]["context"]
            
            descricao = defineExpressao(expressao["previsoes"], dominios[contexto], targets[contexto])
            descricaoR = expressao["anotacao"]["descricao"]
            
            A = ass.parse(descricao)
            B = ass.parse(descricaoR)
            
            DICE = ass.dice(A, B)
            MASI = ass.masi(A, B)
            
#             print descricao
#             print descricaoR
#             print DICE
#             print 10 * "*"
            
            if DICE == 1.0:
                acuracia = acuracia + 1.0
            
            dice.append(DICE)
            masi.append(MASI)
#             if expressao["previsoes"]["relation"] > 0:
#                 print "Descricao Prevista : " + str(expressao["previsoes"])
#                 print "Descricao Prevista : " + str(descricao)
#                 print "Descricao Real : " + str(expressao["classes"])
#                 print "Descricao Real : " + str(descricaoR)
#                 print "Dice: " + str(DICE)
#                 print 30 * "-"
        
#         for atributo in acertos.keys():
#             print "Atributo: " + str(atributo)
#             print "Acuracia: " + str(acertos[atributo] / total[atributo])
# #             print "Verdadeiros Positivos: " + str(tp[atributo])
# #             print "Falsos Positivos: " + str(fp[atributo])
# #             print "Verdadeiros Negativos: " + str(tn[atributo])
# #             print "Falsos Negativos: " + str(fn[atributo])
#             print 10 * "-"
#          
#         print 50 * "*"
        
#     print 50 * "*"
#     print "Expressoes: "
#     print "Dice Total: " + str(np.mean(dice))
#     print "Masi Total: " + str(np.mean(masi))
#     print "Acuracia: " + str(acuracia / len(dice))
#     print 50 * "*"

    acertosT = {}
    totalT = {}
    
    for resultados in resultadoTotal:
        acertos = resultados[0]
        total = resultados[1]
        
        for atributo in acertos.keys():
            if atributo not in acertosT:
                acertosT[atributo] = 0.0
                totalT[atributo] = 0.0
            
            acertosT[atributo] = acertosT[atributo] + acertos[atributo]
            totalT[atributo] = totalT[atributo] + total[atributo]
            
#     for atributo in acertosT.keys():
#         print "Atributo: " + str(atributo)
#         print "Acuracia: " + str(acertosT[atributo] / totalT[atributo])
#         print 10 * "-"
        
    return resultadoTotal, dice, masi, acuracia

#contabiliza frequenca dos atributos
def countAttributeFrequency(folds, teste):
    foldsAux = {}
    
    for fold in folds:
        if fold != teste:
            foldsAux[fold] = folds[fold]
            
    frequency = {}
    
    for fold in foldsAux:
        for participante in folds[fold]:
            for anotacao in folds[fold][participante]:
                target = anotacao["caracteristicas"]["target"]
                
                if participante not in frequency.keys():
                    frequency[participante] = {}
                    frequency[participante]["target"] = {}
                    frequency[participante]["landmark"] = {}
                
                for objeto in anotacao["descricao"]:
                    for key in anotacao["descricao"][objeto].keys():
                        if objeto == target:
                            if key in frequency[participante]["target"].keys():
                                frequency[participante]["target"][key] = frequency[participante]["target"][key] + 1
                            else:
                                frequency[participante]["target"][key] = 1
                        else:
                            if key in frequency[participante]["landmark"].keys():
                                frequency[participante]["landmark"][key] = frequency[participante]["landmark"][key] + 1
                            else:
                                frequency[participante]["landmark"][key] = 1
    return frequency
    return frequency

def defineExpressao(previsoes, dominio, target):
    #descricao prevista pela svm
    descricao = {}
    
    descricao[target] = {}
    
    for atributo in dominio[target].keys():
        descricao[target][atributo] = dominio[target][atributo]
    
    relacional = False
    landmark = str
    second_landmark = ""
    for atributo in ["type", "colour", "hpos", "vpos", "relation", "lm_type", "lm_colour", "lm_hpos", "lm_vpos", "lm_relation", "lm2_type", "lm2_colour", "lm2_hpos", "lm2_vpos"]:
        element = atributo.split("_")
        
        if len(element) == 1 and atributo != "relation":
            if previsoes[atributo] == 0:
                if atributo in descricao[target].keys():
                    del descricao[target][atributo]
        
        elif len(element) == 2 and relacional == True and element[1] != "relation":
            if element[0] == "lm":
                if previsoes[atributo] == 0:
                    del descricao[landmark][element[1]]
            else:
                if previsoes[atributo] == 0:
                    if second_landmark in descricao.keys():
                        del descricao[second_landmark][element[1]]
        
        elif len(element) == 2 and relacional == True and element[1] == "relation":
            if previsoes[atributo] == 0:
                del descricao[landmark]["below"]
                del descricao[landmark]["above"]
                del descricao[landmark]["near"]
                del descricao[landmark]["right"]
                del descricao[landmark]["left"]
            else:
                if previsoes[atributo] == 1:
                    del descricao[landmark]["below"]
                    del descricao[landmark]["above"]
                    del descricao[landmark]["right"]
                    del descricao[landmark]["left"]
                    
                    if len(descricao[landmark]["near"]) == 0:
                        del descricao[landmark]["near"]
                    else:
                        second_landmark = descricao[landmark]["near"][0]
                        descricao[second_landmark] = {}
                        
                        for key in dominio[second_landmark].keys():
                            if key not in ["near", "left", "right", "below", "above"]:
                                descricao[second_landmark][key] = dominio[second_landmark][key]
                
                elif previsoes[atributo] == 2:
                    del descricao[landmark]["above"]
                    del descricao[landmark]["below"]
                    del descricao[landmark]["near"]
                    del descricao[landmark]["right"]
                    
                    if len(descricao[landmark]["left"]) == 0:
                        del descricao[landmark]["left"]
                    else:
                        second_landmark = descricao[landmark]["left"][0]
                        descricao[second_landmark] = {}
                        
                        for key in dominio[second_landmark].keys():
                            if key not in ["near", "left", "right", "below", "above"]:
                                descricao[second_landmark][key] = dominio[second_landmark][key]
                
                elif previsoes[atributo] == 3:
                    del descricao[landmark]["below"]
                    del descricao[landmark]["near"]
                    del descricao[landmark]["right"]
                    del descricao[landmark]["left"]
                    
                    if len(descricao[landmark]["above"]) == 0:
                        del descricao[landmark]["above"]
                    else:
                        second_landmark = descricao[landmark]["above"][0]
                        descricao[second_landmark] = {}
                        
                        for key in dominio[second_landmark].keys():
                            if key not in ["near", "left", "right", "below", "above"]:
                                descricao[second_landmark][key] = dominio[second_landmark][key]
                
                elif previsoes[atributo] == 4:
                    del descricao[landmark]["above"]
                    del descricao[landmark]["below"]
                    del descricao[landmark]["near"]
                    del descricao[landmark]["left"]
                    
                    if len(descricao[landmark]["right"]) == 0:
                        del descricao[landmark]["right"]
                    else:
                        second_landmark = descricao[landmark]["right"][0]
                        descricao[second_landmark] = {}
                        
                        for key in dominio[second_landmark].keys():
                            if key not in ["near", "left", "right", "below", "above"]:
                                descricao[second_landmark][key] = dominio[second_landmark][key]
                
                elif previsoes[atributo] == 5:
                    del descricao[landmark]["above"]
                    del descricao[landmark]["near"]
                    del descricao[landmark]["right"]
                    del descricao[landmark]["left"]
                    
                    if len(descricao[landmark]["below"]) == 0:
                        del descricao[landmark]["below"]
                    else:
                        second_landmark = descricao[landmark]["below"][0]
                        descricao[second_landmark] = {}
                        
                        for key in dominio[second_landmark].keys():
                            if key not in ["near", "left", "right", "below", "above"]:
                                descricao[second_landmark][key] = dominio[second_landmark][key]
        
        elif len(element) == 1 and atributo == "relation":
            if previsoes[atributo] == 0:
                del descricao[target]["below"]
                del descricao[target]["above"]
                del descricao[target]["near"]
                del descricao[target]["right"]
                del descricao[target]["left"]
            else:
                if previsoes[atributo] == 1:
                    del descricao[target]["below"]
                    del descricao[target]["above"]
                    del descricao[target]["right"]
                    del descricao[target]["left"]
                    
                    if len(descricao[target]["near"]) == 0:
                        del descricao[target]["near"]
                    else:
                        landmark = descricao[target]["near"][0]
                        descricao[landmark] = {}
                        relacional = True
                        
                        for key in dominio[landmark].keys():
                            descricao[landmark][key] = dominio[landmark][key]
                
                elif previsoes[atributo] == 2:
                    del descricao[target]["above"]
                    del descricao[target]["below"]
                    del descricao[target]["near"]
                    del descricao[target]["right"]
                    
                    if len(descricao[target]["left"]) == 0:
                        del descricao[target]["left"]
                    else:
                        landmark = descricao[target]["left"][0]
                        descricao[landmark] = {}
                        relacional = True
                        
                        for key in dominio[landmark].keys():
                            descricao[landmark][key] = dominio[landmark][key]
                
                elif previsoes[atributo] == 3:
                    del descricao[target]["below"]
                    del descricao[target]["near"]
                    del descricao[target]["right"]
                    del descricao[target]["left"]
                    
                    if len(descricao[target]["above"]) == 0:
                        del descricao[target]["above"]
                    else:
                        landmark = descricao[target]["above"][0]
                        descricao[landmark] = {}
                        relacional = True
                        
                        for key in dominio[landmark].keys():
                            descricao[landmark][key] = dominio[landmark][key]
                
                elif previsoes[atributo] == 4:
                    del descricao[target]["above"]
                    del descricao[target]["below"]
                    del descricao[target]["near"]
                    del descricao[target]["left"]
                    
                    if len(descricao[target]["right"]) == 0:
                        del descricao[target]["right"]
                    else:
                        landmark = descricao[target]["right"][0]
                        descricao[landmark] = {}
                        relacional = True
                        
                        for key in dominio[landmark].keys():
                            descricao[landmark][key] = dominio[landmark][key]
                
                elif previsoes[atributo] == 5:
                    del descricao[target]["above"]
                    del descricao[target]["near"]
                    del descricao[target]["right"]
                    del descricao[target]["left"]
                    
                    if len(descricao[target]["below"]) == 0:
                        del descricao[target]["below"]
                    else:
                        landmark = descricao[target]["below"][0]
                        descricao[landmark] = {}
                        relacional = True
                        
                        for key in dominio[landmark].keys():
                            descricao[landmark][key] = dominio[landmark][key]
    return descricao