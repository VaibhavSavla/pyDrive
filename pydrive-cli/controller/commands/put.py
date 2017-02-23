import os
from apiclient.http import MediaFileUpload
from utility.utils import getcwd
from utility.utils import name_to_id
from model.file import file
from controller.commands.mkdir import mkdir

def handle_put(args, service, cache):

    std_in = False
    if '--std-in' in args:
        std_in = True
        args.remove('--std-in')

    location = os.path.abspath(os.path.expanduser(args[1]))
    if not os.path.exists(location) and not std_in:
        print('No such file or directory.')
        return cache

    if os.path.isdir(location):
        return put_recursive(service, cache, location)
    else:
        return put_file(service, cache, location, getcwd(), std_in)


def put_recursive(service, cache, location):
    cache = mkdir(service, os.path.basename(location), cache)    
    for x, y, z in os.walk(location):
        temp_list = x.split('/')
        temp_index = temp_list.index(os.path.basename(location))
        temp_loc = os.path.join(*temp_list[temp_index:])
        for new_dir in y:
            cache = mkdir(service, os.path.join(temp_loc, new_dir), cache)
        for new_file in z:
            cache = put_file(service, cache, os.path.join(x, new_file), name_to_id(temp_loc, cache)[-1], False)
    return cache

def put_file(service, cache, location, parent_id, std_in):
    title = os.path.basename(location)
    if title.startswith('.'):
        return cache

    if std_in:
        try:
            with open(location, 'w') as f:
                while True:
                    f.write(input() + '\n')
        except:
            pass

    file_metadata = {
        'name': title,
        'parents': [ parent_id ]
    }
    print('uploading - ' + location)
    media = MediaFileUpload(location, resumable=True)
    f = service.files().create(body=file_metadata, media_body=media, fields='id, mimeType').execute()
    cache.files[f['id']] = file(f['id'], title, f['mimeType'], False, False)
    cache.directory_tree[f['id']] = [ parent_id ]

    if std_in:
        os.remove(title)
    return cache
