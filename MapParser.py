'''
Created on 23/07/2013

@author: thiagocastroferreira
'''

def parse():
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

#parse()