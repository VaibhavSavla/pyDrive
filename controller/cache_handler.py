from model.file import file
from model.cache import cache
from utility.paths import account_dir
import sys
import os
import pickle

def build_cache(service, account_id):
    cache_file = os.path.join(account_dir(account_id), "cache.p")
    if os.path.exists(cache_file):
        return pickle.load(open(cache_file, 'rb'))
    page_token = None
    all_files = []
    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            fields = "files(id,mimeType,name,parents,shared,trashed), nextPageToken"
            files = service.files() \
                    .list(pageSize=1000, fields=fields, **param).execute()
            all_files += files.get('files', [])
            page_token = files.get('nextPageToken')
            if not page_token:
                break
        except:
            print('An error occurred' + str(sys.exc_info()[0]))
            break

    files = {}
    directory_tree = {}
    for f in all_files:
        files[f['id']] = file(f['id'], f['name'], f['mimeType'], f['shared'], f['trashed'])
        if 'parents' in f:
            directory_tree[f['id']] = f['parents']
        else:
            directory_tree[f['id']] = 'shared_root'
    c = cache(files, directory_tree)
    pickle.dump(c, open(cache_file, 'wb'))
    return c

def rebuild_cache(service, account_id):
    cache_file = os.path.join(account_dir(account_id), "cache.p")
    os.remove(cache_file)
    return build_cache(service, account_id)
