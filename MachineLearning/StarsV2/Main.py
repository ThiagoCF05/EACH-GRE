'''
Created on 19/12/2012

@author: thiagocastroferreira
'''
import numpy as np
from scipy.stats import wilcoxon, chisquare
# import matplotlib.pyplot as plt
# from hcluster import *
import ParserStars as parser
import CrossValidation as cross
import SVMValidatedExperiment as exp2
import SVMValidatedExperiment2 as exp3
import ExperimentDecisionTree as exp4
import ValidatedExperimentIndividual as exp5

def initialize():
    anotacoes = parser.parseAnnotation()
    dominios = parser.parseDominio()
    participantes = {}
    atributos = ["type", "colour", "hpos", "vpos", "near", "left", "right", "below", "above"]
    targets = {"abs1":"e2", "abs3":"e2", "abs5":"e3", "proj1":"e2", "proj3":"e4", "proj5":"e2" }
    return dominios, targets, anotacoes, atributos, participantes


if __name__ == '__main__':
    dominios, targets, anotacoes, atributos, participantes = initialize()
    
    folds = cross.crossValidation(6, anotacoes)
    
    print "Machine Learning sem ID"
#     exp5.run(dominios, targets, anotacoes, atributos, False)
    exp2.run(dominios, targets, folds, atributos, {}, False)
    
    print "\n\n"
    print "Machine Learning com ID"
#     exp5.run(dominios, targets, anotacoes, atributos, True)
    exp2.run(dominios, targets, folds, atributos, {}, True)