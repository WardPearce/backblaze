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
    update = "b2_update_bucket"
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
    get = "b2_get_file_info"
    start_large = "b2_start_large_file"
    finish_large = "b2_finish_large_file"
    cancel_large = "b2_cancel_large_file"
    list_parts = "b2_list_parts"
    download_by_id = "b2_download_file_by_id"
    download_by_name = "b2_download_file_by_name"
    delete = "b2_delete_file_version"
    copy = "b2_copy_file"
    copy_part = "b2_copy_part"


class UploadRoute(Route):
    _prefix = "b2api/v2"

    upload = "b2_get_upload_url"
    upload_part = "b2_get_upload_part_url"


class DownloadRoute(Route):
    file = "file"
