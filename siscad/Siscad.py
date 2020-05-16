import requests
from bs4 import BeautifulSoup as BS
from collections import namedtuple
from urllib.parse import urljoin
import os
import re
from .model import Nota,Disciplina,Semestre
from . import HEADERS
from .utils import parse_table

regex_extract_number=lambda s:int(re.search(r"\d+",s).group(0))

base_url_join=lambda *args:urljoin(Siscad.base_url,os.path.join(*args))


class Siscad:
    base_url="https://siscad.ufms.br"
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
        self.sess=requests.Session()
        self.sess.headers=HEADERS
        res=self.sess.post(
            base_url_join("login"), 
            data={"passaporte":passaporte,"senha":senha}
        )
        if res.url!=base_url_join("academico"):
            raise RuntimeError("Senha/Passaporte Invalido")
        self.__main_parser(res.text)
    def __request_getter(self,*args):
        return self.sess.get(base_url_join(*args))
    def get_semestres(self):
        res=self.__request_getter("academico","disciplinas")
        if not res.ok:
            raise RuntimeError("Falha ao acessar endereço \"%s\""%res.url)
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
            for d in parse_table(div.select_one("table")):
                try:
                    _id=        regex_extract_number(d["Código da Disciplina"].select_one("a").attrs["href"])
                    nome=       d["Nome da Disciplina"].text.strip()
                    situacao=   d["Situação"].text.strip()
                    ch=         regex_extract_number(d["C.H."].text.strip())
                except KeyError as e:
                    print("keys available:",list(d.keys()))
                    raise e
                sem.discs.append(Disciplina(Siscad.base_url,self.sess.cookies.get("CAKEPHP"),nome,ch,_id))
            ans.append(sem)
        return ans[::-1]

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