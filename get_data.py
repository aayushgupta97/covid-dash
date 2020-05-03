import pandas as pd
import requests


def make_national_timeseries_data_csv():
    r = requests.get("https://api.covid19india.org/data.json").json()
    df = pd.DataFrame(r['cases_time_series'])
    df.to_csv("data/covid_national_timeseries.csv", index=False, sep=",")


if __name__=="__main__":
    make_national_timeseries_data_csv()