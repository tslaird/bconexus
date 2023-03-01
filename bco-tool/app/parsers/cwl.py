import yaml, json

class cwl:
    def __init__(self, cwl_file_path) -> None:
        self.__path__ = cwl_file_path
        self.__bco_obj__ = self.__load_bco__()
    
    def __load_bco__(self):
        with open('app/schemas/biocompute.json') as f:
            return json.load(f)

    def __parse__(self):
        with open(self.__path__, 'r') as cwl_file:  
            return yaml.safe_load(cwl_file)

    def map_to_bco(self):
        cwl_dict = self.__parse__()
        self.__bco_obj__['execution_domain']['script'] = cwl_dict['baseCommand']
        self.__bco_obj__['execution_domain']['script_driver'] = 'dxCompiler'
        steps = cwl_dict['steps']
        inputs = cwl_dict['inputs']
        outputs = cwl_dict['output']

        for key in inputs.keys():
            if inputs[key]['type'].lower() == 'file':
                self.__bco_obj__['io_domain']['input_domain']['filename'] = key

        for key in outputs.keys():
            self.__bco_obj__['io_domain']['output_domain']['media_type'] = outputs[key]['type']
            self.__bco_obj__['io_domain']['output_domain']['media_type'] = outputs[key]['outputSource']

        step_number = 1
        for key in steps.keys():
            self.__bco_obj__['description_domain']['pipeline_steps']['step_number'] = step_number
            self.__bco_obj__['description_domain']['pipeline_steps']['name'] = key
            self.__bco_obj__['description_domain']['pipeline_steps']['input_list'] = steps[key]['in']
            self.__bco_obj__['description_domain']['pipeline_steps']['runtime'] = steps[key]['run']
            self.__bco_obj__['description_domain']['pipeline_steps']['output_list'] = steps[key]['out']
            for k in steps[key]['in'].keys():
                self.__bco_obj__['parametric_domain']['step'] = step_number
                self.__bco_obj__['parametric_domain']['param'] = k
                self.__bco_obj__['parametric_domain']['step'] = steps[key]['in'][k]