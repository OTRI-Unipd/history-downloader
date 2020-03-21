'''
Classes:
AVDownloader -- Download historical data from Alpha Vantage.

Script:
If main module then requests a key and symbol via user input and stores in a subdirectory of the module file's parent directory.
'''
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
from pathlib import Path
import json

class AVDownloader:
    '''
    '''
    def __init__(self, key, dir_path):
        '''Init method.

        Keyword arguments:
        key -- string, the Alpha Vantage API key to use
        dir_path -- string, the absolute path of the directory, file names will be concatenated directly.
        '''
        self.ts = TimeSeries(key)
        self.dir_path = dir_path
    
    def download(self, symbol, interval='1min'):
        '''Downloads data for a single symbol.

        Downloads the full record of the TimeSeries Alpha Vantage api and stores the result in a file, returnin its name.
        The name will be: 'symbol_interval.json'. Ignores a symbol that returns no data, and returns an empty string in that case.

        Keyword arguments:
        symbol -- string, the symbol for which to download data.
        interval -- string, the interval of the data, see Alpha Vantage for allowed intervals (default '1m')
        '''

        time_now = datetime.now()
        string_date = time_now.strftime('%H_%M_%S_%d_%m_%Y')
        file_name = '{}_{}_{}.json'.format(symbol, interval, string_date);
        file_path = Path(self.dir_path, file_name)
        
        try:
            data, meta = self.ts.get_intraday(symbol, interval=interval, outputsize='full')
            with file_path.open('w+') as result_file:
                json.dump(data, result_file, indent=4)
            return file_path
        except ValueError:
                return ""

if __name__ == '__main__':
    dir_path = Path(Path.cwd(), 'av_historical_1m')
    key = input("Key: ")
    symbol = input("Symbol: ")
    result = AVDownloader(key, dir_path).download(symbol)
    if result:
        print('Saved output to: {}'.format(result))
    else:
        print('No data found for symbol {}'.format(symbol))
