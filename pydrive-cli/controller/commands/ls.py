from utility.paths import getcwd
from utility.utils import name_to_id
from utility.paths import set_root_dir
from utility.utils import print_blue

def handle_ls(args, cache, mode, printing=True):
    trashed = mode == 'trashed'
    mime = False
    if '-m' in args:
        mime = True
        args.remove('-m')
    display_id = False
    if '-i' in args:
        display_id = True
        args.remove('-i')
    if len(args) > 1:
        ids = name_to_id(args[1], cache)
        if len(ids) != 0:
            id = ids[-1]
        else:
            return
    else:
        id = getcwd()
    return ls(id, cache, trashed, mime, display_id, printing)


def ls(id, cache, trashed, mime, display_id, printing):
    result = []
    for k, v in cache.directory_tree.items():
        file = cache.files[k]
        if id in v and file.trashed == trashed:
            if display_id:
                if printing:
                    print(cache.files[k].id[0], end='\t')
            if mime:
                print('{0:40s}'.format(cache.files[k].mime_type), end='\t')
            if cache.files[k].mime_type == 'application/vnd.google-apps.folder':
                if printing:
                    print_blue(cache.files[k].name)
                result.append(cache.files[k].name.replace(' ', '\ ') + '/')
            else:
                if printing:
                    print(cache.files[k].name)
                result.append(cache.files[k].name.replace(' ', '\ '))

    return result
