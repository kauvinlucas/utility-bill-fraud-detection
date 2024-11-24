from src.generators import generator_bill_1, generator_bill_2
from tqdm import tqdm
import argparse

argparse = argparse.ArgumentParser()
argparse.add_argument("--n", type=int, default=10)
argparse.add_argument("--template", type=int, default=1)
args = argparse.parse_args()

n = args.n
template = args.template

# Date formats
short_date_format = "%m-%y"
standard_date_format = "%d/%m/%y"
long_date_format = "%d/%m/%Y"

# Names and addresses
names = ["JOSE", "JORGE", "SANTIAGO", "JULIA", "ANA", "JUSTINIANO", "BERNADETH", "CARLOS", "PEDRO", "LUIS",
         "CRISTIAN", "LUCIA", "CESAR", "HENRY", "MARCO", "EDUARDO", "ALEJANDRA", "MARIA", "JULIO", "MARCELA",
         "ELVIN", "PAOLA", "VIVIANA", "RODRIGO", "LAURA", "JOSEFA", "ISABEL", "LAURA", "CARMEN"]
middle_names = ["CASTEDO", "LUCAS", "CHAMBI", "TOLEDO", "MORALES", "MATEO", "DOLORES", "PILAR", "ANTONIO"]
last_names = ["SUAREZ", "BARBERY", "POLANCO", "VARGAS", "HURTADO", "GUTIERREZ", "FRANCISCO", "MAMAMI", "GARCIA",
             "GONZALES", "FERNANDEZ", "LOPEZ", "MARTINEZ", "PEREZ", "SANCHEZ", "MARTIN", "GOMEZ", "JAVIER"]

addresses1 = ["LOS CUSIS", "MAQUINA VIEJA", "POLANCO", "ESTACION ARGENTINA", "SAN JUAN MACIAS", "RAMAFA", "SANTA ROSA", "LAS PALMAS",
             "NTE INTERNO", "PALERMO", "LOS PENOCOS", "LA BELGICA", "EL PARAISO", "AERONAUTICO", "BRANIFF", "SAN CARLOS"]

addresses2 = [ "CALLE CHARAGUA,", "CALLE CORDILLERA,", "CALLE MOCAPINI,",
             "CALLE RIO GRANDE,", "AVENIDA ANA BARBA,", "CALLE SOLIZ DE OLGUIN,", "AVENIDA ANDRES MANSO,", "AV. CAP. MARIANO ARRIEN,",
             "CALLE CABO QUIROGA,", "CALLE PEDRO SUAREZ,", "CALLE EL CARMEN,", "AVE TRINIDAD,","CALLE NICARAGUA,", 
              "AVENIDA HERNANDO SANABRIA,", "CALLE BIBOSI,", "CALLE SAN JAVIER,", "CALLE AZUBI,",  "CALLE MIGUEL CASTRO,", 
              "CALLE OBAJ,", "CALLE BATALLA DE TOLEDO,", "RADIAL 17,", "AVE TOMAS DE LEZO,", "CALLE ALAPO,",
             "CALLE BRUNO RACUA,", "CALLE RIO BLANCO,"]
depto_prefixes = ["A","B","C","D","E","F","G"]

def main(n, template):
    for bill in tqdm(range(n)):
        if template == 1:
            generator = generator_bill_1(names, middle_names, last_names, addresses1, addresses2, depto_prefixes)
            generator.first_header()
            generator.second_header()
            generator.third_header()
            generator.historical_consumption()
            generator.fourth_header()
            generator.details()
            generator.municipal_rates()
            generator.print_image(bill+1)
        if template == 2:
            generator = generator_bill_2(names, middle_names, last_names, addresses1, addresses2, depto_prefixes)
            generator.first_header()
            generator.historical_consumption()
            generator.second_header()
            generator.details()
            generator.print_image(bill+1)

if __name__ == "__main__":
    print("Generating {} bills".format(n))
    main(n, template)