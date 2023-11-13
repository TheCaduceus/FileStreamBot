class HTTPError(Exception):
    status_code:int = None
    description:str = None
    def __init__(self, status_code, description):
        self.status_code = status_code
        self.description = description
        super().__init__(self.status_code, self.description)

error_messages = {
    400: 'Invalid request.',
    401: 'File code is required to download the file.',
    403: 'Invalid file code.',
    404: 'File not found.',
    500: 'Internal server error.'
}

async def invalid_request(_):
    return 'Invalid request.', 400

async def not_found(_):
    return 'Resource not found.', 404

async def invalid_method(_):
    return 'Invalid request method.', 405

async def http_error(error: HTTPError):
    error_message = error_messages.get(error.status_code)
    return error.description or error_message, error.status_code

def abort(status_code: int = 500, description: str = None):
    raise HTTPError(status_code, description)
