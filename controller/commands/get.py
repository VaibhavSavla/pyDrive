from utility.utils import name_to_id
from utility.paths import DEFAULT_DOWNLOAD_LOCATION
from apiclient.http import MediaIoBaseDownload
import os
import io

def handle_get(args, service, cache):
    exported = False
    location = DEFAULT_DOWNLOAD_LOCATION
    std_out = False

    if '--std-out' in args:
        args.remove('--std-out')
        std_out = True

    if '-e' in args:
        args.remove('-e')
        exported = True

    if '-d' in args:
        location = args[args.index('-d')+1]
        args.remove('-d')
        args.remove(location)
        location = os.path.abspath(os.path.expanduser(location))
        if not os.path.exists(location):
            print('Invalid download location')
            return

    ids = name_to_id(args[1], cache)
    if len(ids) != 0:
        file_id = ids[-1]
    else:
        return

    if std_out:
        print_file(service, file_id)
    elif cache.files[file_id].mime_type != 'application/vnd.google-apps.folder':
        get_file(service, file_id, cache.files[file_id].name, location, exported)
    else:
        get_recursive(service, file_id, cache, location)


def get_recursive(service, file_id, cache, location):
    if cache.files[file_id].mime_type != 'application/vnd.google-apps.folder':
        get_file(service, file_id, cache.files[file_id].name, location, False)
        return

    location = os.path.join(location, cache.files[file_id].name)
    os.mkdir(location)
    for id, parents in cache.directory_tree.items():
        if file_id in parents:
            get_recursive(service, id, cache, location)


def get_file(service, file_id, file_name, location, exported):
    if exported:
        request = service.files().export_media(fileId=file_id, mimeType='application/pdf')
        file_name += '.pdf'
    else:
        request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(os.path.join(location, file_name), mode='wb')
    print('downloading -' + str(os.path.join(location, file_name)))
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()


def print_file(service, file_id):
    location = DEFAULT_DOWNLOAD_LOCATION
    request = service.files().get_media(fileId=file_id)
    file_name = os.path.join(location, "." + file_id)
    fh = io.FileIO(file_name, mode='wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    with open(file_name, 'r') as f:
        for line in f:
            print(line, end='')
    os.remove(file_name)
