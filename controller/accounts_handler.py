import pickle

from utility.paths import *
from model.account import account
from utility.utils import full_email
from auth.auth import get_service
import sys
import controller.cache_handler as cache_handler

class handler:
    def __init__(self):
        self.current = 0
        self.num_accounts = 0
        self.mode= 'myfiles'
        self.accounts = []
        self.accounts_info = []
        try:
            self.accounts_info = pickle.load(open(ACCOUNTS_INFO_FILE, "rb"))
            self.num_accounts = len(self.accounts_info)
            for i in range(1, self.num_accounts + 1):
                service = get_service('account' + str(i))
                email = self.accounts_info[i-1]['email']
                root_dir = self.accounts_info[i-1]['root']
                a = account(i, service, email, root_dir)
                self.accounts.append(a)
        except:
            print(sys.exc_info()[0])
            self.add_account()

        acc = self.accounts[self.current]
        set_root_dir(self.accounts_info[self.current]['root'])        
        acc.cache = cache_handler.build_cache(acc.service, self.current+1)
    
    def handle_account(self, args):
        if args[1] == '-a' or args[1] == '--add':
            self.add_account()
        elif args[1] == '-s' or args[1] == '--switch':
            self.switch_account(args[2])
        elif args[1] == '-l' or args[1] == '--list':
            self.list_accounts()
        elif args[1] == '-P':
            self.mode = 'myfiles'
            set_root_dir(self.accounts_info[self.current]['root'])
        elif args[1] == '-S':
            self.mode = 'shared'
            set_root_dir('shared_root')
        elif args[1] == '-t':
            self.mode = 'trashed'

    def add_account(self):
        self.num_accounts += 1 
        service = get_service("account" + str(self.num_accounts))
        data = service.about().get(fields="user").execute()
        email = data['user']['emailAddress']
        root_dir = service.files().get(fileId='root', fields='id').execute()['id']
        acc = account(self.num_accounts, service, email, root_dir)
        self.accounts.append(acc)
        self.accounts_info.append({ 'email': email, 'root': root_dir})
        pickle.dump(self.accounts_info, open(ACCOUNTS_INFO_FILE, "wb"))
        
    def switch_account(self, email):
        for account in self.accounts:
            if account.email == full_email(email):
                self.current = account.id-1
                account.cache = cache_handler.build_cache(account.service, account.id)
                set_root_dir(self.accounts_info[self.current]['root'])
                return
        print('Invalid email or email not added to pyDrive. ')

    def list_accounts(self):
        print("Number of accounts - " + str(len(self.accounts)))
        print("Email Ids")
        for account in self.accounts:
            print(account.email)

