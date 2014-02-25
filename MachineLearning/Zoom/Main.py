'''
Created on 19/12/2012

@author: thiagocastroferreira
'''
import numpy as np
from scipy.stats import wilcoxon, chisquare
# import matplotlib.pyplot as plt
# from hcluster import *
import Parser as parser
import CrossValidation as cross
import Experiment1 as exp1

def initialize():
    anotacoes = parser.parseAnnotation()
    dominios = parser.parseMapas()
    participantes = anotacoes[1]
    targets = {"1":["rest3"],"2":["cafe1"],"3":["drug3"],"4":["chur3"],"5":["pub1"],"6":["chur2","chur3"],"7":["rest1","rest2"],"8":["drug2","drug3"],"9":["drug3","drug4"],"10":["rest4","rest5"],"11":["rest3"],"12":["cafe1"],"13":["rest4","rest5"],"14":["chur3"],"15":["pub1"],"16":["chur2","chur3"],"17":["rest1","rest2"],"18":["drug2","drug3"],"19":["drug3","drug4"],"20":["rest4","rest5"]}
    atributos = ["type","in","name","next-to","in-front-of","other","right-to","left-to","behind"]
    return dominios, targets, anotacoes[0], atributos, participantes


if __name__ == '__main__':
    dominios, targets, anotacoes, atributos, participantes = initialize()
    
    folds = cross.crossValidation(10, anotacoes)
    
    print "Machine Learning sem ID"
    exp1.run(dominios, targets, folds, atributos, participantes, False)
    print participantes
    print "\n\n"
    print "Machine Learning com ID"
    exp1.run(dominios, targets, folds, atributos, participantes, True)
    
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