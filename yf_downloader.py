'''
Classes:
YFinanceDownloader -- Download all kind of data from Yahoo Finance
'''
import yfinance as yf
import jsbeautifier
from pathlib import Path
from datetime import datetime, timedelta


class YFinanceDownloader:
    '''
    '''
    def __init__(self, dir_path):
        '''Init method.

        Keyword arguments:
        dir_path -- string, the absolute path of the directory, file names will be concatenated directly.
        '''
        self.dir_path = dir_path
    
    def downloadLastWeek(self, ticker):
        '''Downloads data for a single symbol.

        Keyword arguments:
        symbol -- string, the symbol for which to download data.
        interval -- string, the interval of the data, see Alpha Vantage for allowed intervals (default '1m')
        '''

        today = datetime.now()
        today_string = today.strftime("%Y-%m-%d")
        seven_days_ago = today - timedelta(days = 7)
        seven_days_ago_string = seven_days_ago.strftime("%Y-%m-%d")

        json_filename = "{}_{}_{}.json".format(ticker, seven_days_ago.strftime("%m-%y"),today.strftime("%m-y"))
        json_filepath = Path(self.dir_path, json_filename)

        yf_data = yf.download(ticker, start=seven_days_ago_string, end=today_string, interval = "1m")

        json_filepath.open("w+").write(jsbeautifier.beautify(yf_data.to_json(orient="table")))
