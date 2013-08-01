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
                            
                            description[target][propriedade].append(valor)
    
            if objeto_id not in descriptions.keys():
                descriptions[objeto_id] = []
            descriptions[objeto_id].append(description) 
    return descriptions            
#parse()