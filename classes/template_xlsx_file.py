
from io import BytesIO
from xlsxwriter import Workbook

class Template_XLSX:
    def _create_template_xlsx_file(self):
        output = BytesIO()
        wb = Workbook(output, {'in_memory': True})
        ws = wb.add_worksheet()

        with wb:
            ws.write('A1', 'Article ID')
            ws.write('A2', """
        Obligatoire \n 
        1""")
            
            ws.write('B1', 'Client')
            ws.write('B2', """
        Obligatoire \n
        Nom du client : 
        "Ma Cave à Vin", 
        "Aixam", 
        "Vicat",
        etc.""")
            
            ws.write('C1', 'Type de page')
            ws.write('C2', """
        Obligatoire \n
        "Catégorie", 
        "Article de blog", 
        "Newsletter", 
        "Page produit", 
        etc.""")
            
            ws.write('D1', 'Sujet')
            ws.write('D2', """
        Obligatoire \n
        "Cave à vin de vieillissement", 
        "Voiture sans permis", 
        "Béton de chanvre", 
        etc.""")
            
            ws.write('E1', 'Consignes')
            ws.write('E2', """
        Obligatoire \n
        "Utiliser le vouvoiement et un discourd professionnel", 
        "Utiliser un discours familier, simple et direct", 
        "Utiliser des termes simples avec des phrases courtes", 
        etc.""")
            
            ws.write('F1', 'Nombre de mots')
            ws.write('F2', """
        Obligatoire \n
        "1000", 
        "500", 
        "750",
        etc.""")
            
            ws.write('G1', 'Structure')
            ws.write('G2', """
        Obligatoire \n
        "Libre", 

        "H1, 3 H2 et 4 H3 pour chaque sous-partie", 

        "<h1>[CAVE]</h1>
        <h2>Qu'est ce qu'une [CAVE] ?</h2>
        <h2>Comment choisir sa cave [CAVE] ?</h2>
        <h2>Quelles marques de [CAVE] proposées sur Ma Cave a Vin ?</h2>
        <h2>Nos conseils pour l'achat de votre [CAVE]</h2>
        <h2>Comparer les [CAVE]</h2>
        <h2>Quelle température pour une [CAVE] ?</h2>
        <h2>Où installer sa [CAVE] ?</h2>",

        etc.""")
            
            ws.write('H1', 'Mots clés primaires')
            ws.write('H2', """
        Obligatoire \n
        "Vins, caves à vin, vieillissement, température",

        "Voiture sans permis, voiture aixam",
        
        "Béton de chanvre", 

        etc.""")
            
            ws.write('I1', 'Mots clés secondaires')
            ws.write('I2', """
        Facultative \n
        "",

        "aixam city sport, voiturette",

        "Louis Vicat",

        etc.""")
            
            ws.write('J1', 'Meta titre')
            ws.write('J2', """Facultative""")
            
            ws.write('K1', 'Meta description')
            ws.write('K2', """Facultative""")
            
            ws.write('L1', 'Textes d\'exemples')
            ws.write('L2', """Facultative""")
            
        return output
        