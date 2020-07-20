import pandas as pd
import numpy as np
import requests

# url = "https://covid-19-statistics.p.rapidapi.com/reports/total"

# querystring = {"date": "2020-07-18"}

# headers = {
#     'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com",
#     'x-rapidapi-key': "fe50ef6954msh39d259c6247a27bp1b8b89jsndf4254f2ec79"
# }

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)

raw = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/07-18-2020.csv"

df = pd.read_csv(raw)
df = df[df.ISO3 == "USA"]

print(df)
