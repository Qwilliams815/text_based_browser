import os
import sys
import requests
from collections import deque
from bs4 import BeautifulSoup
import colorama

# CHECK/CREATE DIRECTORY FOR TABS
args = sys.argv
saved_tabs_dir = args[1]
os.makedirs(saved_tabs_dir, exist_ok=True)
search_history = deque()

while True:
    search = input()
    current_index = 0

# SEARCH VALIDATION CHECKER
    if search == 'exit':
        quit()
    elif search == 'back':
        if not search_history:
            pass
        else:
            print(search_history[current_index])
    elif '.' not in search:
        print("error, not a valid search")
    else:
        if not search.startswith('https://'):
            search = 'https://' + search

# CREATING THE WEB PAGE FILE
        file_name = search.lstrip('https://') + '.txt'
        r = requests.get(search)
        soup = BeautifulSoup(r.content, 'html.parser')
        if not os.path.isfile(os.getcwd() + '/' + file_name):
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(soup.get_text())

# PRINTING THE PAGE
        tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'li', 'head', 'title', 'div']
        page = soup.find_all(tags)
        for tag in page:
            if tag.string is None:
                pass
            elif tag.name == "a":
                print(colorama.Fore.BLUE + tag.string)
                print(colorama.Style.RESET_ALL)
            else:
                print(tag.string)

# MOVING THE FILE
        if not os.path.isfile(os.getcwd() + saved_tabs_dir + '/' + search):
            old = os.getcwd() + '/' + file_name
            new = os.getcwd() + '/' + saved_tabs_dir + '/' + file_name
            os.rename(old, new)
            current_index += 1
            search_history.append(soup.get_text())
