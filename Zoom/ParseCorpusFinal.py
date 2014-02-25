'''
Created on 11/11/2013

@author: thiagocastroferreira
'''

# Gera Versao Final do Corpus Zoom a partir do arquivo corpus.csv (Descricao Final do Corpus.xls)
def parse():
    propriedades = []
    anotacoes = {}
    
    file = open("corpus.csv", "r")
    doc = file.readline()
    file.close()
    doc = doc.split('\r')
    
    file = open("corpus_zoom.csv", "w")
    
    elements = doc[0].split(";")
    
    for element in elements:
        propriedades.append(element)
        file.write(element.strip())
        file.write(";")
    file.write("\r")
    
    i = 1
    while i < len(doc) - 1:
        #anotacao de adriano
        anotacao1 = doc[i].split(";") 
        i = i + 1
        # anotacao de alan
        anotacao2 = doc[i].split(";") 
        # pula espaco
        i = i + 1
        i = i + 1
        
        if anotacao1[0].strip() == "c" or anotacao1[0].strip() == "*":
            parseDescricao(anotacao1, propriedades, file)
        else:
            if anotacao2[0].strip() == "c":
                parseDescricao(anotacao2, propriedades, file)
            else:
                parseDescricao(anotacao1, propriedades, file)
        print anotacao1
        print anotacao2
        print "\n"
       
    
    print propriedades

def parseDescricao(anotacao, propriedades, file):
    
    for element in anotacao:
        file.write(element.strip())
        file.write(";")
    file.write("\r")
        
 
parse()