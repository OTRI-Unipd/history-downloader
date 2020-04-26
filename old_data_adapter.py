import json
from pathlib import Path
from datetime import datetime
from pytz import timezone

DATA_DIRECTORY = 'data'
TZ_DICT_FILE = Path("tz_dict.json")


def list_jsons(folder: str):
    '''
    Lists all json files in a folder
    '''
    docs_path = Path(folder).rglob('*.json')
    files = [x.name.replace('.json', '') for x in docs_path if x.is_file()]
    return files


def list_folders(folder: str):
    data_path = Path(folder)
    assert(data_path.is_dir())
    folder_list = list()
    for x in data_path.iterdir():
        if x.is_dir():
            folder_list.append(x.name)
    return folder_list


def add_meta(file_path: Path, file_name: str, provider: str, interval="1m") -> None:
    try:
        json_contents = json.load(file_path.open("r"))
        filename_split = file_name.split("_")
        meta = dict()
        meta['ticker'] = filename_split[0]
        meta['interval'] = interval
        meta['provider'] = provider
        json_contents['metadata'] = meta
        file_path.open("w+").write(json.dumps(json_contents, indent=4))
    except (Exception, json.decoder.JSONDecodeError) as error:
        print("Error adding metadata to {}: {}".format(file_name, error))


def adapt_from_yf(file_path: Path, file_name: str, interval="1m") -> None:
    add_meta(file_path, file_name, "yahoo finance", interval)


def adapt_from_av(file_path: Path, file_name: str, interval="1m") -> None:
    def __convert_to_gmt(*, date_time: datetime, zonename: str) -> datetime:
        zone = timezone(zonename)
        base = zone.localize(date_time)
        return base.astimezone(timezone("GMT"))
    try:
        json_contents = json.load(file_path.open("r"))
        tz_dict = json.load(TZ_DICT_FILE.open("r"))
        tz = tz_dict[file_name.split("_")[0]]
        new_data = dict()
        for k, v in json_contents.items():
            # Datetime key and atom value
            if k == "metadata":
                continue
            new_data[
                __convert_to_gmt(
                    date_time=datetime.strptime(k, "%Y-%m-%d %H:%M:%S"),
                    zonename=tz
                ).strftime("%Y-%m-%d %H:%M:%S")
            ] = v
        file_path.open("w+").write(json.dumps(new_data, indent=4))
    except (Exception, json.decoder.JSONDecodeError) as error:
        print("Unable to work on {}: {}".format(file_name, error))
    add_meta(file_path, file_name, "alpha vantage", interval=interval)


service_folder_name = input(
    "Choose a service from the following: {} ".format(list_folders(DATA_DIRECTORY)))
chosen_folder_name = input("Choose a folder from the following: {} ".format(
    list_folders("{}/{}".format(DATA_DIRECTORY, service_folder_name))))
procedure = None
while True:
    provider_name = input("Who provided this data? y/a: ")
    if(provider_name == "y"):
        procedure = adapt_from_yf
        break
    if(provider_name == "a"):
        procedure = adapt_from_av
        break
    print("You couldn't even choose between two letters, wow")

for file_name in list_jsons("{}/{}/{}".format(DATA_DIRECTORY, service_folder_name, chosen_folder_name)):
    file_path = Path(DATA_DIRECTORY, service_folder_name,
                     chosen_folder_name, file_name + ".json")
    if procedure:
        procedure(file_path, file_name)
