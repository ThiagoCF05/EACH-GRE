'''
Created on 19/12/2012

@author: thiagocastroferreira
'''
import numpy as np
from scipy.stats import wilcoxon, chisquare
# import matplotlib.pyplot as plt
# from hcluster import *
import Assurance as ass
import Parser as parser
import Experiment1 as exp1
import Experiment5 as exp5
import Experiment6 as exp6
import CrossValidation as cross
import SVMValidatedExperiment as exp7

def initialize():
    trials = parser.parse()
    atributos = ["type", "colour", "orientation", "size", "x-dimension", "y-dimension"]
    return trials, atributos

if __name__ == '__main__':
    trials, atributos = initialize()
    
    #trials = exp1.run(trials, atributos)
    
    folds = cross.crossValidation(10, trials)
      
    #exp5.run(folds, atributos, 0.7)
    
    #exp6.run(folds, atributos, 0.7)
      
    exp7.run(trials, folds, atributos, {}, False)
    
    exp7.run(trials, folds, atributos, {}, True)