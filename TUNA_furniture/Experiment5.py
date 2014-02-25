'''
Created on 03/09/2013

@author: thiagocastroferreira
'''

import Assurance as ass
from IncrementalAlgorithmRelational5 import *
from IncrementalAlgorithmRelationalOverspecified import *
import numpy as num

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

def countAttributeFrequency(anotacoes):
    frequency = {}
    frequency["target"] = {}
    
    for anotacao in anotacoes:
        targets = anotacao["caracteristicas"]["target"]
        
        for objeto in anotacao["descricao"]:
            for key in anotacao["descricao"][objeto].keys():
                if objeto in targets:
                    if key in frequency["target"].keys():
                        frequency["target"][key] = frequency["target"][key] + 1
                    else:
                        frequency["target"][key] = 1
    return frequency

def run(folds, atributos, probabilidade):
    
    diceGeral = []
    masiGeral = []
    acuraciaGeral = []
    diceGeralSuperespecificada = []
    masiGeralSuperespecificada = []
    acuraciaGeralSuperespecificada = []
    anotacoes = {}
    
    print 50 * "*"
    print 50 * "-"
    print "Experimento TUNA Furniture Global"
    print 50 * "-"
    
    for fold in folds:
        print 50 * "-"
        print "FOLD: ", fold
        print 50 * "-"
        [treinamento, teste] = toList(folds, fold)
        
        anotacoes[fold] = {}
    
        frequencia = countAttributeFrequency(treinamento)
        
        lista_preferencia = getListaPreferencia(frequencia, atributos)
        
        frequencia = countAttributeFrequency(treinamento)
        
        # inclui os atributos nao mencionados no final da lista de preferencia
#         random.shuffle(atributos)
#         for atributo in atributos:
#             if atributo not in lista_preferencia["target"]:
#                 lista_preferencia["target"].append(atributo)
#               
#             if atributo not in lista_preferencia["landmark"]:
#                 lista_preferencia["landmark"].append(atributo)
        
        mediaDice = []
        mediaMasi = []
        mediaDiceSuperespecificada = []
        mediaMasiSuperespecificada = []
        acuracia = 0.
        acuraciaSuperespecificada = 0.
        numeroDescricoes = 0.
        numeroDescricoesSuperespecificada = 0.
        
        for anotacao in teste:
            participante = str(anotacao["caracteristicas"]["participante"])
            targets = anotacao["caracteristicas"]["target"]
            
            A = ass.parse(anotacao["descricao"])
            
            descricao = IncrementalAlgorithmRelational5(anotacao["domain"], targets, lista_preferencia, frequencia, probabilidade, len(treinamento), False).run()
            B = ass.parse(descricao)
                
            DICE = ass.dice(A, B)
            MASI = ass.masi(A, B)
            
            if DICE == 1.0:
                acuracia = acuracia + 1
            numeroDescricoes = numeroDescricoes + 1
            
            mediaDice.append(DICE)
            mediaMasi.append(MASI)
            
            anotacao["dice_global"] = DICE
            anotacao["masi_global"] = MASI
            anotacao["algoritmo_global"] = descricao
            
            descricao = IncrementalAlgorithmRelationalOverspecified(anotacao["domain"], targets, lista_preferencia, frequencia, probabilidade, len(treinamento), False).run()
            B = ass.parse(descricao)
                
            DICE = ass.dice(A, B)
            MASI = ass.masi(A, B)
            
            if DICE == 1.0:
                acuraciaSuperespecificada = acuraciaSuperespecificada + 1
            numeroDescricoesSuperespecificada = numeroDescricoesSuperespecificada + 1
            
            mediaDiceSuperespecificada.append(DICE)
            mediaMasiSuperespecificada.append(MASI)
            
            anotacao["dice_global_superespecificado"] = DICE
            anotacao["masi_global_superespecificado"] = MASI
            anotacao["algoritmo_global_superespecificado"] = descricao
            
            #anotacoes[fold][participante] = anotacao
            
#             print anotacao["descricao"]
#             print anotacao["algoritmo_global"]
#             print anotacao["caracteristicas"]
#             print anotacao["dice_global"] 
#             print anotacao["masi_global"] 
#             print 50 * "*"
            
        print "DICE: ", num.mean(mediaDice)
        print "MASI: ", num.mean(mediaMasi)
        print "ACURACIA: ", acuracia / numeroDescricoes
        print "\n"
        
        diceGeral.append(num.mean(mediaDice))
        masiGeral.append(num.mean(mediaMasi))
        acuraciaGeral.append(acuracia / numeroDescricoes)
        diceGeralSuperespecificada.append(num.mean(mediaDiceSuperespecificada))
        masiGeralSuperespecificada.append(num.mean(mediaMasiSuperespecificada))
        acuraciaGeralSuperespecificada.append(acuraciaSuperespecificada / numeroDescricoesSuperespecificada)
        
#         for key in lista_preferencia:
#             print key, lista_preferencia[key]
    print 50 * "-"
    print "GERAL: "
    print 50 * "-"
    print "DICE: ", num.mean(diceGeral)
    print "MASI: ", num.mean(masiGeral)
    print "ACURACIA: ", num.mean(acuraciaGeral)
    print "DICE SUPERESPECIFICADO: ", num.mean(diceGeralSuperespecificada)
    print "MASI SUPERESPECIFICADO: ", num.mean(masiGeralSuperespecificada)
    print "ACURACIA SUPERESPECIFICADA: ", num.mean(acuraciaGeralSuperespecificada)
    print 50 * "*"
    print "\n"
    
    return folds

def getListaPreferencia(frequencia, atributos):
    lista_preferencia  = {}
    lista_preferencia["target"]  = []
    preferencia  = {}
    preferencia["target"]  = []
    
    while len(frequencia["target"]) != 0:
        maximo = max(frequencia["target"].values())
        
        for key in frequencia["target"].keys():
            if frequencia["target"][key] == maximo:
                lista_preferencia["target"].append(key)
                del(frequencia["target"][key])    

    for atributo in lista_preferencia["target"]:
        if atributo in atributos:
            preferencia["target"].append(atributo)
    return preferencia     