import warnings
warnings.filterwarnings("ignore")
from bs4 import BeautifulSoup
from datetime import datetime
import urllib3
http = urllib3.connection_from_url("https://uci.campusdish.com",cert_reqs='CERT_NONE')



PIPPINS = 4832
ANTEATERY = 3056
BREAKFAST = 49
BRUNCH = 2651
LUNCH = 106
DINNER = 107
LATENIGHT = 108
code_to_name = {PIPPINS:"Pippins",ANTEATERY:"Anteatery", BREAKFAST:"Breakfast",
BRUNCH:"Brunch",LUNCH:"Lunch",DINNER:"Dinner",LATENIGHT:"Late Night"}
datestr = "%m/%d/%Y"
url = "/api/menus/GetMenu?locationId={}&mode=Daily&periodId={}&date={}"

pippins_section_skip = ["Deli","Desserts","Grill","Salad Bar"]
anteatery_section_skip = ["Dessert","Grill","Produce Market"]

item_skip = ['Classic Cheese Pizza', 'Pepperoni Pizza','Signature Chips', 
'Banana Peppers', 'Green Leaf Lettuce', 'Sliced Red Onions', 'Sliced Tomatoes', 
'Deli Tortilla Wrap', 'Fresh Baked Ciabatta', 'White Bread', 'Whole Wheat Bread', 
'Cheddar Cheese', 'Chunky Chicken Salad', 'Ham', 'Pepper Jack Cheese', 'Provolone Cheese', 
'Salami', 'Swiss Cheese', 'Turkey Breast', 'Chipotle Mayonnaise', 'Dijon Mustard', 'Hummus',
 'Mayonnaise', 'Pesto Mayonnaise', 'Yellow Mustard','Diced Onions', 'Fresh Garlic', 
 'Sliced Mixed Bell Peppers', 'Olive Oil Blend', "Broccoli", "Sliced Mushrooms"]
#sections to apply the item skip to
section_item_skip = ["Saute","Pizza", "Deli", "Oven"]
for meal in [LUNCH,DINNER,LATENIGHT]:
	print(code_to_name[meal])
	for place in [ANTEATERY, PIPPINS]:
		print(code_to_name[place])
		formatted=url.format(place, meal, datetime.strftime(datetime.now(),datestr))
		text = http.request("GET",formatted).data
		soup = BeautifulSoup(text, 'html.parser')
		for section in soup.find_all("div",{"class":"menu__station"}):
			section_name = (section.find("h2",{"class":"location-headers section-subtitle"}).text)
			if place==ANTEATERY and section_name not in anteatery_section_skip or place==PIPPINS and section_name not in pippins_section_skip:
				items = [x.text for x in section.findAll("a",{"class":"viewItem"})]
				if section_name in section_item_skip:
					items = list(filter(lambda x: x not in item_skip,items))
				if items:
					items = ", ".join(items)
					print(section_name,items)
