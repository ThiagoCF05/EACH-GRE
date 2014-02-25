'''
Created on 03/09/2013

@author: thiagocastroferreira
'''

def crossValidation(fold = int, anotacoes = {}):
    folds = {}
    
    nroParticipantes = contabilizaParticipantes(anotacoes)
    nroAnotacoes = len(anotacoes)
    
    expressoesParticipantePorFold = (nroAnotacoes / nroParticipantes) / fold
    
    nroExpressoes = {}
    for i in range(1,fold+1):
        folds[str(i)] = {}
        nroExpressoes[str(i)] = {}
    
    for anotacao in anotacoes:
        participante = anotacao["caracteristicas"]["participante"]
        
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
    return folds

def contabilizaParticipantes(anotacoes):
    participantes = 0
    visitados = []
    for anotacao in anotacoes:
        participante = anotacao["caracteristicas"]["participante"]
        if participante not in visitados:
            participantes = participantes + 1
            visitados.append(participante)
    
    return participantes