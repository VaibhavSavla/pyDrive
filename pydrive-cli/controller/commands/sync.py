import os
import pickle
from controller.commands.mkdir import mkdir
from controller.commands.get import get_file

def sync_handler(args, service, cache):
    sync_down(service, '0B05FwVakQMdpZ3ViRng2VEItMUU', cache, '/Users/vaibhav/drive')


def sync_up():
    pass


def sync_down(service, file_id, cache, location):
    if cache.files[file_id].mime_type != 'application/vnd.google-apps.folder':
        if not os.path.exists(os.path.join(location, cache.files[file_id].name)):
            get_file(service, file_id, cache.files[file_id].name, location, False)
        return

    location = os.path.join(location, cache.files[file_id].name)
    if not os.path.exists(location):
        os.mkdir(location)
    for id, parents in cache.directory_tree.items():
        if file_id in parents:
            sync_down(service, id, cache, location)


def add_folder(service, folder_name, cache):
    try:
        synced_files = pickle.load(open(os.path.expanduser('~/.pyDrive/') + 'sync.p', 'rb'))
    except:
        synced_files = []
    synced_files.append(folder_name)
    pickle.dump(synced_files, open(os.path.expanduser('~/.pyDrive/') + 'sync.p', 'wb'))
    os.mkdir(folder_name)
    return mkdir(service, folder_name, cache)


def sync_list():
    try:
        synced_files = pickle.load(open(os.path.expanduser('~/.pyDrive/') + 'sync.p', 'rb'))
    except:
        print('No synced files')
        return
    for file in synced_files:
        print(file)