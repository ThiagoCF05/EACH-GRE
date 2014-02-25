'''
Created on 19/12/2012

@author: thiagocastroferreira
'''
import numpy as np
from scipy.stats import wilcoxon, chisquare
# import matplotlib.pyplot as plt
# from hcluster import *
import Assurance as ass
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
    targets = {"1":"b3","2":"b2","3":"b3","4":"b2","5":"b3","6":"b1","7":"b3","8":"b1","9":"b2","10":"b1","11":"b2","12":"b1","13":"b3","14":"b1","15":"b3","16":"b1","17":"b1","18":"b1","19":"b1","20":"b1","21":"b1","22":"b1","23":"b1","24":"b1","25":"b4","26":"b3","27":"b4","28":"b3","29":"b3","30":"b3","31":"b3","32":"b3"}
    atributos = ['loc', 'left-of', 'next-to', 'on-top-of', 'right-of', 'type', 'col', 'size']
    return dominios, targets, anotacoes, participantes, atributos

if __name__ == '__main__':
    dominios, targets, anotacoes, participantes, atributos = initialize()
    
    folds = cross.crossValidation(10, anotacoes)
    
    print "Machine Learning sem ID"
#     exp5.run(dominios, targets, anotacoes, atributos, participantes, False)
    exp2.run(dominios, targets, folds, atributos, participantes, False)
    
    print "\n\n"
    print "Machine Learning com ID"
#     exp5.run(dominios, targets, anotacoes, atributos, participantes, True)
#     exp2.run(dominios, targets, folds, atributos, participantes, True)