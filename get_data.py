import pandas as pd
import requests
import time
import os

pd.options.mode.chained_assignment = None 


def make_national_timeseries_data_csv():
    """
    National data, with daily confirmed, deceased and recovered counts and
    total number of confirmed, deceased and recovered count upto that day.
    """
    r = requests.get("https://api.covid19india.org/data.json").json()
    df = pd.DataFrame(r['cases_time_series'])
    df.to_csv("data/covid_national_timeseries.csv", index=False, sep=",")


def statewise_total_cases_csv():
    """
    Table data for India.
    Statewise total confirmed, deceased and recovered counts.
    """
    r = requests.get("https://api.covid19india.org/data.json").json()
    df = pd.DataFrame(r['statewise'])
    df.to_csv("data/covid_statewise_total_cases.csv", index=False, sep=",")


def make_raw_gender_age_data_csv():
    """
    Raw patient level and district level data. Only extracting and saving
    the age and gender of few patients.
    """
    list_of_dataframes = list()
    url = lambda x: f"https://api.covid19india.org/raw_data{x}.json"
    for i in range(1, 20):
        r = requests.get(url(i)).json()
        print(f"GET: {url(i)}")
        df = pd.DataFrame(r['raw_data'])[['gender', 'agebracket']]
        list_of_dataframes.append(df)
    # r1 = requests.get("https://api.covid19india.org/raw_data1.json").json()
    # r2 = requests.get("https://api.covid19india.org/raw_data2.json").json()
    # r3 = requests.get("https://api.covid19india.org/raw_data3.json").json()
    # r4 = requests.get("https://api.covid19india.org/raw_data4.json").json()
    # r5 = requests.get("https://api.covid19india.org/raw_data5.json").json()
    # r6 = requests.get("https://api.covid19india.org/raw_data6.json").json()
    # r7 = requests.get("https://api.covid19india.org/raw_data7.json").json()
    # r8 = requests.get("https://api.covid19india.org/raw_data8.json").json()
    # r9 = requests.get("https://api.covid19india.org/raw_data9.json").json()
    # r10 = requests.get("https://api.covid19india.org/raw_data10.json").json()
    # r11 = requests.get("https://api.covid19india.org/raw_data11.json").json()
    # r12 = requests.get("https://api.covid19india.org/raw_data12.json").json()



    # df1 = pd.DataFrame(r1['raw_data'])[['gender', 'agebracket']]
    # df2 = pd.DataFrame(r2['raw_data'])[['gender', 'agebracket']]
    # df3 = pd.DataFrame(r3['raw_data'])[['gender', 'agebracket']]
    # df4 = pd.DataFrame(r4['raw_data'])[['gender', 'agebracket']]
    # df5 = pd.DataFrame(r5['raw_data'])[['gender', 'agebracket']]
    # df6 = pd.DataFrame(r6['raw_data'])[['gender', 'agebracket']]
    # df7 = pd.DataFrame(r7['raw_data'])[['gender', 'agebracket']]
    # df8 = pd.DataFrame(r8['raw_data'])[['gender', 'agebracket']]
    # df9 = pd.DataFrame(r9['raw_data'])[['gender', 'agebracket']]
    # df10 = pd.DataFrame(r10['raw_data'])[['gender', 'agebracket']]
    # df11 = pd.DataFrame(r11['raw_data'])[['gender', 'agebracket']]
    # df12 = pd.DataFrame(r12['raw_data'])[['gender', 'agebracket']]



    raw_df = pd.concat(list_of_dataframes)
    raw_df = raw_df.rename(columns={"agebracket": "age"})
    raw_df.to_csv("data/covid_raw_gender_age_full.csv", index=False)


def daily_statewise_and_cumulative_csv():
    """
    State data, with daily confirmed, deceased and recovered counts and
    total number of confirmed, deceased and recovered count upto that day.
    """
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

def world_timeline_data():
    """
    Time Series data for each country for line plot.
    API: 
    """
    r=requests.get("https://thevirustracker.com/timeline/map-data.json").json()
    df = pd.DataFrame(r['data'])
    df['date'] = df['date'].astype('datetime64[ns]')
    df = df.sort_values(by=['date'])
    df.rename(columns={"cases": "confirmed", "deaths": "deceased"}, inplace=True)
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x if bool(x) else 0)
    df['confirmed'] = df['confirmed'].astype(int)
    df['deceased'] = df['deceased'].astype(int)
    df['recovered'] = df['recovered'].astype(int)

    df.to_csv("data/COVID_Global_Timeseries.csv", index=False)

    
def countrywise_total_data():
    """
    Data to make a Table with Each countries totals.
    Contains totals upto that day and new cases on that day. 
    """
    try:
        r = requests.get("https://api.thevirustracker.com/free-api?countryTotals=ALL").json()
    except Exception as e:
        print("An error occurred in countrywise total data")
        print(str(e))
        return False
    data_dict = r['countryitems'][0].copy()
    data_dict['stat']
    del data_dict['stat']
    final = dict(
    country = list(),
    code = list(),
    confirmed = list(),
    active = list(),
    recovered = list(),
    deaths = list(),
    cases_today = list(),
    deaths_today = list(),
    serious = list()
    )
    for k, v in data_dict.items():
        final['country'].append(v['title'])
        final['code'] .append(v['code'])
        final['confirmed'].append(v['total_cases'])
        final['active'].append(v['total_active_cases'])
        final['recovered'].append(v['total_recovered'])
        final['deaths'].append(v['total_deaths'])
        final['cases_today'].append(v['total_new_cases_today'])
        final['deaths_today'].append(v['total_new_deaths_today'])
        final['serious'].append(v['total_serious_cases'])
    
    df = pd.DataFrame(final)

    df_top_6 = df.sort_values('confirmed', ascending=False).iloc[:6]
    country_codes = df_top_6['code'].tolist()
    make_top_6_country_data(country_codes)

    obj = dict(df.sum())
    df = df.append({
        "country": "World",
        "code": "W",
        "confirmed": obj['confirmed'],
        "active": obj['active'],
        "recovered": obj['recovered'],
        "deaths": obj['deaths'],
        "cases_today": obj['cases_today'],
        "deaths_today": obj['deaths_today'],
        "serious": obj['serious']
    }, ignore_index=True)
    df.to_csv("data/COVID_countrywise_total_data.csv", index=False)




def make_top_6_country_data(country_codes):
    base_url = "https://api.thevirustracker.com/free-api?countryTimeline="
    count = 1
    for code in country_codes:
        url = base_url + code
        try:
            r = requests.get(url).json()
        except Exception as e:
            print("Make top 6 data failed. Check TVT API")
            print(f"An error occurred: {str(e)}")
            return False
        # print(r.keys())
        # print(r)
        df = pd.DataFrame(r['timelineitems'][0]).T
        df = df.reset_index()
        df = df.rename(columns={"index": "date"})
        df.drop(df.tail(1).index,inplace=True) 
        df['date'] = df['date'].astype('datetime64[ns]')
        df.iloc[:,1:]=df.iloc[:,1:].astype(int)   
        df['country'] = r['countrytimelinedata'][0]['info']['title']
        df['code'] = r['countrytimelinedata'][0]['info']['code']

        df["new_daily_cases"] = df['new_daily_cases'].apply(lambda x: 0 if x<0 else x)
        filepath = "data/top_6_timeseries/country_"+str(count)+".csv"
        df.to_csv(filepath, index=False)
        count= count+ 1

def parse_global_stats():
    """
    Daily count and total count stored in df
    """
    try:
        r = requests.get("https://api.thevirustracker.com/free-api?global=stats").json()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
    del r['results'][0]['source']
    df = pd.DataFrame(r['results'][0], index=[0])
    df.to_csv("data/globalstats.csv", index=False)


def execute_all():
    start = time.time()
    data_dir = 'data/'
    os.makedirs(data_dir, exist_ok=True)
    daily_dir = 'daily/'
    cumulative_dir = 'cumulative/'
    top6 = 'top_6_timeseries/'
    os.makedirs(os.path.join(data_dir, daily_dir), exist_ok=True)
    os.makedirs(os.path.join(data_dir, cumulative_dir), exist_ok=True)
    os.makedirs(os.path.join(data_dir, top6), exist_ok=True)

    print("Starting Data Collection: ")
    print("Gathering data from api.covid19india.org")
    print("*** make_national_timeseries_data_csv ***")
    make_national_timeseries_data_csv()
    print("*** make_raw_gender_age_data_csv ***")
    make_raw_gender_age_data_csv()
    print("*** statewise_total_cases_csv ***")
    statewise_total_cases_csv()
    print("*** daily_statewise_and_cumulative_csv ***")
    daily_statewise_and_cumulative_csv()
    print("Gathering data from thevirustracker.com")
    print("*** world_timeline_data ***")
    world_timeline_data()
    print("*** countrywise_total_data ***")
    countrywise_total_data()
    print("*** parse_global_stats ***")
    parse_global_stats()
    print("Completed in: ", time.time() - start)

if __name__=="__main__":
    execute_all()
    
