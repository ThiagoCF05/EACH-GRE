'''
Created on 11/02/2014

@author: thiagocastroferreira
'''

import CrossValidation as cross
import SVMValidatedExperiment as exp2
import ExperimentDecisionTree as exp4
import numpy as np

def run(dominios, targets, anotacoes, atributos, incluiParticipante):
    folds = cross.crossValidationParticipant(10, anotacoes)
    
    diceTotal = []
    masiTotal = []
    acuraciaTotal = 0.0
    results = []
    
    acertosT = {}
    totalT = {}
    
    for participante in folds.keys():
        resultadoTotal, dice, masi, acuracia = exp4.run(dominios, targets, folds[participante], atributos, {}, incluiParticipante)
        
        diceTotal.extend(dice)
        masiTotal.extend(masi)
        acuraciaTotal = acuraciaTotal + acuracia
        
        for resultados in resultadoTotal:
            acertos = resultados[0]
            total = resultados[1]
            
            for atributo in acertos.keys():
                if atributo not in acertosT:
                    acertosT[atributo] = 0.0
                    totalT[atributo] = 0.0
                
                acertosT[atributo] = acertosT[atributo] + acertos[atributo]
                totalT[atributo] = totalT[atributo] + total[atributo]
        results.append([acertosT, totalT])
    
    print "\n"
    print "General:"
    print 50 * "*"
    print "Expressions: "
    print "Dice: " + str(np.mean(diceTotal))
    print "Masi: " + str(np.mean(masiTotal))
    print "Accuracy: " + str(acuraciaTotal / len(diceTotal))
    print "\n"       
    
    print "Attributes:"
    print 15 * "-"     
    for atributo in acertosT.keys():
        print "Attribute: " + str(atributo)
        print "Accuracy: " + str(acertosT[atributo] / totalT[atributo])
        print 10 * "-" 
        
    return results, diceTotal, masiTotal, acuraciaTotal