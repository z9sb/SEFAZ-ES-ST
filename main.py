from os import listdir
from pathlib import Path
from easygui import diropenbox #type: ignore 
from request_sefaz import Api
from requests import Session  # type: ignore

url_html = 'http://www2.sefaz.es.gov.br/LegislacaoOnline/lpext.dll/InfobaseLegislacaoOnline/portarias/2019/port16-r%20-%20atualizada.htm?f=templates&fn=document-frame.htm&2.0'
html_content = Session().get(url_html)

rootdir = diropenbox(default= 'C:\donwload\*.xml')
root_dir = Path(rootdir)
file_xml = list(i for i in listdir(root_dir) if i.endswith('.xml'))

Api(html_content, file_xml, root_dir)