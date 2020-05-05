import pandas as pd
import requests


def make_national_timeseries_data_csv():
    r = requests.get("https://api.covid19india.org/data.json").json()
    df = pd.DataFrame(r['cases_time_series'])
    df.to_csv("data/covid_national_timeseries.csv", index=False, sep=",")


def statewise_total_cases_csv():
    r = requests.get("https://api.covid19india.org/data.json").json()
    df = pd.DataFrame(r['statewise'])
    df.to_csv("data/covid_statewise_total_cases.csv", index=False, sep=",")


def make_raw_gender_age_data_csv():
    r1 = requests.get("https://api.covid19india.org/raw_data1.json").json()
    r2 = requests.get("https://api.covid19india.org/raw_data2.json").json()
    r3 = requests.get("https://api.covid19india.org/raw_data3.json").json()

    df1 = pd.DataFrame(r1['raw_data'])[['gender', 'agebracket']]
    df2 = pd.DataFrame(r2['raw_data'])[['gender', 'agebracket']]
    df3 = pd.DataFrame(r3['raw_data'])[['gender', 'agebracket']]

    raw_df = pd.concat([df1,df2,df3])
    raw_df = raw_df.rename(columns={"agebracket": "age"})
    raw_df.to_csv("data/covid_raw_gender_age_full.csv", index=False)


def daily_statewise_and_cumulative_csv():
    integer_columns = ['an', 'ap', 'ar', 'as', 'br', 'ch', 'ct', 'dd', 'dl', 'dn',
       'ga', 'gj', 'hp', 'hr', 'jh', 'jk', 'ka', 'kl', 'la', 'ld', 'mh', 'ml',
       'mn', 'mp', 'mz', 'nl', 'or', 'pb', 'py', 'rj', 'sk', 'tg',
       'tn', 'tr', 'tt', 'up', 'ut', 'wb']
    r = requests.get("https://api.covid19india.org/states_daily.json").json()
    df = pd.DataFrame(r['states_daily'])
    df['mp'] = 6
    confirmed = df[df['status'].str.lower() == "confirmed"]
    recovered = df[df['status'].str.lower()== "recovered"]
    deceased = df[df['status'].str.lower() == "deceased"]
    confirmed[integer_columns] = confirmed[integer_columns].astype(int)
    recovered[integer_columns] = recovered[integer_columns].astype(int)
    deceased[integer_columns] = deceased[integer_columns].astype(int)

    confirmed.to_csv("data/daily/confirmed.csv", index=False)
    deceased.to_csv("data/daily/deceased.csv", index=False)
    recovered.to_csv("data/daily/recovered.csv", index=False)

    confirmed[integer_columns] = confirmed[integer_columns].cumsum()
    recovered[integer_columns] = recovered[integer_columns].cumsum()
    deceased[integer_columns] = deceased[integer_columns].cumsum()

    confirmed.to_csv("data/cumulative/confirmed.csv", index=False)
    recovered.to_csv("data/cumulative/recovered.csv", index=False)
    deceased.to_csv("data/cumulative/deceased.csv", index=False)

    

if __name__=="__main__":
    # make_national_timeseries_data_csv()
    # make_raw_gender_age_data_csv()
    # statewise_total_cases_csv()
    daily_statewise_and_cumulative_csv()