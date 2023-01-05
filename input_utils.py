import os
import json
import csv

from request_utils import *


prompt_prefix = "\n[Prompt] "
prompt_suffix = ": "

# prompts user for data not needing validation
def prompt_user(msg):
    return input(prompt_prefix + msg + prompt_suffix)


# prompts users for an input. checks the entered input against valid options. returns a valid choice
def prompt_user_options(msg, retry_msg="", options=[]):
    #setup
    str_options = ""
    for i in options:
        str_options += i + "/"
    str_options = str_options[0:-1]
    
    #get input
    entered = input(prompt_prefix + msg + " (" + str_options + ")" + prompt_suffix)
    
    #validate input
    if entered in options:
        return entered

    #ask again
    if prompt_retry(retry_msg):
        return prompt_user_options(msg, retry_msg, options)


# prompts users for an input. checks the entered input is in a valid range. returns a valid choice
def prompt_user_list(msg, retry_msg="", range=0):
    #setup
    str_options = "1-" + str(range)
    
    #get input
    entered = input(prompt_prefix + msg + " (" + str_options + ")" + prompt_suffix)
    
    #validate input
    if int(entered) > 0 and int(entered) <= range:
        return int(entered)-1

    #ask again
    if prompt_retry(retry_msg):
        return prompt_user_list(msg, retry_msg, range)


# prompts user if they want to ignore the last, potentially problematic, input option
def prompt_continue_anyways(msg):
    entered = input(prompt_prefix + msg + " Continue Anyways? (y/n)" + prompt_suffix)
    if entered == 'y':
        return True
    elif entered == 'n':
        return False
    else:
        return prompt_continue_anyways(msg)

        
# prompts the users if they want to retry the last input option
def prompt_retry(msg):
    entered = input(prompt_prefix + msg + " Try Again? (y/n)" + prompt_suffix)
    if entered == 'y':
        return True
    elif entered == 'n':
        exit()
    else:
        return prompt_retry(msg)




# gets the file path of a json to be imported, checks if the file exists, and trys to load and return the data
def handle_load_json_data(msg):
    json_file_path = prompt_user(prompt_prefix + msg + "(relative file path, including file extention)" + prompt_suffix)

    if not os.path.exists(json_file_path):
        if prompt_retry(f'Specified JSON file at \'{json_file_path}\' does not exist.'):
            return handle_load_json_data(msg)
    
    try:
        with open(json_file_path, 'r', encoding="utf8") as file:
            json_data = json.load(file)
    except Exception as e:
        if prompt_retry(f'Error loading file: {e}'):
            return handle_load_json_data(msg)
    
    return json_data


# gets the file path of a csv to be imported, checks if the file exists, and trys to load and return the data
def handle_load_csv_data(msg):
    csv_file_path = prompt_user(msg + " (relative file path, including file extention)")

    if not os.path.exists(csv_file_path):
        if prompt_retry(f'Specified CSV file at \'{csv_file_path}\' does not exist.'):
            return handle_load_csv_data(msg)
    
    csv_headers = []
    csv_data = []

    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if csv_headers == []:
                    csv_headers = row

                csv_data.append(row)

    except Exception as e:
        if prompt_retry(f'Error loading file: {e}'):
            return handle_load_csv_data(msg)
    
    return csv_headers, csv_data