import os

HOME_DIR = os.path.expanduser("~")
META_DIR = ".pyDrive"

ACCOUNTS_INFO_FILE = os.path.join(HOME_DIR, META_DIR, ".account_info.p")
DEFAULT_DOWNLOAD_LOCATION = os.path.join(HOME_DIR, "DriveDownloads")
if not os.path.exists(DEFAULT_DOWNLOAD_LOCATION):
    os.mkdir(DEFAULT_DOWNLOAD_LOCATION)

DRIVE_CWD = []

def getcwd():
    global DRIVE_CWD
    return DRIVE_CWD[-1]

def add_dir_to_path(dir):
    global DRIVE_CWD
    DRIVE_CWD.append(dir)

def account_dir(id):
    return os.path.join(HOME_DIR, META_DIR, "account" + str(id))

def set_root_dir(root_dir):
    global DRIVE_CWD
    DRIVE_CWD = [root_dir]

def getpwd():
    global DRIVE_CWD
    return DRIVE_CWD

def pop():
    global DRIVE_CWD
    DRIVE_CWD.pop()
