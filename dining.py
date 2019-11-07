
import warnings
warnings.filterwarnings("ignore")
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import urllib3
http = urllib3.connection_from_url("https://uci.campusdish.com",cert_reqs='CERT_NONE')



PIPPINS = 3314
ANTEATERY = 3056
BREAKFAST = 49
BRUNCH = 2651
LUNCH = 106
DINNER = 107
LATENIGHT = 108
code_to_name = {PIPPINS:"Brandywine",ANTEATERY:"Anteatery", BREAKFAST:"Breakfast",
BRUNCH:"Brunch",LUNCH:"Lunch",DINNER:"Dinner",LATENIGHT:"Late Night"}
datestr = "%m/%d/%Y"
datetimestr = "%m/%d/%Y %H:%M:%S"

url = "/api/menus/GetMenu?locationId={}&mode=Daily&periodId={}&date={}"

pippins_section_skip = ["Honeycakes/Bakery","Ember/Grill","The Farm Stand/ Deli", "The Farm Stand/ Salad Bar"]
anteatery_section_skip = ["Dessert","Grill","Produce Market"]

item_skip = ['Classic Cheese Pizza', 'Pepperoni Pizza','Signature Chips',
'Banana Peppers', 'Green Leaf Lettuce', 'Sliced Red Onions', 'Sliced Tomatoes',
'Deli Tortilla Wrap', 'Fresh Baked Ciabatta', 'White Bread', 'Whole Wheat Bread',
'Cheddar Cheese', 'Chunky Chicken Salad', 'Ham', 'Pepper Jack Cheese', 'Provolone Cheese',
'Salami', 'Swiss Cheese', 'Turkey Breast', 'Chipotle Mayonnaise', 'Dijon Mustard', 'Hummus',
 'Mayonnaise', 'Pesto Mayonnaise', 'Yellow Mustard','Diced Onions', 'Fresh Garlic',
 'Sliced Mixed Bell Peppers', 'Olive Oil Blend', "Broccoli", "Sliced Mushrooms"]
#sections to apply the item skip to
section_item_skip = ["Saute", "Pizza", "Deli", "Oven"]

def main():
    lines = []
    for day in [datetime.now(),datetime.now()+timedelta(days=1)]:
        today = datetime.strftime(day,datestr)
        now = datetime.strftime(day,datetimestr)
        lines += [now]
        for meal in [LUNCH,DINNER,LATENIGHT]:
            lines +=["-------------------------",code_to_name[meal]]
            for place in [ANTEATERY, PIPPINS]:
                lines += ["\n",code_to_name[place]]
                formatted=url.format(place, meal, today)
                text = http.request("GET",formatted).data
                soup = BeautifulSoup(text, 'html.parser')
                for section in soup.find_all("div",{"class":"menu__station"}):
                    section_name = section.find("h2",{"class":"location-headers section-subtitle"})
                    if section_name:
                        section_name = (section_name.text)
                        if place==ANTEATERY and section_name not in anteatery_section_skip or place==PIPPINS and section_name not in pippins_section_skip:
                            items = [x.text for x in section.findAll("a",{"class":"viewItem"})]
                            if section_name in section_item_skip:
                                items = list(filter(lambda x: x not in item_skip,items))
                            if items:
                                items = ", ".join(items)
                                lines +=[section_name+": "+items]
    return "\n".join(lines)

res = main()
with open("/home/jamesal1/public_html/dining.txt","w") as f:
    f.write(res)

