import pickle
import os
import readline
import controller.accounts_handler as acc
from utility.utils import input_prompt
from utility.utils import process_args
from controller.commands.ls import handle_ls
from controller.commands.cd import handle_cd
from controller.commands.rm import handle_rm
from controller.commands.get import handle_get
from controller.commands.mkdir import mkdir
from controller.commands.put import handle_put
from controller.cache_handler import rebuild_cache
from controller.commands.share import share


from utility.paths import account_dir


def main():
    acc_handler = acc.handler()
    print('pyDrive: Command Line Interface for Google Drive')
    print('Type "help" for more information')
    while True:
        account = acc_handler.accounts[acc_handler.current]
        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind("tab: complete")

        def complete(text, state):
            temp = '/'.join(text.rstrip().split('/')[:-1])
            if len(temp) > 0:
                files = handle_ls(['ls', temp], account.cache, acc_handler.mode, False)
            else:
                files = handle_ls(['ls'], account.cache, acc_handler.mode, False)

            matching_files = []
            for file in files:
                if file.startswith(text.rstrip().split('/')[-1]):
                    if len(temp) < 1:
                        matching_files.append(temp + file)
                    else:
                        matching_files.append(temp + '/' + file)

            return (matching_files+[None])[state]

        readline.set_completer(complete)
        args_str = input(input_prompt(account.email, account.cache, acc_handler.mode))
        args = process_args(args_str)

        if len(args) < 1:
            continue

        if args[0] == 'account':
            acc_handler.handle_account(args)
        elif args[0] == 'ls':
            handle_ls(args, account.cache, acc_handler.mode)
        elif args[0] == 'cd':
            handle_cd(args, account.cache, acc_handler.mode)
        elif args[0] == 'rm':
            account.cache = handle_rm(args, account.service, account.cache)
        elif args[0] == 'mkdir':
            account.cache = mkdir(account.service, args[1], account.cache)
        elif args[0] == 'get':
            handle_get(args, account.service, account.cache)
        elif args[0] == 'put':
            account.cache = handle_put(args, account.service, account.cache)
        elif args[0] == 'share':
            share(args, account.service, account.cache)
        elif args[0] == 'cache':
            account.cache = rebuild_cache(account.service, account.id)
        elif args[0] == 'help':
            with open('./help.txt', 'r') as f:
                for line in f:
                    print(line, end='')
        # elif args[0] == 'sync':
        #    sync_handler(args, account.service, account.cache)
        elif args[0] == 'done':
            break
        else:
            print("{}: No such command".format(args[0]))

    pickle.dump(account.cache, open(os.path.join(account_dir(account.id), 'cache.p'), 'wb'))


if __name__ == "__main__":
    main()
