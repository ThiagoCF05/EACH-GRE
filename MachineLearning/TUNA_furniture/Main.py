'''
Created on 21/12/2012

@author: thiagocastroferreira
'''
# import matplotlib.pyplot as plt
# from hcluster import *
import Parser as parser
import CrossValidation as cross
import SVMValidatedExperiment as exp2
import ExperimentDecisionTree as exp4
import ValidatedExperimentIndividual as exp5

def initialize():
    trials = parser.parse()
    atributos = ["type", "colour", "orientation", "size", "x-dimension", "y-dimension"]
    return trials, atributos


if __name__ == '__main__':
    trials, atributos = initialize()
    
#     exp5.run(trials, atributos, False)
    
#     exp5.run(trials, atributos, True)
    
    folds = cross.crossValidation(10, trials)
     
    print "Machine Learning sem ID"
#     exp2.run(trials, folds, atributos, {}, False)
      
    print "\n\n"
    print "Machine Learning com ID"
    exp2.run(trials, folds, atributos, {}, True)