'''
Created on 19/12/2012

@author: thiagocastroferreira
'''

import itertools as iter
from IncrementalAlgorithmRelational5 import *
from IncrementalAlgorithmRelationalOverspecified import *

def isUnderspecified(expressao, dominio):
    properties = expressao["descricao"]["tg"]
    
    distractors = {}
    for property in properties.keys():
        distractors = {}
        for element in properties[property]:
            for object in dominio.keys():
                if property in dominio[object].keys():
                    if element in dominio[object][property]:
                        distractors[object] = dominio[object]
            dominio = distractors
    
    if len(distractors.keys()) > 1:
        return True
    return False
    
def isOverspecified(expressao, dominio):
    properties = expressao["descricao"]["tg"]
    
    permutations = iter.permutations(properties.keys())
    
    for permutation in permutations:
        i = 0
        
        for property in permutation:
            i = i + 1
            distractors = {}
            for element in properties[property]:
                for object in dominio.keys():
                    if property in dominio[object].keys():
                        if element in dominio[object][property]:
                            distractors[object] = dominio[object]
                dominio = distractors
        
            if len(distractors.keys()) == 1 and i < len(properties.keys()):
                return True
    return False

#contabiliza frequenca dos atributos
def countAttributeFrequencyIndividual(folds, teste):
    foldsAux = {}
    
    for fold in folds:
        if fold != teste:
            foldsAux[fold] = folds[fold]
            
    frequency = {}
    
    for fold in foldsAux:
        for anotacao in folds[fold]:
            target = "tg"
            participante = anotacao["caracteristicas"]["trial"]
            
            if participante not in frequency.keys():
                frequency[participante] = {}
                frequency[participante]["target"] = {}
                frequency[participante]["landmark"] = {}
            
            for objeto in anotacao["descricao"]:
                for key in anotacao["descricao"][objeto].keys():
                    if objeto == target:
                        if key in frequency[participante]["target"].keys():
                            frequency[participante]["target"][key] = frequency[participante]["target"][key] + 1
                        else:
                            frequency[participante]["target"][key] = 1
                    else:
                        if key in frequency[participante]["landmark"].keys():
                            frequency[participante]["landmark"][key] = frequency[participante]["landmark"][key] + 1
                        else:
                            frequency[participante]["landmark"][key] = 1
    return frequency

def defineExpressao(expressao, frequencias, tamanhoTreinamento, dominio, target):
    lista_preferencia = {}
    lista_preferencia["target"] = []
    lista_preferencia["landmark"] = []
    
    previsoes = {"type":expressao["previsoes"]["type"],"col":expressao["previsoes"]["col"],"size":expressao["previsoes"]["size"],"loc":expressao["previsoes"]["loc"], "relation":expressao["previsoes"]["relation"]}
    
    frequency = {}
    for atributo in ['left-of', 'next-to', 'on-top-of', 'right-of']:
        if atributo in frequencias["target"].keys():
            frequency[atributo] = frequencias["target"][atributo]
    
    relacoes = []
    while len(frequency) != 0:
        maximo = 0
        atributoMaximo = str
        for atributo in frequency.keys():
            if frequency[atributo] > maximo:
                atributoMaximo = atributo
                maximo = frequency[atributo]
        relacoes.append(atributoMaximo)
        del frequency[atributoMaximo]
    
    while len(previsoes) != 0:
        maximo = 0
        atributoMaximo = str
        for atributo in previsoes.keys():
            if previsoes[atributo] > maximo:
                atributoMaximo = atributo
                maximo = previsoes[atributo]
        if atributoMaximo == "relation":
            lista_preferencia["target"].extend(relacoes)
        else:
            lista_preferencia["target"].append(atributoMaximo)
        del previsoes[atributoMaximo]
        
    
    previsoes = {"lm_type":expressao["previsoes"]["lm_type"],"lm_col":expressao["previsoes"]["lm_col"],"lm_size":expressao["previsoes"]["lm_size"],"lm_loc":expressao["previsoes"]["lm_loc"]}
    
    frequency = {}
    for atributo in ['left-of', 'next-to', 'on-top-of', 'right-of']:
        if atributo in frequencias["landmark"].keys():
            frequency[atributo] = frequencias["landmark"][atributo]
            
    relacoes = []
    
    while len(frequency) != 0:
        maximo = 0
        atributoMaximo = str
        for atributo in frequency.keys():
            if frequency[atributo] > maximo:
                atributoMaximo = atributo
                maximo = frequency[atributo]
        relacoes.append(atributoMaximo)
        del frequency[atributoMaximo]
    
    while len(previsoes) != 0:
        maximo = 0
        atributoMaximo = str
        for atributo in previsoes.keys():
            if previsoes[atributo] > maximo:
                atributoMaximo = atributo
                maximo = previsoes[atributo]
        if atributoMaximo == "lm_relation":
            lista_preferencia["landmark"].extend(relacoes)
        else:
            lista_preferencia["landmark"].append(atributoMaximo.split("_")[1])
        del previsoes[atributoMaximo]
        
    descricao = IncrementalAlgorithmRelational5(dominio, target, lista_preferencia, frequencias, 0.7, tamanhoTreinamento, False).run()
    
    return descricao