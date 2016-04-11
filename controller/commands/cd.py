from utility.paths import *
from utility.utils import name_to_id

def handle_cd(args, cache, mode):
    if len(args) == 1:
        set_root_dir(getpwd()[0])
    elif args[1] == '..':
        pop()
    else:
        ids = name_to_id(args[1], cache)
        if len(ids) != 0:
            for id in ids:
                if cache.files[id].mime_type == 'application/vnd.google-apps.folder':
                    add_dir_to_path(id)
                else:
                    print('Not a directory')
                    break
