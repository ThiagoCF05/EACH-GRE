'''
Created on 02/12/2013

@author: thiagocastroferreira
'''

import numpy as np
import Parser as parser
import CrossValidation as cross
import SVMValidated as svm
import Assurance as ass
from random import choice
import Utils as utils

def run(trials, folds, atributos, participantesInput, incluirParticipante):
    featureVector = parser.parseFeatureVector(trials)
    
    inputs = {}
    frequencias = {}
    participantes = {}
    # Cross Validation
    #folds = cross.crossValidation(6, annotations)
    
    # Inicializa Vetor de Caracteristicas
    for fold in folds:
        frequencias[fold] = utils.countAttributeFrequencyIndividual(folds, fold)
        participantes[fold] = parser.descriptionsMeans(folds, fold)
        inputs[fold] = parser.parseSVMInput(folds[fold], featureVector, participantes[fold], frequencias[fold], incluirParticipante)
    
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
        
        combinacoes = run_validation(trials, treinamentoFolds, featureVector, participantesInput, incluirParticipante)
        
        resultados = svm.run2(inputsTreinamento, inputTeste, combinacoes)
        resultadoTotal.append(resultados)
        acertos = resultados[0]
        total = resultados[1]
        expressoes = resultados[2]
         
        dice = []
        masi = []
        acuracia = 0
        
        for expressao in expressoes:
            participante = expressao[expressao.keys()[0]]["anotacao"]["caracteristicas"]["participante"]
            
            descricao = utils.defineExpressao(expressao, frequencias[testeFold][participante], participantes[testeFold][participante]["numeroExpressoes"])
            descricaoR = expressao[expressao.keys()[0]]["anotacao"]["descricao"]
            
            A = ass.parse(descricao)
            B = ass.parse(descricaoR)
            
            if len(A) == 0 and len(B) == 0:
                DICE = 0.0
                MASI = 0.0
            else:
                DICE = ass.dice(A, B)
                MASI = ass.masi(A, B)
            
#             print descricao
#             print descricaoR
#             print DICE
#             print 10 * "-"
            
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
    
    return resultadoTotal, diceTotal, masiTotal, acuraciaTotal
        
def run_validation(dominios, folds, featureVector, participantesInput, incluirParticipante):
    [inputs, frequencias, participantes] = [{}, {}, {}]
    
    # Inicializa Vetor de Caracteristicas
    for fold in folds:
        frequencias[fold] = utils.countAttributeFrequencyIndividual(folds, fold)
        participantes[fold] = parser.descriptionsMeans(folds, fold)
        inputs[fold] = parser.parseSVMInput(folds[fold], featureVector, participantes[fold], frequencias[fold], incluirParticipante)
    
    [acertos, total] = [{}, {}]
    
    keys = folds.keys()
    keys.sort()
    for fold in folds:
#             print "Fold: ", fold
#             print 50 * "-"
        resultados = svm.run(inputs, fold)
        
        for combination in resultados.keys():
            if combination not in acertos.keys():
                acertos[combination] = {}
                total[combination] = {}
            
            for svm1 in resultados[combination][0].keys():
                if svm1 not in acertos[combination].keys():
                    acertos[combination][svm1] = 0.0
                    total[combination][svm1] = 0.0
                
                acertos[combination][svm1] = acertos[combination][svm1] + resultados[combination][0][svm1]
                total[combination][svm1] = total[combination][svm1] + resultados[combination][1][svm1]
    
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
            if total[combination][svm1] == 0:
                acuracia = 0
            else:
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
    return combinacoes     