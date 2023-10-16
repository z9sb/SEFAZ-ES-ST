from bs4 import BeautifulSoup as bs  # type: ignore
from xml_file import NFe
from csv import writer

class Api:
    def __init__(self, html_content, file_xml, root_dir) -> None:
        self.html = bs(html_content.text, 'html.parser')
        self.file_xml = file_xml
        self.root_dir = root_dir
        self.loc_class()
        self.xml_search(self.file_xml, self.root_dir)

    def find_all_tag_html(self, html_parser, tag):
        return [valor for valor in html_parser.find_all(tag)]

    def style_check(self, item):
        style = ('font-size:8.0pt;font-family:"Verdana","sans-serif";\r\n' +
                 '  color:black')
        if item.find('span') is not None and style == item.find(
            'span')['style'] and item['width'] == '74' and item.find(
                'span').text != '\xa0':
            return True
        else:
            return False

    def loc_class(self):
        dados = []
        for index, tag_tr in enumerate(self.find_all_tag_html(self.html, 'tr')):
            linha = {'CEST': [], 'NCM': []}
            for item in self.find_all_tag_html(tag_tr, 'td'):
                if self.style_check(item):
                    for valor in str(item.text).replace(
                            '.', '').strip().split():
                        if valor.isdigit():
                            if len(valor) == 7:
                                linha['CEST'].append(valor)
                                
                            elif len(valor) >= 4:
                                linha['NCM'].append(valor)
                else:
                    continue
                
            if not linha == {'CEST': [], 'NCM': []} and index != 1:
                dados.append(linha)
            
        self.ncm_l = set({item for sub in dados for item in sub['NCM']})
        self.cst_l = set({item for sub in dados for item in sub['CEST']})
        
        return dados

    def comparation_ncm_cst(self, chave, ncms, cests, cfops, name_prods):
        with open('test.csv', 'a', newline="") as csv_file:
            self.csv_withe = writer(csv_file, delimiter=";")
            for ncm, cest, cfop, name_prod in zip(ncms, cests, cfops, name_prods):
                if any(ncm.startswith(item) for item in self.ncm_l):
                    if cest != 0:
                        if cest in self.cst_l:
                            self.csv_withe.writerow([chave, ncm, cest, cfop, name_prod])
                            
                    else:
                        self.csv_withe.writerow([chave, ncm, cest, cfop, name_prod])

    def xml_search(self, file_xml, root_dir):
        for root_file in file_xml:
            root = (f'{root_dir}/{root_file}')
            
            xml = NFe(root)
            cests = xml.cest()
            ncms = xml.ncm()
            chave = xml.acess_key()
            cfops = xml.cfop()
            name_prods = xml.name_prod()
            estado_cli = xml.estado_cli()
            estado_for = xml.estado_for()

            if estado_cli == estado_for:
                pass
            
            else:
                print(chave)
                self.comparation_ncm_cst(chave, ncms, cests, cfops, name_prods)