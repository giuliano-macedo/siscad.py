from requests import Session
from bs4 import BeautifulSoup as BS

def main_parser(doc):
	soup=BS(doc,"lxml")

class Siscad:
	def __init__(self,passaporte,senha):
		self.sess=Session()
		res=main_parser(self.sess.post(
			'https://siscad.ufms.br/login', 
			data={"passaporte":passaporte,"senha":senha}
		))