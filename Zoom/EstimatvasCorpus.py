'''
Created on 24/10/2013

@author: thiagocastroferreira
'''
import Assurance as ass

# formata as expressoes no seguinte layout: ANOTADOR -> PARTICIPANTE -> MAPA -> DESCRICAO
# Neste parser, eh retornado os atributos que descrevem os objetos,
# A anotacao da expressao de referncia
# e a expressao de referencia em lingua natural
# AVISO: NAO ESQUECA DE SUBSTITUIR OS PONTOS VIRGULAS NO DOCUMENTO EXPRESSOES.CSV
def parseExpressoes():
    propriedades = []
    anotacoes = {}
    descriptions = {}
    
    file = open("expressoes1.csv", "r")
    doc = file.readline()
    file.close()
    doc = doc.split('\r')
    
    for i in range(0, len(doc)):
        elements = doc[i].split(";")
        if i == 0:
            for element in elements:
                propriedades.append(element)
        else:
            if elements[0] not in anotacoes.keys():
                anotacoes[elements[0]] = {}
            if elements[2] not in anotacoes[elements[0]].keys():
                anotacoes[elements[0]][elements[2]] = {}
                descriptions[elements[2]] = {}
            if elements[3] not in anotacoes[elements[0]][elements[2]].keys():
                anotacoes[elements[0]][elements[2]][elements[3]] = {}
                anotacoes[elements[0]][elements[2]][elements[3]]["object1"] = {}
                anotacoes[elements[0]][elements[2]][elements[3]]["object2"] = {}
                descriptions[elements[2]][elements[3]] = {}
            
            descriptions[elements[2]][elements[3]]["n"] = elements[1]
            descriptions[elements[2]][elements[3]]["description"] = elements[4]
            
            j = 0
            for j in range(5, len(elements)):
                if propriedades[j].strip() == "/":
                    break
                objetos = elements[j].split(",")
                
                if objetos[0].strip() != "":
                    anotacoes[elements[0]][elements[2]][elements[3]]["object1"][propriedades[j]] = []
                    
                    for objeto in objetos:
                        anotacoes[elements[0]][elements[2]][elements[3]]["object1"][propriedades[j]].append(objeto.strip())
            
            j = j + 1
            for j in range(j, len(elements)):
                objetos = elements[j].split(",")
                
                if objetos[0].strip() != "":
                    anotacoes[elements[0]][elements[2]][elements[3]]["object2"][propriedades[j]] = []
                    
                    for objeto in objetos:
                        anotacoes[elements[0]][elements[2]][elements[3]]["object2"][propriedades[j]].append(objeto.strip())
    
    return [propriedades, anotacoes, descriptions]
        

# Retorna um documento para fazer Juizo das expressoes que devem compor o corpus Zoom
def parseExpressoesParaCorpusFinal():
    participantes = [1,166,291,294,295,299,301,302,303,305,306,309,319,321,325,330,333,353,354,355,356,357,360,361,362,364,367,368,369,374,375,378,381,382,383,385,386,392,394,397,398,400,403,404,407,409,411,412,414,415,416,417,419,421,422,429,435,436,437,441,442,446,447,448,449,450,452,458,459,460,462,463,464,465,469,470,475,476,480,481,482,488,489,490,491,494,495,496,497,498,499,501,502,503,504,505,506,507,508]
    mapas = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
    
    resultados = parseExpressoes()
    propriedades = resultados[0]
    anotacoes = resultados[1]
    descricoes = resultados[2]
    
    file = open("expressoesOrdenado.csv", "w")
    
    file.write("concordancia")
    file.write(";")
    for propriedade in propriedades:
        file.write(propriedade)
        file.write(";")
    file.write("\r")
    
    for participante in participantes:
        participante = str(participante)
        for mapa in mapas:
            
            if mapa in anotacoes["adriano"][participante].keys() and mapa in anotacoes["alan"][participante].keys():
                if anotacoes["adriano"][participante][mapa] == anotacoes["alan"][participante][mapa]:
                    file.write("sim")
                else:
                    file.write("nao")
            else:
                file.write("nao")
            file.write(";")
            
            anotador = "adriano"
            if mapa in anotacoes["adriano"][participante].keys():
                objeto = "object1"
                for propriedade in propriedades:
                    if propriedade.strip() == "/":
                        objeto = "object2"
                    if propriedade == "anotador":
                        file.write(anotador)
                        file.write(";")
                    elif propriedade == "n":
                        file.write(descricoes[participante][mapa]["n"])
                        file.write(";")
                    elif propriedade == "sub":
                        file.write(participante)
                        file.write(";")
                    elif propriedade == "map":
                        file.write(mapa)
                        file.write(";")
                    elif propriedade == "description":
                        file.write(descricoes[participante][mapa]["description"])
                        file.write(";")
                    else:
                        if propriedade in anotacoes[anotador][participante][mapa][objeto].keys():
                            if propriedade == "between":
                                part1 = str(anotacoes[anotador][participante][mapa][objeto][propriedade][0])
                                if len(anotacoes[anotador][participante][mapa][objeto][propriedade]) > 1:
                                    file.write(part1 + "," + str(anotacoes[anotador][participante][mapa][objeto][propriedade][1]))
                                else:
                                    file.write(part1)
                            else:
                                file.write(anotacoes[anotador][participante][mapa][objeto][propriedade][0])
                        else:
                            file.write("")
                        file.write(";")
            file.write("\r")
            
            if mapa in anotacoes["adriano"][participante].keys() and mapa in anotacoes["alan"][participante].keys():
                if anotacoes["adriano"][participante][mapa] == anotacoes["alan"][participante][mapa]:
                    file.write("sim")
                else:
                    file.write("nao")
            else:
                file.write("nao")
            file.write(";")
            
            anotador = "alan"
            if mapa in anotacoes["alan"][participante].keys():
                objeto = "object1"
                for propriedade in propriedades:
                    if propriedade.strip() == "/":
                        objeto = "object2"
                    if propriedade == "anotador":
                        file.write(anotador)
                        file.write(";")
                    elif propriedade == "n":
                        file.write(descricoes[participante][mapa]["n"])
                        file.write(";")
                    elif propriedade == "sub":
                        file.write(participante)
                        file.write(";")
                    elif propriedade == "map":
                        file.write(mapa)
                        file.write(";")
                    elif propriedade == "description":
                        file.write(descricoes[participante][mapa]["description"])
                        file.write(";")
                    else:
                        if propriedade in anotacoes[anotador][participante][mapa][objeto].keys():
                            if propriedade == "between":
                                part1 = str(anotacoes[anotador][participante][mapa][objeto][propriedade][0])
                                if len(anotacoes[anotador][participante][mapa][objeto][propriedade]) > 1:
                                    file.write(part1 + "," + str(anotacoes[anotador][participante][mapa][objeto][propriedade][1]))
                                else:
                                    file.write(part1)
                            else:
                                file.write(anotacoes[anotador][participante][mapa][objeto][propriedade][0])
                        else:
                            file.write("")
                        file.write(";")
            file.write("\r")
            file.write("\r")
    
    file.close()
    
    print descricoes
    
    
def parse(A):
    result = []
    for target in A.keys():
        between = ""
        for value in A[target]:
            if target == "between" or target == "2.between":
                if between == "":
                    between = target + '.' + value
                else: 
                    between = between + '.' + value
            else:
                element = target + '.' + value
                result.append(element)
            
            element = target
            result.append(element)
        if between != "":
            result.append(between)
    return set(result)

def simpleParse(A):
    result = []
    for objeto in A.keys():
        for target in A[objeto].keys():
            result.append(target.strip())
        
    return set(result)


def getConcorcanciaCompleta():
    resultados = parseExpressoes()
    propriedades = resultados[0]
    descricoes = resultados[1]
    #anotadores
    anotadores = descricoes.keys()
    #participantes
    participantes = descricoes["adriano"].keys()
    #mapas
    mapas = descricoes["adriano"]["1"].keys()
    
    acertos = 0
    acertosParticipante = {}
    acertosMapa= {}
    
    expressoes = 0
    expressoesParticipante = {}
    expressoesMapa = {}
    
    classList = []
    classes = {}
    classes[anotadores[0]] = {}
    classes[anotadores[1]] = {}
    
    for participante in participantes:
        if participante not in acertosParticipante.keys():
            acertosParticipante[participante] = 0.
            expressoesParticipante[participante] = 0.
        
        for mapa in mapas:
            if mapa not in acertosMapa.keys():
                acertosMapa[mapa] = 0.
                expressoesMapa[mapa] = 0.
            
            if mapa in descricoes[anotadores[0]][participante].keys():
                A = simpleParse(descricoes[anotadores[0]][participante][mapa])
            if mapa in descricoes[anotadores[1]][participante].keys():
                B = simpleParse(descricoes[anotadores[1]][participante][mapa])
            
            if str(A) not in classList:
                classList.append(str(A))  
            if str(B) not in classList:
                classList.append(str(B))
            
            if str(A) not in classes[anotadores[0]].keys():
                classes[anotadores[0]][str(A)] = 1
            else:
                classes[anotadores[0]][str(A)] = classes[anotadores[0]][str(A)] + 1
                 
            if str(B) not in classes[anotadores[1]].keys():
                classes[anotadores[1]][str(B)] = 1
            else:
                classes[anotadores[1]][str(B)] = classes[anotadores[1]][str(B)] + 1
                
            dice = ass.dice(A, B)
            
            
            if dice >= 1.0:
    #             print 10 * "-"
    #             print "Participante: " + participante
    #             print "Mapa: " + mapa
    #             print "Expressao A: " + str(A)
    #             print "Expressao B: " + str(B)
    #             print 10 * "-"
                acertos = acertos + 1.
                acertosParticipante[participante] = acertosParticipante[participante] + 1.
                acertosMapa[mapa] = acertosMapa[mapa] + 1.
            
            expressoes = expressoes + 1.
            expressoesParticipante[participante] = expressoesParticipante[participante] + 1.
            expressoesMapa[mapa] = expressoesMapa[mapa] + 1.
    
    # print acertos
    # print expressoes
    
    print "Concordancia Completa: "
    concordancia = acertos / expressoes
    print "Precisao Total: " + str(concordancia)
    
    probE = 0.
    for classe in classList:
        if classe in classes[anotadores[0]].keys():
            part1 = classes[anotadores[0]][classe] / 1980. 
        else:
            part1 = 0. 
            
        if classe in classes[anotadores[1]].keys():
            part2= classes[anotadores[1]][classe] / 1980.
        else:
            part2 = 0.
    
        part3 = part1 * part2
        probE = probE + part3
            
    print "Precisao Aleatoria: " + str(probE)
    
    print "KAPPA: " + str((concordancia - probE) / (1 - probE))
    # for participante in participantes:
    #     print 10 * "-"
    #     print "Precisao participante " + participante + ": " + str(acertosParticipante[participante] / expressoesParticipante[participante])
            
    for mapa in mapas:
        print 10 * "-"
        print "Precisao mapa " + mapa + ": " + str(acertosMapa[mapa] / expressoesMapa[mapa])
    print 50 * "*"

def getConcordanciaPorAtributo():
    resultados = parseExpressoes()
    propriedades = resultados[0][5:32]
    propriedades.remove("target.id")
    propriedades.remove("d1.id")
    propriedades.remove("d2.id")
    propriedades.remove("d3.id")
    propriedades.remove("d4.id")
#     propriedades.remove("anotador")
#     propriedades.remove("n")
#     propriedades.remove("sub")
#     propriedades.remove("map")
#     propriedades.remove("description")
    
    descricoes = resultados[1]
    #anotadores
    anotadores = descricoes.keys()
    #participantes
    participantes = descricoes["adriano"].keys()
    #mapas
    mapas = descricoes["adriano"]["1"].keys()
    
    classes = {}
    classes["ss"] = 0
    classes["sn"] = 0
    classes["ns"] = 0
    classes["nn"] = 0
    
        
    count = 0
    countPropriedade = {}
    countMapa = {}
    classesPropriedade = {}
        
    for propriedade in propriedades: 
        countPropriedade[propriedade] = 0
        classesPropriedade[propriedade] = {}
        classesPropriedade[propriedade]["ss"] = 0
        classesPropriedade[propriedade]["sn"] = 0
        classesPropriedade[propriedade]["ns"] = 0
        classesPropriedade[propriedade]["nn"] = 0
        
    classesMapa = {}
        
    for mapa in mapas: 
        countMapa[mapa] = 0
        classesMapa[mapa] = {}
        classesMapa[mapa]["ss"] = 0
        classesMapa[mapa]["sn"] = 0
        classesMapa[mapa]["ns"] = 0
        classesMapa[mapa]["nn"] = 0
    
    for participante in participantes:
        
        for mapa in mapas:
            if mapa in descricoes[anotadores[0]][participante].keys():
                A = simpleParse(descricoes[anotadores[0]][participante][mapa])
            if mapa in descricoes[anotadores[1]][participante].keys():
                B = simpleParse(descricoes[anotadores[1]][participante][mapa])
            
            for propriedade in propriedades:
                count = count + 1.
                countPropriedade[propriedade] = countPropriedade[propriedade] + 1.
                countMapa[mapa] = countMapa[mapa] + 1.
                
                if propriedade in A:
                    
                    if propriedade in B:
                        classes["ss"] = classes["ss"] + 1
                        classesPropriedade[propriedade]["ss"] = classesPropriedade[propriedade]["ss"] + 1
                        classesMapa[mapa]["ss"] = classesMapa[mapa]["ss"] + 1
                    else:
                        classes["sn"] = classes["sn"] + 1
                        classesPropriedade[propriedade]["sn"] = classesPropriedade[propriedade]["sn"] + 1
                        classesMapa[mapa]["sn"] = classesMapa[mapa]["sn"] + 1
#                 else:
#                     classes[anotadores[0]]["no"] = classes[anotadores[0]]["no"] + 1
#                     classesPropriedade[anotadores[0]][propriedade]["no"] = classesPropriedade[anotadores[0]][propriedade]["no"] + 1
#                     classesMapa[anotadores[0]][mapa]["no"] = classesMapa[anotadores[0]][mapa]["no"] + 1
                else:
                    if propriedade in B:
                        classes["ns"] = classes["ns"] + 1
                        classesPropriedade[propriedade]["ns"] = classesPropriedade[propriedade]["ns"] + 1
                        classesMapa[mapa]["ns"] = classesMapa[mapa]["ns"] + 1
                        
                    else:
                        classes["nn"] = classes["nn"] + 1
                        classesPropriedade[propriedade]["nn"] = classesPropriedade[propriedade]["nn"] + 1
                        classesMapa[mapa]["nn"] = classesMapa[mapa]["nn"] + 1
                    
    print 50 * "*"
    print "Concordancia Completa: "
    print "SS: " + str(classes["ss"])
    print "SN: " + str(classes["sn"])
    print "NS: " + str(classes["ns"])
    print "NN: " + str(classes["nn"])
    print 50 * "*"
    
    part1 = (classes["nn"] + classes["ns"]) / count
    part2 = (classes["nn"] + classes["sn"]) / count
    probE = part1 * part2
    
    concordancia = (classes["ss"] + classes["nn"]) / count
    print "Count: " + str(count)
    print "Concordancia Total: " + str(concordancia)   
    print "Concordancia por Chance: " + str(probE)
    print "KAPPA: " + str((concordancia - probE) / (1 - probE))
    
#     print 50 * "*"
#     print "\n\n"
#     print "Concordancia por Atributo: "
#     print 50 * "-"
#     for propriedade in propriedades:
#         print "Atributo:" + propriedade
#         print "Classe: yes" + "\t" + anotadores[0] + ": " + str(classesPropriedade[anotadores[0]][propriedade]["yes"]) + "\t - \t" + anotadores[1] + ": " + str(classesPropriedade[anotadores[1]][propriedade]["yes"])
#         
#         print "Classe: no " + "\t" + anotadores[0] + ": " + str(classesPropriedade[anotadores[0]][propriedade]["no"]) + "\t - \t" + anotadores[1] + ": " + str(classesPropriedade[anotadores[1]][propriedade]["no"])
#         print 10 * "-"
#         
#         probE = 0.
#         for classe in ["yes", "no"]:
#             if classesPropriedade[anotadores[0]][propriedade][classe] > 0:
#                 part1 = classesPropriedade[anotadores[0]][propriedade][classe] / countPropriedade[propriedade]
#             else:
#                 part1 = 0. 
#                 
#             if classesPropriedade[anotadores[1]][propriedade][classe] > 0:
#                 part2= classesPropriedade[anotadores[1]][propriedade][classe] / countPropriedade[propriedade]
#             else:
#                 part2 = 0.
#         
#             part3 = part1 * part2
#             probE = probE + part3
#         
#         concordancia = ((max(classesPropriedade[anotadores[0]][propriedade]["yes"], classesPropriedade[anotadores[1]][propriedade]["yes"]) - abs(classesPropriedade[anotadores[0]][propriedade]["yes"] - classesPropriedade[anotadores[1]][propriedade]["yes"])) + (max(classesPropriedade[anotadores[0]][propriedade]["no"], classesPropriedade[anotadores[1]][propriedade]["no"]) - abs(classesPropriedade[anotadores[0]][propriedade]["no"] - classesPropriedade[anotadores[1]][propriedade]["no"]))) /countPropriedade[propriedade]
#         print "Concordancia: " + str(concordancia)   
#         print "Concordancia por Chance: " + str(probE)
#         if probE != 1 and concordancia != 1:
#             print "KAPPA: " + str((concordancia - probE) / (1 - probE))
#         print 50 * "*"
#         
#         
#     print 50 * "*"
#     print "\n\n"
#     print "Concordancia por Mapa: "
#     print 50 * "-"
#     
#     mapas.sort()
#     
#     for mapa in mapas:
#         print "Mapa:" + mapa
#         print "Classe: yes" + "\t" + anotadores[0] + ": " + str(classesMapa[anotadores[0]][mapa]["yes"]) + "\t - \t" + anotadores[1] + ": " + str(classesMapa[anotadores[1]][mapa]["yes"])
#         
#         print "Classe: no " + "\t" + anotadores[0] + ": " + str(classesMapa[anotadores[0]][mapa]["no"]) + "\t - \t" + anotadores[1] + ": " + str(classesMapa[anotadores[1]][mapa]["no"])
#         print 10 * "-"
#         
#         probE = 0.
#         for classe in ["yes", "no"]:
#             if classesMapa[anotadores[0]][mapa][classe] > 0:
#                 part1 = classesMapa[anotadores[0]][mapa][classe] / countMapa[mapa]
#             else:
#                 part1 = 0. 
#                 
#             if classesMapa[anotadores[1]][mapa][classe] > 0:
#                 part2= classesMapa[anotadores[1]][mapa][classe] / countMapa[mapa]
#             else:
#                 part2 = 0.
#         
#             part3 = part1 * part2
#             probE = probE + part3
#         
#         concordancia = ((max(classesMapa[anotadores[0]][mapa]["yes"], classesMapa[anotadores[1]][mapa]["yes"]) - abs(classesMapa[anotadores[0]][mapa]["yes"] - classesMapa[anotadores[1]][mapa]["yes"])) + (max(classesMapa[anotadores[0]][mapa]["no"], classesMapa[anotadores[1]][mapa]["no"]) - abs(classesMapa[anotadores[0]][mapa]["no"] - classesMapa[anotadores[1]][mapa]["no"]))) /countMapa[mapa]
#         print "Concordancia: " + str(concordancia)   
#         print "Concordancia por Chance: " + str(probE)
#         print "KAPPA: " + str((concordancia - probE) / (1 - probE))
#         print 50 * "*"
    
getConcordanciaPorAtributo()

# parseExpressoesParaCorpusFinal()

# descriptions = parseExpressoes()[1]
# 
# for anotador in descriptions.keys():
#     for participante in descriptions[anotador].keys():
#         for mapa in descriptions[anotador][participante].keys():
#             print descriptions[anotador][participante][mapa]
        
