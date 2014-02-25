'''
Created on 19/12/2012

@author: thiagocastroferreira
'''
import numpy as np
# import matplotlib.pyplot as plt
# from hcluster import *
import Assurance as ass
from ParserGIVE import *
import CrossValidation as cross
import Experiment1 as exp1
import Experiment2 as exp2
import Experiment3 as exp3
import Experiment4 as exp4
import Experiment5 as exp5

def initialize():
    dominios = parseDominio()
    anotacoes = parseAnnotation()
    atributos = ['leftaround', 'right', 'orientation', 'color', 'straight', 'next', 'slightlyleft', 'rightaround', 'left', 'type', 'slightlyright']
    return dominios, anotacoes, atributos

if __name__ == '__main__':
    contextos, anotacoes, atributos = initialize()
     
    folds = cross.crossValidation(10, anotacoes) 
    
    anotacoes = exp1.run(contextos, anotacoes, atributos)
    
    exp2.run(contextos, folds, atributos)
     
    exp3.run(contextos, folds, atributos)
    
    exp4.run(contextos, folds, atributos)
     
    exp5.run(contextos, folds, atributos)
    