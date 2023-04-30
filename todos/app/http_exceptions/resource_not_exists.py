class ResourceNotExists(Exception):
    def __init__(self, *, resource: str):
        self.msg = f'{resource} does not exist'
        super().__init__(self.msg)
