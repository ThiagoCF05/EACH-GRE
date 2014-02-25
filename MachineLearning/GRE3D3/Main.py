'''
Created on 19/12/2012

@author: thiagocastroferreira
'''
# import numpy as np
# from scipy.stats import wilcoxon, chisquare
# import matplotlib.pyplot as plt
# from hcluster import *
import ParserGRE3D as parser
import CrossValidation as cross
import Experiment1 as exp1
import SVMValidatedExperiment as exp2
import ExperimentDecisionTree as exp4

import ValidatedExperimentIndividual as exp5

def initialize():
    anotacoes = parser.parseAnnotation()
    dominios = parser.parseDominio()
    participantes = parser.parseParticipantes()
    targets = {"1":"b1","2":"b1","3":"b1","4":"c2","5":"c1","6":"b1","7":"b1","8":"b1","9":"c1","10":"c2","11":"b1","12":"b1","13":"b1","14":"c2","15":"c1","16":"b1","17":"b1","18":"b1","19":"c1","20":"c1"}
    atributos = ['loc', 'left-of', 'next-to', 'on-top-of', 'right-of', 'type', 'col', 'size', 'in-front-of']
    return dominios, targets, anotacoes, atributos, participantes


if __name__ == '__main__':
    dominios, targets, anotacoes, atributos, participantes = initialize()
    
    folds = cross.crossValidation(10, anotacoes)
    
    print "Machine Learning sem ID"
#     exp5.run(dominios, targets, anotacoes, atributos, participantes, False)
    exp2.run(dominios, targets, folds, atributos, participantes, False)
    
    print "\n\n"
    print "Machine Learning com ID"
#     exp5.run(dominios, targets, anotacoes, atributos, participantes, True)
#     exp2.run(dominios, targets, folds, atributos, participantes, True)
    
#     anotacoesParticipante = {}
#     
#     for anotacao in anotacoes:
#         participante = anotacao["caracteristicas"]["trial"]
#         if participante not in anotacoesParticipante:
#             anotacoesParticipante[participante] = []
#         anotacoesParticipante[participante].append(anotacao)
#     
#     acuraciaTotal = 0.0
#     diceTotal = []
#     masiTotal = []
#     
#     acertosT = {}
#     totalT = {}
#     for participante in anotacoesParticipante:
#         folds = cross.crossValidation(10, anotacoesParticipante[participante])   
#         
#         resultadoTotal, dice, masi, acuracia = exp1.run(dominios, targets, folds, atributos, False)
#         
#         for resultados in resultadoTotal:
#             acertos = resultados[0]
#             total = resultados[1]
#             
#             for atributo in acertos.keys():
#                 if atributo not in acertosT:
#                     acertosT[atributo] = 0.0
#                     totalT[atributo] = 0.0
#                 
#                 acertosT[atributo] = acertosT[atributo] + acertos[atributo]
#                 totalT[atributo] = totalT[atributo] + total[atributo]
#         
#         for d in dice:
#             diceTotal.append(d)
#         
#         for m in masi:
#             masiTotal.append(m)
#             
#         acuraciaTotal = acuraciaTotal + acuracia
#         
#     print 50 * "*"
#     print "Expressoes: "
#     print "Dice Total: " + str(np.mean(diceTotal))
#     print "Masi Total: " + str(np.mean(masiTotal))
#     print "Acuracia: " + str(acuraciaTotal / len(diceTotal))
#     print 50 * "*"
#     
#     for atributo in acertosT.keys():
#         print "Atributo: " + str(atributo)
#         print "Acuracia: " + str(acertosT[atributo] / totalT[atributo])
#         print 10 * "-"