class HttpException(Exception):
    def __init__(self, status_code: int, content: dict[str, str] | None = None, headers: dict[str, str] | None = None):
        self.status_code = status_code
        self.content = content
        self.headers = headers
