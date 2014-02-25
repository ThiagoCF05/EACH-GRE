'''
Created on 13/09/2013

@author: thiagocastroferreira
'''

class IncrementalAlgorithmRelational5(object):
    def __init__(self, dominio = {}, target = str, preferred_attributes = [], frequencia = {}, probabilidade = float, tamanho = int, restricaoContexto = False):
        self.dominio = dominio
        self.target = target
        self.preferred_attributes = preferred_attributes
        self.distractors = {}
        self.restricaoContexto = restricaoContexto
        self.frequencia = frequencia
        self.probabilidade = probabilidade
        
        if tamanho == 0: self.tamanho = 16.
        else: self.tamanho = float(tamanho)
        
        # restricao de contexto
        self.distractors[target] = self.initializeDistractors(target, restricaoContexto, self.dominio)
        
        self.atributos = {}
        self.atributos[target] = self.listaAtributos(target, True)
        
        self.description = {}
        self.description[self.target] = {}

    def run(self):
        return self.searchDescription(self.target)

    def searchDescription(self, target):
        for atributo in self.atributos[target]:
            for element in self.dominio[target][atributo]:
                
                properties = {}
                for key in self.description[target].keys():
                    properties[key] = self.description[target][key]
                if atributo in properties.keys():
                    aux = []
                    for row in properties[atributo]:
                        aux.append(row)
                    aux.append(element)
                    properties[atributo] = aux
                else:
                    properties[atributo] = [element]  
                
                previousDistractor = {}
                for distractor in self.distractors[target].keys():
                    previousDistractor[distractor] = self.distractors[target][distractor]
                
                self.distractors[target] = self.findDistractorsByProperties(properties, target, self.distractors)
                
                if len(self.distractors[target]) < len(previousDistractor):
                    if self.relationalAttribute(atributo):
                        if element not in self.description.keys():
                            if atributo in self.description[target].keys():
                                self.description[target][atributo].append(element)
                            else:
                                self.description[target][atributo] = [element]
                            self.atributos[element] = self.listaAtributos(element, False)
                            self.distractors[element] = self.initializeDistractors(element, self.restricaoContexto, self.dominio)
                            self.description[element] = {}
                            self.description = self.searchDescription(element)
                        else:
                            self.distractors[target] = previousDistractor
                    else:
                        self.description[target][atributo] = [element]
                # Se a probabilidade de aparicao do atributo for alta, este eh inserido na descricao      
#                 elif self.checaProbabilidade(atributo, target):
#                     if self.relationalAttribute(atributo):
#                         #if self.relationalDescription(target) == False:
#                             if element not in self.description.keys():
#                                 if atributo in self.description[target].keys():
#                                     self.description[target][atributo].append(element)
#                                 else:
#                                     self.description[target][atributo] = [element]
#                                 self.atributos[element] = self.listaAtributos(element, False)
#                                 self.distractors[element] = self.initializeDistractors(element, self.restricaoContexto, self.dominio)
#                                 self.description[element] = {}
#                                 self.description = self.searchDescription(element)
#                     else:
#                         self.description[target][atributo] = [element]
                if len(self.distractors[target]) == 1:
                    return self.description
        return self.description
    
    def listaAtributos(self, target, ehAlvo):
        atributos = []
        
        if ehAlvo:
            if len(self.preferred_attributes["target"]) == 0:
                atributos = self.dominio[target].keys()
            else:
                atributos = self.preferred_attributes["target"]
        else:
            if len(self.preferred_attributes["landmark"]) == 0:
                atributos = self.dominio[target].keys()
            else:
                atributos = self.preferred_attributes["landmark"]
        
        return atributos
    
    def relationalAttribute(self, atributo = str):
        lista = atributo.split("_")
        
        if lista[0] != "colour" and lista[0] != "type" and lista[0] != "hpos" and lista[0] != "vpos" and lista[0] != "size":
            return True
        else:
            return False
    
    def initializeDistractors(self, target, contextRestriction, dominio = {}):
        distractors = {}
        if contextRestriction:
            for element in dominio[target]['near-to']:
                distractors[element] = dominio[element]
            distractors[target] = dominio[target]
        else:
            distractors = dominio
        
        return distractors
            
    def findDistractorsByProperties(self, properties = {}, target = str, distract = {}):
        distractors = {}
        dominio = distract[target]
        for property in properties.keys():
            distractors = {}
            for element in properties[property]:
                for object in dominio.keys():
                    if element in dominio[object][property]:
                        distractors[object] = dominio[object]
                dominio = distractors
                
        return distractors
    
    def getFrequenciaRelacional(self):
        frequenciaRelacional = 0
        
        for atributo in self.frequencia["target"].keys():
            if self.relationalAttribute(atributo):
                frequenciaRelacional = frequenciaRelacional + self.frequencia["target"][atributo]
        return frequenciaRelacional
    
    def relationalDescription(self, objeto):
        for atributo in self.description[objeto]:
            if self.relationalAttribute(atributo):
                return True
        return False
    
    def checaProbabilidade(self, atributo, objeto):
        if self.target == objeto:
            if self.relationalAttribute(atributo):
                if (self.getFrequenciaRelacional()/self.tamanho) >= self.probabilidade:
                    return True
                else:
                    return False
            else:
                if (self.frequencia["target"][atributo]/ self.tamanho) >= self.probabilidade:
                    return True
                else:
                    return False
        else:
            if (self.frequencia["landmark"][atributo] / self.tamanho) >= self.probabilidade:
                return True
            else:
                return False