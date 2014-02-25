'''
Created on 06/01/2014

@author: thiagocastroferreira
'''

import ParserGRE3D as parser
import itertools as iter

targets = {"1":"b1","2":"b1","3":"b1","4":"c2","5":"c1","6":"b1","7":"b1","8":"b1","9":"c1","10":"c2","11":"b1","12":"b1","13":"b1","14":"c2","15":"c1","16":"b1","17":"b1","18":"b1","19":"c1","20":"c1"}
dominios = parser.parseDominio()

def isUnderspecified(expressao):
    for target in expressao["descricao"].keys():
        if target == "tg":
            properties = expressao["descricao"][target]
            dominio = dominios[expressao["caracteristicas"]["context"]]
            distractors = {}
            for property in properties.keys():
                distractors = {}
                for element in properties[property]:
                    for object in dominio.keys():
                        if property in dominio[object].keys():
                            if element in dominio[object][property]:
                                distractors[object] = dominio[object]
                    dominio = distractors
            
            if len(distractors.keys()) > 1:
                return True
    return False
    
def isOverspecified(expressao):
    for target in expressao["descricao"].keys():
        if target == "tg":
            properties = expressao["descricao"][target]
            
            permutations = iter.permutations(properties.keys())
            
            for permutation in permutations:
                i = 0
                dominio = dominios[expressao["caracteristicas"]["context"]]
                for property in permutation:
                    i = i + 1
                    distractors = {}
                    for element in properties[property]:
                        for object in dominio.keys():
                            if property in dominio[object].keys():
                                if element in dominio[object][property]:
                                    distractors[object] = dominio[object]
                        dominio = distractors
                
                    if len(distractors.keys()) == 1 and i < len(properties.keys()):
                        return True
    return False

def run():
    expressoes = parser.parseAnnotation()
    dadosParticipantes = parser.parseParticipantes()
    
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
    
    participantesRelacionaisEtaria = {}
    participantesRelacionaisEtaria["<=20"] = 0
    participantesRelacionaisEtaria["20-25"] = 0
    participantesRelacionaisEtaria["26-30"] = 0
    participantesRelacionaisEtaria["30-40"] = 0
    participantesRelacionaisEtaria["40-50"] = 0
    participantesRelacionaisEtaria["50-60"] = 0
    participantesRelacionaisEtaria[">60"] = 0
    
    participantesNaoRelacionaisEtaria = {}
    participantesNaoRelacionaisEtaria["<=20"] = 0
    participantesNaoRelacionaisEtaria["20-25"] = 0
    participantesNaoRelacionaisEtaria["26-30"] = 0
    participantesNaoRelacionaisEtaria["30-40"] = 0
    participantesNaoRelacionaisEtaria["40-50"] = 0
    participantesNaoRelacionaisEtaria["50-60"] = 0
    participantesNaoRelacionaisEtaria[">60"] = 0
    
    participantesSuperespecificadosHomens = 0
    participantesSuperespecificadosMulheres = 0
    participantesSubespecificadosHomens = 0
    participantesSubespecificadosMulheres = 0
    
    participantesSuperespecificadosEtaria = {}
    participantesSuperespecificadosEtaria["<=20"] = 0
    participantesSuperespecificadosEtaria["20-25"] = 0
    participantesSuperespecificadosEtaria["26-30"] = 0
    participantesSuperespecificadosEtaria["30-40"] = 0
    participantesSuperespecificadosEtaria["40-50"] = 0
    participantesSuperespecificadosEtaria["50-60"] = 0
    participantesSuperespecificadosEtaria[">60"] = 0
    
    participantesSubespecificadosEtaria = {}
    participantesSubespecificadosEtaria["<=20"] = 0
    participantesSubespecificadosEtaria["20-25"] = 0
    participantesSubespecificadosEtaria["26-30"] = 0
    participantesSubespecificadosEtaria["30-40"] = 0
    participantesSubespecificadosEtaria["40-50"] = 0
    participantesSubespecificadosEtaria["50-60"] = 0
    participantesSubespecificadosEtaria[">60"] = 0
    
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
            
            if dadosParticipantes[expressao["caracteristicas"]["trial"]][0] == 0:
                expressoesSubespecificadasHomens = expressoesSubespecificadasHomens + 1
                participantesHomensSuperespecificadas[expressao["caracteristicas"]["trial"]] = False
            else:
                expressoesSubespecificadasMulheres = expressoesSubespecificadasMulheres + 1
                participantesMulheresSuperespecificadas[expressao["caracteristicas"]["trial"]] = False
        
        if isOverspecified(expressao) == True:
            expressoesSuperespecificadas = expressoesSuperespecificadas + 1
            
            if dadosParticipantes[expressao["caracteristicas"]["trial"]][0] == 0:
                expressoesSuperespecificadasHomens = expressoesSuperespecificadasHomens + 1
                participantesHomensSubespecificadas[expressao["caracteristicas"]["trial"]] = False
            else:
                expressoesSuperespecificadasMulheres = expressoesSuperespecificadasMulheres + 1
                participantesMulheresSubespecificadas[expressao["caracteristicas"]["trial"]] = False
        
        for objeto in expressao["descricao"].keys():
            for atributo in expressao["descricao"][objeto].keys():
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
    
        if checkRelation(expressao["descricao"]) == True:
            expressoesRelacionais = expressoesRelacionais + 1  
            
            if participantes[expressao["caracteristicas"]["trial"]] == False:
                participantes[expressao["caracteristicas"]["trial"]] = True
        else:
            if participantesRelacionaiss[expressao["caracteristicas"]["trial"]] == True:
                participantesRelacionaiss[expressao["caracteristicas"]["trial"]] = False
    
    for participante in participantes.keys():
        if dadosParticipantes[participante][0] == 0:
            participantesHomens = participantesHomens + 1
            
            if participantesHomensSuperespecificadas[participante] == True:
                participantesSuperespecificadosHomens = participantesSuperespecificadosHomens + 1
                
                if dadosParticipantes[participante][1] == 0:
                    participantesSuperespecificadosEtaria["<=20"] = participantesSuperespecificadosEtaria["<=20"] + 1
                elif dadosParticipantes[participante][1] == 1:
                    participantesSuperespecificadosEtaria["20-25"] = participantesSuperespecificadosEtaria["20-25"] + 1
                elif dadosParticipantes[participante][1] == 2:
                    participantesSuperespecificadosEtaria["26-30"] = participantesSuperespecificadosEtaria["26-30"] + 1
                elif dadosParticipantes[participante][1] == 3:
                    participantesSuperespecificadosEtaria["30-40"] = participantesSuperespecificadosEtaria["30-40"] + 1
                elif dadosParticipantes[participante][1] == 4:
                    participantesSuperespecificadosEtaria["40-50"] = participantesSuperespecificadosEtaria["40-50"] + 1
                elif dadosParticipantes[participante][1] == 5:
                    participantesSuperespecificadosEtaria["50-60"] = participantesSuperespecificadosEtaria["50-60"] + 1
                else:
                    participantesSuperespecificadosEtaria[">60"] = participantesSuperespecificadosEtaria[">60"] + 1
                    
            elif participantesHomensSubespecificadas[participante] == True:
                participantesSubespecificadosHomens = participantesSubespecificadosHomens + 1
                
                if dadosParticipantes[participante][1] == 0:
                    participantesSubespecificadosEtaria["<=20"] = participantesSubespecificadosEtaria["<=20"] + 1
                elif dadosParticipantes[participante][1] == 1:
                    participantesSubespecificadosEtaria["20-25"] = participantesSubespecificadosEtaria["20-25"] + 1
                elif dadosParticipantes[participante][1] == 2:
                    participantesSubespecificadosEtaria["26-30"] = participantesSubespecificadosEtaria["26-30"] + 1
                elif dadosParticipantes[participante][1] == 3:
                    participantesSubespecificadosEtaria["30-40"] = participantesSubespecificadosEtaria["30-40"] + 1
                elif dadosParticipantes[participante][1] == 4:
                    participantesSubespecificadosEtaria["40-50"] = participantesSubespecificadosEtaria["40-50"] + 1
                elif dadosParticipantes[participante][1] == 5:
                    participantesSubespecificadosEtaria["50-60"] = participantesSubespecificadosEtaria["50-60"] + 1
                else:
                    participantesSubespecificadosEtaria[">60"] = participantesSubespecificadosEtaria[">60"] + 1
                
        else:
            participantesMulheres = participantesMulheres + 1
            
            if participantesMulheresSuperespecificadas[participante] == True:
                participantesSuperespecificadosMulheres = participantesSuperespecificadosMulheres + 1
                
                if dadosParticipantes[participante][1] == 0:
                    participantesSuperespecificadosEtaria["<=20"] = participantesSuperespecificadosEtaria["<=20"] + 1
                elif dadosParticipantes[participante][1] == 1:
                    participantesSuperespecificadosEtaria["20-25"] = participantesSuperespecificadosEtaria["20-25"] + 1
                elif dadosParticipantes[participante][1] == 2:
                    participantesSuperespecificadosEtaria["26-30"] = participantesSuperespecificadosEtaria["26-30"] + 1
                elif dadosParticipantes[participante][1] == 3:
                    participantesSuperespecificadosEtaria["30-40"] = participantesSuperespecificadosEtaria["30-40"] + 1
                elif dadosParticipantes[participante][1] == 4:
                    participantesSuperespecificadosEtaria["40-50"] = participantesSuperespecificadosEtaria["40-50"] + 1
                elif dadosParticipantes[participante][1] == 5:
                    participantesSuperespecificadosEtaria["50-60"] = participantesSuperespecificadosEtaria["50-60"] + 1
                else:
                    participantesSuperespecificadosEtaria[">60"] = participantesSuperespecificadosEtaria[">60"] + 1
            elif participantesMulheresSubespecificadas[participante] == True:
                participantesSubespecificadosMulheres = participantesSubespecificadosMulheres + 1
                
                if dadosParticipantes[participante][1] == 0:
                    participantesSubespecificadosEtaria["<=20"] = participantesSubespecificadosEtaria["<=20"] + 1
                elif dadosParticipantes[participante][1] == 1:
                    participantesSubespecificadosEtaria["20-25"] = participantesSubespecificadosEtaria["20-25"] + 1
                elif dadosParticipantes[participante][1] == 2:
                    participantesSubespecificadosEtaria["26-30"] = participantesSubespecificadosEtaria["26-30"] + 1
                elif dadosParticipantes[participante][1] == 3:
                    participantesSubespecificadosEtaria["30-40"] = participantesSubespecificadosEtaria["30-40"] + 1
                elif dadosParticipantes[participante][1] == 4:
                    participantesSubespecificadosEtaria["40-50"] = participantesSubespecificadosEtaria["40-50"] + 1
                elif dadosParticipantes[participante][1] == 5:
                    participantesSubespecificadosEtaria["50-60"] = participantesSubespecificadosEtaria["50-60"] + 1
                else:
                    participantesSubespecificadosEtaria[">60"] = participantesSubespecificadosEtaria[">60"] + 1
        
        if participantes[participante] == False:        
            participantesNaoRelacionais = participantesNaoRelacionais + 1
            
            if dadosParticipantes[participante][1] == 0:
                participantesNaoRelacionaisEtaria["<=20"] = participantesNaoRelacionaisEtaria["<=20"] + 1
            elif dadosParticipantes[participante][1] == 1:
                participantesNaoRelacionaisEtaria["20-25"] = participantesNaoRelacionaisEtaria["20-25"] + 1
            elif dadosParticipantes[participante][1] == 2:
                participantesNaoRelacionaisEtaria["26-30"] = participantesNaoRelacionaisEtaria["26-30"] + 1
            elif dadosParticipantes[participante][1] == 3:
                participantesNaoRelacionaisEtaria["30-40"] = participantesNaoRelacionaisEtaria["30-40"] + 1
            elif dadosParticipantes[participante][1] == 4:
                participantesNaoRelacionaisEtaria["40-50"] = participantesNaoRelacionaisEtaria["40-50"] + 1
            elif dadosParticipantes[participante][1] == 5:
                participantesNaoRelacionaisEtaria["50-60"] = participantesNaoRelacionaisEtaria["50-60"] + 1
            else:
                participantesNaoRelacionaisEtaria[">60"] = participantesNaoRelacionaisEtaria[">60"] + 1
            
            if dadosParticipantes[participante][0] == 0:
                participantesHomensNaoRelacionais = participantesHomensNaoRelacionais + 1
            else:
                participantesMulheresNaoRelacionais = participantesMulheresNaoRelacionais + 1
            
        else:
            participantesMistos = participantesMistos + 1
            
            if dadosParticipantes[participante][1] == 0:
                participantesRelacionaisEtaria["<=20"] = participantesRelacionaisEtaria["<=20"] + 1
            elif dadosParticipantes[participante][1] == 1:
                participantesRelacionaisEtaria["20-25"] = participantesRelacionaisEtaria["20-25"] + 1
            elif dadosParticipantes[participante][1] == 2:
                participantesRelacionaisEtaria["26-30"] = participantesRelacionaisEtaria["26-30"] + 1
            elif dadosParticipantes[participante][1] == 3:
                participantesRelacionaisEtaria["30-40"] = participantesRelacionaisEtaria["30-40"] + 1
            elif dadosParticipantes[participante][1] == 4:
                participantesRelacionaisEtaria["40-50"] = participantesRelacionaisEtaria["40-50"] + 1
            elif dadosParticipantes[participante][1] == 5:
                participantesRelacionaisEtaria["50-60"] = participantesRelacionaisEtaria["50-60"] + 1
            else:
                participantesRelacionaisEtaria[">60"] = participantesRelacionaisEtaria[">60"] + 1
        
        if participantesRelacionaiss[participante] == True:
            participantesRelacionais = participantesRelacionais + 1
            
            if dadosParticipantes[participante][0] == 0:
                participantesHomensRelacionais = participantesHomensRelacionais + 1
            else:
                participantesMulheresRelacionais = participantesMulheresRelacionais + 1
                   
    
    print "Numero de Expressoes do Corpus: " +  str(len(expressoes))
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
    for etaria in participantesNaoRelacionaisEtaria.keys():
        print "Participantes Nao Relacionais " + etaria + ": " + str(participantesNaoRelacionaisEtaria[etaria])
    print 20 * "*"
    print "Participantes Relacionais: " + str(participantesRelacionais)
    print "Participantes Relacionais Homens: " + str(participantesHomensRelacionais)
    print "Participantes Relacionais Mulheres: " + str(participantesMulheresRelacionais)
    print 20 * "*"
    for etaria in participantesRelacionaisEtaria.keys():
        print "Participantes Relacionais " + etaria + ": " + str(participantesRelacionaisEtaria[etaria])
    print 20 * "-"
    print "Frequencias Target:"
    for atributo in frequencias["tg"].keys():
        print atributo, ": ", str(frequencias["tg"][atributo])
    print 20 * "-"  
    print "Frequencias Landmark:"
    for atributo in frequencias["lm"].keys():
        print atributo, ": ", str(frequencias["lm"][atributo])

def checkRelation(expressao):
    for atributo in expressao["tg"].keys():
        if atributo in ["left-of", "right-of", "next-to", "on-top-of", "in-front-of"]:
            return True
    return False   


run()