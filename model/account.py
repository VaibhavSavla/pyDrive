class account:
    def __init__(self, id, service, email, root_dir):
        self.id = id
        self.root_dir = root_dir
        self.service = service
        self.email = email
        self.user_name = ''
        self.used_data = 0.0
        self.total_data = 0.0

