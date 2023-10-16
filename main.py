from os import path, remove, listdir
from pathlib import Path
from easygui import diropenbox #type: ignore 
from request_sefaz import Api
from requests import Session  # type: ignore

url_html = 'http://www2.sefaz.es.gov.br/LegislacaoOnline/lpext.dll/InfobaseLegislacaoOnline/portarias/2019/port16-r%20-%20atualizada.htm?f=templates&fn=document-frame.htm&2.0'
html_content = Session().get(url_html)

if path.exists('rootdir.txt'):
    remove('rootdir.txt')
    
if not path.exists('rootdir.txt'):
    rootdir = diropenbox(default= 'C:\donwload\*.xml')
    
    with open('rootdir.txt', 'w') as f:
        f.write(rootdir)

with open('rootdir.txt') as dir_name:
    root_dir = Path(dir_name.readline())
    file_xml = list(i for i in listdir(root_dir) if i.endswith('.xml'))

Api(html_content, file_xml, root_dir)
