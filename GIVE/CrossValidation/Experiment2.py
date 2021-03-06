'''
Created on 03/09/2013

@author: thiagocastroferreira
'''

import Assurance as ass
from IncrementalAlgorithmRelational3 import *
import numpy as num
from itertools import permutations
import random

# Experimento no corpus GIVE com o algoritmo IA com a lista de preferencia ordenada pela frequencia de atributos
def run(contextos, folds, atributos):
    
    print 100 * "-"
    print "Experimento GIVE"
    print "algoritmo IA com a lista de preferencia ordenada pela frequencia de atributos"
    print 100 * "-"
    mediaDice = []
    mediaMasi = []
    acuracia = 0.
    numeroDescricoes = 0.
    
    mediaFoldDice = {}
    mediaFoldMasi = {}
    acuraciaFold = {}
    numeroDescricoesFold = {}
    
    for i in range(1, len(folds)+1):
        fold = str(i)
        mediaFoldDice[fold] = []
        mediaFoldMasi[fold] = []
        acuraciaFold[fold] = 0.0
        numeroDescricoesFold[fold] = 0.0
        
        [treinamento, teste] = toList(folds, fold)
        
        frequencia = countAttributeFrequency(treinamento)
    
        preferencia = defineListaPreferencia(frequencia, atributos)
        
        for anotacao in teste:
            contexto = anotacao["caracteristicas"]["context"]
            participante = str(anotacao["caracteristicas"]["trial"])
            target = anotacao["caracteristicas"]["target"]
            
            A = ass.parse(anotacao["descricao"]) 
            
            #random.shuffle(atributos)
            descricao = IncrementalAlgorithmRelational3(contextos[contexto], target, preferencia, False).run()
            B = ass.parse(descricao)
            
            DICE = ass.dice(A, B)
            MASI = ass.masi(A, B)
            
            if DICE == 1.0:
                acuracia = acuracia + 1
                acuraciaFold[fold] = acuraciaFold[fold] + 1
            numeroDescricoes = numeroDescricoes + 1
            numeroDescricoesFold[fold] = numeroDescricoesFold[fold] + 1
            
            mediaFoldDice[fold].append(DICE)
            mediaFoldMasi[fold].append(MASI)
            mediaDice.append(DICE)
            mediaMasi.append(MASI)
            
            anotacao["dice"] = DICE
            anotacao["masi"] = MASI
            anotacao["algoritmo"] = descricao
    
    #         print anotacao["descricao"]
    #         print anotacao["algoritmo"]
    #         print anotacao["caracteristicas"]
    #         print anotacao["dice"] 
    #         print anotacao["masi"] 
    #         print 100 * "*"
        print "Fold: " + fold
        print "DICE: " + str(num.mean(mediaFoldDice[fold]))
        print "MASI: " + str(num.mean(mediaFoldMasi[fold]))
        print "Acuracia: " + str(acuraciaFold[fold] / numeroDescricoesFold[fold])
        print 20 * "*"
    
    print 10 * "-" 
    print "Geral: "
    print "DICE: " + str(num.mean(mediaDice))
    print "MASI: " + str(num.mean(mediaMasi))
    print "Acuracia: " + str(acuracia / numeroDescricoes)
    print 10 * "-" 
    print "\n"
    
#     print lista_preferencia

def defineListaPreferencia(frequencia, atributos):
    lista_preferencia = {}
    lista_preferencia["target"]  = []
    while len(frequencia["target"]) != 0:
        maximo = max(frequencia["target"].values())
        
        for key in frequencia["target"].keys():
            if frequencia["target"][key] == maximo:
                lista_preferencia["target"].append(key)
                del(frequencia["target"][key])
       
    lista_preferencia["landmark"]  = []         
    while len(frequencia["landmark"]) != 0:
        maximo = max(frequencia["landmark"].values())
        
        for key in frequencia["landmark"].keys():
            if frequencia["landmark"][key] == maximo:
                lista_preferencia["landmark"].append(key)
                del(frequencia["landmark"][key])
    
    preferencia = {}
    preferencia["target"]  = []
    for atributo in lista_preferencia["target"]:
        if atributo in atributos:
            preferencia["target"].append(atributo)
    
    preferencia["landmark"]  = []
    for atributo in lista_preferencia["landmark"]:
        if atributo in atributos:
            preferencia["landmark"].append(atributo)
    
    return preferencia

def countAttributeFrequency(anotacoes):
    frequency = {}
    frequency["target"] = {}
    frequency["landmark"] = {}
    
    for anotacao in anotacoes:
        target = anotacao["caracteristicas"]["target"]
        
        for objeto in anotacao["descricao"]:
            for key in anotacao["descricao"][objeto].keys():
                if objeto == target:
                    if key in frequency["target"].keys():
                        frequency["target"][key] = frequency["target"][key] + 1
                    else:
                        frequency["target"][key] = 1
                else:
                    if key in frequency["landmark"].keys():
                        frequency["landmark"][key] = frequency["landmark"][key] + 1
                    else:
                        frequency["landmark"][key] = 1
    return frequency

def toList(folds, teste):
    treinamentoSet = []
    testeSet = []
    for fold in folds:
        if fold == teste:
            for participante in folds[fold].keys():
                for anotacao in folds[fold][participante]:
                    testeSet.append(anotacao)
        else:
            for participante in folds[fold].keys():
                for anotacao in folds[fold][participante]:
                    treinamentoSet.append(anotacao)
        
    return [treinamentoSet, testeSet]