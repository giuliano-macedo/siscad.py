from bs4 import BeautifulSoup as BS
from . import Nota,Semestre,Frequencia
import requests
import html2markdown
import re
from itertools import chain
from collections import Counter
from .. import HEADERS

class Disciplina():
	__request_getter=None
	def __init__(self,base_url,cakephp_cookie,nome,ch,_id,notas=None,turma=None,prof=None,situacao=None,formula=None,ementa=None,frequencias=None):
		self.__id=_id
		self.__nome=nome
		self.__ch=ch
		self.__is_cached=False
		self.__sess=requests.Session()
		self.__sess.headers=HEADERS
		cookie_obj = requests.cookies.create_cookie(
			domain='siscad.ufms.br',
			name='CAKEPHP',
			value=cakephp_cookie
		)
		self.__sess.cookies.set_cookie(cookie_obj)
		self.__base_url=base_url
		#Requerem self.update()
		#--------------------------------------------------------------
		self.__notas=notas
		self.__turma=turma
		self.__prof=prof
		self.__situacao=situacao
		self.__formula=formula
		self.__ementa=ementa
		self.__frequencias=frequencias


	def update(self):
		self.__is_cached|=True
		res=self.__sess.get(f"{self.base_url}/academico/disciplinas/{self.id}")
		self.__parser(res.text)
	def get_faltas(self):
		freqs=Counter(chain.from_iterable([f.chamadas for f in self.frequencias])).get(False,0)
		return freqs*100/self.ch
	def get_presencas(self):
		return 100-self.get_faltas()
	def __repr__(self):
		return f"""
				Disciplina(
					base_url={repr(self.__base_url)},
					cakephp_cookie={repr(self.__sess.cookies.get("CAKEPHP"))},
					nome={repr(self.__nome)},
					ch={repr(self.__ch)},
					id={repr(self.__id)},
					notas={repr(self.__notas)},
					turma={repr(self.__turma)},
					prof={repr(self.__prof)},
					situacao={repr(self.__situacao)},
					formula={repr(self.__formula)},
					ementa={repr(self.__ementa)},
					frequencias={repr(self.__frequencias)}

				)
			""".replace("\n","").replace("\t","")

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
		
		mf=Nota._parser(ma.select_one("div.row"))
		
		self.__notas=[mf] if mf else []
		divs=avaliacoes.select("div.box.box-primary")[1].select_one("div.row").find_all("div",recursive=False)
		for div in divs:
			for row in div.select("div.row")[1:-1]:
				nota=Nota._parser(row)
				if nota:
					self.__notas.append(nota)
		
		frequencias=soup.select_one("div#frequencias")

		self.__frequencias=[]

		for div in frequencias.select("div.box.box-primary")[1:]:
			year=div.select_one("div").text.strip().split("/")[-1]
			table=div.select_one("table>tbody")
			for tr in table.select("tr"):
				day_month,hour_minute,tipo,*chamadas=(elem.text.strip() for elem in tr.select("td"))
				self.__frequencias.append(Frequencia._parser(year,day_month,hour_minute,tipo,chamadas))
		
		planos=soup.select_one("div#planos")
		for h3 in planos.select("h3"):
			del h3.attrs["class"]
		planos="".join(re.compile(r'<div.*>|<\/div>|\n+|\t+').split(str(planos)))
		self.__ementa=html2markdown.convert(planos)


		
	def __getattr__(self,attr):
		try:
			value=getattr(self,"_Disciplina__"+attr)
		except Exception:
			raise AttributeError(f"AttributeError: '{type(self)}' object has no attribute '{attr}'")
		if not self.__is_cached:
			self.update()
		value=getattr(self,"_Disciplina__"+attr)
		if value==None:
			raise RuntimeError("Unexpected error")
		return value
