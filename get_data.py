import pandas as pd
import requests


def make_national_timeseries_data_csv():
    r = requests.get("https://api.covid19india.org/data.json").json()
    df = pd.DataFrame(r['cases_time_series'])
    df.to_csv("data/covid_national_timeseries.csv", index=False, sep=",")


def make_raw_gender_age_data_csv():
    r1 = requests.get("https://api.covid19india.org/raw_data1.json").json()
    r2 = requests.get("https://api.covid19india.org/raw_data2.json").json()
    r3 = requests.get("https://api.covid19india.org/raw_data3.json").json()

    df1 = pd.DataFrame(r1['raw_data'])[['gender', 'agebracket']]
    df2 = pd.DataFrame(r2['raw_data'])[['gender', 'agebracket']]
    df3 = pd.DataFrame(r3['raw_data'])[['gender', 'agebracket']]

    raw_df = pd.concat([df1,df2,df3])
    raw_df = raw_df.rename(columns={"agebracket": "age"})
    raw_df.to_csv("data/covid_raw_gender_age_full.csv")



if __name__=="__main__":
    make_national_timeseries_data_csv()
    make_raw_gender_age_data_csv()