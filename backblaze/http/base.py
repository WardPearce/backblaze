from httpx import Response


class BaseHTTP:
    def handle_resp(self, resp: Response, json: bool = True,
                    read: bool = True) -> None:
        """Handles resp response.

        Parameters
        ----------
        resp
            HTTPX response object.
        """

        resp.raise_for_status()

        if json:
            return resp.json()
        elif read:
            return resp.read()
        else:
            return True
