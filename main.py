from os import walk, path
from pathlib import Path
from easygui import diropenbox #type: ignore 
from request_sefaz import Api
from requests import Session  # type: ignore
from patoolib import extract_archive # type: ignore
from tempfile import TemporaryDirectory
from shutil import copy2

class main():
    def __init__(self, root_dir):
        self.url_html = 'http://www2.sefaz.es.gov.br/LegislacaoOnline/lpext.dll/InfobaseLegislacaoOnline/portarias/2019/port16-r%20-%20atualizada.htm?f=templates&fn=document-frame.htm&2.0'
        self.html_content = Session().get(self.url_html)
        self.root_dir = root_dir
        self.file_xml: list = []
        self.xml_dir()
        
    def rar_extract(self, arquivo):
        with TemporaryDirectory() as temp_dir:
            try:
                extract_archive(arquivo, outdir=temp_dir)
            except:
                pass    
            
            for pasta_atual, subpastas, arquivos in walk(temp_dir):
                for arquivo in arquivos:
                    if arquivo.endswith('.xml'):
                        self.file_xml.append(path.join(pasta_atual, arquivo))
                        copy2(path.join(pasta_atual, arquivo), r"C:\Users\raysl_3a68bgu\OneDrive\Documentos\Python\outlook\teste2\\")
    def xml_dir(self):      
        for pasta_atual, subpastas, arquivos in walk(self.root_dir):
            for arquivo in arquivos: 
                if arquivo.endswith('.xml'): 
                    self.file_xml.append(path.join(pasta_atual, arquivo))
                elif arquivo.endswith('.zip') or arquivo.endswith('.rar'):
                    self.rar_extract(path.join(pasta_atual, arquivo))

        Api(self.html_content, self.file_xml)

if __name__ == '__main__': 
    rootdir = diropenbox(default= 'C:\donwload\*.xml')
    root_dir = Path(rootdir)
    main(root_dir)