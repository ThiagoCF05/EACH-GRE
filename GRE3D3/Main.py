'''
Created on 19/12/2012

@author: thiagocastroferreira
'''
# import numpy as np
# from scipy.stats import wilcoxon, chisquare
# import matplotlib.pyplot as plt
# from hcluster import *
import ParserGRE3D as parser
import Experiment1 as exp1
import Experiment5 as exp5
import Experiment6 as exp6
import CrossValidation as cross
import SVMValidatedExperiment as exp7

def initialize():
    anotacoes = parser.parseAnnotation()
    dominios = parser.parseDominio()
    targets = {"1":"b1","2":"b1","3":"b1","4":"c2","5":"c1","6":"b1","7":"b1","8":"b1","9":"c1","10":"c2","11":"b1","12":"b1","13":"b1","14":"c2","15":"c1","16":"b1","17":"b1","18":"b1","19":"c1","20":"c1"}
    atributos = ['loc', 'left-of', 'next-to', 'on-top-of', 'right-of', 'type', 'col', 'size', 'in-front-of']
    return dominios, targets, anotacoes, atributos

if __name__ == '__main__':
    dominios, targets, anotacoes, atributos = initialize()
    
#     anotacoes = exp1.run(dominios, targets, anotacoes, atributos)
    
    folds = cross.crossValidation(10, anotacoes)
    
#     folds = exp5.run(dominios, targets, folds, atributos, 0.7)
    
#     folds = exp6.run(dominios, targets, folds, atributos, 0.7)
    print "Machine Learning sem ID"
    exp7.run(dominios, targets, folds, atributos, {}, False)
    
    print "Machine Learning com ID"
#     exp7.run(dominios, targets, folds, atributos, {}, True)
    
#     f = open('dices.txt','w')
#     dice = []
#     diceGlobal = []
#     dicePersonalizado = []
#     diceGlobalSuperespecificado = []
#     dicePersonalizadoSuperespecificado = []
#     #f = open('dices.txt','w')
#     for fold in folds:
#         for participante in folds[fold].keys():
#             for anotacao in folds[fold][participante]:
#                 diceGlobalSuperespecificado.append(anotacao["dice_global_superespecificado"])
#                 dicePersonalizadoSuperespecificado.append(anotacao["dice_personalizado_superespecificado"])
#                 
#                 f.write(str(anotacao["dice_global"]))
#                 f.write("\t")
#                 f.write(str(anotacao["dice_personalizado"]))
#                 f.write("\n")
#                 
#                 dice.append(anotacao["dice"])
#                 diceGlobal.append(anotacao["dice_global"])
#                 dicePersonalizado.append(anotacao["dice_personalizado"])
#                 #print folds[fold][participante]["dice"], "\t", folds[fold][participante]["dice_global"], "\t", folds[fold][participante]["dice_personalizado"], "\t"
#                 #f.write(str(anotacao["dice"]) + "\t" + str(anotacao["dice_global"]) + "\t" + str(anotacao["dice_personalizado"]) + "\t")
#                 #f.write("\n")
#     
#     #Acuracia sem Superespecificacao Randomico: 0.103348214286
#     #Acuracia sem Superespecificacao Global: 0.6140625
#     #Acuracia sem Superespecificacao Personalizado: 0.608258928571
#     
#     #Acuracia com Superespecificacao Randomico: 0.0975446428571
#     #Acuracia com Superespecificacao Global: 0.6140625
#     #Acuracia com Superespecificacao Personalizado: 0.719419642857
#     
#     print 50 * "*"
#     T, p = wilcoxon(np.array(dicePersonalizado), np.array(dice))
#     print 50 * "-"
#     print "WILCOXON: PERSONALIZADO X RANDOMICO"
#     print "T: ", T, " p-value: ", p
#     print 50 * "-"
#     
#     print 50 * "*"
#     T, p = wilcoxon(dicePersonalizado, diceGlobal)
#     print 50 * "-"
#     print "WILCOXON: PERSONALIZADO X Global"
#     print "T: ", T, " p-value: ", p
#     print 50 * "-"
#     
#     print 50 * "*"
#     T, p = wilcoxon(diceGlobal, dice)
#     print 50 * "-"
#     print "WILCOXON: Global X Randomico"
#     print "T: ", T, " p-value: ", p
#     print 50 * "-"
     
    T, p = wilcoxon(diceGlobalSuperespecificado, dicePersonalizado)
    print "Wilcoxon: Global com Superespecificacao X Personalizado sem Superespecificacao"
    print "T: ", T, " p-value: ", p
    print 50 * "-"
    T, p = wilcoxon(dicePersonalizadoSuperespecificado, dicePersonalizado)
    print 50 * "*"
    print "Wilcoxon: Personalizado com Superespecificacao X Personalizado sem Superespecificacao"
    print "T: ", T, " p-value: ", p
    print 50 * "-"
    print 50 * "*"
     
    print "\n"
     
    print 50 * "*"
    T, p = chisquare(np.array([630 * 0.70, 630 * (1. - 0.70)]), np.array([630 * 0.67, 630 * (1. - 0.67)]))
    print 50 * "-"
    print "CHI-QUADRADO: Global X Randomico"
    print "T: ", T, " p-value: ", p
    print 50 * "-"
#     T, p = chisquare(np.array([630 * 0.24, 630 * (1. - 0.24)]) , np.array([630 * 0.16, 630 * (1. - 0.16)]))
#     print 50 * "-"
#     print "CHI-QUADRADO: Personalizado X Randomico"
#     print "T: ", T, " p-value: ", p
#     print 50 * "-"
#     T, p = chisquare(np.array([630 * 0.24, 630 * (1. - 0.24)]), np.array([630 * 0.24, 630 * (1. - 0.24)]))
#     print 50 * "-"
#     print "CHI-QUADRADO: Personalizado X Global"
#     print "T: ", T, " p-value: ", p
#     print 50 * "-"
#     print 50 * "*"
     
#     T, p = chisquare(np.array([0.61 * 384, (1. - 0.61) * 384]), np.array([0.61 * 384, (1. - 0.61) * 384]))
#     print "CHI-QUADRADO: Global com Superespecificacao X Personalizado sem Superespecificacao"
#     print "T: ", T, " p-value: ", p
#     print 50 * "-"
#     T, p = chisquare(np.array([0.72 * 384, (1. - 0.72) * 384]), np.array([0.61 * 384, (1. - 0.61) * 384]))
#     print 50 * "*"
#     print "CHI-QUADRADO: Personalizado com Superespecificacao X Personalizado sem Superespecificacao"
#     print "T: ", T, " p-value: ", p
#     print 50 * "-"
#     print 50 * "*"
     