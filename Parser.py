'''
Created on 23/07/2013

@author: thiagocastroferreira
'''

def parseDominio():
    propriedades = []
    mapa = {}
    
    file = open("Mapa.csv", "r")
    doc = file.readline()
    file.close()
    doc = doc.split('\r')
    
    linha = 0
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
            mapa[objeto_id] = objeto
#    outfile = open("mapa.json","w")
#    outfile.write(str(mapa))
#    outfile.close()
    return mapa

def test():
    propriedades = []
    descriptions = {}
    
    file = open("anotacoes.csv", "r")
    doc = file.readline()
    file.close()
    doc = doc.split('\r')
    
    newDoc = ""
    linha = 0
    for row in doc:
        linha = linha + 1
        elements = row.split(';')
        if linha == 1:
            newDoc = newDoc + row + "\n"
        else:
            for i in range(0,len(elements)):
                if elements[i].strip() == "":
                    pass
                elif i == 7 or i == 35:
                    if elements[i] != "":
                        lis = elements[i][1:len(elements[i])-1].split(",")
                        for j in range(0, len(lis)):
                            if lis[j].strip() == "d1":
                                if i <= 27:
                                    lis[j] = elements[11]
                                else:
                                    lis[j] = elements[39]
                            elif lis[j].strip() == "d2":
                                if i <= 27:
                                    lis[j] = elements[11+4]
                                else:
                                    lis[j] = elements[39+4]   
                            elif lis[j].strip() == "d3":
                                if i <= 27:
                                    lis[j] = elements[11+(2*4)]
                                else:
                                    lis[j] = elements[39+(2*4)]
                            elif lis[j].strip() == "d4":
                                if i <= 27:
                                    lis[j] = elements[11+(3*4)]
                                else:
                                    lis[j] = elements[11+(3*4)]
                            
                        newElements = "["      
                        lenLis = 0     
                        for l in lis:
                            lenLis = lenLis+1
                            if lenLis == len(lis):
                                newElements = newElements + l
                            else:
                                newElements = newElements + l + ","
                            
                        elements[i] = newElements + "]"
                else:
                    if len(elements[i].split(",")) == 1:
                        if elements[i].strip() == "d1":
                            if i <= 27:
                                elements[i] = elements[11]
                            else:
                                elements[i] = elements[39]
                        elif elements[i].strip() == "d2":
                            if i <= 27:
                                elements[i] = elements[11+4]
                            else:
                                elements[i] = elements[39+4]   
                        elif elements[i].strip() == "d3":
                            if i <= 27:
                                elements[i] = elements[11+(2*4)]
                            else:
                                elements[i] = elements[39+(2*4)]
                        elif elements[i].strip() == "d4":
                            if i <= 27:
                                elements[i] = elements[11+(3*4)]
                            else:
                                elements[i] = elements[39+(3*4)]
                    else:
                        lis = elements[i].split(",")
                        for j in range(0, len(lis)):
                            if lis[j].strip() == "d1":
                                if i <= 27:
                                    lis[j] = elements[11]
                                else:
                                    lis[j] = elements[39]
                            elif lis[j].strip() == "d2":
                                if i <= 27:
                                    lis[j] = elements[11+4]
                                else:
                                    lis[j] = elements[39+4]   
                            elif lis[j].strip() == "d3":
                                if i <= 27:
                                    lis[j] = elements[11+(2*4)]
                                else:
                                    lis[j] = elements[39+(2*4)]
                            elif lis[j].strip() == "d4":
                                if i <= 27:
                                    lis[j] = elements[11+(3*4)]
                                else:
                                    lis[j] = elements[11+(3*4)]
                        
                        newElements = ""      
                        lenLis = 0     
                        for l in lis:
                            lenLis = lenLis+1
                            if lenLis == len(lis):
                                newElements = newElements + l
                            else:
                                newElements = newElements + l + ","
                            
                        elements[i] = newElements
            
            newElements = ""
            pos = 0
            for element in elements:
                pos = pos + 1
                if pos == len(elements):
                    newElements = newElements + element + "\r"
                else:
                    newElements = newElements + element + ";"
            newDoc = newDoc + newElements
    
    file = open("anotacoes_new.csv", "w")
    doc = file.write(newDoc)
    file.close()

def parseAnnotation():
    propriedades = []
    descriptions = {}
    
    file = open("anotacoes.csv", "r")
    doc = file.readline()
    file.close()
    doc = doc.split('\r')
    
    linha = 0
    for row in doc:
        linha = linha + 1
        elements = row.split(';')
        if linha == 1:
            for element in elements:
                if element == "":
                    break
                propriedades.append(element.strip())
        else:
            description = {}
            objeto_id = str
            for i in range(0, len(elements)):
                if i == 0:
                    objeto_id = elements[i].strip()
                    description[objeto_id] = {}
                else:  
                    valor = elements[i].strip()
                    if valor != "":
                        propriedade = propriedades[i].split('.')[0]
                        if propriedade not in ['d1', 'd2', 'd3', 'd4']:
                            if propriedade not in description[objeto_id].keys():
                                description[objeto_id][propriedade] = []
                            description[objeto_id][propriedade].append(valor)
                        else:
                            token = propriedades[i].split('.')
                            target = token[0]
                            propriedade = token[1]
                            
                            if target not in description.keys():
                                description[target] = {}
                            
                            if propriedade not in description[target].keys():
                                description[target][propriedade] = []
                            
                            valor = valor.split(',')
                            
                            for value in valor:
                                description[target][propriedade].append(value)
    
            if objeto_id not in descriptions.keys():
                descriptions[objeto_id] = []
            descriptions[objeto_id].append(description) 
    return descriptions  

def parseAnnotations():
    dominio = parseDominio()
    expressoes = parseAnnotation()
    
    newExpressoes = {}  
    for key in expressoes.keys():
        if key not in newExpressoes.keys():
            newExpressoes[key] = []
        for anotacao in expressoes[key]:
            newAnotacao = {}
            for target in anotacao.keys():
                if target not in ['d1', 'd2', 'd3', 'd4']:
                    newAnotacao[target] = {}
                    for propriedade in anotacao[target].keys():
                        newAnotacao[target][propriedade] = []
                        for row in anotacao[target][propriedade]:
                            elements = row.split('with')
                            for element in elements:
                                element = element.strip()
                                if element in ['d1', 'd2', 'd3', 'd4']:
                                    properties = {}
                                    for atributo in anotacao[element].keys():
                                        for value in anotacao[element][atributo]:
                                            if atributo not in properties.keys():
                                                properties[atributo] = []
                                            properties[atributo].append(value)
                                            
                                    distractors = findDistractorsByProperties(properties, dominio)
                                    if len(distractors.keys()) == 1:
                                        newElement = distractors.keys()[0]
                                        newAnotacao[target][propriedade].append(newElement)
                                        newAnotacao[newElement] = properties
                                    else:
                                        newAnotacao[target][propriedade].append(element)
                                        newAnotacao[element] = anotacao[element]
                                    
                                else:
                                    newAnotacao[target][propriedade].append(element)
            newExpressoes[key].append(newAnotacao)
    return newExpressoes



def findDistractorsByProperties(properties = {}, distract = {}):
    distractors = {}
    dominio = distract
    for property in properties.keys():
        distractors = {}
        for element in properties[property]:
            for object in dominio.keys():
                if element in dominio[object][property]:
                    distractors[object] = dominio[object]
            dominio = distractors
            
    return distractors