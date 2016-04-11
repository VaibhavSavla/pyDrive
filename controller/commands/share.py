from utility.utils import name_to_id

def callback(request_id, response, exception):
    if exception:
        # Handle error
        print("Error sharing file")
    else:
        print("Successfuly shared file")


def share(args, service, cache):
    if not ('-r' in args or '-w' in args):
        print('Provide the type of permission -r (read) or -w (write)')
        return

    role = ''
    if '-r' in args:
        role = 'reader'
        args.remove('-r')
    else:
        role = 'writer'
        args.remove('-w')

    file_id = name_to_id(args[1], cache)[-1]
    user = args[2]

    batch = service.new_batch_http_request(callback=callback)
    user_permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': user
    }

    batch.add(service.permissions().create(
        fileId=file_id,
        body=user_permission,
        fields='id'
    ))
    batch.execute()

