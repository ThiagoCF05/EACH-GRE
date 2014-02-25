'''
Created on 03/01/2014

@author: thiagocastroferreira
'''

import os
import xml.etree.ElementTree as ET

def parseMapas():
    maps = {}
    
    files = os.listdir("Mapas/")

    for f in files:
        if f != ".DS_Store":
            map = f.split()[1].split(".")[0]
            file = open("Mapas/" + f, "r")
            doc = file.readline()
            file.close()
            doc = doc.split('\r')
            maps[map] = doc
    
    for map in ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]:
        linha = 0
        propriedades = []
        
        doc = maps[map]
        maps[map] = {}
        
        for row in doc:
            linha = linha + 1
            elements = row.split(';')
            if linha == 1:
                for element in elements:
                    propriedades.append(element.strip())
            else:
                objeto = {}
                objeto_id = str
                
                for i in range(0, len(elements)):
                    if i == 0:
                        objeto_id = elements[i].strip()
                    
                    elif propriedades[i] == "between":
                        elementos = elements[i].split("-")
                        
                        valores = []
                        for elemento in elementos:
                            valores.append(elemento.strip("[]").split(","))
                        
                        if [''] in valores:
                            valores.remove([''])
                        objeto[propriedades[i]] = valores
                    else:
                        valores = elements[i].split(',')
                        for j in range(0, len(valores)):
                            valores[j] = valores[j].strip()
                        
                        if valores[0] == '':
                            objeto[propriedades[i]] = []
                        else:
                            if '' in valores:
                                valores.remove('')
                            objeto[propriedades[i]] = valores
                maps[map][objeto_id] = objeto
    
    return maps
    
def parseAnnotation():
    expressoes = []
    
    participantes = {}
    files = os.listdir("Expressoes/")
    for f in files:
        if f != ".DS_Store":
            tree = ET.parse("Expressoes/" + f)
            root = tree.getroot()
            
            participantes[root.attrib["ID"]] = root.attrib
            
            participante_id = root.attrib["ID"]
            
            del participantes[root.attrib["ID"]]["ID"]
            
            for contexto in root.findall("CONTEXT"):
                expressao = {}
                expressao["caracteristicas"] = {}
                expressao["caracteristicas"]["context"] = contexto.attrib["ID"]
                expressao["caracteristicas"]["trial"] = participante_id
                expressao["caracteristicas"]["string"] = contexto.attrib["WORD-STRING"]
                
                expressao["anotacoes"] = {}
                
                for child in contexto:
                    target = child.attrib["TARGET.ID"]
                    
                    expressao["anotacoes"][target] = {}
                    expressao["anotacoes"][target]["tg"] = {}
                    
                    for atributo in child:
                        aux = atributo.attrib["NAME"].split(".")
                        
                        if aux[0] in ["d1", "d2", "d3", "d4"]:
                            if aux[0] not in expressao["anotacoes"][target].keys():
                                expressao["anotacoes"][target][aux[0]] = {}
                                
                            expressao["anotacoes"][target][aux[0]][aux[1]] = [atributo.attrib["VALUE"]]
                        else:
                            expressao["anotacoes"][target]["tg"][atributo.attrib["NAME"]] = atributo.attrib["VALUE"].strip("[]").split(",")
                expressoes.append(expressao)
    
    return [expressoes, participantes]