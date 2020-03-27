'''
Script managing a bulk download of ticker data from Alpha Vantage.
Expects a JSON input file containing a list of "companies", each of them being a dictionary containing the symbol.
Sleeps for 15 seconds in between downloads to perform ~4 requests per minute.
If an error occurs it prints the last ticker that was downloaded successfully to a \"log.txt\" file.
'''
from pathlib import Path
import av_downloader
from datetime import datetime
from yf_downloader import YFinanceDownloader
import json
import time

SUBDIR = 'av_historical_1m'
CONFIG_FILE_NAME = 'config.json'
DOCS_DIRECTORY = 'docs'
DOCS_ROOT = 'tickers'
DOCS_TICKER = 'ticker'
AV_SLEEP_TIME = 15
LOG_FILE = 'log.txt'

def symbols_from_dict_list(data, key):
    '''Parses a list of dictionaries (like a JSON array) into a list of symbols

    Keyword arguments:
    data -- list of dictionaries
    key -- the key for the symbol in the list\'s items.
    '''
    symbols = []
    for row in data:
        symbols.append(row[key])
    return symbols

def log_result(msg : str):
    '''Append a message to a file

    Parameters:
        msg
            The message to append to the file
    '''
    Path(LOG_FILE).open('a+').write("{} {}\n".format(datetime.now().strftime("%H:%M:%S %d-%m-%Y"), msg))

def log_ok(service : str, symbol : str):
    msg = "{} - Downloaded {}".format(service,symbol)
    log_result(msg)
    print(msg)

def log_fail(service : str, symbol : str):
    msg = "{} - Failed to download {}".format(service,symbol)
    log_result(msg)
    print(msg)

def load_config(config_key : str):
    '''
    Opens configuration file to retrieve the key

    Parameters:
        config_key : str
            The key to load from a json file
    '''
    config_file = Path(CONFIG_FILE_NAME)

    if(config_file.exists() == False):
        print("Missing config.js file, see documentation for informations about format")
        exit()

    config_content = json.load(config_file.open(mode="r"))

    value = config_content[config_key]
    if(value is None):
        print("Missing alphavantage_api_key in config file")
        exit()
        
    return value

def list_docs():
    docs_path = Path(DOCS_DIRECTORY).rglob('*.json')
    files = [x.name.replace('.json','') for x in docs_path if x.is_file()]
    return files

def make_dir(dir_name : str, parent_path : Path = None):
    if parent_path is None:
        path = Path(dir_name)
    else:
        path = Path(parent_path, dir_name)
    path.mkdir(exist_ok=True)
    return path

if __name__ == '__main__':

    api_choice = input("Aplha Vantage or Yahoo finance? A/Y ")

    symbols_file_path = None

    while True: # Wait until a correct name is given
        symbols_file_name = input('Choose a file from the following: {} '.format(list_docs()))
        symbols_file_path = Path(DOCS_DIRECTORY, "{}.json".format(symbols_file_name))
        if(symbols_file_path.exists()==True):
            break
        else:
            print("File name {} doesn't exist".format(symbols_file_name))

    symbols_file_content = json.load(symbols_file_path.open("r"))
    
    rows = symbols_file_content[DOCS_ROOT]
    symbols = symbols_from_dict_list(rows, DOCS_TICKER)

    data_dir = make_dir('data')

    if(api_choice == "A"):
        api_key = load_config('alphavantage_api_key')
        av_dir = make_dir('AlphaVantage', parent_path=data_dir)

        av_downloader = av_downloader.AVDownloader(api_key, av_dir)

        for symbol in symbols:
            result = av_downloader.download(symbol)
            if result:
                log_ok("AV", symbol)
            else:
                log_fail("AV", symbol)
            time.sleep(AV_SLEEP_TIME)

    elif(api_choice == "Y"):
        yahoo_dir = make_dir('YahooFinance', parent_path=data_dir)

        now = datetime.now()
        
        data_path = make_dir(now.strftime("%H-%M_%d-%m-%y"), parent_path=yahoo_dir)

        yf_downloader = YFinanceDownloader(data_path)

        for symbol in symbols:
            print("Downloading: {}".format(symbol))
            result = yf_downloader.download_last_week(symbol)
            if result:
                log_ok("YF", symbol)
            else:
                log_fail("YF", symbol)
                
