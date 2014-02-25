
'''
Created on 19/12/2012

@author: thiagocastroferreira
'''
import numpy as np
# import matplotlib.pyplot as plt
# from hcluster import *
import Assurance as ass
import ParserGIVE as parser
import CrossValidation as cross
import Experimento1 as exp1

#corner right left up next,  in front of, behind

def initialize():
    dominios = parser.parseDominio()
    anotacoes = parser.parseAnnotation()
    atributos = ['leftaround', 'right', 'orientation', 'color', 'straight', 'next', 'slightlyleft', 'rightaround', 'left', 'type', 'slightlyright']
    return dominios, anotacoes, atributos

if __name__ == '__main__':
    contextos, anotacoes, atributos = initialize()
     
    folds = cross.crossValidation(10, anotacoes) 
    featureVectors = parser.parseFeatureVector()
    
    inputs = {}
    for fold in folds:
        inputs[fold] = parser.parseSVMInput(contextos, folds[fold], featureVectors)
        
    resultadoTotal = []
    for fold in ["1","2","3","4","5","6","7","8","9","10"]:
        print "FOLD: " + fold
        resultados = exp1.run(inputs, fold)
        
        resultadoTotal.append(resultados)
        
        acertos = resultados[0]
        total = resultados[1]
        expressoes = resultados[2]
        tp = resultados[3]
        tn = resultados[4]
        fp = resultados[5]
        fn = resultados[6]

        dice = []
        acuracia = 0.0
        
        
        for atributo in acertos.keys():
            print "Atributo: " + str(atributo)
            print "Acuracia: " + str(acertos[atributo] / total[atributo])
            print "Verdadeiros Positivos: " + str(tp[atributo])
            print "Falsos Positivos: " + str(fp[atributo])
            print "Verdadeiros Negativos: " + str(tn[atributo])
            print "Falsos Negativos: " + str(fn[atributo])
            print 10 * "-"
        
        print 50 * "*"
    
    acertosT = {}
    totalT = {}
    for resultados in resultadoTotal:
        acertos = resultados[0]
        total = resultados[1]
        
        for atributo in acertos.keys():
            if atributo not in acertosT:
                acertosT[atributo] = 0.0
                totalT[atributo] = 0.0
            
            acertosT[atributo] = acertosT[atributo] + acertos[atributo]
            totalT[atributo] = totalT[atributo] + total[atributo]
            
    for atributo in acertosT.keys():
        print "Atributo: " + str(atributo)
        print "Acuracia: " + str(acertosT[atributo] / totalT[atributo])
        print 10 * "-"