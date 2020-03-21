'''
Script managing a bulk download of ticker data from Alpha Vantage.
Expects a JSON input file containing a list of "companies", each of them being a dictionary containing the symbol.
Sleeps for 15 seconds in between downloads to perform ~4 requests per minute.
If an error occurs it prints the last ticker that was downloaded successfully to a \"log.txt\" file.
'''
from pathlib import Path
import av_downloader
import json

SUBDIR = 'av_historical_1m'

def symbols_from_dict_list(data, key):
    '''Parses a list of dictionaries (like a JSON array) into a list of symbols

    Keyword arguments:
    data -- list of dictionaries
    key -- the key for the symbol in the list\'s items.
    '''
    symbols = []
    for company in data:
        symbols.append(company[key])
    return symbols

def bulk_av_download_1min(key, symbols):
    '''Downloads 1min-interval historical data for a list of symbols and waits for 15 seconds in between each one
    
    If some error happens when downloading a symbol then it is reported in an \"error_log-txt\" file in the current working directory

    Keyword arguments:
    key -- Alpha Vantage api key
    symbols -- a list of string symbols
    '''
    SLEEP_TIME = 15
    subdir = Path(Path.cwd(), SUBDIR)
    avd = av_downloader.AVDownloader(key, subdir)
    for symbol in symbols:
        result = avd.download(symbol)
        print('Downloaded ' + symbol + "to " + str(result))
        time.sleep(SLEEP_TIME)
        with Path(subdir, 'last_downloaded.txt').open('a') as log:
            log.write('Last downloaded symbol is ' + symbol)

if __name__ == '__main__':

    print(Path.cwd())

    av_key = input('Insert your Alpha Vantage api key: ')

    file_name = input('Input file should be a local JSON file\nInput file name: ')
    file_content = {}
    with open(file_name) as f:
        file_content = json.load(f)
    
    list_key = input('What\'s the list\'s key? ')
    companies = file_content[list_key]
    
    symbol_key = input('What\'s the key for the symbol in the list\'s items? ')
    symbols = symbols_from_dict_list(companies, symbol_key)

    bulk_av_download_1min(av_key, symbols)
