'''
Created on 07/02/2014

@author: thiagocastroferreira
'''

import itertools as iter

def isUnderspecified(expressao):
    for target in expressao["descricao"].keys():
        properties = expressao["descricao"][target]
        dominio = expressao["domain"]
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
    
def isOverspecified(expressao):
    for target in expressao["descricao"].keys():
        properties = expressao["descricao"][target]
        
        permutations = iter.permutations(properties.keys())
        
        for permutation in permutations:
            i = 0
            dominio = expressao["domain"]
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

def countAttributeFrequency(folds, teste):
    foldsAux = {}
    
    for fold in folds:
        if fold != teste:
            foldsAux[fold] = folds[fold]
            
    frequency = {}
    frequency["target"] = {}
    
    for fold in foldsAux:
        for anotacao in foldsAux[fold]:
            target = anotacao["caracteristicas"]["target"]
            
            for objeto in anotacao["descricao"]:
                for key in anotacao["descricao"][objeto].keys():
                    if objeto == target:
                        if key in frequency["target"].keys():
                            frequency["target"][key] = frequency["target"][key] + 1
                        else:
                            frequency["target"][key] = 1
    return frequency

#contabiliza frequenca dos atributos por participante
def countAttributeFrequencyIndividual(folds, teste):
    foldsAux = {}
    
    for fold in folds:
        if fold != teste:
            foldsAux[fold] = folds[fold]
            
    frequency = {}
    
    for fold in foldsAux:
        for participante in folds[fold]:
            for anotacao in folds[fold][participante]:
                targets = anotacao["caracteristicas"]["target"]
                
                if participante not in frequency.keys():
                    frequency[participante] = {}
                    frequency[participante]["target"] = {}
                
                for target in targets:
                    for objeto in anotacao["descricao"]:
                        for key in anotacao["descricao"][objeto].keys():
                            if objeto in targets:
                                if key in frequency[participante]["target"].keys():
                                    frequency[participante]["target"][key] = frequency[participante]["target"][key] + 1
                                else:
                                    frequency[participante]["target"][key] = 1
    return frequency

def defineExpressao(expressao):
    #descricao prevista pela svm
    descricao = {}
    
    for target in expressao.keys():
        descricao[target] = {}
        dominio = expressao[target]["anotacao"]["domain"]
        
        for atributo in dominio[target].keys():
            descricao[target][atributo] = dominio[target][atributo]
        
        for atributo in ["type", "colour", "orientation", "size", "x-dimension", "y-dimension"]:
            if expressao[target]["previsoes"][atributo] == 0:
                if atributo in descricao[target].keys():
                    del descricao[target][atributo]
    
    return descricao