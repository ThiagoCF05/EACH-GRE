'''
Created on 20/01/2014

@author: thiagocastroferreira
'''

import numpy as np
import ParserStars as parser
import CrossValidation as cross
import SVMValidated2 as svm
import Assurance as ass
from random import choice

def run(dominios, targets, folds, atributos, participantes, incluirParticipante):
    featureVector = parser.parseFeatureVector(dominios, targets)
    
    inputs = {}
    
    # Cross Validation
    #folds = cross.crossValidation(6, annotations)
    
    # Inicializa Vetor de Caracteristicas
    for fold in folds:
        frequencias = countAttributeFrequencyIndividual(folds, fold)
        inputs[fold] = parser.parseSVMInputSecondVersion(folds[fold], featureVector, participantes, frequencias, incluirParticipante)
    
    resultadoTotal = []
    diceTotal = []
    masiTotal = []
    acuraciaTotal = 0.0
    
    for testeFold in folds:
        teste = folds[testeFold]
        inputTeste = inputs[testeFold]
        
        treinamentoFolds = {}
        inputsTreinamento = {}
        
        for foldAux in folds:
            if foldAux != testeFold:
                treinamentoFolds[foldAux] = folds[foldAux]
                inputsTreinamento[foldAux] = inputs[foldAux]
        
        acertos = {}
        total = {}
        tp = {}
        tn = {}
        fp = {}
        fn = {}
        
        keys = folds.keys()
        keys.sort()
        for fold in treinamentoFolds:
#             print "Fold: ", fold
#             print 50 * "-"
            resultados = svm.run(inputsTreinamento, fold)
            
            for combination in resultados.keys():
                if combination not in acertos.keys():
                    acertos[combination] = {}
                    total[combination] = {}
                    tp[combination] = {}
                    tn[combination] = {}
                    fp[combination] = {}
                    fn[combination] = {}
                
                for svm1 in resultados[combination][0].keys():
                    if svm1 not in acertos[combination].keys():
                        acertos[combination][svm1] = 0.0
                        total[combination][svm1] = 0.0
                        tp[combination][svm1] = 0.0
                        tn[combination][svm1] = 0.0
                        fp[combination][svm1] = 0.0
                        fn[combination][svm1] = 0.0
                    
                    acertos[combination][svm1] = acertos[combination][svm1] + resultados[combination][0][svm1]
                    total[combination][svm1] = total[combination][svm1] + resultados[combination][1][svm1]
                    tp[combination][svm1] = tp[combination][svm1] + resultados[combination][3][svm1]
                    tn[combination][svm1] = tn[combination][svm1] + resultados[combination][4][svm1]
                    fp[combination][svm1] = fp[combination][svm1] + resultados[combination][5][svm1]
                    fn[combination][svm1] = fn[combination][svm1] + resultados[combination][6][svm1]
        
        combinacoes = {}
        acuracias = {}
        for combination in acertos.keys():
            aux = combination.split(",")
            C = float(aux[0])
            gamma = float(aux[1])
            
#             print 20 * "-"
#             print str(C) + " - " + str(gamma)
#             print 20 * "-"
            
            for svm1 in acertos[combination].keys():
                acuracia = acertos[combination][svm1] / total[combination][svm1]
#                 print str(svm1) + ": " + str(acuracia)
                if svm1 not in combinacoes.keys():
                    acuracias[svm1] = acuracia
                    combinacoes[svm1] = {}
                    combinacoes[svm1]["C"] = C
                    combinacoes[svm1]["gamma"] = gamma
                elif acuracia > acuracias[svm1]:
                    acuracias[svm1] = acuracia
                    combinacoes[svm1]["C"] = C
                    combinacoes[svm1]["gamma"] = gamma
        
#         print "\n"
#         print "Combinacao: " + str(combinacoes)
         
         
        resultados = svm.run2(inputsTreinamento, inputTeste, combinacoes)
        resultadoTotal.append(resultados)
        acertos = resultados[0]
        total = resultados[1]
        expressoes = resultados[2]
         
        tp = resultados[3]
        tn = resultados[4]
        fp = resultados[5]
        fn = resultados[6]
         
        dice = []
        masi = []
         
        for expressao in expressoes:
            contexto = expressao["anotacao"]["caracteristicas"]["context"]
             
            descricao = defineExpressao(expressao["previsoes"], dominios[contexto], targets[contexto])
            descricaoR = expressao["anotacao"]["descricao"]
             
            A = ass.parse(descricao)
            B = ass.parse(descricaoR)
             
            DICE = ass.dice(A, B)
            MASI = ass.masi(A, B)
             
#             print 20 * "-"
#             print descricaoR
#             print descricao
#             print DICE
#             print 20 * "-"
             
            if DICE == 1.0:
                acuracia = acuracia + 1.0
                acuraciaTotal = acuraciaTotal + 1.0
             
            dice.append(DICE)
            masi.append(MASI)
            diceTotal.append(DICE)
            masiTotal.append(MASI)
         
#         for atributo in acertos.keys():
#             print "Attribute: " + str(atributo)
#             print "Accuracy: " + str(acertos[atributo] / total[atributo])
#             print 10 * "-"
#           
#         print 50 * "*"
#          
#         print "\n"
#         print "General:"
#         print 50 * "*"
#         print "Expressions: "
#         print "Dice: " + str(np.mean(dice))
#         print "Masi: " + str(np.mean(masi))
#         print "Accuracy: " + str(acuracia / len(dice))
#         print "\n"
     
    print "\n"
    print "General:"
    print 50 * "*"
    print "Expressions: "
    print "Dice: " + str(np.mean(diceTotal))
    print "Masi: " + str(np.mean(masiTotal))
    print "Accuracy: " + str(acuraciaTotal / len(diceTotal))
    print "\n"       
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
    
    print "Attributes:"
    print 15 * "-"     
    for atributo in acertosT.keys():
        print "Attribute: " + str(atributo)
        print "Accuracy: " + str(acertosT[atributo] / totalT[atributo])
        print 10 * "-"        

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

#contabiliza frequenca dos atributos por participante
def countAttributeFrequencyIndividual(folds, teste):
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

def defineExpressao(previsoes, dominio, target):
    #descricao prevista pela svm
    descricao = {}
    
    descricao[target] = {}
    
    for atributo in dominio[target].keys():
        descricao[target][atributo] = dominio[target][atributo]
    
    relacional = False
    landmark = str
    second_landmark = ""
    for atributo in ["type", "colour", "hpos", "vpos", "below", "above", "left", "right", "near", "lm_type", "lm_colour", "lm_hpos", "lm_vpos", "lm_below", "lm_above", "lm_left", "lm_right", "lm_near", "lm2_type", "lm2_colour", "lm2_hpos", "lm2_vpos"]:
        element = atributo.split("_")
        
        if len(element) == 1:
            if previsoes[atributo] == 0:
                if atributo in descricao[target].keys():
                    del descricao[target][atributo]
            else:
                if atributo in ["below", "above", "left", "right", "near"]:
                    if len(descricao[target][atributo]) > 0:
                        landmark = descricao[target][atributo][0]
                        relacional = True
                        
                        descricao[landmark] = {}
                        for key in dominio[landmark].keys():
                            descricao[landmark][key] = dominio[landmark][key]
                    else:
                        del descricao[target][atributo]
        
        elif len(element) == 2 and relacional == True:
            if element[0] == "lm":
                if previsoes[atributo] == 0:
                    del descricao[landmark][element[1]]
                else:
                    if element[1] in ["below", "above", "left", "right", "near"]:
                        if len(descricao[landmark][element[1]]) > 0:
                            second_landmark = descricao[landmark][element[1]][0]

                            descricao[second_landmark] = {}
                            for key in dominio[second_landmark].keys():
                                if key not in ["below", "above", "left", "right", "near"]:
                                    descricao[second_landmark][key] = dominio[second_landmark][key]
                        else:
                            del descricao[landmark][element[1]]
            else:
                if previsoes[atributo] == 0:
                    if second_landmark in descricao.keys():
                        del descricao[second_landmark][element[1]]
        
    return descricao