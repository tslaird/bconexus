

class BcoCleanUp():

    def __init__(self, bco) -> None:
        self.bco = bco
        self.description_domain = bco['description_domain'] if "description_domain" in bco.keys() else None 
        self.usability_domain = bco['usability_domain'] if "usability_domain" in bco.keys() else None
        self.provenance_domain = bco['provenance_domain'] if "provenance_domain" in bco.keys() else None
        self.parametric_domain = bco['parametric_domain'] if "parametric_domain" in bco.keys() else None
        self.execution_domain = bco['execution_domain'] if "execution_domain" in bco.keys() else None
        self.error_domain = bco['error_domain'] if "error_domain" in bco.keys() else None
        self.io_domain = bco['io_domain'] if "io_domain" in bco.keys() else None


    def cleanup_bco_json(self):
        self.cleanup_2791_object(self.bco)
        if self.description_domain:
            self.cleanup_description_doamin(self.description_domain)
        if self.error_domain:
            self.cleanup_error_domain(self.error_domain)
        if self.execution_domain:
            self.cleanup_execution_domain(self.execution_domain)
        if self.io_domain:
            self.cleanup_io_domain(self.io_domain)
        if self.parametric_domain:
            self.cleanup_parametric_domain(self.parametric_domain)
        if self.provenance_domain:
            self.cleanup_provenance_domain(self.provenance_domain)
        if self.usability_domain:
            self.cleanup_usability_domain(self.usability_domain)
        return True, "Cleanup for BCO export Successful"
        
        
    def cleanup_2791_object(self, bco):
        required_keys = [ "object_id","spec_version","etag","provenance_domain","usability_domain",
                         "description_domain","execution_domain","io_domain"]
        non_required_keys = ["parametric_domain","error_domain","extension_domain"]

        for key in non_required_keys:
            if key in list(bco.keys()):
                if not bco[key]:
                    bco.pop(key)

    def cleanup_provenance_domain(self, provenance_domain):
        required_keys = [ "name", "version", "created", "modified", "contributors", "license"]
        non_required_keys = ["review", "derived_from", "obsolete_after", "embargo"]

        for key in required_keys:
            if key in ["name", "version", "created", "modified", "license"]:
                pass
            if key == "contributors":
                for index, contributor in enumerate(provenance_domain[key]):
                    if not contributor:
                        pass
                    else:
                        self.cleanup_contributor(index, contributor, True)

        for key in non_required_keys:
            if key in list(provenance_domain.keys()):
                if key in ["derived_from", "obsolete_after"]:
                    if not provenance_domain[key]:
                        provenance_domain.pop(key)
                if key == "embargo":
                    for c_key in list(provenance_domain[key].keys()):
                        if not provenance_domain[key][c_key]:
                            provenance_domain[key].pop(c_key)
                    if not provenance_domain[key]:
                        provenance_domain.pop(key)
                                    
                if key == "review":
                    remove_review = []
                    for index, review in enumerate(provenance_domain[key]):
                        self.cleanup_review(index, review)
                        if not review:
                            remove_review.append(index)
                    [provenance_domain[key].pop(review) for review in sorted(remove_review, reverse=True)]
                    if not provenance_domain[key]:
                        provenance_domain.pop(key)

    def cleanup_review(self, index, review):
        required_keys = ["status", "reviewer"]
        non_required_keys = ["date", "reviewer_comment"]
        status_enum = ["unreviewed", "in-review", "approved", "rejected", "suspended"]
        for key in required_keys:
            if key == "reviewer":
                self.cleanup_contributor(index, review[key], False)
                if not review[key]:
                    review.pop(key)
            
            if key == "status":
                if not review[key]:
                    review.pop(key)
        
        for key in non_required_keys:
            if key in list(review.keys()):
                if key in ["date", "reviewer_comment"]:
                    if not review[key]:
                        review.pop(key)
        if not any([review[key] for key in list(review.keys())]):
            [review.pop(key) for key in list(review.keys())]

    def cleanup_contributor(self, index, contributor, is_contributor=True):
        role = "contributor" if is_contributor else "reviewer"
        required_keys = ["contribution", "name"]
        non_required_keys = ["affiliation", "email", "orcid"]
        contribution_enum =  [ "authoredBy","contributedBy","createdAt","createdBy",
                              "createdWith","curatedBy","derivedFrom","importedBy","importedFrom",
                              "providedBy","retrievedBy","retrievedFrom","sourceAccessedBy"]

        for key in required_keys:
            if key == "name":
                pass
            if key == "contribution":
                pass
        
        for key in non_required_keys:
            if key in list(contributor.keys()):
                if key in ["affiliation", "email", "orcid"]:
                    if not contributor[key]:
                        contributor.pop(key)
        
        if role == "reviewer":
            if not any([contributor[key] for key in list(contributor.keys())]):
                [contributor.pop(key) for key in list(contributor.keys())]
      
    def cleanup_usability_domain(self, usability_domain):
        for index, item in enumerate(usability_domain):
            if not item:
                pass

    def cleanup_description_doamin(self, description_domain):
        required_keys = [ "keywords", "pipeline_steps"]
        non_required_keys = ["xref", "platform"]

        for key in required_keys:
            if key == "keywords":
                pass
            if key == "pipeline_steps":
                for index,pipeline_step in enumerate(description_domain[key]):
                    self.cleanup_pipeline_step(index, pipeline_step)
        
        for key in non_required_keys:
            if key in list(description_domain.keys()):
                if key in ["xref", "platform"]:
                    if key == "xref":
                        remove_xref = []
                        for index,xref in enumerate(description_domain[key]):
                            self.cleanup_xref(index, xref)
                            if not xref:
                                remove_xref.append(index)
                        [description_domain[key].pop(xref) for xref in sorted(remove_xref,reverse=True)]
                        if not description_domain[key]:
                            description_domain.pop(key)
                    if key == "platform":
                        if not description_domain[key]:
                            description_domain.pop(key)
    
    def cleanup_xref(self, index, xref):
        required_keys = ["namespace", "name", "ids", "access_time"]
        for key in required_keys:
            if key in ["namespace", "name", "access_time"]:
                if not xref[key]:
                    xref.pop(key)
            if key == "ids":
                if not xref[key]:
                    xref.pop(key)
                
    def cleanup_pipeline_step(self, index, pipeline_step):
        required_keys = ["step_number","name","description","input_list","output_list"]
        non_required_keys=["prerequisite","version"]
        
        for key in required_keys:
            if key in ["name","description"]:
                pass
            if key == "step_number":
                pass
            if key in ["input_list","output_list"]:
                for local_index, uri in enumerate(pipeline_step[key]):
                    is_input_list = True if key == "input_list" else False
                    self.cleanup_input_list(index, local_index, uri, is_input_list)
        
        for key in non_required_keys:
            if key in list(pipeline_step.keys()):
                if key == "version":
                    if not pipeline_step[key]:
                        pipeline_step.pop(key)
                if key == "prerequisite":
                    remove_prereqs = []
                    for local_index, prerequisite in enumerate(pipeline_step[key]):
                        self.cleanup_prerequisite(index, local_index, prerequisite)
                        if not prerequisite:
                            remove_prereqs.append(local_index)
                    [pipeline_step[key].pop(prereq) for prereq in sorted(remove_prereqs, reverse=True)]

    def cleanup_prerequisite(self, index, local_index, prerequisite):
        required_keys = ["uri", "name"]
        for key in required_keys:
            if key == "name":
                if not prerequisite[key]:
                    pass
            if key == "uri":
                self.cleanup_uri(index, local_index, prerequisite[key])
        
        if not any([prerequisite[key] for key in required_keys]):
            [prerequisite.pop(key) for key in required_keys]


    def cleanup_uri(self, index, local_index, uri):
        required_keys = ["uri"]
        non_required_keys = ["filename", "access_time", "sha1_checksum"]

        for key in required_keys:
            if key == "uri":
                if not uri[key]:
                    pass
        
        for key in non_required_keys:
            if key in list(uri.keys()):
                if key in ["filename", "access_time", "sha1_checksum"]:
                    if not uri[key]:
                        uri.pop(key)
        
        if not any([uri[key] for key in list(uri.keys())]):
            [uri.pop(key) for key in list(uri.keys())]

    def cleanup_input_list(self, index, local_index, uri, is_input_list):
        role = "input_list" if is_input_list else "output_list"
        required_keys = ["uri"]
        non_required_keys = ["filename", "access_time", "sha1_checksum"]

        for key in required_keys:
            if key == "uri":
                pass
        
        for key in non_required_keys:
            if key in list(uri.keys()):
                if key in ["filename", "access_time", "sha1_checksum"]:
                    if not uri[key]:
                        uri.pop(key)

    def cleanup_execution_domain(self, execution_domain):
        required_keys = [ "script", "script_driver", "software_prerequisites",
                         "external_data_endpoints", "environment_variables"]
        
        for key in required_keys:
            
            if key in ["script", "software_prerequisites", "external_data_endpoints"]:
                
                if key == "script":
                    for index, script_uri in enumerate(execution_domain[key]):
                        self.cleanup_script_uri(index, script_uri["uri"])

                if key == "software_prerequisites":
                    for index, software_prerequisite in enumerate(execution_domain[key]):
                        self.cleanup_software_prerequisites(index, software_prerequisite)
                if key == "external_data_endpoints":
                    for index, external_data_endpoint in enumerate(execution_domain[key]):
                        self.cleanup_external_data_endpoint(index, external_data_endpoint)

            if key == "environment_variables":
                self.cleanup_environment_variables(execution_domain[key])

            if key == "script_driver":
                if not execution_domain[key]:
                    pass

    def cleanup_environment_variables(self,environment_variables):
        for key in list(environment_variables.keys()):
            if not environment_variables[key]:
                pass

    def cleanup_external_data_endpoint(self, index, external_data_endpoint):
        required_keys = ["name", "url"]
        for key in required_keys:
            if key in ["name", "url"]:
                if not external_data_endpoint[key]:
                    pass

    def cleanup_software_prerequisites(self, index, software_prerequisite):
        required_keys = ["name", "version", "uri"]
        for key in required_keys:
            if key in ["name", "version"]:
                if not software_prerequisite[key]:
                    pass
            if key == "uri":
                self.cleanup_sw_prereq_uri(index, software_prerequisite[key])

    def cleanup_sw_prereq_uri(self, index, sw_uri):
        required_keys = ["uri"]
        non_required_keys = ["filename", "access_time", "sha1_checksum"]

        for key in required_keys:
            if key == "uri":
                if not sw_uri[key]:
                    pass
        
        for key in non_required_keys:
            if key in list(sw_uri.keys()):
                if key in ["filename", "access_time", "sha1_checksum"]:
                    if not sw_uri[key]:
                        sw_uri.pop(key)

    def cleanup_script_uri(self, index, script_uri):
        required_keys = ["uri"]
        non_required_keys = ["filename", "access_time", "sha1_checksum"]

        for key in required_keys:
            if key == "uri":
                if not script_uri[key]:
                    pass
        for key in non_required_keys:
            if key in list(script_uri.keys()):
                if key in ["filename", "access_time", "sha1_checksum"]:
                    if not script_uri[key]:
                        script_uri.pop(key)
        
    def cleanup_io_domain(self, io_domain):
        required_keys = ["input_subdomain","output_subdomain"]
        for key in required_keys:
            if key in ["input_subdomain","output_subdomain"]:
                for index, subdomain in enumerate(io_domain[key]):
                    if key == "input_subdomain":
                        self.cleanup_input_subdomain(index, subdomain)
                    if key == "output_subdomain":
                        self.cleanup_output_subdomain(index, subdomain)

    def cleanup_output_subdomain(self, index, output_subdomain):
        required_keys = ["uri", "mediatype"]
        
        for key in required_keys:
            if key == "uri":
                self.cleanup_io_uri(index, output_subdomain[key], "output_subdomain")
            if key == "mediatype":
                if not output_subdomain[key]:
                    pass
                    
    def cleanup_input_subdomain(self, index, input_subdomain):
        required_keys = ["uri"]
        
        for key in required_keys:
            if key == "uri":
                self.cleanup_io_uri(index, input_subdomain[key], "input_subdomain")
 
    def cleanup_io_uri(self, index, isd_uri, subdomain):
        required_keys = ["uri"]
        non_required_keys = ["filename", "access_time", "sha1_checksum"]

        for key in required_keys:
            if key == "uri":
                if not isd_uri[key]:
                    pass
    
        for key in non_required_keys:
            if key in list(isd_uri.keys()):
                if key in ["filename", "access_time", "sha1_checksum"]:
                    if not isd_uri[key]:
                        isd_uri.pop(key)

    def cleanup_parametric_domain(self, parametric_domain):
        remove_params = []
        for index, parameter in enumerate(parametric_domain):
            self.cleanup_parameter(index, parameter)
            if not parameter:
                remove_params.append(index)
    
    def cleanup_parameter(self, index, parameter):
        required_keys = ["param","value","step"]
        if any([parameter[key] for key in required_keys]):
            pass
        else:
            [parameter.pop(key) for key in required_keys]
            
    def cleanup_error_domain(self, error_domain):
        required_keys = ["empirical_error","algorithmic_error"]

        for key in required_keys:
            if not error_domain[key]:
                pass
