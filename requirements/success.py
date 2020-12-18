class APIResponse:

    def __init__(self, status, data):
        self.status =   status
        self.data   =   data

    def respond(self):
        return {
            "Status"    :   self.status,
            "Data"      :   self.data
        }