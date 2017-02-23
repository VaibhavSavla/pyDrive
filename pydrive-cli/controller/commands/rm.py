from utility.utils import name_to_id

def handle_rm(args, service, cache):
    recursive = False
    empty = False
    if '-r' in args:
        args.remove('-r')
        recursive = True
    if '-e' in args:
        return empty_trash(service, cache)

    rm_ids = name_to_id(args[1], cache)
    if len(rm_ids) != 0:
        return rm(rm_ids[-1], service, cache, recursive)
    return cache


def rm(id, service, cache, recursive):
    if cache.files[id].mime_type == 'application/vnd.google-apps.folder' and not recursive:
        print('This is a directory. Use -r flag to delete it.')
        return cache
    service.files().delete(fileId=id).execute()
    del cache.directory_tree[id]
    del cache.files[id]
    return cache
    
def empty_trash(service, cache):
    service.files().emptyTrash().execute()
    cache.directory_tree = {key: cache.directory_tree[key] for key in cache.directory_tree.keys() if not cache.files[key].trashed}
    return cache
