import hashlib
import json
import os

import dxpy
import dxpy.api as dnanexus_api
import requests

class DNAnexus():

    def __init__(self, access_token=None):
        print("init")
        self.__access_token__ = access_token
        print("acc", access_token)
        if access_token:
            os.environ['dna_nexus_access_token'] = self.__access_token__
        print(os.environ['dna_nexus_access_token'])
        auth = {"auth_token_type": "Bearer", "auth_token": self.__access_token__ if access_token else os.environ.get('dna_nexus_access_token')}
        dxpy.set_api_server_info(host="api.dnanexus.com",port="443",protocol="https")
        if access_token:
            dxpy.set_security_context(auth)
        # print("s",dxpy.APISERVER_HOST, dxpy.APISERVER_PORT, dxpy.APISERVER_PROTOCOL)
        # print(os.environ.get("DX_SECURITY_CONTEXT"),os.environ.get("DX_APISERVER_HOST"))
        
    def get_projects_list(self):
        print(os.environ.get('dna_nexus_access_token'))
        input_params = {"level":"VIEW", "describe":{'fields':{'name':True}}, "explicitPermission":True, 'public':False}
        projects = dnanexus_api.system_find_projects(input_params=input_params)
        project_list = [project['describe'] for project in projects['results']]
        return project_list


    def describe_project(self, project_id):
        input_params = {"fields":{"allowedExecutables":True}}
        project = dnanexus_api.project_describe(object_id=project_id, input_params=input_params)
        return project

    def get_workflow_list(self, project_id):
        input_params = {"class":"workflow", "scope":{"project":project_id}, "describe":{"fields":{"name":True}}}
        data_objs = dnanexus_api.system_find_data_objects(input_params=input_params)
        workflow_list = [workflow['describe'] for workflow in data_objs['results']]
        return workflow_list


    def get_analysis_list(self, project_id):
        input_params = {"class":"analysis","project":project_id, "describe":{"fields":{"name":True}}}
        analysis_objs = dnanexus_api.system_find_analyses(input_params=input_params)
        analysis_list = [analysis['describe'] for analysis in analysis_objs['results']]
        return analysis_list

    def describe_workflow(self, workflow_id):
        workflow = dnanexus_api.workflow_describe(object_id=workflow_id)
        return workflow


    def describe_analysis(self, analysis_id):
        analysis = dnanexus_api.analysis_describe(object_id=analysis_id)
        return analysis

    def describe_applet(self, applet_id):
        applet = dnanexus_api.applet_describe(object_id=applet_id)
        return applet

    def describe_app(self, app_id):
        app = dnanexus_api.app_describe(app_name_or_id=app_id)
        return app

    def upload_file_to_project(self, project_id, name):
        try:
            file_name = f"{name}.json"
            print("name", name)
            input_params = {"project":project_id, "name":file_name}

            file_id = dnanexus_api.file_new(input_params=input_params)
            print("fd",file_id['id'])
            file_size = os.path.getsize('app/schemas/biocompute_export.json')
            
            with open('app/schemas/biocompute_export.json', 'rb') as bco_json:
                file_bytes = bco_json.read()
                md5 = hashlib.md5(file_bytes).hexdigest()
                print("fs",file_size)
                # md5 = result
                print("md5", md5)


                # md6 = hashlib.
                
                
                response = dnanexus_api.file_upload(object_id=file_id['id'], input_params={"size":file_size, "md5":md5, "index":1, "body":{}})
                print("re", response)
                bco_json.close()
                url = response['url']
                headers = response['headers']

                print("he", headers)
                
                
                with open('app/schemas/biocompute_export.json', 'rb') as bco_upl_json:
                    # file_upl_bytes = bco_upl_json.read()
                    # md6 = hashlib.md5(file_upl_bytes).hexdigest()
                    # print("mds", md6)
                    # files = {"file": file_upl_bytes} 
                    res = requests.put(url, data=bco_upl_json, headers=headers)
                    print("res", res.status_code)
                    if res.status_code == 200:
                        id = dnanexus_api.file_close(object_id=file_id['id'])
                        print("id after upload", id)

            return file_id
        except Exception as e:
            print(f"error -- {repr(e)}")
        
    
    
    
    
    
    
    
    
    
    
    # def get_auth_token():
    #     dna_api.DXHTTPRequest()

    # def get_workflow_details():
    #     name = dxpy.get_auth_server_name()
    #     print('n', name)
    #     ip = {"fields":{"allowedExecutables":True}}
    #     project = dna_api.project_describe(object_id="project-G9FQX8Q0q5y4kJ8ZGKpv2fk6", input_params=ip)
    #     # result =  dna_api.workflow_describe(object_id="workflow-G9FQXgj0q5yKyJgf0p6Zg7jp")
    #     # app_result = dna_api.applet_describe(object_id="applet-FP7590j0kJJ01J6z2vjF31Vj")
    #     # app = dna_api.app_describe(app_name_or_id="app-flexbar_fastq_read_trimmer/1.4.0")
    #     # input_params = {"limit":2,"level":"VIEW", "describe":True}
    #     # projects = dna_api.system_find_projects(input_params=input_params)
    #     print("r",project)
