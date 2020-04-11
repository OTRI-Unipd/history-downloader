import json
from pathlib import Path

DATA_DIRECTORY = 'data'

def list_jsons(folder : str):
    '''
    Lists all json files in a folder
    '''
    docs_path = Path(folder).rglob('*.json')
    files = [x.name.replace('.json','') for x in docs_path if x.is_file()]
    return files

def list_folders(folder : str):
    data_path = Path(folder)
    assert(data_path.is_dir())
    folder_list = list()
    for x in data_path.iterdir():
        if x.is_dir():
            folder_list.append(x.name)
    return folder_list

service_folder_name = input("Choose a service from the following: {} ".format(list_folders(DATA_DIRECTORY)))
chosen_folder_name = input("Choose a folder from the following: {} ".format(list_folders("{}/{}".format(DATA_DIRECTORY,service_folder_name))))
provider = ""
while True:
    provider_name = input("Who provided this data? y/a: ")
    if(provider_name == "y"):
        provider = "yahoo finance"
        break
    if(provider_name == "a"):
        provider = "alpha vantage"
        break
    print("You couldn't even choose between two letters, wow")

for file_name in list_jsons("{}/{}/{}".format(DATA_DIRECTORY,service_folder_name, chosen_folder_name)):
    file_path = Path(DATA_DIRECTORY,service_folder_name,chosen_folder_name,file_name + ".json")
    try:
        json_contents = json.load(file_path.open("r"))
        filename_split = file_name.split("_")
        meta = dict()
        meta['ticker'] = filename_split[0]
        meta['interval'] = "1m"
        meta['provider'] = provider
        json_contents['metadata'] = meta
        file_path.open("w+").write(json.dumps(json_contents, indent=4))
    except (Exception, json.decoder.JSONDecodeError) as error:
        print("Unable to work on {}: {}".format(file_name,error))