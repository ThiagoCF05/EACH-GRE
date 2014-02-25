'''
Created on 03/09/2013

@author: thiagocastroferreira
'''

import ParserStars as parser

def crossValidation(anotacoes = {}):
    if len(anotacoes) == 0: 
        anotacoes = parser.parseAnnotation()
    folds = {}
    
    for i in range(1,7):
        folds[i] = {}
    
    for anotacao in anotacoes:
        contexto = anotacao["caracteristicas"]["context"]
        participante = anotacao["caracteristicas"]["trial"]
        
        for i in range(1,7):
            if participante not in folds[i]:
                folds[i][participante] = anotacao
                break
    return folds
        