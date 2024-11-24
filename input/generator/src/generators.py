from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random
from pathlib import Path

# Plotting libraries
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

class generator_bill_1:
    def __init__(self, names, middle_names, last_names, addresses1, addresses2, depto_prefixes):
        self.short_date_format = "%m-%y"
        self.standard_date_format = "%d/%m/%y"
        self.long_date_format = "%d/%m/%Y"
        self.n = 13
        self.names = names
        self.middle_names = middle_names
        self.last_names = last_names
        self.addresses1 = addresses1
        self.addresses2 = addresses2
        self.depto_prefixes = depto_prefixes
        self.random_with_leading_zeroes = lambda total_len, upper_limit: "0" * (total_len - len(str(random.randint(1, upper_limit))))\
                                            + str(random.randint(1, upper_limit))

    def random_with_leading_zeroes(self, total_len, upper_limit):
        gauge_num = str(random.randint(1, upper_limit))
        leading_zeros = total_len - len(gauge_num)
        return "0" * leading_zeros + gauge_num
        
    def first_header(self):
        # Parameters for dates
        lookup_bill_month = {9:"Septiembre 2024", 10:"Octubre 2024", 11:"Noviembre 2024"}
        # Bill date
        day_bill = random.choice(range(29)) + 1
        month_bill = random.choice([11,10,9])
        self.month_bill_literal = lookup_bill_month[month_bill]
        # Due date
        self.start_date = datetime(2024, month_bill, day_bill)
        self.next_measurement_date = self.start_date + timedelta(days = 30) + timedelta(days=random.choice([-1,0,1]))
        self.due_date = datetime.strftime(self.next_measurement_date + timedelta(days=1), self.standard_date_format)
        self.next_measurement_date = datetime.strftime(self.next_measurement_date, self.standard_date_format)
        self.start_date_str = datetime.strftime(self.start_date, self.standard_date_format)
        
    def second_header(self):
        # Name generation
        name = self.names[random.randint(0, len(self.names)-1)]
        middle_name = self.middle_names[random.randint(0, len(self.middle_names)-1)]
        last_name = self.last_names[random.randint(0, len(self.last_names)-1)]
        last_name2 = [name for name in self.last_names if name != last_name][random.randint(0, len(self.last_names)-2)]
        if random.choice([0,1]) == 1:
            self.full_name = name + " " + middle_name + " " + last_name + " " + last_name2
        else:
            self.full_name = name + " " + last_name + " " + last_name2
        # Address generation
        self.full_address = "BARRIO " + random.choice(self.addresses1) + " " * 2 + random.choice(self.addresses2)
        dept_nro = str(random.randint(1,20)) if random.choice([0,1]) == 0 else str(random.randint(1,20))+random.choice(self.depto_prefixes)
        self.dept_nro = "DEPTO: " + dept_nro + "    CIUDAD: SANTA CRUZ DE LA SIERRA"
        self.uv = "UV: "+str(self.random_with_leading_zeroes(4, 250))
        self.dist = "DIST: "+str(random.choice([1,2,3,4,5,6,7,8,9]))
        self.mza = "MZA: "+str(random.choice(["0003", "0001", "0002", "0004", "0006"]))
        self.section = "SECCION: "+str(random.choice([0,1]))

    def third_header(self):
        self.gauge_num = "MEDI" + self.random_with_leading_zeroes(4, 10000)
        self.meter_type = "Leído"
        self.category = f"DOMICILIARIA-PD-BT   01.001."
        self.location_code = f"{self.random_with_leading_zeroes(3, 100)}.{self.random_with_leading_zeroes(8, 10000)}.{self.random_with_leading_zeroes(4, 100)}"

    def historical_consumption(self):  
        # Parameters for consumption
        consumption_hist_factor_summer = [random.uniform(0, 0.2) for i in range(self.n)]
        consumption_hist_factor_winter = [random.uniform(-0.4, 0.05) for i in range(self.n)]
        self.consumption_rate = random.uniform(0.95, 1.34)
        summer_months = [2,3,4,5,6,7]
        
        # Current consumption
        consumption_current_amount = random.uniform(30, 1500)
        
        # Historial dates
        consumption_periods = [datetime.strftime(self.start_date - relativedelta(months=m), self.short_date_format) for m in range(self.n)]
        start_date_str = datetime.strftime(self.start_date, self.short_date_format)
        
        # Historical consumption
        consumption_hist_amounts_summer = [consumption_current_amount * (1 + factor) for factor in consumption_hist_factor_summer]
        consumption_hist_amounts_winter = [consumption_current_amount * (1 + factor) for factor in consumption_hist_factor_winter]
        self.consumption_hist_amounts = [amount_winter if i in summer_months else amount_summer for i, (amount_winter, amount_summer)\
                                         in enumerate(zip(consumption_hist_amounts_summer, consumption_hist_amounts_winter))]
        self.consumption_hist_kwh = [amount / self.consumption_rate for amount in self.consumption_hist_amounts]
        self.consumption_rate = f"{self.consumption_rate:.2f}"
    
        # Historial paid dates
        date = self.start_date - relativedelta(months=random.choice([0,1])) - timedelta(days=random.randint(2, 20))
        state_date_lst = []
        more_than_one_payment_counter = 0
        for period in range(13):
            more_than_one_payment = True if random.choice([0,1,2,3]) == 0 else False
            if not more_than_one_payment:
                date = self.start_date - relativedelta(months=period+more_than_one_payment_counter) - timedelta(days=random.randint(2, 16))
            else:
                more_than_one_payment_counter += 1
            state_date_lst.append(date)
            if more_than_one_payment_counter >= 3:
                more_than_one_payment_counter = 0
        self.cut_in_progress = True if random.choice([0,1,2]) == 1 else False
        two_months_due = True if random.choice([0,1]) == 1 else False
        self.state_date_lst_updated = []
        for i, date in enumerate(state_date_lst):
            if self.cut_in_progress:
                if i in [0,1]:
                    self.state_date_lst_updated.append("Impaga")
                elif i == 2:
                    self.state_date_lst_updated.append("VENCIDA")
                else:
                    self.state_date_lst_updated.append(datetime.strftime(date,self.long_date_format))
            else:
                if two_months_due:
                    if i in [0,1]:
                        self.state_date_lst_updated.append("Impaga")
                    else:
                        self.state_date_lst_updated.append(datetime.strftime(date,self.long_date_format))
                else:
                    if i == 0:
                        self.state_date_lst_updated.append("Impaga")
                    else:
                        self.state_date_lst_updated.append(datetime.strftime(date,self.long_date_format))
    
        # Formatting numbers
        consumption_hist_kwh_str = [f"{ele:.0f}" for ele in self.consumption_hist_kwh]
        consumption_hist_amounts_str = [f"{ele:.2f}" for ele in self.consumption_hist_amounts]
    
        # Generate historical consumption multiline text
        self.historical_consumption_entries = "\n".join([f"{consumption_periods[i]}"+\
                                              " "*(9 - len(consumption_hist_kwh_str[i]))+f"{consumption_hist_kwh_str[i]}"+\
                                              " "*(16-len(consumption_hist_amounts_str[i]))+ f"{consumption_hist_amounts_str[i]}"\
                                              + " "*(2) + f"{self.state_date_lst_updated[i]}" for i in range(self.n)])

        # Setting cut date
        self.cut_date = datetime.strftime(self.start_date + timedelta(days=random.randint(2,7)), self.standard_date_format)\
                if self.state_date_lst_updated[2] == "VENCIDA" else ""

    def fourth_header(self):
        base_consumption = random.randint(1000, 50000)
        self.previous_emision_date = self.start_date - relativedelta(months=1) + timedelta(days=random.randint(0,2))
        self.days_consumed = str((self.start_date - self.previous_emision_date).days)
        self.previous_emision_date = datetime.strftime(self.previous_emision_date, self.standard_date_format)
        self.actual = f"{base_consumption + self.consumption_hist_kwh[0]:.0f}"
        self.previous = f"{base_consumption + self.consumption_hist_kwh[1]:.0f}"
        self.consumption = f"{self.consumption_hist_kwh[0]:.0f}"
        self.acum_consumption = "0"
        self.total_consumption = self.consumption

    def details(self):
        concepts_lookup = {"Importe por energía": self.consumption_hist_amounts[0],
               "Benef. x T. Dignidad": -11.70,
               "Rest control calidad": -3.30,
               "Tasa AFCOOP": 0.5,
               "Cargo por reconexi?n": random.uniform(60, 90)}
    
        rand_2dn_entry = True if random.choice(range(10)) == 0 else False
        rand_3rd_entry = True if rand_2dn_entry else False
        rand_4th_entry = True if rand_2dn_entry and random.choice([0,1]) == 0  else False
        rand_5th_entry = True if self.state_date_lst_updated[0:3] == ['Impaga','Impaga','VENCIDA'] and random.choice([0,1,2,3]) == 0 else False
        concepts_mask = [True, rand_2dn_entry, rand_3rd_entry, rand_4th_entry, rand_5th_entry]
        self.concepts = [list(concepts_lookup.keys())[c] for c in range(5) if concepts_mask[c]]
        
        total = 0
        self.detail_entries = "\n".join([f"{concept}" + " " * (28 - len(concept)) + " " * (8 - len(f"{concepts_lookup[concept]:.2f}")) + \
                             f"{concepts_lookup[concept]:.2f}" for concept in self.concepts])
        self.total_amount_details = sum([concepts_lookup[concept] for concept in self.concepts])

    def municipal_rates(self):
        if "Benef. x T. Dignidad" in self.concepts:
            urban_cleaning = random.uniform(5,10)
            public_lighting = random.uniform(2,8)
        else:
            urban_cleaning = random.uniform(25,100)
            public_lighting = random.uniform(20,100)
        
        self.municipal_rates_entries = "Aseo Urbano" + " " * (25 - len(f"{urban_cleaning:.2f}")) + f"{urban_cleaning:.2f}\n" +\
                  "Alumbrado publico" + " " * (19 - len(f"{public_lighting:.2f}")) + f"{public_lighting:.2f}\n"
        self.total_amount_municipal_rates = urban_cleaning + public_lighting
        self.total_bill_amount = f"{self.total_amount_details + self.total_amount_municipal_rates:.2f}"
        self.total_amount_details = f"{self.total_amount_details:.2f}"
        self.total_amount_municipal_rates = f"{self.total_amount_municipal_rates:.2f}"

    def print_image(self, image_index):
        rand_v= random.randint(-5,10)
        rand_h = random.randint(-30,30)
        font = ImageFont.truetype("fonts/CONSOLA.TTF",55)
        font_bold = ImageFont.truetype("fonts/CONSOLAB.TTF",70)
        img = Image.open("templates/utility_bill_1_with_cut_date.png") if self.cut_in_progress else Image.open("templates/utility_bill_1.png")
        draw = ImageDraw.Draw(img)
        # Populate header 1
        formated_texts = [self.month_bill_literal, self.start_date_str, self.due_date, 
                          self.next_measurement_date, self.next_measurement_date, # Header 1
                         self.full_name, self.full_address, self.uv, self.dist, self.dept_nro, self.mza, self.section, # Header 2
                         self.gauge_num, self.meter_type, self.category, self.location_code, # Header 3
                         self.start_date_str, self.previous_emision_date, self.days_consumed, self.actual, self.previous, self.consumption_rate,
                         self.consumption, self.acum_consumption, self.total_consumption, # Header 4
                         self.historical_consumption_entries, self.detail_entries, self.municipal_rates_entries, # Entries data
                         self.total_bill_amount, self.cut_date,
                         self.total_amount_details, self.total_amount_municipal_rates]
        v_positions = [250,250,250,250,250,
		       390,390,390,390,462,462,462,
		       590,590,590,590,
			800, 800, 800, 800, 800, 800, 800, 800, 800,
                      965, 1060, 1060, 1810, 1890,
                      1660, 1660]
        h_positions = [760, 1380, 1980, 2730, 3330, 
                       300, 1650, 2990, 3350, 1670, 3050, 3400, 
		       320, 1010, 2260, 3190,
		       380, 830, 1360, 1800, 2240, 2665, 3150, 3620, 4050,
		       320, 1738, 3038, 3900, 1190, 
                       2700, 4040]
        for i in range(len(formated_texts)):
            draw.text((h_positions[i] + rand_h, v_positions[i] + rand_v),formated_texts[i],(0,0,0),font=font, spacing=15)
        fixed_code = f"{random.randint(100000,999999)}"
        draw.text((3950 + rand_h, 170 + rand_v),fixed_code,(0,0,0),font=font_bold)
        max_resolution = (1900, 1200)
        img.thumbnail(max_resolution, Image.LANCZOS)
        Path("data/1/").mkdir(parents=True, exist_ok=True)
        img.save(f'data/1/{image_index}.png')


class generator_bill_2():
    def __init__(self, names, middle_names, last_names, addresses1, addresses2, depto_prefixes):
        self.short_date_format = "%Y-%m"
        self.short_date_format_2 = "%m/%Y"
        self.standard_date_format = "%d/%m/%y"
        self.long_date_format = "%d/%m/%Y"
        self.n = 12
        self.names = names
        self.middle_names = middle_names
        self.last_names = last_names
        self.addresses1 = addresses1
        self.addresses2 = addresses2
        self.depto_prefixes = depto_prefixes
        self.random_with_leading_zeroes = lambda total_len, upper_limit: "0" * (total_len - len(str(random.randint(1, upper_limit))))\
                                            + str(random.randint(1, upper_limit))

    def first_header(self):
        name = self.names[random.randint(0, len(self.names)-1)]
        middle_name = self.middle_names[random.randint(0, len(self.middle_names)-1)]
        last_name = self.last_names[random.randint(0, len(self.last_names)-1)]
        last_name2 = [name for name in self.last_names if name != last_name][random.randint(0, len(self.last_names)-2)]
        if random.choice([0,1]) == 1:
            self.full_name = name + " " + middle_name + " " + last_name + " " + last_name2
        else:
            self.full_name = name + " " + last_name + " " + last_name2
        self.category = str(random.choice([1,2,3]))
        day_bill = random.choice(range(29)) + 1
        month_bill = random.choice([11,10,9])
        self.start_date = datetime(2024, month_bill, day_bill)
        self.start_date_str = self.start_date.strftime(self.long_date_format)
        self.due_date = self.start_date + relativedelta(months=1)
        self.due_date_str = self.due_date.strftime(self.long_date_format)
        self.street_name = "B. " + random.choice(self.addresses1) + " " * 2 + random.choice(self.addresses2)
        dept_nro = str(random.randint(1,20)) if random.choice([0,1]) == 0 else str(random.randint(1,20))+random.choice(self.depto_prefixes)
        self.dept_nro = "No " + dept_nro
        self.uv = "UV "+str(self.random_with_leading_zeroes(3, 250))
        self.mza = "MZ "+str(random.choice(["0003", "0001", "0002", "0004", "0006"]))
        self.dist = str(random.choice([1,2,3,4,5,6,7,8,9]))
        self.full_address = f"{self.dept_nro}  {self.uv} {self.mza} {self.street_name}"
        self.full_address = self.full_address[:-1]
        self.month_year = self.start_date.strftime(self.short_date_format_2)

    def historical_consumption(self):  
        # Parameters for consumption
        consumption_hist_factor_summer = [random.uniform(0.04, 0.3) for i in range(self.n)]
        consumption_hist_factor_winter = [random.uniform(-0.3, 0.05) for i in range(self.n)]
        self.consumption_rate = random.uniform(6.0, 6.5)
        summer_months = [2,3,4,5,6,7]
        
        # Current consumption
        consumption_current_amount = random.uniform(5, 40)
        
        # Historial dates
        consumption_periods = [datetime.strftime(self.start_date - relativedelta(months=m), self.short_date_format) for m in range(self.n)]
        
        # Historical consumption
        consumption_hist_amounts_summer = [consumption_current_amount * (1 + factor) for factor in consumption_hist_factor_summer]
        consumption_hist_amounts_winter = [consumption_current_amount * (1 + factor) for factor in consumption_hist_factor_winter]
        self.consumption_hist_amounts = [amount_winter if i in summer_months else amount_summer for i, (amount_winter, amount_summer)\
                                         in enumerate(zip(consumption_hist_amounts_summer, consumption_hist_amounts_winter))]
        self.consumption_hist_kwh = [amount / self.consumption_rate for amount in self.consumption_hist_amounts]
        self.consumption_rate = f"{self.consumption_rate:.2f}"
    
        # Historial paid dates
        date = self.start_date - relativedelta(months=random.choice([0,1])) - timedelta(days=random.randint(2, 20))
        state_date_lst = []
        more_than_one_payment_counter = 0
        state_date_lst = ["IMPAGA" for i in range(random.randint(0, self.n))]
        state_date_lst_updated = ["IMPAGA" if i < len(state_date_lst) else "" for i in range(self.n)]
    
        # Formatting numbers
        consumption_hist_kwh_str = [f"{ele:.0f}" for ele in self.consumption_hist_kwh]
        consumption_hist_amounts_str = [f"{ele:.2f}" for ele in self.consumption_hist_amounts]
    
        # Generate historical consumption multiline text
        self.historical_consumption_entries = "\n".join([f"{consumption_periods[i]}"+\
                                              " "*(9 - len(consumption_hist_kwh_str[i]))+f"{consumption_hist_kwh_str[i]}"+\
                                              " "*(18-len(consumption_hist_amounts_str[i]))+ f"{consumption_hist_amounts_str[i]}"\
                                              + " "*(9) + f"{state_date_lst_updated[i]}" for i in range(self.n)])

        # Setting cut date
        self.cut_date = datetime.strftime(self.start_date + timedelta(days=random.randint(2,7)), self.standard_date_format)\
                if state_date_lst_updated[2] == "IMPAGA" else ""
        self.cut = "SI" if self.cut_date != "" else "NO"
        self.cut_message = "SI PAGO, IGNORE ESTE MENSAJE" if self.cut == "SI" else "" 
        
        # Summing unpaid consumption
        self.due_debt = f"{sum([amount for i, amount in enumerate(self.consumption_hist_amounts) if state_date_lst_updated[i] == "IMPAGA" and i != 0]):.2f}"
        self.due_debt_including_actual = f"{sum([amount for i, amount in enumerate(self.consumption_hist_amounts) if state_date_lst_updated[i] == "IMPAGA"]):.2f}"

        # Summing months of unpaid consumption
        self.due_months = str(sum([1 for i, _ in enumerate(self.consumption_hist_amounts) if state_date_lst_updated[i] == "IMPAGA" and i != 0]))
        
    def second_header(self):
        base_consumption = random.randint(500, 5000)
        self.previous_emision_date = self.start_date - relativedelta(months=1) + timedelta(days=random.randint(0,2))
        self.previous_emision_date = datetime.strftime(self.previous_emision_date, self.long_date_format)
        self.actual = f"{base_consumption + self.consumption_hist_kwh[0]:.0f}"
        self.previous = f"{base_consumption + self.consumption_hist_kwh[1]:.0f}"
        self.consumption = f"{self.consumption_hist_kwh[0]:.0f}"
        self.consumption_prev_month = f"{self.consumption_hist_kwh[1]:.0f}"

    def details(self):
        concepts_lookup = {"SERV. AGUA POTABL": self.consumption_hist_amounts[0],
               "SERV. ALC. SANITA": self.consumption_hist_amounts[0] / random.uniform(2.5, 3),
               "APORTE DE SOCIO": self.consumption_hist_amounts[0] / 6}
        self.detail_entries = "\n".join([f"{i}"+"   "+  f"{concept}" + " " * (22 - len(concept)) + f"{amount:.2f}" for i, (concept,  amount) in enumerate(concepts_lookup.items(), start=1)])
        self.total_amount_details = f"{sum(concepts_lookup.values()):.2f}"

    def print_image(self, image_index):
        rand_v= random.randint(-5,10)
        rand_h = random.randint(-30,30)
        font = ImageFont.truetype("fonts/CONSOLA.TTF",55)
        font_bold = ImageFont.truetype("fonts/CONSOLAB.TTF",75)
        font_small = ImageFont.truetype("fonts/CONSOLA.TTF",35)
        img = Image.open("templates/utility_bill_2.png")
        draw = ImageDraw.Draw(img)
        formated_texts = [self.full_name, self.category, self.start_date_str, self.full_address, self.month_year, self.due_date_str, self.dist, self.start_date_str, self.actual, self.consumption,
                  self.consumption_rate, self.previous_emision_date, self.previous, self.consumption_prev_month, self.consumption_rate, self.due_debt, self.due_months, self.cut,
                  self.historical_consumption_entries, self.detail_entries, self.due_debt_including_actual, self.total_amount_details]
        h_positions = [150, 3170, 3650, 210, 3130, 3650, 650, 285, 930, 1430, 1720, 285, 930,1430,1720,2400,3050,3750,165, 1800, 1500, 2550]
        v_positions = [470, 460, 460, 640, 660, 660, 730, 908, 908, 908, 908, 980, 980,980,980,930, 930, 900,1230, 1230, 1970, 1970]
        for i in range(len(formated_texts)):
            draw.text((h_positions[i] + rand_h, v_positions[i] + rand_v),formated_texts[i],(0,0,0),font=font, spacing=15)
        draw.text((3700 + rand_h, 215 + rand_v), str(random.randint(100000, 99999999)),(0,0,0),font=font_bold, spacing=15)
        draw.text((3550 + rand_h, 970 + rand_v), self.cut_message,(0,0,0),font=font_small, spacing=15)
        max_resolution = (1900, 1200)
        img.thumbnail(max_resolution, Image.LANCZOS)
        Path("data/2/").mkdir(parents=True, exist_ok=True)
        img.save(f'data/2/{image_index}.png')