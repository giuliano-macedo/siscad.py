# Módulo para extrair informações do Siscad

## Exemplo
```python
from Siscad import Siscad
siscad=Siscad.Siscad("passaporte","senha") 

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