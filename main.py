from os import walk, path
from shutil import rmtree
from uuid import uuid4
from pathlib import Path
from easygui import diropenbox #type: ignore 
from request_sefaz import Api
from requests import Session  # type: ignore
from patoolib import extract_archive # type: ignore
from shutil import copy2

class main():
    def __init__(self, root_dir):
        self.url_html = 'http://www2.sefaz.es.gov.br/LegislacaoOnline/lpext.dll/InfobaseLegislacaoOnline/portarias/2019/port16-r%20-%20atualizada.htm?f=templates&fn=document-frame.htm&2.0'
        self.html_content = Session().get(self.url_html)
        self.root_dir = root_dir
        self.file_xml: list = []
        self.dir_name = []
        self.xml_dir()
                 
    def rar_extract(self, arquivo):
        self.dir_extract = f'{self.root_dir}\\{uuid4()}\\'
        self.dir_name.append(self.dir_extract)
        try:
            extract_archive(arquivo, outdir=self.dir_extract)
        except:
            pass    
        
        for pasta_atual, subpastas, arquivos in walk(self.dir_extract):
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
        for dir_name in self.dir_name:
            rmtree(dir_name)
            print(f"O diretório {dir_name} foi removido!")
            
if __name__ == '__main__': 
    rootdir = diropenbox(default= 'C:\donwload\*.xml')
    root_dir = Path(rootdir)
    main(root_dir)