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
import SVMValidatedExperiment as exp7

def initialize():
    dominios = parseDominio()
    anotacoes = parseAnnotation()
    atributos = ["type", "colour", "hpos", "vpos", "size", "near", "left", "right", "below", "above", "in-front-of"]
    targets = {"01f-t1n":"h", "01f-t1r":"h", "01f-t2n":"h", "01f-t2r":"h", "01o-t1n":"h", "01o-t1r":"h", "01o-t2n":"h", "01o-t2r":"h", "02f-t1n":"o", "02f-t1r":"o", "02f-t2n":"o", "02f-t2r":"o", "02o-t1n":"o", "02o-t1r":"o", "02o-t2n":"o", "02o-t2r":"o", "03f-t1n":"m", "03f-t1r":"m", "03f-t2n":"m", "03f-t2r":"m", "03o-t1n":"m", "03o-t1r":"m", "03o-t2n":"m", "03o-t2r":"m", "04f-t1n":"a", "04f-t1r":"a", "04f-t2n":"a", "04f-t2r":"a", "04o-t1n":"a", "04o-t1r":"a", "04o-t2n":"a", "04o-t2r":"a", "05f-t1n":"m", "05f-t2n":"m", "05f-t1r":"m", "05f-t2r":"m", "05o-t1n":"m", "05o-t1r":"m", "05o-t2n":"m", "05o-t2r":"m", "06f-t1n":"h", "06f-t1r":"h", "06f-t2n":"h", "06f-t2r":"h", "06o-t1n":"h", "06o-t1r":"h", "06o-t2n":"h", "06o-t2r":"h", "07f-t1n":"i", "07f-t1r":"i", "07f-t2n":"i", "07f-t2r":"i", "07o-t1n":"i", "07o-t1r":"i", "07o-t2n":"i", "07o-t2r":"i", "08f-t1n":"a", "08f-t1r":"a", "08f-t2n":"a", "08f-t2r":"a", "08o-t1n":"a", "08o-t1r":"a", "08o-t2n":"a", "08o-t2r":"a" }
    return dominios, anotacoes, atributos, targets

if __name__ == '__main__':
    dominios, anotacoes, atributos, targets = initialize()
    
    #anotacoes = exp1.run(dominios, anotacoes, atributos, targets)
    
    folds = cross.crossValidation(10, anotacoes)
     
    #folds = exp5.run(dominios, folds, atributos, targets, 0.7)
     
#     folds = exp6.run(dominios, folds, atributos, targets, 0.7)
    
    print "Machine Learning sem ID"
#     exp7.run(dominios, targets, folds, atributos, {}, False)
    
    print "Machine Learning com ID"
    exp7.run(dominios, targets, folds, atributos, {}, True)
     
#     dice = []
#     diceGlobal = []
#     dicePersonalizado = []
#     
#     diceGlobalSuperespecificado = []
#     dicePersonalizadoSuperespecificado = []
#     print "DICE \t DICE GLOBAL \t DICE PERSONALIZADO \t"
#     for fold in folds:
#         for participante in folds[fold].keys():
#             dice.append(folds[fold][participante]["dice"])
#             diceGlobal.append(folds[fold][participante]["dice_global"])
#             dicePersonalizado.append(folds[fold][participante]["dice_personalizado"])
#             
#             diceGlobalSuperespecificado.append(folds[fold][participante]["dice_global_superespecificado"])
#             dicePersonalizadoSuperespecificado.append(folds[fold][participante]["dice_personalizado_superespecificado"])
#             #print folds[fold][participante]["dice"], "\t", folds[fold][participante]["dice_global"], "\t", folds[fold][participante]["dice_personalizado"], "\t"
#      
#     print 50 * "*"
#     T, p = wilcoxon(diceGlobal, dice)
#     print 50 * "-"
#     print "WILCOXON: Global X Randomico"
#     print "T: ", T, " p-value: ", p
#     print 50 * "-"
#     
#     print 50 * "*"
#     T, p = wilcoxon(dicePersonalizado, dice)
#     print 50 * "-"
#     print "WILCOXON: Personalizado X Randomico"
#     print "T: ", T, " p-value: ", p
#     print 50 * "-"
#      
#     T, p = wilcoxon(dicePersonalizado, diceGlobal)
#     print 50 * "-"
#     print "WILCOXON: Personalizado X Global"
#     print "T: ", T, " p-value: ", p
#     print 50 * "-"
#     print 50 * "*"
#     
#     T, p = wilcoxon(diceGlobalSuperespecificado, dicePersonalizado)
#     print "Wilcoxon: Global com Superespecificacao X Personalizado sem Superespecificacao"
#     print "T: ", T, " p-value: ", p
#     print 50 * "-"
#     T, p = wilcoxon(dicePersonalizadoSuperespecificado, dicePersonalizado)
#     print 50 * "*"
#     print "Wilcoxon: Personalizado com Superespecificacao X Personalizado sem Superespecificacao"
#     print "T: ", T, " p-value: ", p
#     print 50 * "-"
#     print 50 * "*"
#      
#     print "\n"
#     
#     #Acuracia sem Superespecificacao Randomico: 0.0260416666667
#     #Acuracia sem Superespecificacao Global: 0.119791666667
#     #Acuracia sem Superespecificacao Personalizado: 0.302083333333
#     
#     #Acuracia com Superespecificacao Randomico: 0.0208333333333
#     #Acuracia com Superespecificacao Global: 0.00520833333333
#     #Acuracia com Superespecificacao Personalizado: 0.166666666667
#     
#     print 50 * "*"
#     T, p = chisquare(np.array([0.12 * 384, (1. - 0.12) * 384]), np.array([0.02 * 384, (1. - 0.02) * 384]))
#     print 50 * "-"
#     print "CHI-QUADRADO: Global X Randomico"
#     print "T: ", T, " p-value: ", p
#     print 50 * "-"
#     T, p = chisquare(np.array([0.30 * 384, (1. - 0.30) * 384]) , np.array([0.02 * 384, (1. - 0.02) * 384]))
#     print 50 * "-"
#     print "CHI-QUADRADO: Personalizado X Randomico"
#     print "T: ", T, " p-value: ", p
#     print 50 * "-"
#     T, p = chisquare(np.array([0.30 * 384, (1. - 0.30) * 384]), np.array([0.12 * 384, (1. - 0.12) * 384]))
#     print 50 * "-"
#     print "CHI-QUADRADO: Personalizado X Global"
#     print "T: ", T, " p-value: ", p
#     print 50 * "-"
#     print 50 * "*"
#     
#     T, p = chisquare(np.array([0.005 * 384, (1. - 0.005) * 384]), np.array([0.30 * 384, (1. - 0.30) * 384]))
#     print "CHI-QUADRADO: Global com Superespecificacao X Personalizado sem Superespecificacao"
#     print "T: ", T, " p-value: ", p
#     print 50 * "-"
#     T, p = chisquare(np.array([0.16 * 384, (1. - 0.16) * 384]), np.array([0.30 * 384, (1. - 0.30) * 384]))
#     print 50 * "*"
#     print "CHI-QUADRADO: Personalizado com Superespecificacao X Personalizado sem Superespecificacao"
#     print "T: ", T, " p-value: ", p
#     print 50 * "-"
#     print 50 * "*"
    