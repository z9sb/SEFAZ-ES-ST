from bs4 import BeautifulSoup as bs  # type: ignore
from xml_file import NFe
from csv import writer

class Api:
    def __init__(self, html_content, file_xml) -> None:
        self.html = bs(html_content.text, 'html.parser')
        self.file_xml = file_xml
        self.loc_class()
        self.xml_search(self.file_xml)

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
        self.cest_l = set({item for sub in dados for item in sub['CEST']})
        
        return dados

    def comparation_ncm_cst(
        self, chave, n_nf, name_for, cnpj_dest, ncms, cests, cfops, name_prods,
        v_prods, v_ipis, v_outros, v_fretes, v_descs, v_icms, ali_icms):
        
        with open(f'{cnpj_dest}.csv', 'a', newline="") as csv_file:
            self.csv_withe = writer(csv_file, delimiter=";")
            self.csv_withe.writerow([chave, n_nf, name_for])
            
            for (ncm, cest, cfop, name_prod, v_prod, v_ipi,
                 v_outro, v_frete, v_desc, v_icm, ali_icm) in zip(
                ncms, cests, cfops, name_prods, v_prods, v_ipis,
                v_outros, v_fretes, v_descs, v_icms, ali_icms
                ):
                if any(ncm.startswith(item) for item in self.ncm_l):
                    bc_icms_st = (float(v_prod) + float(v_ipi) + float(v_outro)+
                                          float(v_frete) - float(v_desc))
                    icms_dest = float(v_icm)
                    f_ncm = f'{ncm[0:5]}.{ncm[4:7]}.{ncm[7:9]}'
                    f_cest = f'{cest[0:2]}.{cest[3:6]}.{cest[6:7]}'
                    if cest != 0:
                        if cest in self.cest_l:
                            self.csv_withe.writerow(
                                [f_ncm, f_cest, cfop, bc_icms_st, icms_dest, ali_icm, name_prod])
                    else:
                        self.csv_withe.writerow(
                                [f_ncm, f_cest, cfop, bc_icms_st, icms_dest, ali_icm, name_prod])
                            
    def xml_search(self, file_xml):
        for root_file in file_xml:
            try:
                xml = NFe(root_file)
                estado_cli = xml.estado_cli()
                estado_for = xml.estado_for()
                
                if estado_cli == estado_for:
                    pass
                
                else:
                    cests = xml.cest()
                    ncms = xml.ncm()
                    cfops = xml.cfop()
                    chave = xml.acess_key()
                    n_nf = xml.number_nf()
                    name_prods = xml.name_prod()
                    v_prods = xml.v_prod()
                    v_ipis = xml.v_ipi()
                    v_outros = xml.v_outros()
                    v_fretes = xml.v_frete()
                    v_descs = xml.v_desc()
                    v_icms = xml.v_icms()
                    ali_icms = xml.ali_icms()
                    name_for = xml.name_for()
                    cnpj_dest = xml.cnpj_dest()

                    print(chave)
                    self.comparation_ncm_cst(
                        chave, n_nf, name_for, cnpj_dest, ncms, cests, cfops, name_prods,
                        v_prods, v_ipis, v_outros, v_fretes, v_descs, v_icms, ali_icms
                        )
            except:
                pass