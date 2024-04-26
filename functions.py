import datetime
import yfinance as yf

def get_stock_data(ticker,start_date,end_date):
    print(f'Getting stock data for {ticker}')

    df = yf.download(ticker,
                    #  start=start_date,
                    #  end=end_date
                     )[['Open', 'High', 'Low', 'Close', 'Volume']] # download data from yahoo
    df['Volume'] = df['Volume'].astype(float)
    print(df.dtypes)

    # Convert df to correct format for Lightweight Charts
    df = df.reset_index()
    df.columns = ['time','open','high','low','close','volume']                  # rename columns
    df['time'] = df['time'].dt.strftime('%Y-%m-%d')                             # Date to string
    df.rename(columns={'Volume': 'Values'}, inplace=True)                
    df = df.fillna(0) # Replace NaN with zeros

    return df

def adddaystodatestring(start_date,days):
    if start_date:
        date_1 = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = date_1 + datetime.timedelta(days)
        end_date_str = end_date.strftime("%Y-%m-%d")  # Convert back to string
        return end_date_str
    else:
        return

def convertdatestring(sDate):
    if sDate:
        return datetime.datetime.strptime(sDate, '%d/%m/%Y').strftime('%Y-%m-%d')
    else:
        return