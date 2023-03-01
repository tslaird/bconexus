import requests
import json

class BcoDB():
    def __init__(self, host_url, prefix, owner_group, access_token):
        self.__host_url__ = host_url
        self.__prefix__ = prefix
        self.__owner_group__ = owner_group
        self.__access_token__ = access_token

    def upload(self):
        try:
            with open("app/schemas/biocompute_export.json", "r") as file:
                file_content = json.load(file)

            data = {"POST_api_objects_draft_create": [{"prefix":self.__prefix__, 
            "schema":"IEEE", 
            "owner_group": self.__owner_group__,
            "contents":file_content
            }
            ]}
            response = requests.post(url=self.__host_url__,data=json.dumps(data), headers={ "Authorization": f"Token {self.__access_token__}",
            "Content-type": "application/json; charset=UTF-8"})
            
            if response.status_code == 200:
                print("file uploaded")
                return "File uploaded to BCO DB"
            else:
                print("error", response.__dict__)
                return None
        except Exception as e:
            print(f"error uploading to BCO DB -- {repr(e)}")
            return None