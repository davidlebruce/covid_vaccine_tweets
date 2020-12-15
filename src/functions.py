import pandas as pd
import twint
import nest_asyncio
nest_asyncio.apply()
import datetime
from dateutil.relativedelta import relativedelta

# scraping function
def twint_scrape(
    search,
    since=None,
    until=None,
    limit=None
):
    c = twint.Config()
    c.Search = search
    c.Lang = 'en'
    c.Since = since
    c.Until = until
    c.Limit = limit
    c.Pandas = True
    c.Hide_output = True
    
    twint.run.Search(c)
    
    df = twint.storage.panda.Tweets_df
    
    return df


# loop for scraping function
def search_loop(
    search,
    filename,
    limit=None
):
    
    # instantiate empty dataframe
    df = pd.DataFrame()
    
    for i in range(1,13):
        
        since = pd.datetime(2020,i,1).strftime('%Y-%m-%d')
        
        until = (pd.datetime(2020,i,1) + relativedelta(months=+1)).strftime('%Y-%m-%d')
        
        month_df = twint_scrape(
            search = search,
            since = since,
            until = until,
            limit = limit)
        
        df = pd.concat([df, month_df])
        del month_df
        df.reset_index(drop=True, inplace=True)
        df.to_csv(f'./data/{filename}.csv')
        
        # notifier
        print(f'{since} saved!')
        
    return df

#######################################################################################

# scraper with geolocation
def twint_loc_scrape(
    search,
    since=None,
    until=None,
    limit=None,
    city=None
):
    c = twint.Config()
    c.Search = search
    c.Lang = 'en'
    c.Since = since
    c.Until = until
    c.Limit = limit
    c.Pandas = True
    c.Hide_output = True
    c.Near = city
    
    twint.run.Search(c)
    
    df = twint.storage.panda.Tweets_df
    
    return df


# loop for scraping function
def search_loc_loop(
    search,
    city,
    filename,
    limit=None
):
    
    # instantiate empty dataframe
    df = pd.DataFrame()
    
    for i in range(1,13):
        
        since = pd.datetime(2020,i,1).strftime('%Y-%m-%d')
        
        until = (pd.datetime(2020,i,1) + relativedelta(months=+1)).strftime('%Y-%m-%d')
        
        month_df = twint_loc_scrape(
            search = search,
            since = since,
            until = until,
            limit = limit,
            city = city)
        
        df = pd.concat([df, month_df])
        del month_df
        df.reset_index(drop=True, inplace=True)
        df.to_csv(f'./data/{filename}.csv')
        
        # notifier
        print(f'{since} saved!')
        
    return df

#######################################################################################

# scraper with geolocation
def twint_scrape_3(
    search,
    since=None,
    until=None,
    limit=None,
    city=None
):
    c = twint.Config()
    c.Search = search
    c.Lang = 'en'
    c.Since = since
    c.Until = until
    c.Limit = limit
    c.Pandas = True
    c.Hide_output = True
    c.Near = city
    
    twint.run.Search(c)
    
    df = twint.storage.panda.Tweets_df
    
    return df


# loop for scraping function
def search_loop_3(
    search,
    city,
    filename,
    limit=None
):
    
    # instantiate empty dataframe
    df = pd.DataFrame()
    for j in range(2010,2021):
        for i in range(1,13):

            since = pd.datetime(j,i,1).strftime('%Y-%m-%d')

            until = (pd.datetime(j,i,1) + relativedelta(months=+1)).strftime('%Y-%m-%d')

            month_df = twint_scrape_3(
                search = search,
                since = since,
                until = until,
                limit = limit,
                city = city)

            df = pd.concat([df, month_df])
            del month_df
            df.reset_index(drop=True, inplace=True)
            df.to_csv(f'./data/{filename}.csv')

            # notifier
            print(f'{since} saved!')
        
    return df
