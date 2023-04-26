class ResourceAlreadyExists(Exception):
    def __init__(self, *, resource: str):
        self.msg = f'{resource} already exists'
        super().__init__(self.msg)
