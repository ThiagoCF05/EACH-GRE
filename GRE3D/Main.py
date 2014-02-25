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
    targets = {"1":"b3","2":"b2","3":"b3","4":"b2","5":"b3","6":"b1","7":"b3","8":"b1","9":"b2","10":"b1","11":"b2","12":"b1","13":"b3","14":"b1","15":"b3","16":"b1","17":"b1","18":"b1","19":"b1","20":"b1","21":"b1","22":"b1","23":"b1","24":"b1","25":"b4","26":"b3","27":"b4","28":"b3","29":"b3","30":"b3","31":"b3","32":"b3"}
    atributos = ['loc', 'left-of', 'next-to', 'on-top-of', 'right-of', 'type', 'col', 'size']
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