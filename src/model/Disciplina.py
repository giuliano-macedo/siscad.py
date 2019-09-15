from bs4 import BeautifulSoup as BS
from . import Nota,Semestre
class Disciplina():
	def __init__(self,request_getter,nome,ch,_id):
		self.id=_id
		self.nome=nome
		self.ch=ch
		self.request_getter=request_getter
		self.is_cached=False

		self.__notas=None
		self.__turma=None
		self.__prof=None
		self.__situacao=None
		self.__formula=None

	def __parser(self,doc):
		soup=BS(doc,"html.parser")
		
		table=soup.select_one("div.box.box-primary.collapsed-box")
		table=table.select("table")[1]
		table=table.select_one("tbody")

		self.__turma,self.__prof=(elem.text.strip() for elem in table.select("td")[:2]) 

		avaliacoes=soup.select_one("div#avaliacoes")

		situacao=avaliacoes.select_one("div.row.color-gray").select_one("span")
		situacao.select_one("strong").extract()
		self.__situacao=situacao.text.strip()

		ma=avaliacoes.select_one("div#ma")

		formula=ma.select("span")
		self.__formula=formula[1].text.strip() if len(formula)>=2 else None
		
		row=ma.select_one("div.row")
		mft=tuple(elem.text.strip().replace(",",".") for elem in row.select("span"))
		mf=Nota(*mft) if len(mft)==3 else None
		self.__notas=[mf] if mf else []
		divs=avaliacoes.select("div.box.box-primary")[1].select_one("div.row").find_all("div",recursive=False)
		for div in divs:
			for row in div.select("div.row")[1:-1]:
				nxt=tuple(elem.text.strip().replace(",",".") for elem in row.select("span"))
				if len(nxt)==3:
					self.__notas.append(Nota(*nxt))
				
		
	def update(self):
		self.is_cached|=True
		res=self.request_getter("academico","disciplinas",self.id)
		self.__parser(res.text)
	def __getattr__(self,attr):
		try:
			value=getattr(self,"_Disciplina__"+attr)
		except Exception:
			raise AttributeError(f"AttributeError: '{type(self)}' object has no attribute '{attr}'")
		if not self.is_cached:
			self.update()
		value=getattr(self,"_Disciplina__"+attr)
		if value==None:
			raise RuntimeError("Unexpected error")
		return value
