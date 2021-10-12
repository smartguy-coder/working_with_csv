import requests
import os
import csv


url_api = 'http://api.open-notify.org/astros.json'
STORAGE_FOLDER_FOR_FILES = 'created files'


def raw_astro_data() -> list:
    """
    function tries to open api and prepare data for following processing
    """
    try:
        response = requests.get(url_api, timeout=5)
        response.raise_for_status()
        print(response)
    except requests.exceptions.HTTPError as error:
        print(error)
        return None
    except requests.exceptions.ConnectionError as error:
        print(error)
        return None
    except requests.exceptions.Timeout as error:
        print(error)
        return None
    except requests.exceptions.RequestException as error:
        print(error)
        return None

    ppl = response.json()
    astro_list_data_raw = ppl['people']

    return astro_list_data_raw


def write_all_astros_in_csv_file_manual_processing(raw_list: list):

    # to keep created files in order create a folder to save them by defined name
    if not os.path.isdir(STORAGE_FOLDER_FOR_FILES):
        os.mkdir(STORAGE_FOLDER_FOR_FILES)

    # if we get data from url_api we must write it in file
    if raw_list:
        with open(f'{STORAGE_FOLDER_FOR_FILES}/people-manual_processing.csv', mode="w") as astro_file:
            astro_file.write(f'number in order;space craft;astronaut\n')

            for astro in raw_list:
                astro_file.write(f'{raw_list.index(astro)+1};{astro["craft"]};{astro["name"]}\n')


def write_all_astros_in_csv_file_by_crafts_manual_processing(raw_list: list):

    # to keep created files in order create a folder to save them by defined name
    if not os.path.isdir(STORAGE_FOLDER_FOR_FILES):
        os.mkdir(STORAGE_FOLDER_FOR_FILES)

    if raw_list:
        # extract all the names of space crafts with people on board
        list_of_craft = list()
        for item in raw_list:
            if item['craft'] not in list_of_craft:
                list_of_craft.append([item['craft']])

        # here we create the set with the unique names of space crafts
        list_of_craft_clear = list()
        for i in range(len(list_of_craft)):
            list_of_craft_clear.append(list_of_craft[i][0])
        list_of_craft_clear = set(list_of_craft_clear)

        # here we create a dict, where the keys - names of crafts, value - empty list, where we add later people
        astro_on_craft = dict()
        for item in list_of_craft_clear:
            astro_on_craft[item] = []

        # here we define all the people from the appropriate space craft
        for item in raw_list:
            astro_on_craft[item['craft']] = astro_on_craft[item['craft']] + [item['name']]

        # create all csv-files we need
        for space_craft_name in astro_on_craft:
            with open(f'{STORAGE_FOLDER_FOR_FILES}/{space_craft_name}-manual_processing.csv', mode='w') as space_craft:
                space_craft.write(f'number in order;astronaut\n')

                for astronaut in astro_on_craft[space_craft_name]:
                    space_craft.write(f'{astro_on_craft[space_craft_name].index(astronaut) + 1};{astronaut}\n')


if __name__ == "__main__":
    write_all_astros_in_csv_file_manual_processing(raw_astro_data())
    write_all_astros_in_csv_file_by_crafts_manual_processing(raw_astro_data())