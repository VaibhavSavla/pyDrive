from model.file import file
from utility.paths import getcwd
from utility.utils import name_to_id
from utility.utils import print_blue
import os
def mkdir(service, folder_name, cache):
    """Create a folder in the current working directory

    Args:
    folder_name: name of the folder to be created
    """
    if os.path.dirname(folder_name) != '':
        parent = name_to_id(os.path.dirname(folder_name), cache)[-1]
    else:
        parent = getcwd()
    folder_name = os.path.basename(folder_name)
    file_metadata = {
        'name' : folder_name,
        'mimeType' : 'application/vnd.google-apps.folder',
        'parents' : [ parent ]
    }
    print_blue('Creating directory - ' + folder_name)
    f = service.files().create(body=file_metadata).execute()
    cache.files[f['id']] = file(f['id'], folder_name, 'application/vnd.google-apps.folder', False, False)
    cache.directory_tree[f['id']] = [ parent ]
    return cache
