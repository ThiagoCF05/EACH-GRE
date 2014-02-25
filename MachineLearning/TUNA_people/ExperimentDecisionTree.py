'''
Created on 02/12/2013

@author: thiagocastroferreira
'''

import numpy as np
import Assurance as ass
import Parser as parser
import DecisionTree2 as tree

def run(trials, folds, atributos, participantes, incluirParticipante):
    featureVector = parser.parseFeatureVector(trials)
    
    inputs = {}
    frequencias = {}
    for fold in folds:
        frequencias[fold] = countAttributeFrequency(folds, fold)
        participantes[fold] = parser.descriptionsMeans(folds, fold)
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
    
    for fold in ["1","2","3","4","5","6", "7","8","9","10"]:
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
            descricao = defineExpressao(expressao)
            descricaoR = expressao[expressao.keys()[0]]["anotacao"]["descricao"]
            
            A = ass.parse(descricao)
            B = ass.parse(descricaoR)
            
            if len(A) == 0 and len(B) == 0:
                DICE = 0.0
                MASI = 0.0
            else:
                DICE = ass.dice(A, B)
                MASI = ass.masi(A, B)
            
            if DICE == 1.0:
                acuracia = acuracia + 1.0
            
#             print descricao
#             print descricaoR
#             print DICE
#             print 10 * "-"
            
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
                targets = anotacao["caracteristicas"]["target"]
                
                if participante not in frequency.keys():
                    frequency[participante] = {}
                    frequency[participante]["target"] = {}
                
                for target in targets:
                    for objeto in anotacao["descricao"]:
                        for key in anotacao["descricao"][objeto].keys():
                            if objeto in targets:
                                if key in frequency[participante]["target"].keys():
                                    frequency[participante]["target"][key] = frequency[participante]["target"][key] + 1
                                else:
                                    frequency[participante]["target"][key] = 1
    return frequency

def defineExpressao(expressao):
    #descricao prevista pela svm
    descricao = {}
    
    for target in expressao.keys():
        descricao[target] = {}
        dominio = expressao[target]["anotacao"]["domain"]
        
        for atributo in dominio[target].keys():
            descricao[target][atributo] = dominio[target][atributo]
    
        for atributo in ["type", "orientation", "age", "hairColour", "hasBeard", "hasHair", "hasGlasses", "hasShirt", "hasTie", "hasSuit", "x-dimension", "y-dimension"]:
            if expressao[target]["previsoes"][atributo] == 0:
                if atributo in descricao[target].keys():
                    del descricao[target][atributo]
    
    return descricao