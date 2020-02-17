ROUTES = {
    "authorize": "https://api.backblazeb2.com/b2api/v2/b2_authorize_account",

    "list_unfinished_large_files": "{}/b2api/v2/b2_list_unfinished_large_files",
    "list_parts": "{}/b2api/v2/b2_list_parts",
    "list_keys": "{}/b2api/v2/b2_list_keys",
    "list_file_versions": "{}/b2api/v2/b2_list_file_versions",
    "list_file_names": "{}/b2api/v2/b2_list_file_names",
    "list_buckets": "{}/b2api/v2/b2_list_buckets",

    "hide_file": "{}/b2api/v2/b2_hide_file",

    "get_file_info": "{}/b2api/v2/b2_get_file_info",
    "get_upload_url": "{}/b2api/v2/b2_get_upload_url",
    "get_upload_part_url": "{}/b2api/v2/b2_get_upload_part_url",
    "get_download_authorization": "{}/b2api/v2/b2_get_download_authorization",

    "finish_large_file": "{}/b2api/v2/b2_finish_large_file",

    "download_file_by_name": "{}/file/{}/{}",
    "download_file_by_id": "{}/b2api/v2/b2_download_file_by_id?fileId={}",

    "delete_key": "{}/b2api/v2/b2_delete_key",
    "delete_file_version": "{}/b2api/v2/b2_delete_file_version",
    "delete_bucket": "{}/b2api/v2/b2_delete_bucket",

    "create_key": "{}/b2api/v2/b2_create_key",
    "create_bucket": "{}/b2api/v2/b2_create_bucket",

    "copy_part": "{}/b2api/v2/b2_copy_part",
    "copy_file": "{}/b2api/v2/b2_copy_file",

    "cancel_large_file": "{}/b2api/v2/b2_cancel_large_file",
}