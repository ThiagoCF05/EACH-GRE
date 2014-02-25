'''
Created on 19/12/2012

@author: thiagocastroferreira
'''
import numpy as np
from scipy.stats import wilcoxon, chisquare
# import matplotlib.pyplot as plt
# from hcluster import *
import Assurance as ass
import Experiment1 as exp1
import Experiment5 as exp5
import Experiment6 as exp6
import Parser as parser
import CrossValidation as cross


def initialize():
    anotacoes = parser.parseAnnotation()
    dominios = parser.parseMapas()
    targets = {"1":["rest3"],"2":["cafe1"],"3":["drug3"],"4":["chur3"],"5":["pub1"],"6":["chur2","chur3"],"7":["rest1","rest2"],"8":["drug2","drug3"],"9":["drug3","drug4"],"10":["rest4","rest5"],"11":["rest3"],"12":["cafe1"],"13":["rest4","rest5"],"14":["chur3"],"15":["pub1"],"16":["chur2","chur3"],"17":["rest1","rest2"],"18":["drug2","drug3"],"19":["drug3","drug4"],"20":["rest4","rest5"]}
    atributos = ["type","in","name","next-to","in-front-of","other","right-to","left-to","behind"]
    return dominios, targets, anotacoes, atributos

if __name__ == '__main__':
    dominios, targets, anotacoes, atributos = initialize()

    anotacoes = exp1.run(dominios, targets, anotacoes, atributos)
    
    folds = cross.crossValidation(10, anotacoes)
    
    anotacoes = exp5.run(dominios, targets, folds, atributos, 0.7)
    
    anotacoes = exp6.run(dominios, targets, folds, atributos, 0.7)
    
