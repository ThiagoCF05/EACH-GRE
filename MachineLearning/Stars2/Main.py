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
import Experiment1 as exp1
import SVMValidatedExperiment as exp2
import SVMValidatedExperiment2 as exp3
import ExperimentDecisionTree as exp4
import ValidatedExperimentIndividual as exp5

def initialize():
    anotacoes = parser.parseAnnotation()
    dominios = parser.parseDominio()
    participantes = {}
    atributos = ["type", "size", "colour", "hpos", "vpos", "near", "left", "right", "below", "above", "in-front-of"]
    targets = {"01f-t1n":"h", "01f-t1r":"h", "01f-t2n":"h", "01f-t2r":"h", "01o-t1n":"h", "01o-t1r":"h", "01o-t2n":"h", "01o-t2r":"h", "02f-t1n":"o", "02f-t1r":"o", "02f-t2n":"o", "02f-t2r":"o", "02o-t1n":"o", "02o-t1r":"o", "02o-t2n":"o", "02o-t2r":"o", "03f-t1n":"m", "03f-t1r":"m", "03f-t2n":"m", "03f-t2r":"m", "03o-t1n":"m", "03o-t1r":"m", "03o-t2n":"m", "03o-t2r":"m", "04f-t1n":"a", "04f-t1r":"a", "04f-t2n":"a", "04f-t2r":"a", "04o-t1n":"a", "04o-t1r":"a", "04o-t2n":"a", "04o-t2r":"a", "05f-t1n":"m", "05f-t2n":"m", "05f-t1r":"m", "05f-t2r":"m", "05o-t1n":"m", "05o-t1r":"m", "05o-t2n":"m", "05o-t2r":"m", "06f-t1n":"h", "06f-t1r":"h", "06f-t2n":"h", "06f-t2r":"h", "06o-t1n":"h", "06o-t1r":"h", "06o-t2n":"h", "06o-t2r":"h", "07f-t1n":"i", "07f-t1r":"i", "07f-t2n":"i", "07f-t2r":"i", "07o-t1n":"i", "07o-t1r":"i", "07o-t2n":"i", "07o-t2r":"i", "08f-t1n":"a", "08f-t1r":"a", "08f-t2n":"a", "08f-t2r":"a", "08o-t1n":"a", "08o-t1r":"a", "08o-t2n":"a", "08o-t2r":"a" }
    return dominios, targets, anotacoes, atributos, participantes


if __name__ == '__main__':
    dominios, targets, anotacoes, atributos, participantes = initialize()
    
    folds = cross.crossValidation(10, anotacoes)
    
    print "Machine Learning sem ID"
#     exp5.run(dominios, targets, anotacoes, atributos, False)
    exp2.run(dominios, targets, folds, atributos, {}, False)
    
    print "\n\n"
    print "Machine Learning com ID"
#     exp5.run(dominios, targets, anotacoes, atributos, True)
    exp2.run(dominios, targets, folds, atributos, {}, True)