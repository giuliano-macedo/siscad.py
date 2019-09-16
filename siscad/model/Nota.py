class Nota():
	def __init__(self,nome,individual,turma):
		self.nome=nome if nome else None
		self.individual=float(individual) if individual else None
		self.turma=float(turma) if turma else None
	def __repr__(self):
		return f"Nota({repr(self.nome)},{self.individual},{self.turma})"
	def _parser(row):
		t=tuple(elem.text.strip().replace(",",".") for elem in row.select("span"))
		return Nota(*t) if len(t)==3 else None