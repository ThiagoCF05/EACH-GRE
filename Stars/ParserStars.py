'''
Created on 22/08/2013

@author: thiagocastroferreira
'''

import xml.etree.ElementTree as ET
# Formata as expressoes geradas pelos participantes do experimento Stars
def parseAnnotation():
    file = open("stars.csv", "r")
    doc = file.readline()
    file.close()
    doc = doc.split('\r')
    
    propriedades = []
    anotacoes = []
    
    
    for i in range(0, len(doc)):
        row = doc[i].split(";")
        if i == 0:
            for element in row:
                propriedades.append(element.strip())
        else:
            descricao = {}
            descricao["caracteristicas"] = {}
            descricao["descricao"] = {}
            nroLandmarks = 0
            target = ""
            for j in range(0, len(row)):
                if j < 5:
                    descricao["caracteristicas"][propriedades[j]] = row[j]
                elif j == 5:
                    descricao["caracteristicas"][propriedades[j]] = row[j]
                    descricao["descricao"][row[j]] = {}
                    target = row[j]
                elif j >=6 and j<10:
                    anotacao = []
                    
                    element = row[j]
                    if element != [""]:
                        element = element.split(",")
                        for value in element:
                            anotacao.append(value)
                        
                        if anotacao != [''] and anotacao != []:
                            descricao["descricao"][target][propriedades[j]] = []
                            descricao["descricao"][target][propriedades[j]] = anotacao
                elif j>=10 and j<=12:
                    element = row[j]
                    element = element.split("-")
                    for value in element:
                        if value != "":
                            descricao["descricao"][target][propriedades[j]] = []
                            descricao["descricao"][target][propriedades[j]].append(value)
                            nroLandmarks = nroLandmarks + 1
                            type = []
                            others = []
                            if nroLandmarks == 1:
                                if row[13] != "":
                                    type.append(row[13])
                                if row[14] != "":
                                    elements = row[14].split(",")
                                    for valor in elements:
                                        others.append(valor)
                            else:
                                if row[15] != "":
                                    type.append(row[15])
                                if row[16] != "":
                                    elements = row[16].split(",")
                                    for valor in elements:
                                        others.append(valor)
                            
                            descricao["descricao"][value] = {}
                            if type != [] and type != ['']:
                                descricao["descricao"][value]["type"] = type
                            if others != [] and others != ['']:
                                descricao["descricao"][value]["others"] = others
                    
            anotacoes.append(descricao)
    return anotacoes


# Formata o dominio do experimento Stars em xml
def parseDominio():
    tree = ET.parse('dominio_stars.xml') 
    root = tree.getroot()
    dominios = {}
    for context in root:
        if context.attrib["ID"][0:4] != "fill":
            context_id = context.attrib["ID"]
            dominios[context_id] = {}
            for entity in context:
                entity_id = entity.attrib["ID"]
                dominios[context_id][entity_id] = {}
                dominios[context_id][entity_id]["function"] = entity.attrib["FUNCTION"]
                for attribute in entity:
                    dominios[context_id][entity_id][attribute.attrib["NAME"]] = attribute.attrib["VALUE"]
    return dominios