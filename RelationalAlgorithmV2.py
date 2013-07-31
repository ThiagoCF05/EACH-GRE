'''
Created on 24/07/2013

@author: thiagocastroferreira
'''

# Greedy Heuristic
class RelationalAlgorithmV2(object):


    def __init__(self, dominio = {}, target = str, preferred_attributes = []):
        self.dominio = dominio
        
        ##########################
        for key in self.dominio.keys():
            self.dominio[key]['between'] = []
        ##########################
        
        self.stack = []
        self.stack.append(target)
        self.preferred_attributes = preferred_attributes
        self.atributos = {}
        self.atributos = self.listaAtributos(target)
        # Constraint Network
        self.description = {}
        self.description[target] = {}
        self.distractors = {}
        self.distractors[target] = self.findDistractorsByTarget(target, self.dominio)
            
    def run(self):
        self.checkSuccess()
        return self.description
    
    def checkSuccess(self):
        if len(self.stack) == 0:
            return True
        elif len(self.distractors[self.stack[len(self.stack)-1]]) <= 1:
            self.stack.pop()
            return self.checkSuccess()
        else:
            for key in self.atributos.keys():
                if len(self.atributos[key]) == 0:
                    return False
            return self.checkProperty()
    
    def checkProperty(self):
        target = self.stack.pop()
        if self.description[target] == {} and self.dominio[target]['type'] != []:
            self.description[target]['type'] = self.dominio[target]['type'][0]
            properties = {}
            properties['type'] = self.dominio[target]['type'][0]
            self.distractors[target] = self.findDistractorsByProperties(properties)
            self.atributos[target].remove('type')
        else:
            melhorAtributo = ''
            melhorElemento = ''
            melhorDistractors = {}
            for atributo in self.atributos[target]:
                melhorLandmark = ''
                distractors = {}
                for element in self.dominio[target][atributo]:
                    properties = {}
                    for key in self.description[target].keys():
                        properties[key] = self.description[target][key]
                    properties[atributo] = element
                    
                    auxDistractors = {}
                    auxDistractors = self.findDistractorsByProperties(properties)
                    
                    if melhorLandmark == '' and len(auxDistractors.keys()) > 0:
                        melhorLandmark = element
                        distractors = auxDistractors
                    elif len(auxDistractors.keys()) > 0 and len(auxDistractors.keys()) < len(distractors.keys()):
                        melhorLandmark = element
                        distractors = auxDistractors
                        
                if melhorAtributo == '' and len(distractors.keys()) > 0:
                    melhorAtributo = atributo
                    melhorElemento = melhorLandmark
                    melhorDistractors = distractors
                elif len(distractors.keys()) > 0 and len(distractors.keys()) < len(melhorDistractors.keys()):
                    melhorAtributo = atributo
                    melhorElemento = melhorLandmark
                    melhorDistractors = distractors
                    
            self.description[target][melhorAtributo] = melhorElemento
            self.distractors[target] = melhorDistractors
            self.atributos[target].remove(melhorAtributo)
        
            if self.relationalAttribute(melhorAtributo):
                if melhorElemento not in self.description.keys():
                    self.stack.append(melhorElemento)
                    self.atributos = self.listaAtributos(melhorElemento)
                    self.description[melhorElemento] = {}
                    self.distractors[melhorElemento] = self.findDistractorsByTarget(melhorElemento, self.dominio)
        
        self.stack.append(target)
        return self.checkSuccess()
                    
    def relationalAttribute(self, atributo = str):
        lista = atributo.split("_")
        
        if lista[0] != "name" and lista[0] != "type" and lista[0] != "other":
            return True
        else:
            return False
           
    def listaAtributos(self, target):
        if len(self.preferred_attributes) == 0:
            aux = self.dominio[target].keys()
            atributos = []
            for atributo in aux:
                if len(self.dominio[target][atributo]) != 0:
                    atributos.append(atributo)
            self.atributos[target] = atributos
        else:
            self.atributos[target] = self.preferred_attributes
        return self.atributos
    
    
    def findDistractorsByTarget(self, target, dominio):
        distractors = {}
        for objeto in dominio.keys():
            if objeto != target: 
                distractors[objeto] = dominio[objeto]

        return distractors
    
    def findDistractorsByProperties(self, properties = {}):
        distractors = {}
        
        dominio = self.dominio
        
        for property in properties.keys():
            distractors = {}
            for object in dominio.keys():
                if properties[property] in dominio[object][property]:
                    distractors[object] = dominio[object]
            dominio = distractors
            
        return distractors