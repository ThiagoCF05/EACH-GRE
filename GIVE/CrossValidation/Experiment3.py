'''
Created on 10/09/2013

@author: thiagocastroferreira
'''

import Assurance as ass
from IncrementalAlgorithmRelational3 import *
import numpy as num
from itertools import permutations
import random

# Experimento no corpus GIVE com o algoritmo IA com a lista de preferencia ordenada pela frequencia de atributos
# por participante
def run(contextos, folds, atributos):
    print 100 * "-"
    print "Experimento GIVE"
    print "algoritmo IA com a lista de preferencia ordenada pela frequencia de atributos por participante"
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
            descricao = IncrementalAlgorithmRelational3(contextos[contexto], target, preferencia[participante], True).run()
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
    preferencia = {}
    
    for participante in frequencia.keys():
        if participante not in lista_preferencia.keys():
            lista_preferencia[participante]  = {}
            lista_preferencia[participante]["target"]  = []
            lista_preferencia[participante]["landmark"]  = []
            preferencia[participante]  = {}
            preferencia[participante]["target"]  = []
            preferencia[participante]["landmark"]  = []
    
        while len(frequencia[participante]["target"]) != 0:
            maximo = max(frequencia[participante]["target"].values())
            
            for key in frequencia[participante]["target"].keys():
                if frequencia[participante]["target"][key] == maximo:
                    lista_preferencia[participante]["target"].append(key)
                    del(frequencia[participante]["target"][key])
                  
        while len(frequencia[participante]["landmark"]) != 0:
            maximo = max(frequencia[participante]["landmark"].values())
            
            for key in frequencia[participante]["landmark"].keys():
                if frequencia[participante]["landmark"][key] == maximo:
                    lista_preferencia[participante]["landmark"].append(key)
                    del(frequencia[participante]["landmark"][key])
    
    
        for atributo in lista_preferencia[participante]["target"]:
            if atributo in atributos:
                preferencia[participante]["target"].append(atributo)
        
        preferencia[participante]["landmark"]  = []
        for atributo in lista_preferencia[participante]["landmark"]:
            if atributo in atributos:
                preferencia[participante]["landmark"].append(atributo)
    
    return preferencia


def countAttributeFrequency(anotacoes):
    frequency = {}
    
    for anotacao in anotacoes:
        target = anotacao["caracteristicas"]["target"]
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