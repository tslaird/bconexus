import json
import os
import subprocess

HOME = os.getenv("HOME")
PFDA_CONFIG = os.path.join(HOME, ".pfda_config")
PFDA_SERVER = ""


class PFDAClient:
    scope = ""
    server = PFDA_SERVER or ""

    def __init__(self, access_token="") -> None:
        self.__access_token__ = access_token or os.environ.get("PFDA_ACCESS_TOKEN")
        if not os.path.exists(PFDA_CONFIG):
            pfda_config = {
                "key": "",
                "server": self.server,
                "scope": self.scope,
            }
        else:
            with open(PFDA_CONFIG, "r") as conf:
                pfda_config = json.load(conf)

        if self.__access_token__:
            os.environ["PFDA_ACCESS_TOKEN"] = self.__access_token__
            pfda_config["key"] = self.__access_token__
            with open(PFDA_CONFIG, "w") as conf:
                json.dump(pfda_config, conf)

    def get_spaces_list(self):
        try:
            cmd = ["pfda", "ls-spaces", "-json"]
            spaces = subprocess.check_output(cmd).decode("utf-8")
            spaces_list = json.loads(spaces)
            return spaces_list
        except Exception as e:
            raise Exception(f"error list PFDA spaces -- {repr(e)}")

    def get_folders_list(self, space_id=None):
        try:
            cmd = ["pfda", "ls", "-folders", "-json"]
            if space_id:
                cmd.extend(["-space-id", f"{space_id}"])
            folders = subprocess.check_output(cmd).decode("utf-8")
            folders_list = json.loads(folders).get("files")
            return folders_list
        except Exception as e:
            raise Exception(f"error list PFDA folders -- {repr(e)}")

    def upload_local_file(self, filepath, folder_id=None, space_id=None):
        try:
            cmd = ["pfda", "upload-file", filepath]
            if folder_id:
                cmd.extend(["-folder-id", f"{folder_id}"])
            if space_id:
                cmd.extend(["-space-id", f"{space_id}"])
            subprocess.run(cmd)
            return True
        except Exception as e:
            raise Exception(f"error uploading to PFDA -- {repr(e)}")
