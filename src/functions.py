# twint scraping packages
import pandas as pd
import twint
import nest_asyncio
nest_asyncio.apply()
import datetime
from dateutil.relativedelta import relativedelta

# NLP packages
import spacy, re
from spacy.lang.en import English
import nltk
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
nltk.download('wordnet')
nltk.download('stopwords')


#######################################################################
### scraping functions adapted from Josh Szymanowski & Eric Blander ###
#######################################################################


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


################################################
### Scraping functions for geolocated tweets ###
################################################


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


###########################################################
### Text Preprocessing Function Adapted from Zijing Zhu ###
###########################################################

stop_words = list(set(stopwords.words('english')))
stop_words.extend(['covid', '#covid', 'virus', '#virus',
                   'coronavirus', '#coronavirus', 'vaccine',
                   '#vaccine', 'vaccines', '#vaccines', 'covid-19'
                   'covidvaccine'])
stop_words = [w.lower() for w in stop_words]

def tweet_preprocessing(str_input):
    
    # remove symbols, websites, email addresses
    words = str_input 
    words = [re.sub(r'[^A-Za-z@]', '', word) for word in words] 
    words = [re.sub(r'\S+com', '', word) for word in words]
    words = [re.sub(r'\S+@\S+', '', word) for word in words] 
    words = [word for word in words if word!=' ']
    words = [word for word in words if len(word)!=0] 
    
    # remove stopwords     
    words = [word.lower() for word in words if (word.lower() not in stop_words) & (len(word.lower()) > 1)]
 
    # combine a list into one string   
    string = ' '.join(words)
    
    return string
