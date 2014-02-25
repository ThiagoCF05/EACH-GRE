'''
Created on 02/12/2013

@author: thiagocastroferreira
'''

import Assurance as ass
import ParserGRE3D as parser
import numpy as np
import SVM2 as svm

def run(dominios, targets, folds, atributos, participantes, incluirParticipante):
    featureVector = parser.parseFeatureVector(dominios, targets)
    inputs = {}
    
    inputs = {}
    for fold in folds:
        frequencias = countAttributeFrequencyIndividual(folds, fold)
        inputs[fold] = parser.parseSVMInput(folds[fold], featureVector, participantes, frequencias, incluirParticipante)
        
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
    for fold in ["1","2","3","4","5","6","7","8","9","10"]:
        print "FOLD: " + fold
        resultados = svm.run(inputs, fold)
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
            
            A = ass.parse(descricao, targets[contexto])
            B = ass.parse(descricaoR)
            
            DICE = ass.dice(A, B)
            MASI = ass.masi(A, B)
            
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
    
        for atributo in acertos.keys():
            print "Atributo: " + str(atributo)
            print "Acuracia: " + str(acertos[atributo] / total[atributo])
#             print "Verdadeiros Positivos: " + str(tp[atributo])
#             print "Falsos Positivos: " + str(fp[atributo])
#             print "Verdadeiros Negativos: " + str(tn[atributo])
#             print "Falsos Negativos: " + str(fn[atributo])
            print 10 * "-"
         
        print 50 * "*"

    print 50 * "*"
    print "Expressoes: "
    print "Dice Total: " + str(np.mean(dice))
    print "Masi Total: " + str(np.mean(masi))
    print "Acuracia: " + str(acuracia / len(dice))
    print 50 * "*"
    
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
            
    for atributo in acertosT.keys():
        print "Atributo: " + str(atributo)
        print "Acuracia: " + str(acertosT[atributo] / totalT[atributo])
        print 10 * "-"
    return resultadoTotal, dice, masi, acuracia

def countAttributeFrequency(folds, teste):
    foldsAux = {}
    
    for fold in folds:
        if fold != teste:
            foldsAux[fold] = folds[fold]
            
    frequency = {}
    frequency["target"] = {}
    frequency["landmark"] = {}
    
    for fold in foldsAux:
        for anotacao in foldsAux[fold]:
            target = "tg"
            
            for objeto in anotacao["descricao"]:
                for key in anotacao["descricao"][objeto].keys():
                    if objeto == target:
                        if key in frequency["target"].keys():
                            frequency["target"][key] = frequency["target"][key] + 1
                        else:
                            frequency["target"][key] = 1
                    else:
                        if key in frequency["landmark"].keys():
                            frequency["landmark"][key] = frequency["landmark"][key] + 1
                        else:
                            frequency["landmark"][key] = 1
    return frequency

#contabiliza frequenca dos atributos
def countAttributeFrequencyIndividual(folds, teste):
    foldsAux = {}
    
    for fold in folds:
        if fold != teste:
            foldsAux[fold] = folds[fold]
            
    frequency = {}
    
    for fold in foldsAux:
        for anotacao in folds[fold]:
            target = "tg"
            participante = anotacao["caracteristicas"]["trial"]
            
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

def defineExpressao(previsoes, dominio, target):
    #descricao prevista pela svm
    descricao = {}
    
    descricao[target] = {}
    
    for atributo in dominio[target].keys():
        descricao[target][atributo] = dominio[target][atributo]
    
    if "under" in descricao[target].keys():
        del descricao[target]["under"]
    
    relacional = False
    landmark = str
    for atributo in ["type","col","size","loc","relation","lm_type","lm_col","lm_size","lm_loc"]:
        element = atributo.split("_")
        
        if len(element) == 1 and atributo != "relation":
            if previsoes[atributo] == 0:
                if atributo in descricao[target].keys():
                    del descricao[target][atributo]
        
        elif len(element) == 2 and relacional == True:
            if previsoes[atributo] == 0:
                del descricao[landmark][element[1]]
        
        elif len(element) == 1 and atributo == "relation":
            if previsoes[atributo] == 0:
                del descricao[target]["on-top-of"]
                del descricao[target]["next-to"]
                del descricao[target]["right-of"]
                del descricao[target]["left-of"]
            else:
                if previsoes[atributo] == 1:
                    del descricao[target]["next-to"]
                    del descricao[target]["right-of"]
                    del descricao[target]["left-of"]
                    
                    if len(descricao[target]["on-top-of"]) == 0:
                        del descricao[target]["on-top-of"]
                    else:
                        landmark = descricao[target]["on-top-of"][0]
                        descricao[landmark] = {}
                        relacional = True
                        
                        for key in dominio[landmark].keys():
                            descricao[landmark][key] = dominio[landmark][key]
                        
                        del descricao[landmark]["on-top-of"]
                        del descricao[landmark]["next-to"]
                        del descricao[landmark]["right-of"]
                        del descricao[landmark]["left-of"]
                        del descricao[landmark]["under"]
                
                elif previsoes[atributo] == 2:
                    del descricao[target]["on-top-of"]
                    del descricao[target]["right-of"]
                    del descricao[target]["left-of"]
                    
                    if len(descricao[target]["next-to"]) == 0:
                        del descricao[target]["next-to"]
                    else:
                        landmark = descricao[target]["next-to"][0]
                        descricao[landmark] = {}
                        relacional = True
                        
                        for key in dominio[landmark].keys():
                            descricao[landmark][key] = dominio[landmark][key]
                        
                        del descricao[landmark]["on-top-of"]
                        del descricao[landmark]["next-to"]
                        del descricao[landmark]["right-of"]
                        del descricao[landmark]["left-of"]
                        del descricao[landmark]["under"]
                
                elif previsoes[atributo] == 3:
                    del descricao[target]["on-top-of"]
                    del descricao[target]["next-to"]
                    del descricao[target]["left-of"]
                    
                    if len(descricao[target]["right-of"]) == 0:
                        del descricao[target]["right-of"]
                    else:
                        landmark = descricao[target]["right-of"][0]
                        descricao[landmark] = {}
                        relacional = True
                        
                        for key in dominio[landmark].keys():
                            descricao[landmark][key] = dominio[landmark][key]
                        
                        del descricao[landmark]["on-top-of"]
                        del descricao[landmark]["next-to"]
                        del descricao[landmark]["right-of"]
                        del descricao[landmark]["left-of"]
                        del descricao[landmark]["under"]
                
                elif previsoes[atributo] == 4:
                    del descricao[target]["on-top-of"]
                    del descricao[target]["next-to"]
                    del descricao[target]["right-of"]
                    
                    if len(descricao[target]["left-of"]) == 0:
                        del descricao[target]["left-of"]
                    else:
                        landmark = descricao[target]["left-of"][0]
                        descricao[landmark] = {}
                        relacional = True
                        
                        for key in dominio[landmark].keys():
                            descricao[landmark][key] = dominio[landmark][key]
                        
                        del descricao[landmark]["on-top-of"]
                        del descricao[landmark]["next-to"]
                        del descricao[landmark]["right-of"]
                        del descricao[landmark]["left-of"]
                        del descricao[landmark]["under"]
    return descricao