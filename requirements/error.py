class APIErrorResponse:

    def __init__(self, status, error,message=None):
        self.status =   status
        self.error   =   error
        self.message = message

    def respond(self):
        if self.message is None:
            return {
                "Status"    :   self.status,
                "Error"      :   self.error
            }
        else:
            return {
                "Status"    :   self.status,
                "Error"     :   self.error,
                "Message"   :   self.message

            }          
