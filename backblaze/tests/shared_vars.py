import argparse

cli = argparse.ArgumentParser()

cli.add_argument("--key_id", type=str, default="")
cli.add_argument("--key", type=str, default="")

args = vars(cli.parse_args())

KEY_ID = args["key_id"]
KEY = args["key"]
