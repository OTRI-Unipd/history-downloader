'''
Classes:
YFinanceDownloader -- Download all kind of data from Yahoo Finance
'''
import yfinance as yf
from pathlib import Path
from datetime import datetime, timedelta, date


class YFinanceDownloader:
    '''
    Attributes:
        files_directory : pathlib.Path
            Directory where to put JSON output files in.
    
    '''
    def __init__(self, files_directory : Path):
        '''
        Parameters:
        
            files_directory : pathlib.Path
                Existing system directory where to put JSON output files in.
        '''
        self.files_directory = files_directory
    
    def download_dates(self, ticker : str, start_date : date, end_date : date, interval : str = "1d"):
        '''
        Downloads quote data for a single ticker given the start date and end date.

        Parameters:
            ticker : str
                The simbol to download data of.
            start_datetime : datetime
                Must be before end_datetime.
            end_datetime : datetime
                Must be after start_datetime.
            interval : str
                Could be "1m" (7 days max); "2m", "5m", "15m", "30m", "90m" (60 days max); "60m", "1h" (730 days max); "1d", "5d", "1wk"
        '''
        json_filepath = Path(self.files_directory, self.__output_JSON_filename(ticker, start_date, end_date))

        yf_data = yf.download(ticker, start = self.__yahoo_time_format(start_date), end = self.__yahoo_time_format(end_date), interval = interval, round  = False, progress = False)

        # If no data is downloaded it means that the ticker couldn't be found or there has been an error, we're not creating any output file then.
        if yf_data.empty:
            return False

        json_filepath.open("w+").write(yf_data.to_json(orient="table", indent = 4))
        return json_filepath

    def download_minimum_interval(self, ticker : str, start_date : date, end_date : date):
        '''
        Downloads quote data for a single ticker given the start date and end date, using the smallest interval
        available for the given dates.

        Parameters:
            ticker : str
                The simbol to download data of.
            start_datetime : datetime
                Must be before end_datetime.
            end_datetime : datetime
                Must be after start_datetime.
        '''
        return self.download_dates(ticker, start_date, end_date, self.__calc_minimum_interval(start_date))


    def download_last_week(self, ticker : str):
        '''Downloads quote data for a single ticker a puts it in a beautified JSON file.

        Parameters:
            ticker : str
                The symbol to download data of. Could be with market indication (FTSEMIB) or with market (FTSEMIB.MI).
        '''

        today = date.today()
        seven_days_ago = today - timedelta(days = 7)

        return self.download_minimum_interval(ticker, seven_days_ago, today)

    def __yahoo_time_format(self, date : date):
        '''
        Formats time into yfinance-ready string format for start date and end date.

        Parameters:
            date : datetime.date
                Date to be formatted for yfinance start and end times.
        '''
        return date.strftime("%Y-%m-%d")

    def __output_JSON_filename(self, ticker : str, start_date : date, end_date : date):
        '''
        Generates the JSON output file's name using ticker, data start date and end date.

        Parameters:
            ticker : str
                Output ticker's name.
            start_datetime : datetime
                Beginning date of output data.
            end_datetime : datetime
                End date of output data.
        '''
        return "{}_{}-to-{}.json".format(ticker, end_date.strftime("%d-%m-%y"), start_date.strftime("$d-%m-%y"))

    def __calc_minimum_interval(self, start_date : date):
        '''
        Calculates the shortest interval (from 1min to 1day) allowed for the given interval. For the calculation we only need the start datetime because
        it depends on how old is the wanted data.

        Parameters:
            start_datetime: datetime
                Beginning date of wanted data.

        Returns: The correct shortest yfinance interval
        '''
        days_difference = (date.today() - start_date).days

        if days_difference <= 7:
            return "1m"
        elif days_difference <= 60:
            return "2m"
        elif days_difference <= 730:
            return "1h"
        else:
            return "1d"
