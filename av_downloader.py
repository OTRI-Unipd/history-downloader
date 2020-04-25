'''
Classes:
AVDownloader -- Download historical data from Alpha Vantage.

Script:
If main module then requests a key and symbol via user input and stores in a subdirectory of the module file's parent directory.
'''
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
from pytz import timezone
from pathlib import Path
import json
import pytz

GMT = timezone("GMT")
TIME_ZONE_KEY = "6. Time Zone"


class AVDownloader:
    def __init__(self, key: str, dir_path: Path):
        '''
        Init method.
        Parameters:
            key : str
                the Alpha Vantage API key to use
            dir_path : Path
                The Path object representing the destination folder, file names will be concatenated directly.
        '''
        self.ts = TimeSeries(key)
        self.dir_path = dir_path

    def download(self, symbol: str, interval='1min'):
        '''
        Downloads data for a single symbol.
        Downloads the full record of the TimeSeries Alpha Vantage api and stores the result in a file, returning the output file.
        The name will be: 'symbol_interval.json'. Ignores a symbol that returns no data, and returns an empty string in that case.

        Parameters:
            symbol : str
                The symbol for which to download data.
            interval : str
                The interval of the data, see Alpha Vantage for allowed intervals (default '1m')
        Returns: The Path to the output file or None if no data could be found.
        '''

        time_now = datetime.now()
        string_date = time_now.strftime('%H_%M_%S_%d_%m_%Y')
        file_name = '{}_{}_{}.json'.format(symbol, interval, string_date)
        file_path = Path(self.dir_path, file_name)

        try:
            data, meta = self.ts.get_intraday(
                symbol, interval=interval, outputsize='full')
            # The meta retrieved here are not what we want

            tz = meta[TIME_ZONE_KEY]
            new_data = dict()
            for k, v in data.items():
                # Datetime key and atom value
                new_data[
                    AVDownloader.__convert_to_gmt(
                        date_time=datetime.strptime(k, "%Y-%m-%d %H:%M:%S"),
                        zonename=tz
                    ).strftime("%Y-%m-%d %H:%M:%S")
                ] = v
            meta = dict()
            meta['ticker'] = symbol
            meta['interval'] = interval
            meta['provider'] = "alpha vantage"
            new_data['metadata'] = meta
            with file_path.open('w+') as result_file:
                json.dump(new_data, result_file, indent=4)
            return file_path
        except ValueError:
            return None

    @staticmethod
    def __convert_to_gmt(*, date_time: datetime, zonename: str) -> datetime:
        '''
        Method to convert a datetime in a certain timezone to a GMT datetime
        Parameters:
            date_time : datetime:
                The datetime to convert
            zonename : str
                The time zone's name
        Returns:
            The datetime object in GMT time
        '''
        zone = timezone(zonename)
        base = zone.localize(date_time)
        return base.astimezone(GMT)


if __name__ == '__main__':
    dir_path = Path('/av_historical_1m')
    dir_path.mkdir(exist_ok=True)
    key = input("Key: ")
    symbol = input("Symbol: ")
    result = AVDownloader(key, dir_path).download(symbol)
    if result:
        print('Saved output to: {}'.format(result))
    else:
        print('No data found for symbol {}'.format(symbol))
