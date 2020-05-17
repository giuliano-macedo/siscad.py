![PyPI](https://img.shields.io/pypi/v/siscad)
# Módulo para extrair informações do Siscad

## Exemplo
```python
from siscad import Siscad
siscad=Siscad("passaporte","senha") 

print(siscad.rga)
print(siscad.nome)
print(siscad.carga_hor)
print(siscad.cr)
print(siscad.discs_feitas)
print(siscad.ultima_matricula)

for semestre in siscd.get_semestres():
	print(semestre.date)
	for disciplina in semestre.discs:
		print(disciplina.nome)
		print(*disc.notas,sep="\n")
```
