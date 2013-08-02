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