import os
import requests
import pandas as pd
from random import randint
from django.db.models import Q
from .models import Account
api_key = os.environ.get('IEX_API_KEYS')
TEST_OR_PROD = 'sandbox'

def make_position_request(tickers):

    data = []
    for x in tickers:
        response = requests.get("https://{}.iexapis.com/stable/stock/{}/quote?displayPercent=true&token={}".format(TEST_OR_PROD, x, api_key)).json()
        data.append(response)
    
    df = pd.DataFrame(data)
    return df 

def create_sector_information(tickers):

    data = []
    for x in tickers:
        response = requests.get("https://{}.iexapis.com/stable/stock/{}/company?token={}".format(TEST_OR_PROD, x, api_key)).json()
        data.append(response)
    
    df = pd.DataFrame(data)
    sector_series = df['sector'].value_counts()
    sector_labels = sector_series.index.to_list()
    sector_data = sector_series.tolist()

    return sector_labels, sector_data

def create_stock_table(tickers, df):

    iex_df = make_position_request(tickers)

    df_concat = pd.concat([df, iex_df], axis = 1)

    df_concat['Current_Value_Adjusted_Shares'] = round(df_concat['latestPrice'] * df_concat['num_shares'], 2)
    df_concat['Total_Initial_Cost'] = round(df_concat['purchase_price'] * df_concat['num_shares'],2)
    df_concat['Change_Adjusted_Shares'] = round(df_concat['change'] * df_concat['num_shares'], 2)
    df_concat['Previous_Close_Adjusted_Shares'] = round(df_concat['previousClose'] * df_concat['num_shares'], 2)
    df_concat['Security_Overall_Gain'] = round(df_concat['Current_Value_Adjusted_Shares'] - df_concat['Total_Initial_Cost'], 2)
    df_concat['Security_Overall_Return_Percentage'] = round((df_concat['Security_Overall_Gain'] / df_concat['Total_Initial_Cost']) * 100, 2)

    df_subset = df_concat[['ticker_symbol', 'companyName', 'latestPrice', 'changePercent', 'change', 'num_shares', 'purchase_price', 'Total_Initial_Cost', 'Current_Value_Adjusted_Shares', 'Security_Overall_Gain', 'Change_Adjusted_Shares', 'Security_Overall_Return_Percentage']]

    total = df_concat.sum()
    
    return df_subset, total

def chart_colour_picker (num_colours):

    pool = ['#FFBE0B', '#FB5607', '#FF006E', '#8338EC', '#3A86FF', '#A2FAA3', '#92C9B1', '#4F759B', '#5D5179', '#571F4E', '#031A6B', '#033860', '#087CA7', '#004385', '#05B2DC', '#52489C', '#4062BB', '#59C3C3', '#EBEBEB', '#F45B69']
    colour_palette = []
    for x in range(num_colours):
        s = randint(0, len(pool)-1)
        colour_palette.append(pool.pop(s))
    
    return colour_palette

def portfolio_value_chart(selected_range, tickers, share_count):
    
    count = 0
    for x in tickers:
        response = requests.get("https://{}.iexapis.com/stable/stock/{}/chart/{}?chartCloseOnly=true&token={}".format(TEST_OR_PROD, x, selected_range, api_key)).json()
        df = pd.json_normalize(response)
        df[f'Price_Adjusted_Shares_{x}'] = (df['close'] * share_count[count])

        if count == 0:
            df_main = df
        else:
            df_main = pd.merge(df_main, df, how = "outer", on="date")

        count += 1

    df_main = df_main.fillna(0)
    df_main = df_main.sort_values(by='date')

    interval = int((df_main.shape[0] ) / 15)

    date_val = df_main['date'].tolist()
    date_val = date_val[0::interval]

    data_arr = []
    for x in tickers:
        temp = df_main[f'Price_Adjusted_Shares_{x}'].tolist()
        temp = temp[0::interval]
        data_arr.append(temp)

    return date_val, data_arr

def get_all_user_account_security(current_user):
    current_user_accounts = Account.objects.filter(owner = current_user)

    query = Q(account = current_user_accounts.first())

    if current_user_accounts.count() > 1:
        for e in current_user_accounts:
            query |= Q(account = e)

    return query
