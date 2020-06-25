import requests
import pandas as pd

# Import list of Italian provinces (you can manipulate this part in order to
# search for other cities)
province = pd.read_csv("province-sigle.csv", encoding = "ISO-8859-1",
                       header = None)[[0]].values
prov = list(el[0] for el in province)

# Insert the list of yy/mm you want to scrap, if you want to have many years
# you can also use two lists one for years and one for the months
year_months = ["2019/Novembre","2019/Dicembre", "2020/Gennaio",
            "2020/Febbraio", "2020/Marzo", "2020/Aprile", "2020/Maggio",
            "2020/Giugno"]
            # Other italian names for months:
            # "Luglio", "Agosto", "Settembre", "Ottobre"

# Function to retrieve url for csv download
def get_historic_weather(city, ym = True, year = "2020/Gennaio", month = None):
    base_url = "https://www.ilmeteo.it/portale/archivio-meteo/"
    if ym == True:
        URL = base_url + str(city) + "/" + str(year) + "?format=csv"
    else:
        URL = base_url + str(city) + "/" + str(year) + "/" + str(month) + \
        "?format=csv"
    return URL

tabella = ""
b = False
city = True
# Loop for each province
for p in prov:
    city = True
    # Loop for each combination yy/mm. Use two loops if you want the two
    # separate lists
    for ym in year_months:
        # Do the request only if the city has a csv download or it is the first
        #  attempt
        if city == True:
            # Request the csv download. Pass province and yy/mm to get the url.
            # If using two lists pass get_historic_weather(p, ym = False,
            #                                              year = y, month = m)
            url = get_historic_weather(p, year = ym)
            tmp = requests.get(url, allow_redirects=True)
            # Check if the csv file was found
            if (str(tmp.content[0:1]) != "b'<'"):
                if b == False:
                    tabella = tmp.content
                    b = True
                else:
                    # If it is not the first csv to unpack you need to remove
                    # the headers
                    tabella += tmp.content[182:]
            else:
                city= False

# Save csv file
open('meteoItalianProvinces.csv', 'wb').write(tabella)