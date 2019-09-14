from requests import Session
from bs4 import BeautifulSoup as BS
from collections import namedtuple
from urllib.parse import urljoin
import os
import re

base_url="https://siscad.ufms.br"
base_url_join=lambda *args:urljoin(base_url,os.path.join(*args))
class Semestre:
	def __init__(self,date,discs):
		self.date=date
		self.discs=discs
	def __str__(self):
		return f"<Semestre data={self.date} discs={self.discs}>"
class Disciplina():
	def __init__(self,sess,nome,ch,_id):
		self.id=_id
		self.nome=nome
		self.ch=ch
		self.sess=sess
		self.is_cached=False
	def update(self):
		self.is_cached|=True
		res=self.sess.get(base_url_join("academico","disciplinas",self.id))
		self.__parser(res.text)
	def get_notas(self):
		pass
	def get_presenca(self):
		pass
	def get_plano_ensino(self):
		pass
	def __str__(self):
		return f"<Disciplina nome={self.nome} id={self.id} ch={self.ch}>"
	def __repr__(self):
		return str(self)
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
			base_url_join("login"), 
			data={"passaporte":passaporte,"senha":senha}
		)
		if res.url!=base_url_join("academico"):
			raise RuntimeError("Senha/Passaporte Invalido")
		self.__main_parser(res.text)
	def get_disciplinas(self):
		res=self.sess.get(base_url_join("academico","disciplinas"))
		return self.__disciplinas_parser(res.text)
	def __disciplinas_parser(self,doc):
		soup=BS(doc,"html.parser")
		ans=[]

		for div in soup.select("div.box-primary")[1:]:
			date=div.select_one("h3.box-title.color-gray").text.strip()
			sem=Semestre(
				re.search(r"\d+\/\d+",date).group(0),
				[]
			)
			for tr in div.select_one("table").select("tr")[1:]:
				td=tr.select("td")
				nome=td[0].text.strip()
				situacao=td[1].text.strip()
				ch=	 td[2].text.strip()
				_id= re.search(r"\d+",td[3].select_one("a").attrs["href"]).group(0)
				sem.discs.append(Disciplina(self.sess,nome,ch,_id))
			ans.append(sem)
		return ans

	def __main_parser(self,doc):
		soup=BS(doc,"html.parser")
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
		#ultima_matricula
		self.ultima_matricula=soup.select_one("h3.box-title.color-gray").text.split(":")[-1].strip()

