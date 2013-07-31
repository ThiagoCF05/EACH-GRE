from Objeto import *

class FullBrevity(object):
	"""docstring for FullBrevity"""
	def __init__(self, dominio = [], target = Objeto, distractors = [], preferred_attributes = []):
		super(FullBrevity, self).__init__()
		self.dominio = dominio
		self.target = target
		self.distractors = self.findDistractors()
		if len(preferred_attributes) == 0:
			self.atributos = target.atributos.keys()
		else:
			self.atributos = preferred_attributes

	def run(self):
		lista = self.geraResultado([], None, 1, 1)
		result = {}
		for element in lista:
			result[element] = self.target.atributos[element]
		return result
				
	def geraResultado(self, descriptionProperties, attribute, numeroForInicio, numeroFor):
		
		if attribute != None:
			descriptionProperties.append(attribute)							
		
		numeroFor = numeroFor - 1
		for atributo in self.atributos:
			if atributo not in descriptionProperties:				
				if numeroFor == 0:
					descriptionProperties.append(atributo)
					if self.ruledOut(descriptionProperties) == True:
						return descriptionProperties											
					descriptionProperties.remove(atributo)
				else:					
					return self.geraResultado(descriptionProperties, atributo, numeroForInicio, numeroFor)
				
		if (numeroForInicio < len(self.atributos)):
			return self.geraResultado([], None, numeroForInicio+1, numeroForInicio+1)
		else:
			return []
					
	def ruledOut(self, descriptionProperties = []):
		
		for distractor in self.distractors:
			targetDescription = []
			distractorDescription = []
			
			for atributo in descriptionProperties:
				targetDescription.append(self.target.atributos[atributo])
				distractorDescription.append(distractor.atributos[atributo])
			
			#print 10 * "-"
			#print "Target: "  + self.target.nome
			#print targetDescription
			#print 10 * "-" 
			#print "Distractor: " + distractor.nome
			#print distractorDescription
			#print 10 * "-" 
			#print "\n\n"
				
			if targetDescription == distractorDescription:
				return False
		
		#print descriptionProperties	
		return True


	def findDistractors(self):
		distractors = []
		for objeto in self.dominio:
			if objeto != self.target: 
				distractors.append(objeto)

		return distractors


