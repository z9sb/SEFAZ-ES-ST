from os import walk, path
from pathlib import Path
from easygui import diropenbox #type: ignore 
from request_sefaz import Api
from requests import Session  # type: ignore

url_html = 'http://www2.sefaz.es.gov.br/LegislacaoOnline/lpext.dll/InfobaseLegislacaoOnline/portarias/2019/port16-r%20-%20atualizada.htm?f=templates&fn=document-frame.htm&2.0'
html_content = Session().get(url_html)

rootdir = diropenbox(default= 'C:\donwload\*.xml')
root_dir = Path(rootdir)

file_xml = []
for pasta_atual, subpastas, arquivos in walk(root_dir):
    for arquivo in arquivos: 
        if arquivo.endswith('.xml'): 
            file_xml.append(path.join(pasta_atual, arquivo))

Api(html_content, file_xml)
