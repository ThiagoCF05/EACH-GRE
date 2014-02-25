'''
Created on 06/01/2014

@author: thiagocastroferreira
'''

import Parser as parser
import itertools as iter

targets = {"1":["rest3"],"2":["cafe1"],"3":["drug3"],"4":["chur3"],"5":["pub1"],"6":["chur2","chur3"],"7":["rest1","rest2"],"8":["drug2","drug3"],"9":["drug3","drug4"],"10":["rest4","rest5"],"11":["rest3"],"12":["cafe1"],"13":["rest4","rest5"],"14":["chur3"],"15":["pub1"],"16":["chur2","chur3"],"17":["rest1","rest2"],"18":["drug2","drug3"],"19":["drug3","drug4"],"20":["rest4","rest5"]}
dominios = parser.parseMapas()

def isUnderspecified(expressao):
    
    for anotacao in expressao["anotacoes"]:
        for target in expressao["anotacoes"].keys():
            for objeto in expressao["anotacoes"][target]:
                if objeto == "tg":
                    properties = expressao["anotacoes"][target][objeto]
                    dominio = dominios[expressao["caracteristicas"]["context"]]
                    distractors = {}
                    for property in properties.keys():
                        distractors = {}
                        for element in properties[property]:
                            for object in dominio.keys():
                                if element in dominio[object][property]:
                                    distractors[object] = dominio[object]
                            dominio = distractors
                    
                    if len(distractors.keys()) > 1:
                        return True
    return False
    
def isOverspecified(expressao):
    for anotacao in expressao["anotacoes"]:
        for target in expressao["anotacoes"].keys():
            for objeto in expressao["anotacoes"][target]:
                if objeto == "tg":
                    properties = expressao["anotacoes"][target][objeto]
                    
                    permutations = iter.permutations(properties.keys())
                    
                    for permutation in permutations:
                        i = 0
                        dominio = dominios[expressao["caracteristicas"]["context"]]
                        for property in permutation:
                            i = i + 1
                            distractors = {}
                            for element in properties[property]:
                                for object in dominio.keys():
                                    if element in dominio[object][property]:
                                        distractors[object] = dominio[object]
                                dominio = distractors
                        
                            if len(distractors.keys()) == 1 and i < len(properties.keys()):
                                return True
    return False

def run():
    expressoes, dadosParticipantes = parser.parseAnnotation()
    
    participantes = {}
    participantesRelacionaiss = {}
    
    expressoesSimples = 0
    expressoesConjunto = 0
    
    expressoesSubespecificadas = 0
    expressoesSubespecificadasMulheres = 0
    expressoesSubespecificadasHomens = 0
    expressoesSuperespecificadas = 0
    expressoesSuperespecificadasMulheres = 0
    expressoesSuperespecificadasHomens = 0
    
    expressoesRelacionais = 0
    expressoesRelacionaisConjunto = 0
    
    participantesHomens = 0
    participantesMulheres = 0
    
    participantesRelacionais = 0
    participantesMistos = 0
    participantesNaoRelacionais = 0
    
    participantesHomensRelacionais = 0
    participantesHomensNaoRelacionais = 0
    participantesHomensSuperespecificadas = {}
    participantesHomensSubespecificadas = {}
    
    participantesMulheresRelacionais = 0
    participantesMulheresNaoRelacionais = 0
    participantesMulheresSuperespecificadas = {}
    participantesMulheresSubespecificadas = {}
    
    participantesSuperespecificadosHomens = 0
    participantesSuperespecificadosMulheres = 0
    participantesSubespecificadosHomens = 0
    participantesSubespecificadosMulheres = 0
    
    frequencias = {}
    frequencias["tg"] = {}
    frequencias["lm"] = {}
    
    for expressao in expressoes:
        if expressao["caracteristicas"]["trial"] not in participantesHomensSuperespecificadas.keys():
            participantesHomensSuperespecificadas[expressao["caracteristicas"]["trial"]] = True
            participantesHomensSubespecificadas[expressao["caracteristicas"]["trial"]] = True
            participantesMulheresSuperespecificadas[expressao["caracteristicas"]["trial"]] = True
            participantesMulheresSubespecificadas[expressao["caracteristicas"]["trial"]] = True
        
        if isUnderspecified(expressao) == True:
            expressoesSubespecificadas = expressoesSubespecificadas + 1
            
            if dadosParticipantes[expressao["caracteristicas"]["trial"]]["GENDER"] == "m":
                expressoesSubespecificadasHomens = expressoesSubespecificadasHomens + 1
                participantesHomensSuperespecificadas[expressao["caracteristicas"]["trial"]] = False
            else:
                expressoesSubespecificadasMulheres = expressoesSubespecificadasMulheres + 1
                participantesMulheresSuperespecificadas[expressao["caracteristicas"]["trial"]] = False
        
        if isOverspecified(expressao) == True:
            expressoesSuperespecificadas = expressoesSuperespecificadas + 1
            
            if dadosParticipantes[expressao["caracteristicas"]["trial"]]["GENDER"] == "m":
                expressoesSuperespecificadasHomens = expressoesSuperespecificadasHomens + 1
                participantesHomensSubespecificadas[expressao["caracteristicas"]["trial"]] = False
            else:
                expressoesSuperespecificadasMulheres = expressoesSuperespecificadasMulheres + 1
                participantesMulheresSubespecificadas[expressao["caracteristicas"]["trial"]] = False
        
        for descricao in expressao["anotacoes"].keys():
            for objeto in expressao["anotacoes"][descricao].keys():
                for atributo in expressao["anotacoes"][descricao][objeto].keys():
                    if objeto == "tg":
                        if atributo not in frequencias["tg"].keys():
                            frequencias["tg"][atributo] = 1
                        else:
                            frequencias["tg"][atributo] = frequencias["tg"][atributo] + 1
                    else:
                        if atributo not in frequencias["lm"].keys():
                            frequencias["lm"][atributo] = 1
                        else:
                            frequencias["lm"][atributo] = frequencias["lm"][atributo] + 1
        
        if expressao["caracteristicas"]["trial"] not in participantes.keys():
            participantes[expressao["caracteristicas"]["trial"]] = False
            participantesRelacionaiss[expressao["caracteristicas"]["trial"]] = True
        #print expressao["anotacoes"]
    
        if len(expressao["anotacoes"].keys()) == 2:
            expressoesConjunto = expressoesConjunto + 1
            
            if checkRelation(expressao["anotacoes"]) == True:
                expressoesRelacionaisConjunto = expressoesRelacionaisConjunto + 1  
                
                if participantes[expressao["caracteristicas"]["trial"]] == False:
                    participantes[expressao["caracteristicas"]["trial"]] = True
            else:
                if participantesRelacionaiss[expressao["caracteristicas"]["trial"]] == True:
                    participantesRelacionaiss[expressao["caracteristicas"]["trial"]] = False
        else:
            expressoesSimples = expressoesSimples + 1
            
            if checkRelation(expressao["anotacoes"]) == True:
                expressoesRelacionais = expressoesRelacionais + 1  
                
                if participantes[expressao["caracteristicas"]["trial"]] == False:
                    participantes[expressao["caracteristicas"]["trial"]] = True
            else:
                if participantesRelacionaiss[expressao["caracteristicas"]["trial"]] == True:
                    participantesRelacionaiss[expressao["caracteristicas"]["trial"]] = False
    
    for participante in participantes.keys():
        if dadosParticipantes[participante]["GENDER"] == "m":
            participantesHomens = participantesHomens + 1
            
            if participantesHomensSuperespecificadas[participante] == True:
                participantesSuperespecificadosHomens = participantesSuperespecificadosHomens + 1
            elif participantesHomensSubespecificadas[participante] == True:
                participantesSubespecificadosHomens = participantesSubespecificadosHomens + 1
        else:
            participantesMulheres = participantesMulheres + 1
            
            if participantesMulheresSuperespecificadas[participante] == True:
                participantesSuperespecificadosMulheres = participantesSuperespecificadosMulheres + 1
            elif participantesMulheresSubespecificadas[participante] == True:
                participantesSubespecificadosMulheres = participantesSubespecificadosMulheres + 1
        
        if participantes[participante] == False:        
            participantesNaoRelacionais = participantesNaoRelacionais + 1
            if dadosParticipantes[participante]["GENDER"] == "m":
                participantesHomensNaoRelacionais = participantesHomensNaoRelacionais + 1
            else:
                participantesMulheresNaoRelacionais = participantesMulheresNaoRelacionais + 1
            
        else:
            participantesMistos = participantesMistos + 1
        
        if participantesRelacionaiss[participante] == True:
            participantesRelacionais = participantesRelacionais + 1
            
            if dadosParticipantes[participante]["GENDER"] == "m":
                participantesHomensRelacionais = participantesHomensRelacionais + 1
            else:
                participantesMulheresRelacionais = participantesMulheresRelacionais + 1
                   
    
    print "Numero de Expressoes do Corpus: " +  str(len(expressoes))
    print "Expressoes Simples: " + str(expressoesSimples)
    print "Expressoes a Conjuntos: " + str(expressoesConjunto)
    print 20 * "*"
    print "Expressoes Subespecificadas: " + str(expressoesSubespecificadas)
    print "Expressoes Subespecificadas Homens: " + str(expressoesSubespecificadasHomens)
    print "Expressoes Subespecificadas Mulheres: " + str(expressoesSubespecificadasMulheres)
    print 20 * "*"
    print "Expressoes Superespecificadas: " + str(expressoesSuperespecificadas)
    print "Expressoes Superespecificadas Homens: " + str(expressoesSuperespecificadasHomens)
    print "Expressoes Superespecificadas Mulheres: " + str(expressoesSuperespecificadasMulheres)
    print 20 * "-"
    print "Numero de Expressoes Relacionais: " + str(expressoesRelacionais + expressoesRelacionaisConjunto)
    print "Expressoes Simples Relacionais: " + str(expressoesRelacionais)
    print "Expressoes a Conjuntos Relacionais: " + str(expressoesRelacionaisConjunto)
    print 20 * "-"
    print "Numero de Participantes: " + str(len(participantes))
    print 20 * "*"
    print "Numero de Participantes Homens: " + str(participantesHomens)
    print "Numero de Participantes Homens Superespecificados: " + str(participantesSuperespecificadosHomens)
    print "Numero de Participantes Homens Subespecificados: " + str(participantesSubespecificadosHomens)
    print 20 * "*"
    print "Numero de Participantes Mulheres: " + str(participantesMulheres)
    print "Numero de Participantes Mulheres Superespecificados: " + str(participantesSuperespecificadosMulheres)
    print "Numero de Participantes Mulheres Subespecificados: " + str(participantesSubespecificadosMulheres)
    print 20 * "*"
    print "Participantes Nao Relacionais: " + str(participantesNaoRelacionais)
    print "Participantes Nao Relacionais Homens: " + str(participantesHomensNaoRelacionais)
    print "Participantes Nao Relacionais Mulheres: " + str(participantesMulheresNaoRelacionais)
    print 20 * "*"
    print "Participantes Relacionais: " + str(participantesRelacionais)
    print "Participantes Relacionais Homens: " + str(participantesHomensRelacionais)
    print "Participantes Relacionais Mulheres: " + str(participantesMulheresRelacionais)
    print 20 * "-"
    print "Frequencias Target:"
    for atributo in frequencias["tg"].keys():
        print atributo, ": ", str(frequencias["tg"][atributo])
    print 20 * "-"  
    print "Frequencias Landmark:"
    for atributo in frequencias["lm"].keys():
        print atributo, ": ", str(frequencias["lm"][atributo])

def checkRelation(expressao):
    for descricao in expressao.keys():
        for objeto in expressao[descricao]:
            if objeto in ["d1", "d2", "d3", "d4"]:
                return True
    return False   


run()