'''
Created on 14/09/2013

@author: thiagocastroferreira
'''

import Parser as parser
import Assurance as ass
import IncrementalAlgorithmRelational5 as ie5
import IncrementalAlgorithmRelationalOverspecified as ieo
import numpy as num
import random

def run(dominios, targets, folds, atributos, probabilidade):
    
    mediaDice = []
    mediaMasi = []
    acuracia = 0.
    numeroDescricoes = 0.
    mediaDiceSuperespecificada = []
    mediaMasiSuperespecificada = []
    acuraciaSuperespecificada = 0.
    numeroDescricoesSuperespecificada = 0.
    
    for i in range(1, len(folds)+1):
        fold = str(i)
        
        print "Fold: ", fold
        print 50 * "-"
        
        [treinamento, teste] = toList(folds, fold)
        frequencia = countAttributeFrequency(treinamento)
        
        lista_preferencia = getListaPreferencia(frequencia, atributos)
        
        frequencia = countAttributeFrequency(treinamento)
        
        mediaFoldDice = []
        mediaFoldMasi = []
        acuraciaFold = 0.
        numeroDescricoesFold = 0.
        mediaFoldDiceSuperespecificada = []
        mediaFoldMasiSuperespecificada = []
        acuraciaFoldSuperespecificada = 0.
        numeroDescricoesFoldSuperespecificada = 0.
    
        for anotacao in teste:
            contexto = anotacao["caracteristicas"]["context"]
            participante = str(anotacao["caracteristicas"]["trial"])
            
            A = []
            for expressao in anotacao["anotacoes"].keys():
                A.extend(ass.parse(anotacao["anotacoes"][expressao]))
            A = set(A)
            
            #random.shuffle(atributos)
            descricao = ie5.run(dominios[contexto], targets[contexto], lista_preferencia, False)
            
            B = []
            i = 0
            for expressao in descricao.keys():
                B.extend(ass.parse(descricao[expressao], targets[contexto][i]))
                i = i + 1
            B = set(B)
            
            DICE = ass.dice(A, B)
            MASI = ass.masi(A, B)
            
            if DICE == 1.0:
                acuracia = acuracia + 1
                acuraciaFold = acuraciaFold + 1
            numeroDescricoes = numeroDescricoes + 1
            numeroDescricoesFold = numeroDescricoesFold + 1
            
            mediaDice.append(DICE)
            mediaMasi.append(MASI)
            
            mediaFoldDice.append(DICE)
            mediaFoldMasi.append(MASI)
            
            anotacao["dice_global"] = DICE
            anotacao["masi_global"] = MASI
            anotacao["algoritmo_global"] = descricao
            
            descricao = ieo.run(dominios[contexto], targets[contexto], lista_preferencia, frequencia, probabilidade, len(treinamento), False)
            
            B = []
            i = 0
            for expressao in descricao.keys():
                B.extend(ass.parse(descricao[expressao], targets[contexto][i]))
                i = i + 1
            B = set(B)
            
            DICE = ass.dice(A, B)
            MASI = ass.masi(A, B)
            
            if DICE == 1.0:
                acuraciaSuperespecificada = acuraciaSuperespecificada + 1
                acuraciaFoldSuperespecificada = acuraciaFoldSuperespecificada + 1
            numeroDescricoesSuperespecificada = numeroDescricoesSuperespecificada + 1
            numeroDescricoesFoldSuperespecificada = numeroDescricoesFoldSuperespecificada + 1
            
            mediaDiceSuperespecificada.append(DICE)
            mediaMasiSuperespecificada.append(MASI)
            
            mediaFoldDiceSuperespecificada.append(DICE)
            mediaFoldMasiSuperespecificada.append(MASI)
            
            anotacao["dice_global_superespecificado"] = DICE
            anotacao["masi_global_superespecificado"] = MASI
            anotacao["algoritmo_global_superespecificado"] = descricao
        
#             print anotacao["descricao"]
#             print anotacao["algoritmo"]
#             print anotacao["caracteristicas"]
#             print anotacao["dice"] 
#             print anotacao["masi"] 
#             print 50 * "*"
            
        print "Dice: ", num.mean(mediaFoldDice)
        print "Masi: ",num.mean(mediaFoldMasi)
        print "Acuracia: ",acuraciaFold / numeroDescricoesFold
        print "Dice Superespecificado: ", num.mean(mediaFoldDiceSuperespecificada)
        print "Masi Superespecificado: ",num.mean(mediaFoldMasiSuperespecificada)
        print "Acuracia Superespecificado: ",acuraciaFoldSuperespecificada / numeroDescricoesFoldSuperespecificada
        print "\n"
        
    print "Dice: ", num.mean(mediaDice)
    print "Masi: ",num.mean(mediaMasi)
    print "Acuracia: ",acuracia / numeroDescricoes
    print "Dice Superespecificado: ", num.mean(mediaDiceSuperespecificada)
    print "Masi Superespecificado: ",num.mean(mediaMasiSuperespecificada)
    print "Acuracia Superespecificado: ",acuraciaSuperespecificada / numeroDescricoesSuperespecificada
    print "\n"
    
    return folds
    
    #print lista_preferencia

def countAttributeFrequency(anotacoes):
    frequency = {}
    frequency["target"] = {}
    frequency["landmark"] = {}
    
    for anotacao in anotacoes:
        target = "tg"
        
        for descricao in anotacao["anotacoes"]:
            for objeto in anotacao["anotacoes"][descricao]:
                for key in anotacao["anotacoes"][descricao][objeto].keys():
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

def getListaPreferencia(frequencia, atributos):
    lista_preferencia  = {}
    lista_preferencia["target"]  = []
    lista_preferencia["landmark"]  = []
    preferencia  = {}
    preferencia["target"]  = []
    preferencia["landmark"]  = []
    
    frequenciaRelacionais = {}
    frequenciaRel = 0
    if "right-to" in frequencia["target"].keys():
        frequenciaRelacionais["right-to"] = frequencia["target"]["right-to"]
        frequenciaRel = frequenciaRel + frequencia["target"]["right-to"]
        del(frequencia["target"]["right-to"])
    if "left-to" in frequencia["target"].keys():
        frequenciaRelacionais["left-to"] = frequencia["target"]["left-to"]
        frequenciaRel = frequenciaRel + frequencia["target"]["left-to"]
        del(frequencia["target"]["left-to"])
    if "in-front-of" in frequencia["target"].keys():
        frequenciaRelacionais["in-front-of"] = frequencia["target"]["in-front-of"]
        frequenciaRel = frequenciaRel + frequencia["target"]["in-front-of"]
        del(frequencia["target"]["in-front-of"])
    if "next-to" in frequencia["target"].keys():
        frequenciaRelacionais["next-to"] = frequencia["target"]["next-to"]
        frequenciaRel = frequenciaRel + frequencia["target"]["next-to"]
        del(frequencia["target"]["next-to"])
    if "behind" in frequencia["target"].keys():
        frequenciaRelacionais["behind"] = frequencia["target"]["behind"]
        frequenciaRel = frequenciaRel + frequencia["target"]["behind"]
        del(frequencia["target"]["behind"])
    
    while len(frequencia["target"]) != 0:
        maximo = max(frequencia["target"].values())
        
        if maximo < frequenciaRel and len(frequenciaRelacionais) != 0:
            while len(frequenciaRelacionais) != 0:
                maximo1 = max(frequenciaRelacionais.values())
                
                for key in frequenciaRelacionais.keys():
                    if frequenciaRelacionais[key] == maximo1:
                        lista_preferencia["target"].append(key)
                        del(frequenciaRelacionais[key])
        else:
            for key in frequencia["target"].keys():
                if frequencia["target"][key] == maximo:
                    lista_preferencia["target"].append(key)
                    del(frequencia["target"][key])
    
    while len(frequenciaRelacionais) != 0:
        maximo1 = max(frequenciaRelacionais.values())
        
        for key in frequenciaRelacionais.keys():
            if frequenciaRelacionais[key] == maximo1:
                lista_preferencia["target"].append(key)
                del(frequenciaRelacionais[key])      
              
    while len(frequencia["landmark"]) != 0:
        maximo = max(frequencia["landmark"].values())
        
        for key in frequencia["landmark"].keys():
            if frequencia["landmark"][key] == maximo:
                lista_preferencia["landmark"].append(key)
                del(frequencia["landmark"][key])


    for atributo in lista_preferencia["target"]:
        if atributo in atributos:
            preferencia["target"].append(atributo)
    
    preferencia["landmark"]  = []
    for atributo in lista_preferencia["landmark"]:
        if atributo in atributos:
            preferencia["landmark"].append(atributo)
    return preferencia