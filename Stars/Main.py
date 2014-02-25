'''
Created on 19/12/2012

@author: thiagocastroferreira
'''
import numpy as np
from scipy.stats import wilcoxon, chisquare
# import matplotlib.pyplot as plt
# from hcluster import *
import Assurance as ass
from ParserStars import *
import Experiment1 as exp1
import Experiment5 as exp5
import Experiment6 as exp6
import CrossValidation as cross

def initialize():
    dominios = parseDominio()
    anotacoes = parseAnnotation()
    atributos = ["type", "others", "hpos", "vpos", "next", "left", "right", "below", "above"]
    targets = {"abs1":"e2", "abs3":"e2", "abs5":"e3", "proj1":"e2", "proj3":"e4", "proj5":"e2" }
    return dominios, anotacoes, atributos, targets

if __name__ == '__main__':
    dominios, anotacoes, atributos, targets = initialize()
    
    anotacoes = exp1.run(dominios, anotacoes, atributos, targets)
    
    folds = cross.crossValidation(anotacoes)
     
    folds = exp5.run(dominios, folds, atributos, targets, 0.7)
     
    folds = exp6.run(dominios, folds, atributos, targets, 0.7)
     
    dice = []
    diceGlobal = []
    dicePersonalizado = []
    
    diceGlobalSuperespecificado = []
    dicePersonalizadoSuperespecificado = []
    print "DICE \t DICE GLOBAL \t DICE PERSONALIZADO \t"
    for fold in folds:
        for participante in folds[fold].keys():
            dice.append(folds[fold][participante]["dice"])
            diceGlobal.append(folds[fold][participante]["dice_global"])
            dicePersonalizado.append(folds[fold][participante]["dice_personalizado"])
            
            diceGlobalSuperespecificado.append(folds[fold][participante]["dice_global_superespecificado"])
            dicePersonalizadoSuperespecificado.append(folds[fold][participante]["dice_personalizado_superespecificado"])
            #print folds[fold][participante]["dice"], "\t", folds[fold][participante]["dice_global"], "\t", folds[fold][participante]["dice_personalizado"], "\t"
     
    print 50 * "*"
    T, p = wilcoxon(diceGlobal, dice)
    print 50 * "-"
    print "WILCOXON: Global X Randomico"
    print "T: ", T, " p-value: ", p
    print 50 * "-"
    
    print 50 * "*"
    T, p = wilcoxon(dicePersonalizado, dice)
    print 50 * "-"
    print "WILCOXON: Personalizado X Randomico"
    print "T: ", T, " p-value: ", p
    print 50 * "-"
     
    T, p = wilcoxon(dicePersonalizado, diceGlobal)
    print 50 * "-"
    print "WILCOXON: Personalizado X Global"
    print "T: ", T, " p-value: ", p
    print 50 * "-"
    print 50 * "*"
    
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
    
    #Acuracia sem Superespecificacao Randomico: 0.0260416666667
    #Acuracia sem Superespecificacao Global: 0.119791666667
    #Acuracia sem Superespecificacao Personalizado: 0.302083333333
    
    #Acuracia com Superespecificacao Randomico: 0.0208333333333
    #Acuracia com Superespecificacao Global: 0.00520833333333
    #Acuracia com Superespecificacao Personalizado: 0.166666666667
    
    print 50 * "*"
    T, p = chisquare(np.array([0.12 * 384, (1. - 0.12) * 384]), np.array([0.02 * 384, (1. - 0.02) * 384]))
    print 50 * "-"
    print "CHI-QUADRADO: Global X Randomico"
    print "T: ", T, " p-value: ", p
    print 50 * "-"
    T, p = chisquare(np.array([0.30 * 384, (1. - 0.30) * 384]) , np.array([0.02 * 384, (1. - 0.02) * 384]))
    print 50 * "-"
    print "CHI-QUADRADO: Personalizado X Randomico"
    print "T: ", T, " p-value: ", p
    print 50 * "-"
    T, p = chisquare(np.array([0.30 * 384, (1. - 0.30) * 384]), np.array([0.12 * 384, (1. - 0.12) * 384]))
    print 50 * "-"
    print "CHI-QUADRADO: Personalizado X Global"
    print "T: ", T, " p-value: ", p
    print 50 * "-"
    print 50 * "*"
    
    T, p = chisquare(np.array([0.005 * 384, (1. - 0.005) * 384]), np.array([0.30 * 384, (1. - 0.30) * 384]))
    print "CHI-QUADRADO: Global com Superespecificacao X Personalizado sem Superespecificacao"
    print "T: ", T, " p-value: ", p
    print 50 * "-"
    T, p = chisquare(np.array([0.16 * 384, (1. - 0.16) * 384]), np.array([0.30 * 384, (1. - 0.30) * 384]))
    print 50 * "*"
    print "CHI-QUADRADO: Personalizado com Superespecificacao X Personalizado sem Superespecificacao"
    print "T: ", T, " p-value: ", p
    print 50 * "-"
    print 50 * "*"
    