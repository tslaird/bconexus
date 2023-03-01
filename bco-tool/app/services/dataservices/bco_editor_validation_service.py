import json
import re

from jsonschema import validate




class BcoEditorValidation():

    def __init__(self, bco) -> None:
        self.bco = bco
        self.description_domain = bco['description_domain'] if "description_domain" in bco.keys() else None 
        self.usability_domain = bco['usability_domain'] if "usability_domain" in bco.keys() else None
        self.provenance_domain = bco['provenance_domain'] if "provenance_domain" in bco.keys() else None
        self.parametric_domain = bco['parametric_domain'] if "parametric_domain" in bco.keys() else None
        self.execution_domain = bco['execution_domain'] if "execution_domain" in bco.keys() else None
        self.error_domain = bco['error_domain'] if "error_domain" in bco.keys() else None
        self.io_domain = bco['io_domain'] if "io_domain" in bco.keys() else None


    def validate_bco_editor_json(self):
        self.validate_2791_object(self.bco)
        if self.description_domain:
            self.validate_description_doamin(self.description_domain)
        if self.error_domain:
            self.validate_error_domain(self.error_domain)
        if self.execution_domain:
            self.validate_execution_domain(self.execution_domain)
        if self.io_domain:
            self.validate_io_domain(self.io_domain)
        if self.parametric_domain:
            self.validate_parametric_domain(self.parametric_domain)
        if self.provenance_domain:
            self.validate_provenance_domain(self.provenance_domain)
        if self.usability_domain:
            self.validate_usability_domain(self.usability_domain)
        return True, "Validation successfull"
        
        
    def validate_2791_object(self, bco):
        # with open("app/services/dataservices/2791object.json", "r") as schema2791:
        #     schema_2791 = json.load(schema2791)
        # validate(bco, schema_2791)
        required_keys = [ "object_id","spec_version","etag","provenance_domain","usability_domain",
                         "description_domain","execution_domain","io_domain"]

        for key in required_keys:
            if key not in bco.keys():
                raise Exception(f"{key} is reqiured.")
            else:
                if key == "object_id":
                    if not isinstance(bco[key], str):
                        raise Exception(f"{key} should be a string.")
                if key == "spec_version":
                    if not isinstance(bco[key], str):
                        raise Exception(f"{key} should be a string.")
                if key == "etag":
                    if not isinstance(bco[key], str):
                        raise Exception(f"{key} should be a string.")
                    pattern = re.compile(r"^([A-Za-z0-9]+)$")
                    if not re.fullmatch(pattern, bco[key]):
                        raise Exception(f"{key} should follow the regex pattern ^([A-Za-z0-9]+)$")

    def validate_provenance_domain(self, provenance_domain):
        # with open("app/services/dataservices/provenance_domain.json", "r") as prove_schema:
        #     provenance_domain_schema = json.load(prove_schema)
        # validate(provenance_domain, provenance_domain_schema)
        required_keys = [ "name", "version", "created", "modified", "contributors", "license"]
        non_required_keys = ["review", "derived_from", "obsolete_after", "embargo"]

        for key in required_keys:
            if key not in provenance_domain.keys():
                raise Exception(f"{key} is reqiured in provenance domain.")
            else:
                if key in ["name", "version", "created", "modified", "license"]:
                    if not isinstance(provenance_domain[key], str):
                        raise Exception(f"{key} in provenance domain should be a string.")
                if key == "contributors":
                    if not isinstance(provenance_domain[key], list):
                        raise Exception(f"{key} in provenance domain should be an array.")
                    else:
                        for index, contributor in enumerate(provenance_domain[key]):
                            if not isinstance(contributor, dict):
                                raise Exception(f"contributor {index} in provenance domain should be an object.")
                            else:
                                self.validate_contributor(index, contributor, True)

        
        for key in non_required_keys:
            if key in provenance_domain.keys():
                if key in ["derived_from", "obsolete_after"]:
                    if not isinstance(provenance_domain[key], str):
                        raise Exception(f"{key} in provenance domain should be a string.")
                if key == "embargo":
                    if not isinstance(provenance_domain[key], dict):
                        raise Exception(f"{key} in provenance domain should be a object.")
                    else:
                        required_items = ["start_time", "end_time"]
                        for item in required_items:
                            if item not in provenance_domain[key].keys():
                                raise Exception(f"{item} is reqiured in {key} under provenance domain.")
                            else:
                                if item in required_items:
                                    if not isinstance(item, str):
                                        raise Exception(f"{item} in {key} under provenance domain should be a string.")
                                    
                if key == "review":
                    if not isinstance(provenance_domain[key], list):
                        raise Exception(f"{key} in provenance domain should be an array.")
                    else:
                        for index, review in enumerate(provenance_domain[key]):
                            if not isinstance(review, dict):
                                raise Exception(f"review {index} in provenance domain should be an object.")
                            else:
                                self.validate_review(index, review)

    def validate_review(self, index, review):
        required_keys = ["status", "reviewer"]
        non_required_keys = ["date", "reviewer_comment"]
        status_enum = ["unreviewed", "in-review", "approved", "rejected", "suspended"]
        for key in required_keys:
            if key not in review.keys():
                raise Exception(f"{key} is reqiured in review {index} under provenance domain.")
            else:
                if key == "reviewer":
                    if not isinstance(review[key], dict):
                        raise Exception(f"reviewer in review {index} in provenance domain should be an object.")
                    else:
                        self.validate_contributor(index, review[key], False)
                
                if key == "status":
                    if not isinstance(review[key], str) and (review[key] not in status_enum):
                        raise Exception(f"{key} in review {index} under provenance domain is not an acceptable value.")
        
        for key in non_required_keys:
            if key in review.keys():
                if key in ["date", "reviewer_comment"]:
                    if not isinstance(review[key], str):
                        raise Exception(f"{key} in review {index} under provenance domain should be a string.")

    def validate_contributor(self, index, contributor, is_contributor=True):
        role = "contributor" if is_contributor else "reviewer"
        required_keys = ["contribution", "name"]
        non_required_keys = ["affiliation", "email", "orcid"]
        contribution_enum =  [ "authoredBy","contributedBy","createdAt","createdBy",
                              "createdWith","curatedBy","derivedFrom","importedBy","importedFrom",
                              "providedBy","retrievedBy","retrievedFrom","sourceAccessedBy"]


        for key in required_keys:
            if key not in contributor.keys():
                raise Exception(f"{key} is reqiured in {role} {index} under provenance domain.")
            else:
                if key == "name":
                    if not isinstance(contributor[key], str):
                        raise Exception(f"{key} in {role} {index} under provenance domain should be a string.")
                if key == "contribution":
                    if not isinstance(contributor[key], list):
                        raise Exception(f"{key} in {role} {index} under provenance domain should be an array.")
                    else:
                        for item in contributor[key]:
                            if not isinstance(item, str) and (item not in contribution_enum):
                                raise Exception(f"{key} in {role} {index} under provenance domain is not an acceptable value.")
        
        for key in non_required_keys:
            if key in contributor.keys():
                if key in ["affiliation", "email", "orcid"]:
                    if not isinstance(contributor[key], str):
                        raise Exception(f"{key} in {role} {index} under provenance domain should be a string.")
      
    def validate_usability_domain(self, usability_domain):

        if not isinstance(usability_domain, list):
            raise Exception(f"usability domain should be an array.")
        else:
            for index, item in enumerate(usability_domain):
                if not isinstance(item, str):
                    raise Exception(f"Item {index} in usability domain should be a string.")

    def validate_description_doamin(self, description_domain):
        # with open("app/services/dataservices/description_domain.json", "r") as desc_schema:
        #     description_domain_schema = json.load(desc_schema)
        # validate(description_domain, description_domain_schema)
        required_keys = [ "keywords", "pipeline_steps"]
        non_required_keys = ["xref", "platform"]

        for key in required_keys:
            if key not in description_domain.keys():
                raise Exception(f"{key} is required in description domain.")
            else:
                if key == "keywords":
                    if not isinstance(description_domain[key], list):
                        raise Exception(f"{key} in description domain should be an array.")
                    else:
                        for index,item in enumerate(description_domain[key]):
                            if not isinstance(item, str):
                                raise Exception(f"keyword {index} under description domain should be a string.")
                if key == "pipeline_steps":
                    if not isinstance(description_domain[key], list):
                        raise Exception(f"{key} in description domain should be an array.")
                    else:
                        for index,pipeline_step in enumerate(description_domain[key]):
                            if not isinstance(pipeline_step, dict):
                                raise Exception(f"pipeline_step {index} under description domain should be an object.")
                            else:
                                self.validate_pipeline_step(index, pipeline_step)
        
        for key in non_required_keys:
            if key in description_domain.keys():
                if key in ["xref", "platform"]:
                    if not isinstance(description_domain[key], list):
                        raise Exception(f"{key} in description domain should be an array.")
                    else:
                        if key == "xref":
                            for index,xref in enumerate(description_domain[key]):
                                if not isinstance(xref, dict):
                                    raise Exception(f"xref {index} under description domain should be an object.")
                                else:
                                    self.validate_xref(index, xref)
                        if key == "platform":
                            for index, platform in enumerate(description_domain[key]):
                                if not isinstance(platform, str):
                                    raise Exception(f"platform {index} under description domain should be a string.")
    
    def validate_xref(self, index, xref):
        required_keys = ["namespace", "name", "ids", "access_time"]
        for key in required_keys:
            if key not in xref.keys():
                raise Exception(f"{key} is required in xref {index} under description domain.")
            else:
                if key in ["namespace", "name", "access_time"]:
                    if not isinstance(xref[key], str):
                        raise Exception(f"{key} in xref {index} under description domain should be a string.")
                if key == "ids":
                    if not isinstance(xref[key], list):
                        raise Exception(f"{key} in xref {index} under description domain should be an array.")
                    else:
                        for local_index, id in enumerate(xref[key]):
                            if not isinstance(id, str):
                                raise Exception(f"{key} {local_index} in xref {index} under description domain should be a string.")
                
    def validate_pipeline_step(self, index, pipeline_step):
        required_keys = ["step_number","name","description","input_list","output_list"]
        non_required_keys=["prerequisite","version"]
        

        for key in required_keys:
            if key not in pipeline_step.keys():
                raise Exception(f"{key} is required in pipeline_step {index} under description domain.")
            else:
                if key in ["name","description"]:
                    if not isinstance(pipeline_step[key], str):
                        raise Exception(f"{key} in pipeline_step {index} under description domain should be a string.")
                if key == "step_number":
                    if not isinstance(pipeline_step[key], int):
                        raise Exception(f"{key} in pipeline_step {index} under description domain should be an integer.")
                if key in ["input_list","output_list"]:
                    if not isinstance(pipeline_step[key], list):
                        raise Exception(f"{key} in pipeline_step {index} under description domain should be an array.")
                    else:
                        for local_index, uri in enumerate(pipeline_step[key]):
                            if not isinstance(uri, dict):
                                raise Exception(f"{key} {local_index} in pipeline_step {index} under description domain should be an object.")
                            else:
                                is_input_list = True if key == "input_list" else False
                                self.validate_input_list(index, local_index, uri, is_input_list)
        
        for key in non_required_keys:
            if key in pipeline_step.keys():
                if key == "version":
                    if not isinstance(pipeline_step[key], str):
                        raise Exception(f"{key} in pipeline_step {index} under description domain should be a string.")
                if key == "prerequisite":
                    if not isinstance(pipeline_step[key], list):
                        raise Exception(f"{key} in pipeline_step {index} under description domain should be an array.")
                    else:
                        for local_index, prerequisite in enumerate(pipeline_step[key]):
                            if not isinstance(prerequisite, dict):
                                raise Exception(f"{key} {local_index} in pipeline_step {index} under description domain should be an object.")
                            else:
                                self.validate_prerequisite(index, local_index, prerequisite)

    def validate_prerequisite(self, index, local_index, prerequisite):
        required_keys = ["uri", "name"]
        for key in required_keys:
            if key not in prerequisite.keys():
                raise Exception(f"{key} is required for prerequisite {local_index} in pipeline_step {index} under description domain.")
            else:
                if key == "name":
                    if not isinstance(prerequisite[key], str):
                        raise Exception(f"{key} for prerequisite {local_index} in pipeline_step {index} under description domain should be a string.")
                if key == "uri":
                    if not isinstance(prerequisite[key], dict):
                        raise Exception(f"{key} for prerequisite {local_index} in pipeline_step {index} under description domain should be an object.")
                    else:
                        self.validate_uri(index, local_index, prerequisite[key])

    def validate_uri(self, index, local_index, uri):
        required_keys = ["uri"]
        non_required_keys = ["filename", "access_time", "sha1_checksum"]

        for key in required_keys:
            if key not in uri.keys():
                raise Exception(f"{key} is required for prerequisite {local_index} in pipeline_step {index} under description domain.")
            else:
                if key == "uri":
                    if not isinstance(uri[key], str):
                        raise Exception(f"{key} for prerequisite {local_index} in pipeline_step {index} under description domain should be a string.")
        
        for key in non_required_keys:
            if key in uri.keys():
                if key in ["filename", "access_time", "sha1_checksum"]:
                    if not isinstance(uri[key], str):
                        raise Exception(f"{key} for prerequisite {local_index} in pipeline_step {index} under description domain should be a string.")

    def validate_input_list(self, index, local_index, uri, is_input_list):
        role = "input_list" if is_input_list else "output_list"
        required_keys = ["uri"]
        non_required_keys = ["filename", "access_time", "sha1_checksum"]

        for key in required_keys:
            if key not in uri.keys():
                raise Exception(f"{key} is required for {role} {local_index} in pipeline_step {index} under description domain.")
            else:
                if key == "uri":
                    if not isinstance(uri[key], str):
                        raise Exception(f"{key} for {role} {local_index} in pipeline_step {index} under description domain should be a string.")
        
        for key in non_required_keys:
            if key in uri.keys():
                if key in ["filename", "access_time", "sha1_checksum"]:
                    if not isinstance(uri[key], str):
                        raise Exception(f"{key} for {role} {local_index} in pipeline_step {index} under description domain should be a string.")

    def validate_execution_domain(self, execution_domain):
        # with open("app/services/dataservices/execution_domain.json", "r") as exec_schema:
        #     execution_domain_schema = json.load(exec_schema)
        # validate(execution_domain, execution_domain_schema)
        required_keys = [ "script", "script_driver", "software_prerequisites",
                         "external_data_endpoints", "environment_variables"]
        
        for key in required_keys:
            if key not in execution_domain.keys():
                raise Exception(f"{key} is required in execution domain.")
            else:
                if key in ["script", "software_prerequisites", "external_data_endpoints"]:
                    if not isinstance(execution_domain[key], list):
                        raise Exception(f"{key} in execution domain should be an array.")
                    else:
                        if key == "script":
                            for index, script_uri in enumerate(execution_domain[key]):
                                if not isinstance(script_uri, dict):
                                    raise Exception(f"script {index} under execution domain should be an object.")
                                elif "uri" not in script_uri.keys():
                                    raise Exception(f"uri in script {index} under execution domain is required.")
                                elif not isinstance(script_uri["uri"], dict):
                                    raise Exception(f"uri in script {index} under execution domain should be an object.")
                                else:
                                    self.validate_script_uri(index, script_uri["uri"])
                        if key == "software_prerequisites":
                            for index, software_prerequisite in enumerate(execution_domain[key]):
                                if not isinstance(software_prerequisite, dict):
                                    raise Exception(f"software_prerequisite {index} under execution domain should be an object.")
                                else:
                                    self.validate_software_prerequisites(index, software_prerequisite)
                        if key == "external_data_endpoints":
                            for index, external_data_endpoint in enumerate(execution_domain[key]):
                                if not isinstance(external_data_endpoint, dict):
                                    raise Exception(f"external_data_endpoint {index} under execution domain should be an object.")
                                else:
                                    self.validate_external_data_endpoint(index, external_data_endpoint)

                if key == "environment_variables":
                    if not isinstance(execution_domain[key], dict):
                        raise Exception(f"{key} in execution domain should be an object.")
                    else:
                        self.validate_environment_variables(execution_domain[key])

                if key == "script_driver":
                    if not isinstance(execution_domain[key], str):
                        raise Exception(f"{key} in execution domain should be a string.")

    def validate_environment_variables(self,environment_variables):
        for key in environment_variables.keys():
            pattern = re.compile(r"^[a-zA-Z_]+[a-zA-Z0-9_]*$")
            if not re.fullmatch(pattern, key):
                raise Exception(f"key {key} in environment_variables under execution domain should follow the regex pattern ^[a-zA-Z_]+[a-zA-Z0-9_]*$ ")
            if not isinstance(environment_variables[key], str):
                raise Exception(f"{key} in environment_variables under execution domain should be a string.")

    def validate_external_data_endpoint(self, index, external_data_endpoint):
        required_keys = ["name", "url"]
        for key in required_keys:
            if key not in external_data_endpoint.keys():
                raise Exception(f"{key} is required in external_data_endpoint {index} under execution domain.")
            else:
                if key in ["name", "url"]:
                    if not isinstance(external_data_endpoint[key], str):
                        raise Exception(f"{key} in external_data_endpoint {index} under execution domain should be a string.")

    def validate_software_prerequisites(self, index, software_prerequisite):
        required_keys = ["name", "version", "uri"]
        for key in required_keys:
            if key not in software_prerequisite.keys():
                raise Exception(f"{key} is required in software_prerequisite {index} under execution domain.")
            else:
                if key in ["name", "version"]:
                    if not isinstance(software_prerequisite[key], str):
                        raise Exception(f"{key} in software_prerequisite {index} under execution domain should be a string.")
                if key == "uri":
                    if not isinstance(software_prerequisite[key], dict):
                        raise Exception(f"{key} in software_prerequisite {index} under execution domain should be an object.")
                    else:
                        self.validate_sw_prereq_uri(index, software_prerequisite[key])

    def validate_sw_prereq_uri(self, index, sw_uri):
        required_keys = ["uri"]
        non_required_keys = ["filename", "access_time", "sha1_checksum"]

        for key in required_keys:
            if key not in sw_uri.keys():
                raise Exception(f"{key} is required in software_prerequisite {index} under execution domain.")
            else:
                if key == "uri":
                    if not isinstance(sw_uri[key], str):
                        raise Exception(f"{key} in software_prerequisite {index} under execution domain should be a string.")
        
        for key in non_required_keys:
            if key in sw_uri.keys():
                if key in ["filename", "access_time", "sha1_checksum"]:
                    if not isinstance(sw_uri[key], str):
                        raise Exception(f"{key} in software_prerequisite {index} under execution domain should be a string.")

    def validate_script_uri(self, index, script_uri):
        required_keys = ["uri"]
        non_required_keys = ["filename", "access_time", "sha1_checksum"]

        for key in required_keys:
            if key not in script_uri.keys():
                raise Exception(f"{key} is required in script {index} under execution domain.")
            else:
                if key == "uri":
                    if not isinstance(script_uri[key], str):
                        raise Exception(f"{key} in script {index} under execution domain should be a string.")
        
        for key in non_required_keys:
            if key in script_uri.keys():
                if key in ["filename", "access_time", "sha1_checksum"]:
                    if not isinstance(script_uri[key], str):
                        raise Exception(f"{key} in script {index} under execution domain should be a string.")
        
    def validate_io_domain(self, io_domain):
        # with open("app/services/dataservices/io_domain.json", "r") as io_schema:
        #     io_domain_schema = json.load(io_schema)
        # validate(io_domain, io_domain_schema)
        required_keys = ["input_subdomain","output_subdomain"]
        for key in required_keys:
            if key not in io_domain.keys():
                raise Exception(f"{key} is reqiured in io domain.")
            else:
                if key in ["input_subdomain","output_subdomain"]:
                    if not isinstance(io_domain[key], list):
                        raise Exception(f"{key} in io domain should be an array.")
                    else:
                        for index, subdomain in enumerate(io_domain[key]):
                            if key == "input_subdomain":
                                if not isinstance(subdomain, dict):
                                    raise Exception(f"input_subdomain {index} in io domain should be an object.")
                                else:
                                    self.validate_input_subdomain(index, subdomain)
                            if key == "output_subdomain":
                                if not isinstance(subdomain, dict):
                                    raise Exception(f"output_subdomain {index} in io domain should be an object.")
                                else:
                                    self.validate_output_subdomain(index, subdomain)

    def validate_output_subdomain(self, index, output_subdomain):
        required_keys = ["uri", "mediatype"]
        
        for key in required_keys:
            if key not in output_subdomain.keys():
                raise Exception(f"{key} is reqiured in output_subdomain {index} under io domain.")
            else:
                if key == "uri":
                    self.validate_io_uri(index, output_subdomain[key], "output_subdomain")
                if key == "mediatype":
                    if not isinstance(output_subdomain[key], str):
                        raise Exception(f"{key} in output_subdomain {index} under io domain should be a string.")
                    pattern = re.compile(r"^(.*)$")
                    if not re.fullmatch(pattern, output_subdomain[key]):
                        raise Exception(f"{key} in output_subdomain {index} under io domain should follow the regex pattern ^(.*)$")
                    
    def validate_input_subdomain(self, index, input_subdomain):
        required_keys = ["uri"]
        
        for key in required_keys:
            if key not in input_subdomain.keys():
                raise Exception(f"{key} is reqiured in input_subdomain {index} under io domain.")
            else:
                if key == "uri":
                    self.validate_io_uri(index, input_subdomain[key], "input_subdomain")
 
    def validate_io_uri(self, index, isd_uri, subdomain):
        required_keys = ["uri"]
        non_required_keys = ["filename", "access_time", "sha1_checksum"]

        for key in required_keys:
            if key not in isd_uri.keys():
                raise Exception(f"{key} is required in {subdomain} {index} under io domain.")
            else:
                if key == "uri":
                    if not isinstance(isd_uri[key], str):
                        raise Exception(f"{key} in {subdomain} {index} under io domain should be a string.")
        
        for key in non_required_keys:
            if key in isd_uri.keys():
                if key in ["filename", "access_time", "sha1_checksum"]:
                    if not isinstance(isd_uri[key], str):
                        raise Exception(f"{key} in {subdomain} {index} under io domain should be a string.")

    def validate_parametric_domain(self, parametric_domain):
        if not isinstance(parametric_domain, list):
            raise Exception(f"parametric domain should be an array.")
        else:
            for index, parameter in enumerate(parametric_domain):
                if not isinstance(parameter, dict):
                    raise Exception(f"Item {index} in parametric domain should be an object.")
                else:
                    self.validate_parameter(index, parameter)
    
    def validate_parameter(self, index, parameter):
        required_keys = ["param","value","step"]
        for key in required_keys:
            if key not in parameter.keys():
                raise Exception(f"{key} is reqiured in item {index} under parametric domain.")
            else:
                if key in ["param","value"]:
                    if not isinstance(parameter[key], str):
                        raise Exception(f"{key} in item {index} under parametric domain should be a string.")
                if key == "step":
                    if not isinstance(parameter[key], str):
                        raise Exception(f"{key} in item {index} under parametric domain should be a string.")
                    pattern = re.compile(r"^(.*)$")
                    if not re.fullmatch(pattern, parameter[key]):
                        raise Exception(f"{key} in item {index} under parametric domain should follow the regex pattern ^(.*)$")

    def validate_error_domain(self, error_domain):
        # with open("app/services/dataservices/error_domain.json", "r") as error_schema:
        #     error_domain_schema = json.load(error_schema)
        # validate(error_domain, error_domain_schema)
        required_keys = ["empirical_error","algorithmic_error"]

        for key in required_keys:
            if key not in error_domain.keys():
                raise Exception(f"{key} is reqiured in error domain.")
            else:
                if not isinstance(error_domain[key], dict):
                    raise Exception(f"{key} in error domain should be an object.")


    



    

    

    
