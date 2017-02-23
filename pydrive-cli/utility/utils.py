from utility.paths import getcwd
from utility.paths import getpwd

from colorama import init
from colorama import Fore
from colorama import Style
import os

init()

def process_args(args_str):
    args_str = args_str.replace("\ ", "%20")
    args = args_str.split()
    final_args = []
    for arg in args:
        arg = arg.replace("%20", " ")
        if arg.endswith('/'):
            arg = arg[:-1]
        final_args.append(arg)
    return final_args

def name_to_id(path_name, cache):
    path = [ getcwd() ]
    names = path_name.split('/')
    for name in names:
        for k, v in cache.directory_tree.items():
            if cache.files[k].name == name and path[-1] in v:
                path.append(k)
                break
    if len(path) != (len(names) + 1):
        print('No such file or directory')
        return []
    return path[1:]

def input_prompt(email, cache, mode):
    prompt = ''
    email = email.split('@')[0]
    prompt += Fore.GREEN + email + "@" + mode + " "
    pwd_names = [cache.files[id].name for id in getpwd()[1:]]
    prompt += Fore.BLUE + os.path.join("~", *pwd_names) + ' '
    prompt += Fore.BLUE + "$ "
    prompt += Style.RESET_ALL

    return prompt

def print_blue(message):
    print(Fore.BLUE + message)
    print(Style.RESET_ALL, end='')


def full_email(email):
    if "@" in email:
        return email
    return email + "@gmail.com"
