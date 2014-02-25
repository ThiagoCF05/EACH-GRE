'''
Created on 13/09/2013

@author: thiagocastroferreira
'''
'''
Created on 03/09/2013

@author: thiagocastroferreira
'''

import ParserGIVE as parser

def crossValidation(fold = int, anotacoes = {}):
    if len(anotacoes) == 0: 
        anotacoes = parser.parseAnnotation()
    folds = {}
    
    nroParticipantes = contabilizaParticipantes(anotacoes)
    nroAnotacoes = len(anotacoes)
    
    expressoesParticipantePorFold = (nroAnotacoes / nroParticipantes) / fold
    
    nroExpressoes = {}
    for i in range(1,fold+1):
        folds[str(i)] = {}
        nroExpressoes[str(i)] = {}
    
    for anotacao in anotacoes:
        contexto = anotacao["caracteristicas"]["context"]
        participante = anotacao["caracteristicas"]["trial"]
        
        achou = False
        for i in range(1,fold+1):
            if participante not in folds[str(i)]:
                folds[str(i)][participante] = []
                nroExpressoes[str(i)][participante] = expressoesParticipantePorFold
            if nroExpressoes[str(i)][participante] > 0:
                folds[str(i)][participante].append(anotacao)
                nroExpressoes[str(i)][participante] = nroExpressoes[str(i)][participante] -1
                achou = True
                break
        
        if achou == False:
            for i in range(1,fold+1):
                if nroExpressoes[str(i)][participante] == 0:
                    folds[str(i)][participante].append(anotacao)
                    nroExpressoes[str(i)][participante] = nroExpressoes[str(i)][participante] -1
                    break
        
    newFolds = {}
    for fold in folds:
        if fold not in newFolds.keys():
            newFolds[fold] = []
        for participante in folds[fold].keys():
            for anotacao in folds[fold][participante]:
                newFolds[fold].append(anotacao)
    return newFolds

def contabilizaParticipantes(anotacoes):
    participantes = 0
    visitados = []
    for anotacao in anotacoes:
        participante = anotacao["caracteristicas"]["trial"]
        if participante not in visitados:
            participantes = participantes + 1
            visitados.append(participante)
    
    return participantes
        