from .resources import CONFIG


class Routes:
    """
    Holds all routes what use the auth url.
    Most routes are stored here.
    """

    delete_bucket = "delete_bucket"
    hide_file = "hide_file"
    list_file_versions = "list_file_versions"
    list_file_names = "list_file_names"
    get_download_authorization = "get_download_authorization"
    list_unfinished_large_files = "list_unfinished_large_files"
    get_file_info = "get_file_info"
    finish_large_file = "finish_large_file"
    get_upload_url = "get_upload_url"
    list_parts = "list_parts"
    create_key = "create_key"
    create_bucket = "create_bucket"
    list_keys = "list_keys"
    list_buckets = "list_buckets"
    get_upload_part_url = "get_upload_part_url"
    cancel_large_file = "cancel_large_file"
    copy_part = "copy_part"
    copy_file = "copy_file"
    delete_file_version = "delete_file_version"
    delete_key = "delete_key"

    def format_routes(self):
        """
        Formats the B2 routes using the auth url.
        """

        routes = [
            attr for attr in dir(Routes())
            if not callable(getattr(Routes(), attr))
            and not attr.startswith("__")
        ]

        for var_name in routes:
            setattr(
                self,
                var_name,
                "{}/b2api/v2/b2_{}".format(
                    CONFIG.api_url,
                    getattr(
                        self,
                        var_name
                    )
                )
            )


ROUTES = Routes()


class DownloadRoutes:
    """
    Holds all the routes what use the download url.
    Only a few routes use this.
    """

    file_by_id = "/b2api/v2/b2_download_file_by_id?fileId={}"
    file_by_name = "/file/{}/{}"

    def format_routes(self):
        """
        Formats the B2 routes using the download url.
        """

        routes = [
            attr for attr in dir(DownloadRoutes())
            if not callable(getattr(DownloadRoutes(), attr))
            and not attr.startswith("__")
        ]

        for var_name in routes:
            setattr(
                self,
                var_name,
                "{}{}".format(
                    CONFIG.download_url,
                    getattr(
                        self,
                        var_name
                    )
                )
            )


DL_ROUTES = DownloadRoutes()
