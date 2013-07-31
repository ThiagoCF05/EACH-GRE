'''
Created on 20/01/2013

@author: thiago
'''

from Objeto import *
from Atributo import *

class IncrementalAlgorithmComplete(object):
    '''
    classdocs
    '''


    def __init__(self, dominio = [], target = Objeto, preferred_attributes = []):
        '''
        Constructor
        '''
        super(IncrementalAlgorithmComplete, self).__init__()
        self.dominio = dominio
        self.target = target
        self.distractors = self.findDistractors()
        if len(preferred_attributes) == 0:
            self.atributos = target.atributos.keys()
        else:
            self.atributos = preferred_attributes
            
    def run(self):
        distintores = {}
        ruledOuts = []
        
        for atributo in self.atributos:
            print "BASIC VALUE: " + self.basicLevelValue(self.target.atributos[atributo]).nome
            valor = self.findBestValue(self.target, atributo, self.basicLevelValue(self.target.atributos[atributo]))
            if valor != None:
                print 10 * "-" 
                print "Atributo: " + atributo
                print "Valor: " + valor.nome
                print 10 * "-" 
                print "\n"
                ruledOuts = self.rulesOut(atributo, valor, self.distractors)

            if len(ruledOuts) > 0:
                distintores[atributo] = valor
                self.distractors = self.redefineDistractors(self.distractors, ruledOuts)
            
            if len(self.distractors) == 0:
                return distintores
        if len(distintores) == 0:
            print """Nao foi possivel definir uma referencia para o objeto"""


    def findDistractors(self):
        distractors = []
        for objeto in self.dominio:
            if objeto != self.target: 
                distractors.append(objeto)

        return distractors
    
    def redefineDistractors(self, distractors = [], excluidos = []):
        for excluido in excluidos:
            distractors.remove(excluido)
            
        return distractors

    def findBestValue(self, target, atributo, atributoPai = Atributo):
        _value = None
        if atributoPai.userKnows == True:
            _value = atributoPai
        
            _moreSpecificValue = self.moreSpecificValue(_value)
            
            if _moreSpecificValue != None:
                _newValue = self.findBestValue(target, _moreSpecificValue)
                
                if _newValue != None:
                    if len(self.rulesOut(atributo, _newValue, self.distractors)) > len(self.rulesOut(atributo, _value, self.distractors)):
                        _value = _newValue           
        
        return _value
    
    def moreSpecificValue(self, atributo):
        return atributo.filho
    
    def basicLevelValue(self, atributo):        
        if atributo.pai == None:
            return atributo
        else:
            return self.basicLevelValue(atributo.pai)
        

    def rulesOut(self, atributo = str, valor = Atributo, distractors = []):
        lista = []
        #print atributo
        for distractor in distractors:
            #print distractor.atributos[atributo].nome
            if distractor.atributos[atributo] != valor or distractor.atributos[atributo].userKnows == False:
                lista.append(distractor)

        return lista
