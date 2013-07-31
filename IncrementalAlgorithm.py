
class IncrementalAlgorithm(object):
	"""docstring for IncrementalAlgorithm"""
	def __init__(self, dominio = {}, target = str, preferred_attributes = []):
		super(IncrementalAlgorithm, self).__init__()
		self.dominio = dominio
		self.target = target
		self.distractors = self.findDistractors()
		if len(preferred_attributes) == 0:
			self.atributos = self.dominio[target].keys()
		else:
			self.atributos = preferred_attributes
		self.description = {}
		self.description[self.target] = {}

	def run(self):

		for atributo in self.atributos:
			for element in self.dominio[self.target][atributo]:
				properties = {}
				properties = {}
				for key in self.description:
					properties[key] = self.description
				properties[atributo] = element
				
				previousDistractor = {}
				for element in self.distractors.keys():
					previousDistractor[element] = self.distractors[element]
				
				self.distractors = self.findDistractorsByProperties(properties)
				
				if len(self.distractors) < len(previousDistractor):
					self.description[self.target][atributo] = element
				
				if len(self.distractors) == 1:
					return self.description
		if len(self.distractors) > 0:
			print """Nao foi possivel definir uma referencia para o objeto"""


	def findDistractors(self):
		distractors = []
		for objeto in self.dominio:
			if objeto != self.target: 
				distractors.append(objeto)

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

		