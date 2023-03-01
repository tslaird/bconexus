import json
import logging
from hashlib import new

import WDL
import yaml
from app.services.cwl import CWL
from app.services.dnanexus import DNAnexus
from app.services.min_wdl_parse import Min_WDL_Parser

logger = logging.getLogger("bco_logger")


class BcoDataService():

    def __init__(self):
        self.__bco_file__ = "app/schemas/biocompute.json"
        try:
            with open(self.__bco_file__, "r+") as bco_json:
                self.__bco_object__ = json.load(bco_json)
                logger.info(f"BCO file is loaded")
        except Exception as e:
            logger.error(f"Cannot open the BCO file -- {repr(e)}")


    def load_bco(self, bco_file, override):
        try:
            new_bco = json.loads(bco_file.read())
            if "description_domain" in new_bco.keys():
                self.map_description_domain(new_bco['description_domain'])
            if "parametric_domain" in new_bco.keys():
                self.map_parametric_domain(new_bco['parametric_domain'])
            if "provenance_domain" in new_bco.keys():
                self.map_provenance_domain(new_bco['provenance_domain'])
            if "io_domain" in new_bco.keys():
                self.map_io_domain(new_bco["io_domain"])
            if "execution_domain" in new_bco.keys():
                self.map_execution_domain(new_bco['execution_domain'])
            if "usability_domain" in new_bco.keys():
                self.map_usability_domain(new_bco['usability_domain'])
            if "object_id" in new_bco.keys():
                if new_bco['object_id']:
                    self.__bco_object__["object_id"] = new_bco['object_id']
            if "spec_version" in new_bco.keys():
                if new_bco['spec_version']:
                    self.__bco_object__["spec_version"] = new_bco['spec_version']
            if "etag" in new_bco.keys():
                if new_bco['etag']:
                    self.__bco_object__["etag"] = new_bco['etag']
            if "error_domain" in new_bco.keys():
                self.map_error_domain(new_bco['error_domain'])

            for key, value in new_bco.items():
                expected_list = ["object_id","spec_version","etag","description_domain", "parametric_domain", "provenance_domain", "io_domain", "execution_domain", "usability_domain","error_domain"]
                if key not in expected_list:
                    self.__bco_object__[key] = value

            with open(self.__bco_file__, "w") as outfile:
                json.dump(self.__bco_object__, outfile, indent=4)
        except Exception as e:
            logger.error(f"{repr(e)}")

    def map_execution_domain(self, new_execution_domain):
        try:
            if isinstance(new_execution_domain, dict):
                if "script" in new_execution_domain.keys():
                    if isinstance(new_execution_domain['script'], list):
                        for sc in new_execution_domain['script']:
                            new_sc = {"uri":{"filename": "","uri": "","access_time": "","sha1_checksum": ""}}
                            if "uri" in sc.keys():
                                if isinstance(sc['uri'],dict):
                                    if "filename" in sc["uri"].keys():
                                        new_sc["uri"]["filename"] = sc["uri"]["filename"]
                                    if "uri" in sc["uri"].keys():
                                        new_sc["uri"]["uri"] = sc["uri"]["uri"]
                                    if "access_time" in sc["uri"].keys():
                                        new_sc["uri"]["access_time"] = sc["uri"]["access_time"].split(".")[0]
                                    if "sha1_checksum" in sc["uri"].keys():
                                        new_sc["uri"]["sha1_checksum"] = sc["uri"]["sha1_checksum"]
                            self.__bco_object__['execution_domain']['script'].append(new_sc)
                if "script_driver" in new_execution_domain.keys():
                    self.__bco_object__['execution_domain']['script_driver'] = new_execution_domain['script_driver']
                if "software_prerequisites" in new_execution_domain.keys():
                    if isinstance(new_execution_domain['software_prerequisites'], list):
                        for sw_pre in new_execution_domain['software_prerequisites']:
                            new_sw_pre = {"name": "","version": "","uri": {"filename": "","uri": "","access_time": "","sha1_checksum": ""}}
                            if "name" in sw_pre.keys():
                                new_sw_pre["name"] = sw_pre['name']
                            if "version" in sw_pre.keys():
                                new_sw_pre["version"] = sw_pre['version']
                            if "uri" in sw_pre.keys():
                                if isinstance(sw_pre['uri'], dict):
                                    if "filename" in sw_pre['uri'].keys():
                                        new_sw_pre["uri"]["filename"] = sw_pre["uri"]["filename"]
                                    if "uri" in sw_pre['uri'].keys():
                                        new_sw_pre["uri"]["uri"] = sw_pre["uri"]["uri"]
                                    if "access_time" in sw_pre['uri'].keys():
                                        new_sw_pre["uri"]["access_time"] = sw_pre["uri"]["access_time"].split(".")[0]
                                    if "sha1_checksum" in sw_pre['uri'].keys():
                                        new_sw_pre["uri"]["sha1_checksum"] = sw_pre["uri"]["sha1_checksum"]
                            self.__bco_object__['execution_domain']['software_prerequisites'].append(new_sw_pre)
                if "external_data_endpoints" in new_execution_domain.keys():
                    if isinstance(new_execution_domain['external_data_endpoints'], list):
                        for ex_d_ep in new_execution_domain['external_data_endpoints']:
                            new_ex_d_ep = {"name":"", "url":""}
                            if "name" in ex_d_ep.keys():
                                new_ex_d_ep["name"] = ex_d_ep['name']
                            if "url" in ex_d_ep.keys():
                                new_ex_d_ep["url"] = ex_d_ep['url']
                            self.__bco_object__['execution_domain']['external_data_endpoints'].append(new_ex_d_ep)
                if "environment_variables" in new_execution_domain.keys():
                    self.__bco_object__['execution_domain']['environment_variables'] = new_execution_domain["environment_variables"]

        except Exception as e:
            logger.error(f"{repr(e)}")

    def map_provenance_domain(self, new_provenance_domain):
        try:
            if isinstance(new_provenance_domain, dict):
                if "name" in new_provenance_domain.keys():
                    self.__bco_object__['provenance_domain']['name'] = new_provenance_domain['name']
                if "version" in new_provenance_domain.keys():
                    self.__bco_object__['provenance_domain']['version'] = new_provenance_domain['version']
                if "derived_from" in new_provenance_domain.keys():
                    self.__bco_object__['provenance_domain']['derived_from'] = new_provenance_domain['derived_from']
                if "obsolete_after" in new_provenance_domain.keys():
                    self.__bco_object__['provenance_domain']['obsolete_after'] = new_provenance_domain['obsolete_after'].split(".")[0]
                if "created" in new_provenance_domain.keys():
                    self.__bco_object__['provenance_domain']['created'] = new_provenance_domain['created'].split(".")[0]
                if "modified" in new_provenance_domain.keys():
                    self.__bco_object__['provenance_domain']['modified'] = new_provenance_domain['modified'].split(".")[0]
                if "license" in new_provenance_domain.keys():
                    self.__bco_object__['provenance_domain']['license'] = new_provenance_domain['license']
                if "review" in new_provenance_domain.keys():
                    if isinstance(new_provenance_domain['review'],list):
                        for r in new_provenance_domain['review']:
                            new_r = {"date": "", "reviewer_comment": "", "status": "", "reviewer": {"name": "","affiliation": "","email": "","contribution": [],"orcid": ""}}
                            if isinstance(r, dict):
                                if "date" in r.keys():
                                    new_r["date"] = r['date']
                                if "reviewer_comment" in r.keys():
                                    new_r["reviewer_comment"] = r['reviewer_comment']
                                if "status" in r.keys():
                                    if r['status'] in ["unreviewed","in-review","approved","rejected","suspended"]:
                                        new_r["status"] = r['status']
                                    else:
                                        new_r["status"] = "unreviewed"
                                if "reviewer" in r.keys():
                                    if isinstance(r['reviewer'], dict):
                                        if "name" in r['reviewer'].keys():
                                            new_r['reviewer']["name"] = r['reviewer']['name']
                                        if "affiliation" in r['reviewer'].keys():
                                            new_r['reviewer']["affiliation"] = r['reviewer']['affiliation']
                                        if "email" in r['reviewer'].keys():
                                            new_r['reviewer']["email"] = r['reviewer']['email']
                                        if "orcid" in r['reviewer'].keys():
                                            new_r['reviewer']["orcid"] = r['reviewer']['orcid']
                                        if "contribution" in r['reviewer'].keys():
                                            if isinstance(r['reviewer']['contribution'], list):
                                                expected = ["authoredBy","contributedBy","createdAt","createdBy","createdWith","curatedBy","derivedFrom","importedBy","importedFrom","providedBy","retrievedBy","retrievedFrom","sourceAccessedBy"]
                                                valid = filter(lambda c: c in expected, r['reviewer']['contribution'])
                                                new_r['reviewer']["contribution"].extend(valid)
                            self.__bco_object__['provenance_domain']['review'].append(new_r)
                if "contributors" in new_provenance_domain.keys():
                    if isinstance(new_provenance_domain['contributors'],list):
                        for c in new_provenance_domain['contributors']:
                            new_c = {"name": "","affiliation": "","email": "","contribution": [],"orcid": ""}
                            if isinstance(c, dict):
                                if "name" in c.keys():
                                    new_c["name"] = c['name']
                                if "affiliation" in c.keys():
                                    new_c["affiliation"] = c['affiliation']
                                if "email" in c.keys():
                                    new_c["email"] = c['email']
                                if "orcid" in c.keys():
                                    new_c["orcid"] = c['orcid']
                                if "contribution" in c.keys():
                                    if isinstance(c['contribution'], list):
                                        expected = ["authoredBy","contributedBy","createdAt","createdBy","createdWith","curatedBy","derivedFrom","importedBy","importedFrom","providedBy","retrievedBy","retrievedFrom","sourceAccessedBy"]
                                        valid = filter(lambda e: e in expected, c['contribution'])
                                        new_c["contribution"].extend(valid)
                            self.__bco_object__['provenance_domain']['contributors'].append(new_c)

                if "embargo" in new_provenance_domain.keys():
                    if isinstance(new_provenance_domain["embargo"],dict):
                        if "start_time" in new_provenance_domain['embargo'].keys():
                            self.__bco_object__['provenance_domain']['embargo']['start_time'] = new_provenance_domain['embargo']['start_time']
                        if "end_time" in new_provenance_domain['embargo'].keys():
                            self.__bco_object__['provenance_domain']['embargo']['end_time'] = new_provenance_domain['embargo']['end_time']

        except Exception as e:
            logger.error(f"{repr(e)}")


    def map_error_domain(self, new_error_domain):
        try:
            if isinstance(new_error_domain, dict):
                if "empirical_error" in new_error_domain.keys():
                    self.__bco_object__['error_domain']['empirical_error'] = new_error_domain['empirical_error']
                if "algorithmic_error" in new_error_domain.keys():
                    self.__bco_object__['error_domain']['algorithmic_error'] = new_error_domain['algorithmic_error']
        except Exception as e:
            logger.error(f"{repr(e)}")


    def map_usability_domain(self, new_usability_domain):
        try:
            if isinstance(new_usability_domain, list):
                self.__bco_object__['usability_domain'].extend(new_usability_domain)
        except Exception as e:
            logger.error(f"{repr(e)}")


    def map_description_domain(self, new_description_domain):
        try:
            if "keywords" in new_description_domain.keys():
                if isinstance(new_description_domain['keywords'], list):
                    self.__bco_object__['description_domain']['keywords'].extend(new_description_domain['keywords'])
            if "platform" in new_description_domain.keys():
                if isinstance(new_description_domain['platform'], list):
                    self.__bco_object__['description_domain']['platform'].extend(new_description_domain['platform'])
            if "pipeline_steps" in new_description_domain.keys():
                if isinstance(new_description_domain['pipeline_steps'], list):
                    for step in new_description_domain['pipeline_steps']:
                        new_step = {"step_number": "","name": "","description": "","version": "","prerequisite": [],"input_list": [],"output_list": []}
                        if "step_number" in step.keys():
                            new_step["step_number"] = step["step_number"]
                        if "name" in step.keys():
                            new_step["name"] = step["name"]
                        if "description" in step.keys():
                            new_step["description"] = step["description"]
                        if "version" in step.keys():
                            new_step["version"] = step["version"]
                        if "prerequisite" in step.keys():
                            if isinstance(step['prerequisite'], list):
                                for pre in step['prerequisite']:
                                    new_pre = {"name": "","uri": {"filename": "","uri": "","access_time": "","sha1_checksum": ""}}
                                    if "name" in pre.keys():
                                        new_pre['name'] = pre['name']
                                    if "uri" in pre.keys():
                                        if isinstance(pre['uri'], dict):
                                            if "filename" in pre['uri'].keys():
                                                new_pre["uri"]["filename"] = pre["uri"]["filename"]
                                            if "uri" in pre['uri'].keys():
                                                new_pre["uri"]["uri"] = pre["uri"]["uri"]
                                            if "access_time" in pre['uri'].keys():
                                                new_pre["uri"]["access_time"] = pre["uri"]["access_time"].split(".")[0]
                                            if "sha1_checksum" in pre['uri'].keys():
                                                new_pre["uri"]["sha1_checksum"] = pre["uri"]["sha1_checksum"]
                                    new_step["prerequisite"].append(new_pre)
                        if "input_list" in step.keys():
                            if isinstance(step['input_list'], list):
                                for il in step['input_list']:
                                    new_il = {"filename": "","uri": "","access_time": "","sha1_checksum": ""}
                                    if isinstance(il, dict):
                                        if "filename" in il.keys():
                                            new_il["filename"] = il["filename"]
                                        if "uri" in il.keys():
                                            new_il["uri"] = il["uri"]
                                        if "access_time" in il.keys():
                                            new_il["access_time"] = il["access_time"].split(".")[0]
                                        if "sha1_checksum" in il.keys():
                                            new_il["sha1_checksum"] = il["sha1_checksum"]
                                    new_step["input_list"].append(new_il)
                        if "output_list" in step.keys():
                            if isinstance(step['output_list'], list):
                                for ol in step['output_list']:
                                    new_ol = {"filename": "","uri": "","access_time": "","sha1_checksum": ""}
                                    if isinstance(ol, dict):
                                        if "filename" in ol.keys():
                                            new_ol["filename"] = ol["filename"]
                                        if "uri" in ol.keys():
                                            new_ol["uri"] = ol["uri"]
                                        if "access_time" in ol.keys():
                                            new_ol["access_time"] = ol["access_time"].split(".")[0]
                                        if "sha1_checksum" in ol.keys():
                                            new_ol["sha1_checksum"] = ol["sha1_checksum"]
                                    new_step["output_list"].append(new_ol)
                        self.__bco_object__['description_domain']['pipeline_steps'].append(new_step)
            if "xref" in new_description_domain.keys():
                if isinstance(new_description_domain['xref'],list):
                    for xr in new_description_domain['xref']:
                        new_xref = {"namespace": "","name": "","ids": [],"access_time": ""}
                        if "namespace" in xr.keys():
                            new_xref['namespace'] = xr['namespace']
                        if "name" in xr.keys():
                            new_xref['name'] = xr['name']
                        if "ids" in xr.keys():
                            if isinstance(xr['ids'],list):
                                new_xref['ids'] = xr['ids']
                        if "access_time" in xr.keys():
                            new_xref['access_time'] = xr['access_time'].split(".")[0]
                        self.__bco_object__['description_domain']['xref'].append(new_xref)
        except Exception as e:
            logger.error(f"{repr(e)}")

    def map_parametric_domain(self, new_parametric_domain):
        try:
            if isinstance(new_parametric_domain, list):
                for prm in new_parametric_domain:
                    new_prm = {"param": "","value": "","step": ""}
                    if "param" in prm.keys():
                        new_prm["param"] = prm['param']
                    if "value" in prm.keys():
                        new_prm["value"] = prm['value']
                    if "step" in prm.keys():
                        new_prm["step"] = prm['step']
                    self.__bco_object__['parametric_domain'].append(new_prm)
        except Exception as e:
            logger.error(f"{repr(e)}")

    def map_io_domain(self, new_io_domain):
        try:
            if isinstance(new_io_domain, dict):
                if "input_subdomain" in new_io_domain.keys():
                    if isinstance(new_io_domain['input_subdomain'], list):
                        for in_sd in new_io_domain['input_subdomain']:
                            new_in_sd = {"uri":{"filename": "","uri": "","access_time": "","sha1_checksum": ""}}
                            if isinstance(in_sd, dict):
                                if "uri" in in_sd.keys():
                                    if isinstance(in_sd["uri"], dict):
                                        if "filename" in in_sd["uri"].keys():
                                            new_in_sd["uri"]["filename"] = in_sd["uri"]["filename"]
                                        if "uri" in in_sd["uri"].keys():
                                            new_in_sd["uri"]["uri"] = in_sd["uri"]["uri"]
                                        if "access_time" in in_sd["uri"].keys():
                                            new_in_sd["uri"]["access_time"] = in_sd["uri"]["access_time"].split(".")[0]
                                        if "sha1_checksum" in in_sd["uri"].keys():
                                            new_in_sd["uri"]["sha1_checksum"] = in_sd["uri"]["sha1_checksum"]
                            self.__bco_object__['io_domain']['input_subdomain'].append(new_in_sd)
                if "output_subdomain" in new_io_domain.keys():
                    if isinstance(new_io_domain['output_subdomain'], list):
                        for out_sd in new_io_domain['output_subdomain']:
                            new_out_sd = {"mediatype":"","uri":{"filename": "","uri": "","access_time": "","sha1_checksum": ""}}
                            if isinstance(out_sd, dict):
                                if "mediatype" in out_sd.keys():
                                    new_out_sd["mediatype"] = out_sd["mediatype"]
                                if "uri" in out_sd.keys():
                                    if isinstance(out_sd["uri"], dict):
                                        if "filename" in out_sd["uri"].keys():
                                            new_out_sd["uri"]["filename"] = out_sd["uri"]["filename"]
                                        if "uri" in out_sd["uri"].keys():
                                            new_out_sd["uri"]["uri"] = out_sd["uri"]["uri"]
                                        if "access_time" in out_sd["uri"].keys():
                                            new_out_sd["uri"]["access_time"] = out_sd["uri"]["access_time"].split(".")[0]
                                        if "sha1_checksum" in out_sd["uri"].keys():
                                            new_out_sd["uri"]["sha1_checksum"] = out_sd["uri"]["sha1_checksum"]
                            self.__bco_object__['io_domain']['output_subdomain'].append(new_out_sd)
        except Exception as e:
            logger.error(f"{repr(e)}")




    # Get DNA Nexus workflow and analysis objects
    def get_dna_workflow_json(self, override, workflow_id=None, analysis_id=None):
        try:
            workflow_obj = DNAnexus().describe_workflow(workflow_id)
            # print("xx", workflow_obj)
            name = workflow_obj['name'] if "name" in workflow_obj.keys() else ""
            input_subdomain = [{"uri":{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}}]
            if "inputSpec" in workflow_obj.keys():
                if workflow_obj['inputSpec']:
                    for input_spec in workflow_obj['inputSpec']:
                        isd = {"uri":{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}}
                        if input_spec['class'] == "File":
                            isd['uri']['filename'] = input_spec['name']
                            input_subdomain.append(isd)
            output_subdomain = [{"mediatype":"","uri":{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}}]
            if "outputSpec" in workflow_obj.keys():
                if workflow_obj['outputSpec']:
                    for output_spec in workflow_obj['outputSpec']:
                        osd = {"mediatype":"","uri":{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}}
                        if output_spec['class'] == "File":
                            osd['uri']['filename'] = output_spec['name']
                            # osd['uri']['uri'] = osd_value['outputSource']
                            output_subdomain.append(osd)
            workflow = {"name":name, "input_subdomain":input_subdomain, "output_subdomain":output_subdomain}
            app_ids = map(lambda stage: stage['executable'],workflow_obj['stages'])
            print("y",app_ids)
            analysis_obj = self.get_dna_analysis_json(analysis_id)
            analysis_stages = analysis_obj['stages']

            param_steps = []
            steps = []
            for i, app_id in enumerate(app_ids):
                step_count = (0 if override else len(self.__bco_object__['description_domain']['pipeline_steps'])) + i + 1
                if "applet" in app_id:
                    app = self.get_dna_applet_json(app_id)
                else:
                    app = self.get_dna_app_json(app_id)
                if app:
                    input_list = [{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}]
                    output_list = [{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}]
                    name = app["name"] if "name" in app.keys() else ""

                    if "inputSpec" in app.keys():
                        for in_spec in app['inputSpec']:
                            if in_spec['class'] == "file":
                                filename=in_spec['name']
                                input_list.append({"filename":filename, "uri":"", "access_time":"", "sha1_checksum":""})
                    if "outputSpec" in app.keys():
                        for out_spec in app['outputSpec']:
                            if out_spec['class'] == "file":
                                filename=in_spec['name']
                                output_list.append({"filename":filename, "uri":"", "access_time":"", "sha1_checksum":""})
                    step = {"step_number":step_count, "name":name, "description":"", "version":"", "prerequisite":[{"name":"","uri":{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}}], "input_list":input_list, "output_list":output_list}
                else:
                    step = {"step_number":step_count, "name":app_id, "description":"", "version":"", "prerequisite":[{"name":"","uri":{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}}], "input_list":[{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}], "output_list":[{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}]}
                steps.append(step)
                if analysis_stages[i]:
                    if "input" in analysis_stages[i]['execution'].keys():
                        for key, value in analysis_stages[i]['execution']['input'].items():
                            param_step = {"step":str(step_count), "param":key, "value":value}
                            param_steps.append(param_step)
            workflow_json = {"workflow":workflow, "steps":steps, "param_steps":param_steps}
            return workflow_json
        except Exception as e:
            logger.error(f"Cannot get workflow and corresponding app/applet details --{repr(e)}")
            return None


    def get_dna_app_json(self, app_id):
        try:
            app = DNAnexus().describe_app(app_id)
            return app
        except Exception as e:
            logger.error(f"Cannot get app ({app_id}) details --{repr(e)}")
            return None


    def get_dna_applet_json(self, applet_id):
        try:
            applet = DNAnexus().describe_applet(applet_id)
            return applet
        except Exception as e:
            logger.error(f"Cannot get applet ({applet_id}) details --{repr(e)}")
            return None


    def get_dna_analysis_json(self, analysis_id):
        try:
            analysis = DNAnexus().describe_analysis(analysis_id)
            # print("aka", analysis)
            return analysis
        except Exception as e:
            logger.error(f"Cannot get applet ({analysis_id}) details --{repr(e)}")
            return None



    # Update BCO execution domain
    def update_execution_domain(self, override, script=None):
        try:
            if script:
                item = {"uri":{"filename":script, "uri":"", "access_time":"", "sha1_checksum":""}}
                self.__bco_object__['execution_domain']['script'].append(item)
            else:
                logger.error(f"Cannot update execution domain")
        except Exception as e:
            logger.error(f"Cannot update execution domain -- {repr(e)}")


    # Update BCO IO domain
    def update_io_domain(self, override, input_subdomain = None, output_subdomain = None):
        try:

            self.update_input_subdomain(override, input_subdomain)

            self.update_output_subdomain(override, output_subdomain)
        except Exception as e:
            logger.error(f"Cannot update IO domain -- {repr(e)}")

    def update_input_subdomain(self, override, input_subdomain=None):
        try:
            if override:
                try:
                    print("in iv")
                    self.__bco_object__['io_domain']['input_subdomain'] = []
                except Exception as e:
                    logger.error(f"iv {repr(e)}")
            if input_subdomain:
                for item in input_subdomain:
                    self.__bco_object__['io_domain']['input_subdomain'].append(item)
            else:
                logger.error(f"Cannot update IO domain.input_subdomain with None")
        except Exception as e:
            logger.error(f"Cannot update IO domain.input_subdomain -- {repr(e)}")


    def update_output_subdomain(self, override, output_subdomain=None):
        try:
            if override:
                try:
                    print("in ov")
                    self.__bco_object__['io_domain']['output_subdomain'] = []
                except Exception as e:
                    logger.error(f"ov {repr(e)}")
            if output_subdomain:
                for item in output_subdomain:
                    self.__bco_object__['io_domain']['output_subdomain'].append(item)
            else:
                logger.error(f"Cannot update IO domain.output_subdomain with None")
        except Exception as e:
            logger.error(f"Cannot update IO domain.output_subdomain -- {repr(e)}")


    # Update BCO Description domain
    def update_description_domain(self, override, steps=None):
        try:
            if override:
                self.__bco_object__['description_domain']['pipeline_steps'] = []
            if steps:
                for step in steps:
                    # print("s",step)
                    self.__bco_object__['description_domain']['pipeline_steps'].append(step)

            else:
                logger.error(f"Cannot update Description domain.pipe_linesteps with None")
        except Exception as e:
            logger.error(f"Cannot update Description domain.pipe_linesteps -- {repr(e)}")


    # Update BCO Parametric Domain
    def update_parametric_domain(self, override, param_steps=None):
        try:
            if override:
                self.__bco_object__['parametric_domain'] = []
            if param_steps:
                for param_step in param_steps:
                    # print("ps", param_step)
                    step = param_step['step']
                    param = param_step['param']
                    value = param_step['value']
                    if step != "" or param != "" or value != "":
                        p_d_s = {"step":step,"param":param,"value":value}
                        self.__bco_object__['parametric_domain'].append(p_d_s)
                    else:
                        logger.error(f"Cannot update Parametric domain with an empty record")
            else:
                logger.error(f"Cannot update Parametric domain with None")

        except Exception as e:
            logger.error(f"Cannot update Parametric domain -- {repr(e)}")


    # Load DNAnexus workflow into BCO
    def load_dnanexus_workflow(self, override, workflow_id=None, analysis_id=None):
        try:
            workflow_json = self.get_dna_workflow_json(override, workflow_id, analysis_id)
            self.update_execution_domain(script=workflow_json['workflow']['name'], override = override)
            self.update_io_domain(override, input_subdomain = workflow_json['workflow']['input_subdomain'] if workflow_json['workflow'] else None, output_subdomain = workflow_json['workflow']['output_subdomain'] if workflow_json['workflow'] else None)
            self.update_description_domain(steps=workflow_json['steps'], override= override)
            self.update_parametric_domain(param_steps=workflow_json['param_steps'], override = override)
            logger.info(f"workflow({workflow_id}) loaded successfully")
            with open(self.__bco_file__, "w") as outfile:
                json.dump(self.__bco_object__, outfile, indent=4)
        except Exception as e:
            logger.error(f"Cannot load workflow({workflow_id}) -- {repr(e)}")

    def load_cwl(self, cwl_file, override):
        try:
            workflow_json = self.get_cwl_json(cwl_file, override)
            # print("wf1", workflow_json)
            self.update_execution_domain(script=workflow_json['workflow']['name'], override = override)
            self.update_io_domain(override, input_subdomain = workflow_json['workflow'] ['input_subdomain'] if workflow_json['workflow'] else None, output_subdomain = workflow_json['workflow']['output_subdomain'] if workflow_json['workflow'] else None)
            self.update_description_domain(steps=workflow_json['steps'], override= override)
            self.update_parametric_domain(param_steps=workflow_json['param_steps'], override = override)
            logger.info(f"CWL workflow loaded successfully")
            with open('app/schemas/biocompute.json', 'w') as outfile:
                json.dump(self.__bco_object__, outfile, indent=4)

        except Exception as e:
            logger.error(f"Error loading cwl workflow -- {repr(e)}")

    def load_wdl(self, wdl_file, override):
        try:
            workflow_json = self.get_wdl_json(wdl_file, override)
            self.update_execution_domain(script=workflow_json['workflow']['name'] if workflow_json['workflow'] else None, override = override)
            self.update_io_domain(override, input_subdomain = workflow_json['workflow']['input_subdomain'] if workflow_json['workflow'] else None, output_subdomain = workflow_json['workflow']['output_subdomain'] if workflow_json['workflow'] else None)
            self.update_description_domain(steps=workflow_json['steps'], override= override)
            self.update_parametric_domain(param_steps=workflow_json['param_steps'], override = override)
            logger.info(f"WDL workflow loaded successfully")
            with open(self.__bco_file__, "w") as outfile:
                json.dump(self.__bco_object__, outfile, indent=4)
        except Exception as e:
            logger.error(f"Error loading wdl workflow -- {repr(e)}")

    def get_wdl_json(self, wdl_file, override):
        try:
            wdl_obj = Min_WDL_Parser(wdl_file).load()
            if wdl_obj['workflow_details']:

                name = wdl_obj['workflow_details']['workflow_name']
                input_subdomain = []
                if "workflow_inputs" in wdl_obj['workflow_details'].keys():

                    for workflow_input in wdl_obj['workflow_details']['workflow_inputs']:
                        isd = {"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}
                        if workflow_input['type'] == "File":
                            isd['filename'] = workflow_input['name']
                            input_subdomain.append(isd)
                output_subdomain = []
                if "workflow_outputs" in wdl_obj['workflow_details'].keys():

                    for workflow_output in wdl_obj['workflow_details']['workflow_outputs']:
                        osd = {"mediatype":"","uri":{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}}
                        if workflow_output['type'] == "File":
                            osd['uri']['filename'] = workflow_output['name']
                            output_subdomain.append(osd)
                workflow = {"name":name, "input_subdomain":input_subdomain, "output_subdomain":output_subdomain}
            else:
                workflow = None
            param_steps = []
            steps = []
            if "tasks_details" in wdl_obj.keys():

                for i, task in enumerate(wdl_obj['tasks_details']):

                    step_number = (0 if override else len(self.__bco_object__['description_domain']['pipeline_steps'])) + i + 1
                    name = task['task_name']
                    input_list = [{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}]
                    for task_input in wdl_obj['tasks_details'][i]["task_inputs"]:

                        if isinstance(task_input["type"], WDL.Type.File):

                            step_input = {"filename":task_input['name'], "uri":task_input['value'], "access_time":"", "sha1_checksum":""}
                            input_list.append(step_input)
                    output_list = [{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}]
                    for task_output in wdl_obj['tasks_details'][i]["task_outputs"]:

                        if isinstance(task_output["type"], WDL.Type.File):
                            step_output = {"filename":task_output['name'], "uri":task_output['value'], "access_time":"", "sha1_checksum":""}
                            output_list.append(step_output)
                    step = {"step_number": step_number, "name":name, "description":"", "version":"", "prerequisite":[{"name":"","uri":{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}}],"input_list":input_list, "output_list": output_list}
                    steps.append(step)

                    step = step_number
                    for task_input in wdl_obj['tasks_details'][i]["task_inputs"]:

                        param = task_input['name']
                        value = task_input['value']
                        param_step = {"step":step,"param":param,"value":value}
                        param_steps.append(param_step)
            workflow_json = {"workflow":workflow, "steps":steps, "param_steps":param_steps}
            print("x",workflow_json)
            return workflow_json
        except Exception as e:
            logger.error(f"Cannot load WDL workflow -- {repr(e)}")
            return None

    def get_cwl_json(self, cwl_file, override):
        try:
            cwl_obj = CWL(cwl_file, self.__bco_file__).load()
            name = cwl_obj["baseCommand"] if "baseCommand" in cwl_obj.keys() else ""
            input_subdomain = []
            if "inputs" in cwl_obj.keys():
                for isd_key, isd_value in cwl_obj['inputs'].items():
                    isd = {"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}
                    if isd_value['type'] == "File":
                        isd['filename'] = isd_key
                        input_subdomain.append(isd)
            output_subdomain = []
            if "outputs" in cwl_obj.keys():
                for osd_key, osd_value in cwl_obj['outputs'].items():
                    osd = {"mediatype":"","uri":{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}}
                    if osd_value['type'] == "File":
                        osd['uri']['filename'] = osd_key
                        osd['uri']['uri'] = osd_value['outputSource']
                        output_subdomain.append(osd)
            workflow = {"name":name, "input_subdomain":input_subdomain, "output_subdomain":output_subdomain}
            param_steps = []
            steps = []
            if "steps" in cwl_obj.keys():
                    for i, (key, value) in enumerate(cwl_obj['steps'].items()):
                        step_number = (0 if override else len(self.__bco_object__['description_domain']['pipeline_steps'])) + i + 1
                        name = key
                        input_list = []
                        for in_key, in_value in cwl_obj['steps'][key]["in"].items():
                            step_input = {"filename":in_key, "uri":in_value, "access_time":"", "sha1_checksum":""}
                            input_list.append(step_input)
                        output_list = []
                        for output in cwl_obj['steps'][key]["out"]:
                            step_output = {"filename":output, "uri":"", "access_time":"", "sha1_checksum":""}
                            output_list.append(step_output)
                        step = {"step_number": step_number, "name":name, "description":"", "version":"", "prerequisite":[{"name":"","uri":{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}}],"input_list":input_list, "output_list": output_list}
                        steps.append(step)

                        step = step_number
                        for s_key, s_value in cwl_obj['steps'][key]["in"].items():
                            # print("in for", s_key, s_value)
                            param = s_key
                            value = s_value
                            param_step = {"step":step,"param":param,"value":value}
                            # print("p", param_step)
                            param_steps.append(param_step)
            workflow_json = {"workflow":workflow, "steps":steps, "param_steps":param_steps}
            return workflow_json
        except Exception as e:
            logger.error(f"Cannot load CWL workflow -- {repr(e)}")
            return None




    # def validate_bco(self):
    #     try:
    #         with open('app/schemas/biocompute_meta.json', 'r+') as bco_json_meta:
    #             self.__bco_meta_object__ = json.load(bco_json_meta)
    #         # for key, value in self.__bco_object__.items():
    #             print("after")
    #             # self.__bco_validation_status__ = self.validate_2791()
    #             # self.__bco_validation_status__.update(self.validate_usability())
    #             # self.__bco_validation_status__.update(self.validate_parametric())
    #             # self.__bco_validation_status__.update(self.validate_error())
    #             # self.__bco_validation_status__.update(self.validate_io())
    #             # self.validate_error()
    #             self.validate_usability()
    #             # print(self.__bco_validation_status__)
    #         return self.__bco_object__
    #     except Exception as e:
    #         print(f"{repr(e)}")


    # def validate_2791(self):

    #     object_id_check = isinstance(self.__bco_object__['object_id'], str)
    #     object_id_status = "pass" if object_id_check else f"fail -- object_id is not a string: {self.__bco_object__['object_id']}"

    #     spec_version_check = isinstance(self.__bco_object__['spec_version'], str)
    #     spec_version_status = "pass" if spec_version_check else f"fail -- spec_version is not a string: {self.__bco_object__['spec_version']}"

    #     etag_check = isinstance(self.__bco_object__['etag'], str)
    #     etag_status = "pass" if etag_check else f"fail -- etag is not a string: {self.__bco_object__['etag']}"

    #     return {"object_id":object_id_status, "spec_version": spec_version_status, "etag":etag_status}


    # def validate_error(self):
    #     error_item_check = [f"Error item {key} is empty" if not value else f"Error item {key} is not an object" if not isinstance(value, dict) else "pass" for key, value in self.__bco_object__['error_domain'].items()]
    #     error_domain_errors = [message for message in error_item_check if message != "pass"]
    #     error_domain_status = "Pass" if len(error_domain_errors) == 0 else "Fail"

    #     return {"error_domain": {"error_domain_status":error_domain_status, "error_domain_errors":error_domain_errors}}



    # def validate_provenance(self):
    #     pass

    # def validate_description(self):
    #     pass

    # def validate_io(self):
    #     io_isd_item_check = [f"Error item input_sub_domain.{index}.{key} is empty" if not value else f"Error item .{index}.{key} is not a string" if not isinstance(value, str) else "pass" for index,item in enumerate(self.__bco_object__['io_domain']['input_subdomain']) for key, value in item.items()]
    #     io_osd_item_check = [f"Error item input_sub_domain.{index}.{key} is empty" if not value else f"Error item .{index}.{key} is not a string" if not isinstance(value, str) else ("pass" if key == "uri" else "pass" for u_key, u_value in value.items() ) for index,item in enumerate(self.__bco_object__['io_domain']['output_subdomain']) for key, value in item.items()]

    #     io_domain_errors =  [message for message in io_item_check if message != "pass"]
    #     io_domain_status = "Pass" if len(io_domain_errors) == 0 else "Fail"
    #     return {"io_domain": {"io_domain_status":io_domain_status, "io_domain_errors":io_domain_errors}}


    # def validate_execution(self):
    #     pass


    # def validate_parametric(self):
    #     parametric_item_check = [f"Parametric item {index + 1}.{key} is empty" if not value else f"Parametric item {index + 1}.{key} is not a string" if not isinstance(value, str) else "pass" for index, item in enumerate(self.__bco_object__['parametric_domain']) for key, value in item.items()]
    #     parametric_domain_errors =  [message for message in parametric_item_check if message != "pass"]
    #     parametric_domain_status = "Pass" if len(parametric_domain_errors) == 0 else "Fail"
    #     return {"parametric_domain": {"parametric_domain_status":parametric_domain_status, "parametric_domain_errors":parametric_domain_errors}}


    # def validate_usability(self):

    #     usability_domain_status = ("Pass","black")

    #     for index, item in enumerate(self.__bco_object__['usability_domain']):
    #         if item:
    #             if isinstance(item, str):
    #                 self.__bco_object__['usability_domain'][index] = (item, 'pass', 'black', f'item {index} is a string', f'vr_usability_domain', f'vr_ud_items_{index}')
    #             else:
    #                 self.__bco_object__['usability_domain'][index] = (item, 'fail', 'red', f'item {index} is not a string', f'vr_usability_domain', f'vr_ud_items_{index}')
    #                 usability_domain_status = ("Fail","red")
    #         else:
    #             self.__bco_object__['usability_domain'][index] = (item, 'pass', 'red', f'item {index} is a null value', f'vr_usability_domain', f'vr_ud_items_{index}')
    #             usability_domain_status = ("Fail","red")
    #     # breakpoint()
    #     self.__bco_object__.update({"usability_domain_status":usability_domain_status})


class ComparisonBcoDataService(BcoDataService):
    def __init__(self):
        self.__bco_file__ = "app/schemas/biocompute_compare.json"
        try:
            with open(f"app/schemas/biocompute_skeleton.json", "r+") as bco_json:
                self.__bco_object__ = json.load(bco_json)
                logger.info(f"BCO file is loaded")
        except Exception as e:
            logger.error(f"Cannot open the BCO file -- {repr(e)}")
