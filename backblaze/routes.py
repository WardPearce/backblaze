class Route:
    _prefix = None

    def __init__(self, route: str) -> None:
        if route[-1:] == "/":
            route = route[:-1]

        self.route = route

    def format(self) -> None:
        """Used to format URL.
        """

        routes = [
            attr for attr in dir(self.__class__)
            if not callable(getattr(self.__class__, attr))
            and not attr.startswith("__")
            and not attr.startswith("_")
        ]

        for var_name in routes:
            value = "{}{}/{}".format(
                self.route,
                "/" + self._prefix if self._prefix else "",
                getattr(
                    self,
                    var_name
                )
            )

            if value[-1:] == "/":
                value = value[:-1]

            setattr(
                self,
                var_name,
                value
            )


class BucketRoute(Route):
    _prefix = "b2api/v2"

    create = "b2_create_bucket"
    delete = "b2_delete_bucket"
    list = "b2_list_buckets"


class KeyRoute(Route):
    _prefix = "b2api/v2"

    create = "b2_create_key"
    delete = "b2_delete_key"
    list = "b2_list_keys"


class FileRoute(Route):
    _prefix = "b2api/v2"

    names = "b2_list_file_names"
    versions = "b2_list_file_versions"
