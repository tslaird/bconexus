import json

import yaml


class CWL:
    def __init__(self, cwl_file, bco_file) -> None:
        self.__cwl_file__ = cwl_file
        self.__bco_file__ = bco_file

    def load(self):
        try:
            self.__cwl_dict__ = yaml.safe_load(self.__cwl_file__)
            return self.__cwl_dict__
        except Exception as e:
            print("Error reading the CWL file.",str(e))

    def update_execution_domain(self):
        try:
            with open(self.__bco_file__) as f_exec:
                exec_json = json.load(f_exec)
                if "baseCommand" in self.__cwl_dict__:
                    exec_json['execution_domain']['script'].append({"uri":self.__cwl_dict__["baseCommand"]})
                # what to update on script driver

        except Exception as e:
            print("Error updating exec BCO with CWL.", str(e))

    def override_execution_domain(self):
        try:
            with open(self.__bco_file__) as f_exec:
                exec_json = json.load(f_exec)
                if "baseCommand" in self.__cwl_dict__:
                    exec_json['execution_domain']['script'] = {"uri":self.__cwl_dict__["baseCommand"]}
                # what to update on script driver

        except Exception as e:
            print("Error updating exec BCO with CWL.", str(e))

    def override_io_domain(self):
        try:
            with open(self.__bco_file__, "r+") as f_exec:
                exec_json = json.load(f_exec)
                if "inputs" in self.__cwl_dict__:
                    exec_json['io_domain']['input_subdomain'].clear()
                    for key, value in self.__cwl_dict__['inputs'].items():
                        if self.__cwl_dict__['inputs'][key]["type"] == "File":
                            isd = {"uri":self.__cwl_dict__["inputs"][key]["doc"], "filename":"", "access_time":""}
                            exec_json['io_domain']['input_subdomain'].append(isd)
                if "outputs" in self.__cwl_dict__:
                    exec_json['io_domain']['output_subdomain'].clear()
                    for key, value in self.__cwl_dict__['outputs'].items():
                        if self.__cwl_dict__['outputs'][key]["type"] == "File":
                            if "outputSource" in self.__cwl_dict__["outputs"][key]:
                                osd = {"uri":self.__cwl_dict__["outputs"][key]["outputSource"],"media_type":"", "access_time":""}
                                exec_json['io_domain']['output_subdomain'].append(osd)

            with open(self.__bco_file__, "w") as outfile:
                json.dump(exec_json, outfile)

        except Exception as e:
            print("Error updating io BCO with CWL.", str(e))

    def update_io_domain(self):
        try:
            with open(self.__bco_file__, "r+") as f_exec:
                exec_json = json.load(f_exec)
                if "inputs" in self.__cwl_dict__:
                    for key, value in self.__cwl_dict__['inputs'].items():
                        if self.__cwl_dict__['inputs'][key]["type"] == "File":
                            isd = {"uri":self.__cwl_dict__["inputs"][key]["doc"], "filename":"", "access_time":""}
                            exec_json['io_domain']['input_subdomain'].append(isd)
                if "outputs" in self.__cwl_dict__:
                    for key, value in self.__cwl_dict__['outputs'].items():
                        if self.__cwl_dict__['outputs'][key]["type"] == "File":
                            osd = {"uri":self.__cwl_dict__["outputs"][key]["outputSource"],"media_type":"", "access_time":""}
                            exec_json['io_domain']['output_subdomain'].append(osd)

            with open(self.__bco_file__, "w") as outfile:
                json.dump(exec_json, outfile)

        except Exception as e:
            print("Error updating io BCO with CWL.", str(e))

    def update_description_and_parametric_domain(self):
        try:
            with open('app/schemas/biocompute.json', 'r+') as f_exec:
                exec_json = json.load(f_exec)
                if "steps" in self.__cwl_dict__:
                    for key, value in self.__cwl_dict__['steps'].items():
                        step_number = len(exec_json['description_domain']['pipeline_steps']) + 1
                        name = key
                        runtime = self.__cwl_dict__['steps'][key]["run"]
                        input_list = [value for key, value in self.__cwl_dict__['steps'][key]["in"].items()]
                        output_list = self.__cwl_dict__['steps'][key]["out"]
                        isd = {"step_number": step_number, "name":name, "description":"","version":"","runtime": runtime, "input_list":input_list, "output_list": output_list}
                        exec_json['description_domain']['pipeline_steps'].append(isd)
                        for key1, value1 in self.__cwl_dict__['steps'][key]["in"].items():
                            step = str(step_number)
                            param = key1
                            value = value1
                            pd = {"step":step,"param":param,"value":value}
                            exec_json['parametric_domain'].append(pd)
            with open(self.__bco_file__, "w") as outfile:
                json.dump(exec_json, outfile)

        except Exception as e:
            print("Error updating desc BCO with CWL.", str(e))

    def override_description_and_parametric_domain(self):
        try:
            with open(self.__bco_file__, "r+") as f_exec:
                exec_json = json.load(f_exec)
                if "steps" in self.__cwl_dict__:
                    exec_json['description_domain']['pipeline_steps'] = []
                    exec_json['parametric_domain'] = []
                    for key, value in self.__cwl_dict__['steps'].items():
                        step_number = len(exec_json['description_domain']['pipeline_steps']) + 1
                        name = key
                        runtime = self.__cwl_dict__['steps'][key]["run"]
                        input_list = [value for key, value in self.__cwl_dict__['steps'][key]["in"].items()]
                        output_list = self.__cwl_dict__['steps'][key]["out"]
                        isd = {"step_number": step_number, "name":name, "description":"","version":"","runtime": runtime, "input_list":input_list, "output_list": output_list}
                        exec_json['description_domain']['pipeline_steps'].append(isd)
                        for key1, value1 in self.__cwl_dict__['steps'][key]["in"].items():
                            step = str(step_number)
                            param = key1
                            value = value1
                            pd = {"step":step,"param":param,"value":value}
                            exec_json['parametric_domain'].append(pd)
            with open(self.__bco_file__, "w") as outfile:
                json.dump(exec_json, outfile)

        except Exception as e:
            print("Error updating desc BCO with CWL.", str(e))

    def update(self):
        try:
            with open(self.__bco_file__) as f_exec:
                exec_json = json.load(f_exec)
                exec_json['properities']['script']

        except Exception as e:
            print("Error updating BCO with CWL.", str(e))