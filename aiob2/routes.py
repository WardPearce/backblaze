from .resources import CONFIG


class Routes:
    delete_bucket = "delete_bucket"
    hide_file = "hide_file"
    list_file_versions = "list_file_versions"
    list_file_names = "list_file_names"
    get_download_authorization = "get_download_authorization"
    list_unfinished_large_files = "list_unfinished_large_files"
    get_file_info = "get_file_info"
    finish_large_file = "finish_large_file"
    download_file_by_id = "download_file_by_id?fileId={}"
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
