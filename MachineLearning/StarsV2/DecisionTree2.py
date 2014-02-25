'''
Created on 31/10/2013

@author: thiagocastroferreira
'''
from sklearn import tree
import numpy as np

def run(inputs, fold):
    svms = {}
    svms["type"] = None
    svms["colour"] = None
    svms["hpos"] = None
    svms["vpos"] = None
    svms["relation"] = None
    svms["lm_type"] = None
    svms["lm_colour"] = None
    svms["lm_hpos"] = None
    svms["lm_vpos"] = None
    svms["lm_relation"] = None
    svms["lm2_type"] = None
    svms["lm2_colour"] = None
    svms["lm2_hpos"] = None
    svms["lm2_vpos"] = None
    
    #Trained only with relational descriptions
    svmsRelational = {}
    svmsRelational["lm_type"] = None
    svmsRelational["lm_colour"] = None
    svmsRelational["lm_hpos"] = None
    svmsRelational["lm_vpos"] = None
    svmsRelational["lm_relation"] = None
    svmsRelational["lm2_type"] = None
    svmsRelational["lm2_colour"] = None
    svmsRelational["lm2_hpos"] = None
    svmsRelational["lm2_vpos"] = None
    
    treinamento = {}
    for dir in inputs:
        treinamento[dir] = inputs[dir]
        
    teste = treinamento[fold]
    del treinamento[fold]
    
    svms = train(svms, treinamento)
    
    svmsRelational = trainRelationalAttributes(svmsRelational, treinamento)
    
    svms["lm_type"] = svmsRelational["lm_type"]
    svms["lm_colour"] = svmsRelational["lm_colour"]
    svms["lm_hpos"] = svmsRelational["lm_hpos"]
    svms["lm_vpos"] = svmsRelational["lm_vpos"]
    svms["lm_relation"] = svmsRelational["lm_relation"]
    
    svmsRelational = trainRelationalAttributes(svmsRelational, treinamento, True)
    svms["lm2_type"] = svmsRelational["lm2_type"]
    svms["lm2_colour"] = svmsRelational["lm2_colour"]
    svms["lm2_hpos"] = svmsRelational["lm2_hpos"]
    svms["lm2_vpos"] = svmsRelational["lm2_vpos"]
    
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
        
        if len(classe) <= 1:
            svms[svm1] = None
        else:
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
            
            if svms[svm1] == None:
                resultado = [0]
            else:
                resultado = svms[svm1].predict([anotacao["data"]])
            real = anotacao["classes"][str(svm1)]
            
            anotacao["previsoes"][str(svm1)] = resultado[0]
            
            if svm1 in ["lm_type", "lm_colour", "lm_vpos", "lm_hpos"] and anotacao["classes"]["relation"] > 0:
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
                    
            elif svm1 in ["lm2_type", "lm2_colour", "lm2_vpos", "lm2_hpos"] and anotacao["classes"]["lm_relation"] > 0:
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
            elif svm1 not in ["lm_type", "lm_colour", "lm_vpos", "lm_hpos", "lm2_type", "lm2_colour", "lm2_vpos", "lm2_hpos"]:
                if real == int(resultado[0]):
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

def trainRelationalAttributes(svms, treinamento, landmark = False):
    for svm1 in svms:
        data = []
        classe = []
        
        for fold in treinamento:
            for anotacao in treinamento[fold]:
                if landmark == False:
                    if anotacao["classes"]["relation"] > 0:
                        data.append(anotacao["data"])
                        classe.append(anotacao["classes"][svm1])
                else:
                    if anotacao["classes"]["lm_relation"] > 0:
                        data.append(anotacao["data"])
                        classe.append(anotacao["classes"][svm1])
        
        
        if len(classe) <= 1:
            svms[svm1] = None
        else:
            list = np.unique(classe)
            
            if len(list) == 1:
                if classe[0] == 0:
                    classe[0] = 1
                else:
                    classe[0] = 0
            
            svms[svm1] = tree.DecisionTreeClassifier()
            svms[svm1].fit(data, classe)
    return svms       
    