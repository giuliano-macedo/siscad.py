from requests import Session
from bs4 import BeautifulSoup as BS
from collections import namedtuple
import re

Disciplina=namedtuple("Disciplina",["nome","ch","id"])
class Siscad:
	def __init__(self,passaporte,senha):
		"""
			login no SISCAD
				passaporte:str
				senha:str
			atributos:
				rga:str
				nome:str
				carga_hor:float
				cr:float
				discs_feitas:int
				discs:list de tipo Disciplina
		"""
		self.sess=Session()
		res=self.sess.post(
			'https://siscad.ufms.br/login', 
			data={"passaporte":passaporte,"senha":senha}
		)
		if res.url!="https://siscad.ufms.br/academico":
			raise RuntimeError("Senha/Passaporte Invalido")
		self.__main_parser(res.text)
	def __main_parser(self,doc):
		soup=BS(doc,"lxml")
		# nome / rga
		self.rga=soup.select_one("li.user-header>p>small").text.strip().split(" ")[-1]
		self.nome=soup.select_one("div.pull-left.info>p").text
		#carga_hor,cr,discs_feitas
		box_content=soup.select("div.info-box-content")
		carga_hor,cr,discs_feitas=(
			elem.select_one("span.info-box-number").text.strip() for elem in box_content
		)
		self.carga_hor=float(carga_hor.replace(",",".")[:-1])
		self.cr=float(cr.replace(",","."))
		self.discs_feitas=int(discs_feitas)
		#ultima_matricula,discs
		self.ultima_matricula=soup.select_one("h3.box-title.color-gray").text.split(":")[-1].strip()
		self.discs=[]
		for tr in soup.select_one("div.box-body").select("tr")[1:]:
			td=tr.select("td")
			nome=td[0].text.strip()
			ch=	 td[2].text.strip()
			_id= td[3].select_one("a").attrs["href"].split("/")[-1]
			self.discs.append(Disciplina(nome,ch,_id))
