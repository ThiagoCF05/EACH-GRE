'''
Created on 31/10/2013

@author: thiagocastroferreira
'''
from sklearn import tree
import numpy as np

def run(inputs, fold):
    svms = {}
    svms["type"] = None
    svms["col"] = None
    svms["size"] = None
    svms["loc"] = None
    svms["relation"] = None
    svms["lm_type"] = None
    svms["lm_col"] = None
    svms["lm_size"] = None
    svms["lm_loc"] = None
    
    treinamento = {}
    for dir in inputs:
        treinamento[dir] = inputs[dir]
        
    teste = treinamento[fold]
    del treinamento[fold]
    
    svms = train(svms, treinamento)
    
    resultados = test(svms, teste)
    
    return resultados
    
def train(svms, treinamento):
    for svm1 in svms:
        data = []
        classe = []
        
        for fold in treinamento:
            for anotacao in treinamento[fold]:
                data.append(anotacao["data"])
                classe.append(anotacao["classes"][svm1])
        
        list = np.unique(classe)
        
        if len(list) == 1:
            if classe[0] == 0:
                classe[0] = 1
            else:
                classe[0] = 0
        
        svms[svm1] = tree.DecisionTreeClassifier()
        svms[svm1].fit(data, classe)
    return svms

def test(svms, teste):
    acertos = {}
    total = {}
    expressoes = []
    
    #matriz de confusao
    tp = {}
    tn = {}
    fp = {}
    fn = {}
    
    for anotacao in teste:

        anotacao["previsoes"] = {}
        for svm1 in svms:
            if svm1 not in acertos.keys():
                acertos[svm1] = 0.0
                total[svm1] = 0.0
                tp[svm1] = 0
                tn[svm1] = 0
                fp[svm1] = 0
                fn[svm1] = 0
            
            resultado = svms[svm1].predict([anotacao["data"]])
            real = anotacao["classes"][str(svm1)]
            
            anotacao["previsoes"][str(svm1)] = resultado[0]
            
            if real == resultado[0]:
                acertos[svm1] = acertos[svm1] + 1.0
            
            total[svm1] = total[svm1] + 1.0
            
            if real == 0 and resultado[0] == 0:
                tn[svm1] = tn[svm1] + 1
            elif real != 0 and resultado[0] != 0:
                tp[svm1] = tp[svm1] + 1
            elif real != 0 and resultado[0] == 0:
                fn[svm1] = fn[svm1] + 1
            elif real == 0 and resultado[0] != 0:
                fp[svm1] = fp[svm1] + 1
            
        expressoes.append(anotacao)
        
    return [acertos, total, expressoes, tp, tn, fp, fn]