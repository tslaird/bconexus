import json
import logging

logger = logging.getLogger("bco_logger")


class BcoValidationService():

    def __init__(self):
        try:
            with open('app/schemas/biocompute.json', 'r+') as bco_json:
                self.__bco_object__ = json.load(bco_json)
                logger.info(f"BCO file is loaded")
        except Exception as e:
            logger.error(f"Cannot open the BCO file -- {repr(e)}")

    def validate_bco(self):
        try:
            with open('app/schemas/biocompute_meta.json', 'r+') as bco_json_meta:
                self.__bco_meta_object__ = json.load(bco_json_meta)
                self.validate_2791()
                self.validate_usability_domain()
                self.validate_parametric_domain()
                self.validate_io_domain()
                self.validate_error_domain()
                self.validate_provenance_domain()
                self.validate_description_domain()
                self.validate_execution_domain()
            return self.__bco_object__
        except Exception as e:
            print(f"{repr(e)}")

    def validate_2791(self):
        try:
            object_2791_status = ["Pass", ""]
            for key, value in self.__bco_object__.items():
                if key in ['object_id', 'spec_version', 'etag']:
                    if value:
                        if isinstance(value, str):
                            self.__bco_object__[key] = [value, "pass", "", f"{key} is valid", "vr_2791", f"vr_2791_{key}"]
                        else:
                            object_2791_status = ["Fail", "red"]
                            self.__bco_object__[key] = [value, "fail", "red", f"{key} is not a string", "vr_2791", f"vr_2791_{key}"]
                    else:
                        object_2791_status = ["Fail", "red"]
                        self.__bco_object__[key] = [value, "fail", "red", f"{key} is empty", "vr_2791", f"vr_2791_{key}"]
            self.__bco_object__.update({"object_2791_status":object_2791_status})
        except Exception as e:
            logger.error(f"Cannot validate 2791 object -- {repr(e)}")

    def validate_usability_domain(self):
        try:
            usability_domain_status = ("Fail","red","usability domain is empty", 'vr_usability_domain')
            if len(self.__bco_object__['usability_domain']):
                usability_domain_status = ("Pass","black")
                for index, item in enumerate(self.__bco_object__['usability_domain']):
                    if item:
                        if isinstance(item, str):
                            self.__bco_object__['usability_domain'][index] = (item, 'pass', 'black', f'item {index} is a string', 'vr_usability_domain', f'vr_ud_items_{index}')
                        else:
                            self.__bco_object__['usability_domain'][index] = (item, 'fail', 'red', f'item {index} is not a string', 'vr_usability_domain', f'vr_ud_items_{index}')
                            usability_domain_status = ("Fail","red")
                    else:
                        self.__bco_object__['usability_domain'][index] = (item, 'fail', 'red', f'item {index} is a null value', 'vr_usability_domain', f'vr_ud_items_{index}')
                        usability_domain_status = ("Fail","red")

            self.__bco_object__.update({"usability_domain_status":usability_domain_status})
        except Exception as e:
            logger.error(f"Cannot validate usability domain -- {repr(e)}")


    def validate_parametric_domain(self):
        try:
            parametric_domain_status = ("Fail","red","parametric domain is empty", "vr_parametric_domain")
            if len(self.__bco_object__['parametric_domain']):
                parametric_domain_status = ("Pass","black")
                for index, item in enumerate(self.__bco_object__['parametric_domain']):
                    self.__bco_object__['parametric_domain'][index] = [item,"pass","",f'item {index} pass','',f'vr_pd_items_{index}']
                    for key,value in item.items():
                        if value:
                            if isinstance(value, str):
                                self.__bco_object__['parametric_domain'][index][0][key] = (value, 'pass', 'black', f'item {index}.{key} is a string', f'vr_parametric_domain-vr_pd_items_{index}', f'vr_pd_items_{index}_{key}')
                            else:
                                self.__bco_object__['parametric_domain'][index][0][key] = (value, 'fail', 'red', f'item {index}.{key} is not a string', f'vr_parametric_domain-vr_pd_items_{index}', f'vr_pd_items_{index}_{key}')
                                self.__bco_object__['parametric_domain'][index] = [item,"fail","red",f'item {index} fail','',f'vr_pd_items_{index}']
                                parametric_domain_status = ("Fail","red")
                        else:
                            self.__bco_object__['parametric_domain'][index][0][key] = (value, 'fail', 'red', f'item {index}.{key} is a null value', f'vr_parametric_domain-vr_pd_items_{index}', f'vr_pd_items_{index}_{key}')
                            self.__bco_object__['parametric_domain'][index] = [item,"fail","red",f'item {index} fail','',f'vr_pd_items_{index}']
                            parametric_domain_status = ("Fail","red")

            self.__bco_object__.update({"parametric_domain_status":parametric_domain_status})
            # print("pd", self.__bco_object__['parametric_domain'])
        except Exception as e:
            logger.error(f"Cannot validate parametric domain -- {repr(e)}")

    def validate_io_domain(self):
        try:
            io_domain_status = ("Pass","")
            input_subdomain_status = ("Pass","")
            output_subdomain_status = ("Pass","")
            if len(self.__bco_object__["io_domain"]["input_subdomain"]) == 0 and len(self.__bco_object__["io_domain"]["output_subdomain"]) == 0:
                io_domain_status = ("Fail","red","io_domain is empty", "vr_io_domain")
                input_subdomain_status = ("Fail","red","input_subdomain is empty", "vr_io_domain-vr_isd", "vr_isd")
                output_subdomain_status = ("Fail","red","output_subdomain is empty", "vr_io_domain-vr_osd", "vr_osd")

            if len(self.__bco_object__["io_domain"]["input_subdomain"]) == 0:
                io_domain_status = ("Fail","red")
                input_subdomain_status = ("Fail","red","input_subdomain is empty", "vr_io_domain-vr_isd", "vr_isd")
            else:
                for index, isd in enumerate(self.__bco_object__["io_domain"]["input_subdomain"]):
                    for key, value in isd['uri'].items():
                        if value:
                            if isinstance(value, str):
                                self.__bco_object__["io_domain"]["input_subdomain"][index]["uri"][key]=[value,"pass", "black", f"input_subdomain item.{index}.uri.{key} is valid", f"vr_io_domain-vr_isd-vr_isd_items_{index}-vr_isd_items_{index}_uri", f"vr_isd_items_{index}_uri_{key}"]
                            else:
                                io_domain_status = ("Fail","red")
                                input_subdomain_status = ("Fail","red")
                                self.__bco_object__["io_domain"]["input_subdomain"][index]["uri"][key]=[value,"fail", "red", f"input_subdomain item.{index}.uri.{key} is not a string", f"vr_io_domain-vr_isd-vr_isd_items_{index}-vr_isd_items_{index}_uri", f"vr_isd_items_{index}_uri_{key}"]
                        else:
                            if key == "uri":
                                io_domain_status = ("Fail","red")
                                input_subdomain_status = ("Fail","red")
                                # self.__bco_object__["io_domain"]["input_subdomain"][index]["color"] = ["red"]
                                # self.__bco_object__["io_domain"]["input_subdomain"][index]["uri"]["color"] = ["red"]
                                self.__bco_object__["io_domain"]["input_subdomain"][index]["uri"][key]=[value,"fail", "red", f"input_subdomain item.{index}.uri.{key} is empty", f"vr_io_domain-vr_isd-vr_isd_items_{index}-vr_isd_items_{index}_uri", f"vr_isd_items_{index}_uri_{key}"]

            if len(self.__bco_object__["io_domain"]["output_subdomain"]) == 0:
                io_domain_status = ("Fail","red")
                output_subdomain_status = ("Fail","red","output_subdomain is empty", "vr_io_domain-vr_osd", "vr_osd")
            else:
                for index, osd in enumerate(self.__bco_object__["io_domain"]["output_subdomain"]):
                    for key, value in osd.items():
                        if key == "mediatype":
                            if value:
                                if isinstance(value, str):
                                    self.__bco_object__["io_domain"]["output_subdomain"][index][key]=[value,"pass", "black", f"output_subdomain item.{index}.{key} is valid", f"vr_io_domain-vr_osd-vr_osd_items_{index}", f"vr_osd_items_{index}_mediatype"]
                                else:
                                    io_domain_status = ("Fail","red")
                                    output_subdomain_status = ("Fail","red")
                                    self.__bco_object__["io_domain"]["output_subdomain"][index][key]=[value,"fail", "red", f"output_subdomain item.{index}.{key} is not a string", f"vr_io_domain-vr_osd-vr_osd_items_{index}", f"vr_osd_items_{index}_mediatype"]
                            else:
                                io_domain_status = ("Fail","red")
                                output_subdomain_status = ("Fail","red")
                                self.__bco_object__["io_domain"]["output_subdomain"][index][key]=[value,"fail", "red", f"output_subdomain item.{index}.{key} is empty", f"vr_io_domain-vr_osd-vr_osd_items_{index}", f"vr_osd_items_{index}_mediatype"]

                        elif key == "uri":
                            for key, value in osd['uri'].items():
                                if value:
                                    if isinstance(value, str):
                                        self.__bco_object__["io_domain"]["output_subdomain"][index]["uri"][key]=[value,"pass", "black", f"output_subdomain item.{index}.uri.{key} is valid", f"vr_io_domain-vr_osd-vr_osd_items_{index}-vr_osd_items_{index}_uri", f"vr_osd_items_{index}_uri_{key}"]
                                    else:
                                        io_domain_status = ("Fail","red")
                                        output_subdomain_status = ("Fail","red")
                                        self.__bco_object__["io_domain"]["output_subdomain"][index]["uri"][key]=[value,"fail", "red", f"output_subdomain item.{index}.uri.{key} is not a string", f"vr_io_domain-vr_osd-vr_osd_items_{index}-vr_osd_items_{index}_uri", f"vr_osd_items_{index}_uri_{key}"]
                                else:
                                    if key == "uri":
                                        io_domain_status = ("Fail","red")
                                        output_subdomain_status = ("Fail","red")
                                        # self.__bco_object__["io_domain"]["input_subdomain"][index]["color"] = ["red"]
                                        # self.__bco_object__["io_domain"]["input_subdomain"][index]["uri"]["color"] = ["red"]
                                        self.__bco_object__["io_domain"]["output_subdomain"][index]["uri"][key]=[value,"fail", "red", f"output_subdomain item.{index}.uri.{key} is empty", f"vr_io_domain-vr_osd-vr_osd_items_{index}-vr_osd_items_{index}_uri", f"vr_osd_items_{index}_uri_{key}"]



            self.__bco_object__.update({"io_domain_status":io_domain_status})
            self.__bco_object__["io_domain"].update({"input_subdomain_status":input_subdomain_status})
            self.__bco_object__["io_domain"].update({"output_subdomain_status":output_subdomain_status})


        except Exception as e:
            logger.error(f"Cannot validate IO domain -- {repr(e)}")

    def validate_error_domain(self):
        try:
            error_domain_status = ("Pass", "")
            empirical_error_status = ("Pass", "")
            algorithmic_error_status = ("Pass", "")


            if not self.__bco_object__['error_domain']['empirical_error']:
                error_domain_status = ("Fail", "red")
                empirical_error_status = ("Fail", "red", "empirical_error is empty", "vr_error_domain-vr_emp_err", "vr_emp_err")
            else:
                for key, value in self.__bco_object__['error_domain']['empirical_error'].items():
                    if key and value:
                        self.__bco_object__["error_domain"]["empirical_error"][key]=[value, "pass", "black", "entry valid", "vr_error_domain-vr_emp_err", f"vr_emp_err_{key}"]
                    else:
                        error_domain_status = ("Fail", "red")
                        empirical_error_status = ("Fail", "red")
                        self.__bco_object__["error_domain"]["empirical_error"][key]=[value, "fail", "red", "empirical_error entry has a null value", "vr_error_domain-vr_emp_err", f"vr_emp_err_{key}"]

            if not self.__bco_object__['error_domain']['algorithmic_error']:
                error_domain_status = ("Fail", "red")
                algorithmic_error_status = ("Fail", "red", "algorithmic_error is empty", "vr_error_domain-vr_alg_err", "vr_alg_err")
            else:
                for key, value in self.__bco_object__['error_domain']['algorithmic_error'].items():
                    if key and value:
                        self.__bco_object__["error_domain"]["algorithmic_error"][key]=[value, "pass", "black", "entry valid", "vr_error_domain-vr_alg_err", f"vr_alg_err_{key}"]
                    else:
                        error_domain_status = ("Fail", "red")
                        algorithmic_error_status = ("Fail", "red")
                        self.__bco_object__["error_domain"]["algorithmic_error"][key]=[value, "fail", "red", "algorithmic_error entry has a null value", "vr_error_domain-vr_alg_err", f"vr_alg_err_{key}"]

            if (not self.__bco_object__['error_domain']['empirical_error']) and (not self.__bco_object__['error_domain']['empirical_error']):
                error_domain_status = ("Fail","red","error_domain is empty", "vr_error_domain")
                empirical_error_status = ("Fail","red","empirical_error is empty", "vr_error_domain-vr_emp_err", "vr_emp_err")
                algorithmic_error_status = ("Fail","red","algorithmic_error is empty", "vr_error_domain-vr_alg_err", "vr_alg_err")


            self.__bco_object__.update({"error_domain_status":error_domain_status})
            self.__bco_object__["error_domain"].update({"empirical_error_status":empirical_error_status})
            self.__bco_object__["error_domain"].update({"algorithmic_error_status":algorithmic_error_status})
        except Exception as e:
            logger.error(f"Cannot validate error domain -- {repr(e)}")

    def validate_provenance_domain(self):
        try:
            provenance_domain_status = ("Pass", "")
            if not self.__bco_object__["provenance_domain"]:
                provenance_domain_status = ("Fail", "red", "Provenance domain is empty", "vr_provenance_domain", "vr_provenance_domain")
            provenance_domain_review_status = ("Pass", "")
            provenance_domain_embargo_status = ("Pass", "")
            provenance_domain_contributors_status = ("Pass", "")
            for key, value in self.__bco_object__["provenance_domain"].items():
                if key not in ["review", "embargo", "contributors"]:
                    if value:
                        if isinstance(value, str):
                            self.__bco_object__["provenance_domain"][key] = [value, "pass", "black", f"{key} is valid","vr_provenance_domain", f"vr_po_{key}"]
                        else:
                            provenance_domain_status = ("Fail", "red")
                            self.__bco_object__["provenance_domain"][key] = [value, "fail", "red", f"{key} is not a string","vr_provenance_domain", f"vr_po_{key}"]
                    else:
                        if key not in ["derived_from", "obsolete_after"]:
                            provenance_domain_status = ("Fail", "red")
                            self.__bco_object__["provenance_domain"][key] = [value, "fail", "red", f"{key} is empty","vr_provenance_domain", f"vr_po_{key}"]
                elif key == "review":
                    if value:
                        for index, r in enumerate(value):
                            for c_key, c_value in r.items():
                                if c_key not in ["reviewer", "status"] :
                                    if c_value:
                                        if isinstance(c_value, str):
                                            self.__bco_object__["provenance_domain"][key][index][c_key] = [c_value, "pass", "black", f"{key}.{index}.{c_key} is valid", f"vr_provenance_domain-vr_po_{key}-vr_po_{key}_{index}", f"vr_po_{key}_{index}_{c_key}"]
                                        else:
                                            provenance_domain_status = ("Fail", "red")
                                            provenance_domain_review_status = ("Fail", "red")
                                            self.__bco_object__["provenance_domain"][key][index][c_key] = [c_value, "fail", "red", f"{key}.{index}.{c_key} is not a string", f"vr_provenance_domain-vr_po_{key}-vr_po_{key}_{index}", f"vr_po_{key}_{index}_{c_key}"]
                                    else:
                                        provenance_domain_status = ("Fail", "red")
                                        provenance_domain_review_status = ("Fail", "red")
                                        self.__bco_object__["provenance_domain"][key][index][c_key] = [c_value, "fail", "red", f"{key}.{index}.{c_key} is empty", f"vr_provenance_domain-vr_po_{key}-vr_po_{key}_{index}", f"vr_po_{key}_{index}_{c_key}"]
                                elif c_key == "status":
                                    if c_value:
                                        if c_value in ["unreviewed","in-review","approved","rejected","suspended"]:
                                            self.__bco_object__["provenance_domain"][key][index][c_key] = [c_value, "pass", "black", f"{key}.{index}.{c_key} is valid", f"vr_provenance_domain-vr_po_{key}-vr_po_{key}_{index}", f"vr_po_{key}_{index}_{c_key}"]
                                        else:
                                            provenance_domain_status = ("Fail", "red")
                                            provenance_domain_review_status = ("Fail", "red")
                                            self.__bco_object__["provenance_domain"][key][index][c_key] = [c_value, "fail", "red", f"{key}.{index}.{c_key} is not part of status enum", f"vr_provenance_domain-vr_po_{key}-vr_po_{key}_{index}", f"vr_po_{key}_{index}_{c_key}"]
                                    else:
                                        provenance_domain_status = ("Fail", "red")
                                        provenance_domain_review_status = ("Fail", "red")
                                        self.__bco_object__["provenance_domain"][key][index][c_key] = [c_value, "fail", "red", f"{key}.{index}.{c_key} is empty", f"vr_provenance_domain-vr_po_{key}-vr_po_{key}_{index}", f"vr_po_{key}_{index}_{c_key}"]
                                else:
                                    for cc_key, cc_value in c_value.items():
                                        if cc_key != "contribution":
                                            if cc_value:
                                                if isinstance(cc_value, str):
                                                    self.__bco_object__["provenance_domain"][key][index][c_key][cc_key] = [cc_value, "pass", "black", f"{key}.{index}.{c_key}.{cc_key} is valid", f"vr_provenance_domain-vr_po_{key}-vr_po_{key}_{index}-vr_po_{key}_{index}_{c_key}", f"vr_po_{key}_{index}_{c_key}_{cc_key}"]
                                                else:
                                                    provenance_domain_status = ("Fail", "red")
                                                    provenance_domain_review_status = ("Fail", "red")
                                                    self.__bco_object__["provenance_domain"][key][index][c_key][cc_key] = [cc_value, "fail", "red", f"{key}.{index}.{c_key}.{cc_key} is not a string", f"vr_provenance_domain-vr_po_{key}-vr_po_{key}_{index}-vr_po_{key}_{index}_{c_key}", f"vr_po_{key}_{index}_{c_key}_{cc_key}"]
                                            else:
                                                provenance_domain_status = ("Fail", "red")
                                                provenance_domain_review_status = ("Fail", "red")
                                                self.__bco_object__["provenance_domain"][key][index][c_key][cc_key] = [cc_value, "fail", "red", f"{key}.{index}.{c_key}.{cc_key} is empty", f"vr_provenance_domain-vr_po_{key}-vr_po_{key}_{index}-vr_po_{key}_{index}_{c_key}", f"vr_po_{key}_{index}_{c_key}_{cc_key}"]
                                        else:
                                            if cc_value:
                                                for contrib_index, contrib in enumerate(cc_value):
                                                    if contrib in ["authoredBy","contributedBy","createdAt","createdBy","createdWith","curatedBy","derivedFrom","importedBy","importedFrom","providedBy","retrievedBy","retrievedFrom","sourceAccessedBy"]:
                                                        self.__bco_object__["provenance_domain"][key][index][c_key][cc_key][contrib_index] = [contrib, "pass", "black", f"{key}.{c_key}.{cc_key}.{contrib_index} is valid", f"vr_provenance_domain-vr_po_{key}-vr_po_{key}_{index}-vr_po_{key}_{index}_{c_key}-vr_po_{key}_{index}_{c_key}_{cc_key}", f"vr_po_{key}_{index}_{c_key}_{cc_key}_{contrib_index}"]
                                                    else:
                                                        provenance_domain_status = ("Fail", "red")
                                                        provenance_domain_review_status = ("Fail", "red")
                                                        # self.__bco_object__["provenance_domain"][key][index][c_key][cc_key] = [cc_value, "fail", "red", f"{key}.{c_key}.{cc_key} is not part of enum", f"vr_provenance_domain-vr_po_{key}-vr_po_{key}_{index}-vr_po_{key}_{index}_{c_key}", f"vr_po_{key}_{index}_{c_key}_{cc_key}"]
                                                        self.__bco_object__["provenance_domain"][key][index][c_key][cc_key][contrib_index] = [contrib, "fail", "red", f"{key}.{index}.{c_key}.{cc_key}.{contrib_index} is not part of enum", f"vr_provenance_domain-vr_po_{key}-vr_po_{key}_{index}-vr_po_{key}_{index}_{c_key}-vr_po_{key}_{index}_{c_key}_{cc_key}", f"vr_po_{key}_{index}_{c_key}_{cc_key}_{contrib_index}"]
                                            else:
                                                provenance_domain_status = ("Fail", "red")
                                                provenance_domain_review_status = ("Fail", "red")
                                                self.__bco_object__["provenance_domain"][key][index][c_key][cc_key] = [cc_value, "fail", "red", f"{key}.{c_key}.{cc_key} is empty", f"vr_provenance_domain-vr_po_{key}-vr_po_{key}_{index}-vr_po_{key}_{index}_{c_key}", f"vr_po_{key}_{index}_{c_key}_{cc_key}"]

                    # else:
                    #     provenance_domain_status = ("Fail", "red")
                    #     provenance_domain_review_status = ("Fail", "red", "review is empty", "vr_provenance_domain-vr_review", "vr_review")
                elif key == "embargo":
                    for c_key, c_value in value.items():
                        if c_value:
                            if isinstance(c_value, str):
                                self.__bco_object__["provenance_domain"][key][c_key] = [c_value, "pass", "black", f"{key}.{c_key} is valid",f"vr_provenance_domain-vr_po_{key}", f"vr_po_{key}_{c_key}" ]
                            else:
                                provenance_domain_status = ("Fail", "red")
                                provenance_domain_embargo_status = ("Fail", "red")
                                self.__bco_object__["provenance_domain"][key][c_key] = [c_value, "fail", "red", f"{key}.{c_key} is not a string",f"vr_provenance_domain-vr_po_{key}", f"vr_po_{key}_{c_key}" ]
                        # else:
                        #     provenance_domain_status = ("Fail", "red")
                        #     provenance_domain_embargo_status = ("Fail", "red")
                        #     self.__bco_object__["provenance_domain"][key][c_key] = [c_value, "fail", "red", f"{key}.{c_key} is empty",f"vr_provenance_domain-vr_po_{key}", f"vr_po_{key}_{c_key}" ]
                elif key == "contributors":
                    if value:
                        for index, contributor in enumerate(value):
                            for c_key, c_value in contributor.items():
                                if c_key != "contribution":
                                    if c_value:
                                        if isinstance(c_value, str):
                                            self.__bco_object__['provenance_domain'][key][index][c_key]=[c_value, "pass", "black", f"{key}.{index}.{c_key} is valid", f"vr_provenance_domain-vr_po_{key}-vr_po_{key}_{index}", f"vr_po_{key}_{index}_{c_key}"]
                                        else:
                                            provenance_domain_status = ("Fail", "red")
                                            provenance_domain_contributors_status = ("Fail", "red")
                                            self.__bco_object__['provenance_domain'][key][index][c_key]=[c_value, "fail", "red", f"{key}.{index}.{c_key} is not a string", f"vr_provenance_domain-vr_po_{key}-vr_po_{key}_{index}", f"vr_po_{key}_{index}_{c_key}"]
                                    else:
                                        provenance_domain_status = ("Fail", "red")
                                        provenance_domain_contributors_status = ("Fail", "red")
                                        self.__bco_object__['provenance_domain'][key][index][c_key]=[c_value, "fail", "red", f"{key}.{index}.{c_key} is empty", f"vr_provenance_domain-vr_po_{key}-vr_po_{key}_{index}", f"vr_po_{key}_{index}_{c_key}"]
                                else:
                                    if c_value:
                                        for contrib_index, contrib in enumerate(c_value):
                                            if contrib in ["authoredBy","contributedBy","createdAt","createdBy","createdWith","curatedBy","derivedFrom","importedBy","importedFrom","providedBy","retrievedBy","retrievedFrom","sourceAccessedBy"]:
                                                self.__bco_object__["provenance_domain"][key][index][c_key][contrib_index] = [contrib, "pass", "black", f"{key}.{index}.{c_key}.{contrib_index} is valid", f"vr_provenance_domain-vr_po_{key}-vr_po_{key}_{index}-vr_po_{key}_{index}_{c_key}", f"vr_po_{key}_{index}_{c_key}_{contrib_index}"]
                                            else:
                                                provenance_domain_status = ("Fail", "red")
                                                provenance_domain_contributors_status = ("Fail", "red")
                                                self.__bco_object__["provenance_domain"][key][index][c_key][contrib_index] = [contrib, "fail", "red", f"{key}.{index}.{c_key}.{contrib_index} is not part of enum", f"vr_provenance_domain-vr_po_{key}-vr_po_{key}_{index}-vr_po_{key}_{index}_{c_key}", f"vr_po_{key}_{index}_{c_key}_{contrib_index}"]
                                    else:
                                        provenance_domain_status = ("Fail", "red")
                                        provenance_domain_contributors_status = ("Fail", "red")
                                        self.__bco_object__['provenance_domain'][key][index][c_key] = [c_value, "fail", "red", f"{key}.{index}.{c_key} is empty", f"vr_provenance_domain-vr_po_{key}-vr_po_{key}_{index}",f"vr_po_{key}_{index}_{c_key}"]

                    else:
                        provenance_domain_status = ("Fail", "red")
                        provenance_domain_contributors_status = ("Fail", "red", f"contributors is empty", f"vr_provenance_domain-vr_po_{key}", "vr_po_contributors")

            self.__bco_object__.update({"provenance_domain_status":provenance_domain_status})
            self.__bco_object__['provenance_domain'].update({"provenance_domain_review_status":provenance_domain_review_status})
            self.__bco_object__['provenance_domain'].update({"provenance_domain_embargo_status":provenance_domain_embargo_status})
            self.__bco_object__['provenance_domain'].update({"provenance_domain_contributors_status":provenance_domain_contributors_status})
            # print(self.__bco_object__['provenance_domain'])
        except Exception as e:
            logger.error(f"Cannot validate provenance domain -- {repr(e)}")

    def validate_description_domain(self):
        try:
            description_domain_status = ["Pass", "", ]

            if not self.__bco_object__["description_domain"]:
                description_domain_status = ("Fail", "red", "description domain is empty", "vr_description_domain", "vr_description_domain")

            for key, value in self.__bco_object__["description_domain"].items():

                if key == "keywords":
                    for index, keyword in enumerate(value):
                        if keyword:
                            if isinstance(keyword, str):
                                self.__bco_object__['description_domain'][key][index]=[keyword, "pass", "", f"{key}.{index} is valid", f"vr_description_domain-vr_dd_{key}", f"vr_dd_{key}_{index}"]
                            else:
                                description_domain_status=["Fail","red"]
                                self.__bco_object__['description_domain'][key][index]=[keyword, "fail", "red", f"{key}.{index} is not a string", f"vr_description_domain-vr_dd_{key}", f"vr_dd_{key}_{index}"]
                        else:
                            description_domain_status=["Fail","red"]
                            self.__bco_object__['description_domain'][key][index]=[keyword, "fail", "red", f"{key}.{index} is empty", f"vr_description_domain-vr_dd_{key}", f"vr_dd_{key}_{index}"]
                elif key == "platform":
                    for index, pl in enumerate(value):
                        if pl:
                            if isinstance(pl, str):
                                self.__bco_object__['description_domain'][key][index]=[pl, "pass", "", f"{key}.{index} is valid", f"vr_description_domain-vr_dd_{key}", f"vr_dd_{key}_{index}"]
                            else:
                                description_domain_status=["Fail","red"]
                                self.__bco_object__['description_domain'][key][index]=[pl, "fail", "red", f"{key}.{index} is not a string", f"vr_description_domain-vr_dd_{key}", f"vr_dd_{key}_{index}"]
                        else:
                            description_domain_status=["Fail","red"]
                            self.__bco_object__['description_domain'][key][index]=[pl, "fail", "red", f"{key}.{index} is empty", f"vr_description_domain-vr_dd_{key}", f"vr_dd_{key}_{index}"]
                elif key == "xref":
                    for index, x in enumerate(value):
                        for c_key, c_value in x.items():
                            if c_key == "ids":
                                if c_value:
                                    for id_index, id in enumerate(c_value):
                                        if id:
                                            if isinstance(id, str):
                                                self.__bco_object__['description_domain'][key][index][c_key][id_index] = [id, "pass", "", f"{key}.{index}.{c_key}.{id_index} is valid", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{index}-vr_dd_{key}_{index}_{c_key}", f"vr_dd_{key}_{index}_{c_key}_{id_index}"]
                                            else:
                                                description_domain_status=["Fail","red"]
                                                self.__bco_object__['description_domain'][key][index][c_key][id_index] = [id, "fail", "red", f"{key}.{index}.{c_key}.{id_index} is not a string", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{index}-vr_dd_{key}_{index}_{c_key}", f"vr_dd_{key}_{index}_{c_key}_{id_index}"]
                                        else:
                                            description_domain_status=["Fail","red"]
                                            self.__bco_object__['description_domain'][key][index][c_key][id_index] = [id, "fail", "red", f"{key}.{index}.{c_key}.{id_index} is empty", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{index}-vr_dd_{key}_{index}_{c_key}", f"vr_dd_{key}_{index}_{c_key}_{id_index}"]
                                # else:
                                #     description_domain_status=["Fail","red"]
                                #     self.__bco_object__['description_domain'][key][index][c_key] = [c_value, "fail", "red", f"{key}.{index}.{c_key} is empty", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{index}", f"vr_dd_{key}_{index}_{c_key}"]
                            else:
                                if c_value:
                                    if isinstance(c_value, str):
                                        self.__bco_object__['description_domain'][key][index][c_key] = [c_value, "pass", "", f"{key}.{index}.{c_key} is valid", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{index}", f"vr_dd_{key}_{index}_{c_key}"]
                                    else:
                                        description_domain_status=["Fail","red"]
                                        self.__bco_object__['description_domain'][key][index][c_key] = [c_value, "fail", "red", f"{key}.{index}.{c_key} is not a string", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{index}", f"vr_dd_{key}_{index}_{c_key}"]
                                else:
                                    description_domain_status=["Fail","red"]
                                    self.__bco_object__['description_domain'][key][index][c_key] = [c_value, "fail", "red", f"{key}.{index}.{c_key} is empty", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{index}", f"vr_dd_{key}_{index}_{c_key}"]
                elif key=="pipeline_steps":
                    for st_index, step in enumerate(value):
                        for c_key, c_value in step.items():
                            if c_key == "prerequisite":
                                for pr_index, pr in enumerate(c_value):
                                    # print("pr", pr_index)
                                    for cc_key, cc_value in pr.items():
                                        if cc_key == "uri":
                                            for ccc_key, ccc_value in cc_value.items():
                                                if ccc_value:
                                                    if isinstance(ccc_value, str):
                                                        self.__bco_object__["description_domain"][key][st_index][c_key][pr_index][cc_key][ccc_key] = [ccc_value, "pass", "", f"{key}.{st_index}.{c_key}.{pr_index}.{cc_key}.{ccc_key} is valid", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{st_index}-vr_dd_{key}_{st_index}_{c_key}-vr_dd_{key}_{st_index}_{c_key}_{pr_index}-vr_dd_{key}_{st_index}_{c_key}_{pr_index}_{cc_key}", f"vr_dd_{key}_{st_index}_{c_key}_{pr_index}_{cc_key}_{ccc_key}"]
                                                    else:
                                                        description_domain_status=["Fail", "red"]
                                                        self.__bco_object__["description_domain"][key][st_index][c_key][pr_index][cc_key][ccc_key] = [ccc_value, "fail", "red", f"{key}.{st_index}.{c_key}.{pr_index}.{cc_key}.{ccc_key} is not a string", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{st_index}-vr_dd_{key}_{st_index}_{c_key}-vr_dd_{key}_{st_index}_{c_key}_{pr_index}-vr_dd_{key}_{st_index}_{c_key}_{pr_index}_{cc_key}", f"vr_dd_{key}_{st_index}_{c_key}_{pr_index}_{cc_key}_{ccc_key}"]
                                                else:
                                                    if ccc_key == "uri":
                                                        description_domain_status=["Fail", "red"]
                                                        self.__bco_object__["description_domain"][key][st_index][c_key][pr_index][cc_key][ccc_key] = [ccc_value, "fail", "red", f"{key}.{st_index}.{c_key}.{pr_index}.{cc_key}.{ccc_key} is empty", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{st_index}-vr_dd_{key}_{st_index}_{c_key}-vr_dd_{key}_{st_index}_{c_key}_{pr_index}-vr_dd_{key}_{st_index}_{c_key}_{pr_index}_{cc_key}", f"vr_dd_{key}_{st_index}_{c_key}_{pr_index}_{cc_key}_{ccc_key}"]
                                        else:
                                            if cc_value:
                                                if isinstance(cc_value, str):
                                                    self.__bco_object__['description_domain'][key][st_index][c_key][pr_index][cc_key]=[cc_value, "pass", "", f"{key}.{st_index}.{c_key}.{pr_index}.{cc_key} is valid", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{st_index}-vr_dd_{key}_{st_index}_{c_key}-vr_dd_{key}_{st_index}_{c_key}_{pr_index}", f"vr_dd_{key}_{st_index}_{c_key}_{pr_index}_{cc_key}"]
                                                else:
                                                    description_domain_status=["Fail","red"]
                                                    self.__bco_object__['description_domain'][key][st_index][c_key][pr_index][cc_key]=[cc_value, "fail", "red", f"{key}.{st_index}.{c_key}.{pr_index}.{cc_key} is not a string", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{st_index}-vr_dd_{key}_{st_index}_{c_key}-vr_dd_{key}_{st_index}_{c_key}_{pr_index}", f"vr_dd_{key}_{st_index}_{c_key}_{pr_index}_{cc_key}"]
                                            else:
                                                # print("inside else")
                                                description_domain_status=["Fail","red"]
                                                # print(key,st_index,c_key,cc_key)
                                                self.__bco_object__['description_domain'][key][st_index][c_key][pr_index][cc_key]=[cc_value, "fail", "red", f"{key}.{st_index}.{c_key}.{pr_index}.{cc_key} is empty", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{st_index}-vr_dd_{key}_{st_index}_{c_key}-vr_dd_{key}_{st_index}_{c_key}_{pr_index}", f"vr_dd_{key}_{st_index}_{c_key}_{pr_index}_{cc_key}"]
                                                # print("inside after else")
                            elif c_key == "input_list":
                                for il_index, il in enumerate(c_value):

                                    for cc_key, cc_value in il.items():
                                        if cc_value:
                                            if isinstance(cc_value, str):
                                                self.__bco_object__['description_domain'][key][st_index][c_key][il_index][cc_key]=[cc_value, "pass", "", f"{key}.{st_index}.{c_key}.{il_index}.{cc_key} is valid", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{st_index}-vr_dd_{key}_{st_index}_{c_key}-vr_dd_{key}_{st_index}_{c_key}_{il_index}", f"vr_dd_{key}_{st_index}_{c_key}_{il_index}_{cc_key}"]
                                            else:
                                                description_domain_status=["Fail","red"]
                                                self.__bco_object__['description_domain'][key][st_index][c_key][il_index][cc_key]=[cc_value, "fail", "red", f"{key}.{st_index}.{c_key}.{il_index}.{cc_key} is not a string", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{st_index}-vr_dd_{key}_{st_index}_{c_key}-vr_dd_{key}_{st_index}_{c_key}_{il_index}", f"vr_dd_{key}_{st_index}_{c_key}_{il_index}_{cc_key}"]
                                        else:
                                            if cc_key == "uri":
                                                description_domain_status=["Fail","red"]
                                                self.__bco_object__['description_domain'][key][st_index][c_key][il_index][cc_key]=[cc_value, "fail", "red", f"{key}.{st_index}.{c_key}.{il_index}.{cc_key} is empty", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{st_index}-vr_dd_{key}_{st_index}_{c_key}-vr_dd_{key}_{st_index}_{c_key}_{il_index}", f"vr_dd_{key}_{st_index}_{c_key}_{il_index}_{cc_key}"]

                            elif c_key == "output_list":
                                for ol_index, ol in enumerate(c_value):
                                    for cc_key, cc_value in ol.items():
                                        if cc_value:
                                            if isinstance(cc_value, str):
                                                self.__bco_object__['description_domain'][key][st_index][c_key][ol_index][cc_key]=[cc_value, "pass", "", f"{key}.{st_index}.{c_key}.{ol_index}.{cc_key} is valid", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{st_index}-vr_dd_{key}_{st_index}_{c_key}-vr_dd_{key}_{st_index}_{c_key}_{ol_index}", f"vr_dd_{key}_{st_index}_{c_key}_{ol_index}_{cc_key}"]
                                            else:
                                                description_domain_status=["Fail","red"]
                                                self.__bco_object__['description_domain'][key][st_index][c_key][ol_index][cc_key]=[cc_value, "fail", "red", f"{key}.{st_index}.{c_key}.{ol_index}.{cc_key} is not a string", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{st_index}-vr_dd_{key}_{st_index}_{c_key}-vr_dd_{key}_{st_index}_{c_key}_{ol_index}", f"vr_dd_{key}_{st_index}_{c_key}_{ol_index}_{cc_key}"]
                                        else:
                                            if cc_key == "uri":
                                                description_domain_status=["Fail","red"]
                                                self.__bco_object__['description_domain'][key][st_index][c_key][ol_index][cc_key]=[cc_value, "fail", "red", f"{key}.{st_index}.{c_key}.{ol_index}.{cc_key} is empty", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{st_index}-vr_dd_{key}_{st_index}_{c_key}-vr_dd_{key}_{st_index}_{c_key}_{ol_index}", f"vr_dd_{key}_{st_index}_{c_key}_{ol_index}_{cc_key}"]

                            elif c_key == "step_number":
                                if c_value:
                                    if isinstance(c_value, int):
                                        self.__bco_object__['description_domain'][key][st_index][c_key] = [c_value, "pass", "", f"{key}.{st_index}.{c_key} is valid", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{st_index}", f"vr_dd_{key}_{st_index}_{c_key}"]
                                    else:
                                        description_domain_status=["Fail","red"]
                                        self.__bco_object__['description_domain'][key][st_index][c_key] = [c_value, "fail", "red", f"{key}.{st_index}.{c_key} is not a integer", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{st_index}", f"vr_dd_{key}_{st_index}_{c_key}"]
                                else:
                                    description_domain_status=["Fail","red"]
                                    self.__bco_object__['description_domain'][key][st_index][c_key] = [c_value, "fail", "red", f"{key}.{st_index}.{c_key} is empty", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{st_index}", f"vr_dd_{key}_{st_index}_{c_key}"]

                            else:
                                if c_value:
                                    if isinstance(c_value, str):
                                        self.__bco_object__['description_domain'][key][st_index][c_key] = [c_value, "pass", "", f"{key}.{st_index}.{c_key} is valid", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{st_index}", f"vr_dd_{key}_{st_index}_{c_key}"]
                                    else:
                                        description_domain_status=["Fail","red"]
                                        self.__bco_object__['description_domain'][key][st_index][c_key] = [c_value, "fail", "red", f"{key}.{st_index}.{c_key} is not a string", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{st_index}", f"vr_dd_{key}_{st_index}_{c_key}"]
                                else:
                                    description_domain_status=["Fail","red"]
                                    self.__bco_object__['description_domain'][key][st_index][c_key] = [c_value, "fail", "red", f"{key}.{st_index}.{c_key} is empty", f"vr_description_domain-vr_dd_{key}-vr_dd_{key}_{st_index}", f"vr_dd_{key}_{st_index}_{c_key}"]

            self.__bco_object__.update({"description_domain_status":description_domain_status})
            # print(self.__bco_object__['description_domain'])
        except Exception as e:
            logger.error(f"Cannot validate description_domain -- {repr(e)}")

    def validate_execution_domain(self):
        try:
            execution_domain_status = ["Pass", "", ]

            if not self.__bco_object__["execution_domain"]:
                execution_domain_status = ("Fail", "red", "execution domain is empty", "vr_execution_domain", "vr_execution_domain")
            # breakpoint()
            for key, value in self.__bco_object__["execution_domain"].items():
                if key == "script":
                    for sc_index, sc in enumerate(value):
                        for c_key, c_value in sc.items():
                            for cc_key, cc_value in c_value.items():
                                if cc_value:
                                    if isinstance(cc_value, str):
                                        self.__bco_object__['execution_domain'][key][sc_index][c_key][cc_key] = [cc_value, "pass", "", f"{key}.{sc_index}.{c_key}.{cc_key} is valid", f"vr_execution_domain-vr_ed_{key}-vr_ed_{key}_{sc_index}-vr_ed_{key}_{sc_index}_{c_key}",f"vr_ed_{key}_{sc_index}_{c_key}_{cc_key}"]
                                    else:
                                        execution_domain_status = ["Fail", "red", ]
                                        self.__bco_object__['execution_domain'][key][sc_index][c_key][cc_key] = [cc_value, "fail", "red", f"{key}.{sc_index}.{c_key}.{cc_key} is not a string", f"vr_execution_domain-vr_ed_{key}-vr_ed_{key}_{sc_index}-vr_ed_{key}_{sc_index}_{c_key}",f"vr_ed_{key}_{sc_index}_{c_key}_{cc_key}"]
                                else:
                                    if cc_key == "uri":
                                        execution_domain_status = ["Fail", "red", ]
                                        self.__bco_object__['execution_domain'][key][sc_index][c_key][cc_key] = [cc_value, "fail", "red", f"{key}.{sc_index}.{c_key}.{cc_key} is empty", f"vr_execution_domain-vr_ed_{key}-vr_ed_{key}_{sc_index}-vr_ed_{key}_{sc_index}_{c_key}",f"vr_ed_{key}_{sc_index}_{c_key}_{cc_key}"]
                elif key=="script_driver":
                    if value:
                        if isinstance(value, str):
                            self.__bco_object__['execution_domain'][key] = [value, "pass", "", f"{key} is valid", f"vr_execution_domain", f"vr_ed_{key}"]
                        else:
                            execution_domain_status = ["Fail", "red", ]
                            self.__bco_object__['execution_domain'][key] = [value, "fail", "red", f"{key} is not a string", f"vr_execution_domain", f"vr_ed_{key}"]
                    else:
                        execution_domain_status = ["Fail", "red", ]
                        self.__bco_object__['execution_domain'][key] = [value, "fail", "red", f"{key} is empty", f"vr_execution_domain", f"vr_ed_{key}"]

                elif key == "software_prerequisites":
                    for sw_index, sw in enumerate(value):
                        for c_key, c_value in sw.items():
                            if c_key == "uri":
                                for cc_key, cc_value in c_value.items():
                                    if cc_value:
                                        if isinstance(cc_value, str):
                                            self.__bco_object__['execution_domain'][key][sw_index][c_key][cc_key] = [cc_value, "pass", "", f"{key}.{sw_index}.{c_key}.{cc_key} is valid", f"vr_execution_domain-vr_ed_{key}-vr_ed_{key}_{sw_index}-vr_ed_{key}_{sw_index}_{c_key}",f"vr_ed_{key}_{sw_index}_{c_key}_{cc_key}"]
                                        else:
                                            execution_domain_status = ["Fail", "red", ]
                                            self.__bco_object__['execution_domain'][key][sw_index][c_key][cc_key] = [cc_value, "fail", "red", f"{key}.{sw_index}.{c_key}.{cc_key} is not a string", f"vr_execution_domain-vr_ed_{key}-vr_ed_{key}_{sw_index}-vr_ed_{key}_{sw_index}_{c_key}",f"vr_ed_{key}_{sw_index}_{c_key}_{cc_key}"]
                                    else:
                                        if cc_key == "uri":
                                            execution_domain_status = ["Fail", "red", ]
                                            self.__bco_object__['execution_domain'][key][sw_index][c_key][cc_key] = [cc_value, "fail", "red", f"{key}.{sw_index}.{c_key}.{cc_key} is empty", f"vr_execution_domain-vr_ed_{key}-vr_ed_{key}_{sw_index}-vr_ed_{key}_{sw_index}_{c_key}",f"vr_ed_{key}_{sw_index}_{c_key}_{cc_key}"]
                            else:
                                if c_value:
                                    if isinstance(c_value, str):
                                        self.__bco_object__['execution_domain'][key][sw_index][c_key] = [c_value, "pass", "", f"{key}.{sw_index}.{c_key} is valid", f"vr_execution_domain-vr_ed_{key}-vr_ed_{key}_{sw_index}", f"vr_ed_{key}_{sw_index}_{c_key}"]
                                    else:
                                        execution_domain_status = ["Fail", "red", ]
                                        self.__bco_object__['execution_domain'][key][sw_index][c_key] = [c_value, "fail", "red", f"{key}.{sw_index}.{c_key} is not a string", f"vr_execution_domain-vr_ed_{key}-vr_ed_{key}_{sw_index}", f"vr_ed_{key}_{sw_index}_{c_key}"]
                                else:
                                    execution_domain_status = ["Fail", "red", ]
                                    self.__bco_object__['execution_domain'][key][sw_index][c_key] = [c_value, "fail", "red", f"{key}.{sw_index}.{c_key} is empty", f"vr_execution_domain-vr_ed_{key}-vr_ed_{key}_{sw_index}", f"vr_ed_{key}_{sw_index}_{c_key}"]
                elif key == "external_data_endpoints":
                    for edp_index, edp in enumerate(value):
                        for c_key, c_value in edp.items():
                            if c_value:
                                if isinstance(c_value, str):
                                    self.__bco_object__['execution_domain'][key][edp_index][c_key] = [c_value, "pass", "", f"{key}.{edp_index}.{c_key} is valid", f"vr_execution_domain-vr_ed_{key}-vr_ed_{key}_{edp_index}", f"vr_ed_{key}_{edp_index}_{c_key}"]
                                else:
                                    execution_domain_status = ["Fail", "red", ]
                                    self.__bco_object__['execution_domain'][key][edp_index][c_key] = [c_value, "fail", "red", f"{key}.{edp_index}.{c_key} is not a string", f"vr_execution_domain-vr_ed_{key}-vr_ed_{key}_{edp_index}", f"vr_ed_{key}_{edp_index}_{c_key}"]
                            else:
                                execution_domain_status = ["Fail", "red", ]
                                self.__bco_object__['execution_domain'][key][edp_index][c_key] = [c_value, "fail", "red", f"{key}.{edp_index}.{c_key} is empty", f"vr_execution_domain-vr_ed_{key}-vr_ed_{key}_{edp_index}", f"vr_ed_{key}_{edp_index}_{c_key}"]

                elif key == "environment_variables":
                    for c_key, c_value in value.items():
                        if c_key and c_value:
                            self.__bco_object__['execution_domain'][key][c_key] = [c_value, "pass", "", f"{key}.{c_key} is a valid entry", f"vr_execution_domain-vr_ed_{key}", f"vr_ed_{key}_{c_key}"]
                        else:
                            execution_domain_status = ["Fail", "red", ]
                            self.__bco_object__['execution_domain'][key][c_key] = [c_value, "fail", "red", f"{key}.{c_key} is not a valid entry", f"vr_execution_domain-vr_ed_{key}", f"vr_ed_{key}_{c_key}"]
            self.__bco_object__.update({"execution_domain_status":execution_domain_status})
            # print(self.__bco_object__['execution_domain'])
        except Exception as e:
            logger.error(f"Cannot validate execution_domain -- {repr(e)}")



    # def validate_io_domain(self):
    #     try:
    #         io_domain_status = ("Pass", "black")
    #         for key, value in self.__bco_object__['io_domain'].items():
    #             if key == "input_subdomain":
    #                 self.__bco_object__['io_domain'][key] = [value,"pass","",f'item {key} pass','',f'vr_io_domain_{key}']
    #                 for index, isd in enumerate(value):
    #                     print("in for")
    #                     self.__bco_object__['io_domain'][key][index] = [isd,"pass","",f'item {key}.{index} pass','',f'vr_io_domain_{key}_{index}']
    #                     for c_key, c_value in isd['uri'].items():
    #                         if c_value:
    #                             print("in if")
    #                             if isinstance(c_value, str):
    #                                 print("in if if")
    #                                 self.__bco_object__['io_domain'][key][index][0][c_key] = (c_value, 'pass', 'black', f'item {key}.{index}.{c_key} is a string', f'vr_io_domain-vr_io_domain_{key}-vr_io_domain_{key}_{index}',f'vr_io_{key}_items_{index}_{c_key}')
    #                             else:
    #                                 print("in if else")
    #                                 self.__bco_object__['io_domain'][key][index][0][c_key] = (c_value, 'fail', 'red', f'item {key}.{index}.{c_key} is not a string', f'vr_io_domain-vr_io_domain_{key}-vr_io_domain_{key}_{index}',f'vr_io_{key}_items_{index}_{c_key}')
    #                                 self.__bco_object__['io_domain'][key][index] = [isd,"fail","red",f'item {key}.{index} fail','',f'vr_io_domain_{key}_{index}']
    #                                 self.__bco_object__['io_domain'][key] = [value,"fail","red",f'item {key} fail','',f'vr_io_domain_{key}']
    #                                 io_domain_status = ("Fail", "red")
    #                         else:
    #                             print("in else")
    #                             self.__bco_object__['io_domain'][key][index][0][c_key] = (c_value, 'fail', 'red', f'item {key}.{index}.{c_key} is a null value', f'vr_io_domain-vr_io_domain_{key}-vr_io_domain_{key}_{index}',f'vr_io_{key}_items_{index}_{c_key}')
    #                             self.__bco_object__['io_domain'][key][index] = [isd,"fail","red",f'item {key}.{index} fail','',f'vr_io_domain_{key}_{index}']
    #                             self.__bco_object__['io_domain'][key] = [value,"fail","red",f'item {key} fail','',f'vr_io_domain_{key}']
    #                             io_domain_status = ("Fail", "red")

    #             if key == "output_subdomain":
    #                 for index, osd in enumerate(value):
    #                     print("ot for")
    #                     self.__bco_object__['io_domain'][key][index] = [osd,"pass","",f'item {key}.{index} pass','',f'vr_io_domain_{key}_{index}']
    #                     for c_key, c_value in osd.items():
    #                         print("ot for for")
    #                         if c_key == "uri":
    #                             print("ot if")
    #                             for c_c_key, c_c_value in c_value.items():
    #                                 print("ot if for")
    #                                 if c_c_value:
    #                                     print("ot if for if")
    #                                     if isinstance(c_c_value, str):
    #                                         print("ot if for if if")
    #                                         self.__bco_object__['io_domain'][key][index][0][c_key][c_c_key] = (c_value, 'pass', 'black', f'item {key}.{index}.{c_key}.{c_c_key} is a string', f'vr_io_domain-vr_io_domain_{key}-vr_io_domain_{key}_{index}-vr_io_domain_{key}_{index}_{c_key}',f'vr_io_{key}_items_{index}_{c_key}_{c_c_key}')

    #                                     else:
    #                                         print("ot if for if else")
    #                                         self.__bco_object__['io_domain'][key][index][0][c_key][c_c_key] = (c_value, 'fail', 'red', f'item {key}.{index}.{c_key}.{c_c_key} is not a string', f'vr_io_domain-vr_io_domain_{key}-vr_io_domain_{key}_{index}-vr_io_domain_{key}_{index}_{c_key}',f'vr_io_{key}_items_{index}_{c_key}_{c_c_key}')
    #                                         self.__bco_object__['io_domain'][key][index][0][c_key] = (c_value, 'fail', 'red', f'item {key}.{index}.{c_key} is not a string', f'vr_io_domain-vr_io_domain_{key}-vr_io_domain_{key}_{index}',f'vr_io_{key}_items_{index}_{c_key}')
    #                                         self.__bco_object__['io_domain'][key][index] = [osd,"fail","red",f'item {key}.{index} fail','',f'vr_io_domain_{key}_{index}']
    #                                         self.__bco_object__['io_domain'][key] = [value,"fail","red",f'item {key} fail','',f'vr_io_domain_{key}']
    #                                         io_domain_status = ("Fail", "red")
    #                                 else:
    #                                     print("ot if for else")
    #                                     self.__bco_object__['io_domain'][key][index][0][c_key][c_c_key] = (c_value, 'fail', 'red', f'item {key}.{index}.{c_key}.{c_c_key} is not a string', f'vr_io_domain-vr_io_domain_{key}-vr_io_domain_{key}_{index}-vr_io_domain_{key}_{index}_{c_key}',f'vr_io_{key}_items_{index}_{c_key}_{c_c_key}')
    #                                     self.__bco_object__['io_domain'][key][index][0][c_key] = (c_value, 'fail', 'red', f'item {key}.{index}.{c_key} is not a string', f'vr_io_domain-vr_io_domain_{key}-vr_io_domain_{key}_{index}',f'vr_io_{key}_items_{index}_{c_key}')
    #                                     self.__bco_object__['io_domain'][key][index] = [osd,"fail","red",f'item {key}.{index} fail','',f'vr_io_domain_{key}_{index}']
    #                                     self.__bco_object__['io_domain'][key] = [value,"fail","red",f'item {key} fail','',f'vr_io_domain_{key}']
    #                                     io_domain_status = ("Fail", "red")
    #                         else:
    #                             if c_value:
    #                                 print("ot else if")
    #                                 if isinstance(c_value, str):
    #                                     print("ot else if if")
    #                                     self.__bco_object__['io_domain'][key][index][0][c_key] = (c_value, 'pass', 'black', f'item {key}.{index}.{c_key} is a string', f'vr_io_domain-vr_io_domain_{key}-vr_io_domain_{key}_{index}',f'vr_io_{key}_items_{index}_{c_key}')
    #                                 else:
    #                                     print("ot else if else")
    #                                     self.__bco_object__['io_domain'][key][index][0][c_key] = (c_value, 'fail', 'red', f'item {key}.{index}.{c_key} is not a string', f'vr_io_domain-vr_io_domain_{key}-vr_io_domain_{key}_{index}',f'vr_io_{key}_items_{index}_{c_key}')
    #                                     self.__bco_object__['io_domain'][key][index] = [osd,"fail","red",f'item {key}.{index} fail','',f'vr_io_domain_{key}_{index}']
    #                                     self.__bco_object__['io_domain'][key] = [value,"fail","red",f'item {key} fail','',f'vr_io_domain_{key}']
    #                                     io_domain_status = ("Fail", "red")
    #                             else:
    #                                 print("ot else else")
    #                                 self.__bco_object__['io_domain'][key][index][0][c_key] = (c_value, 'fail', 'red', f'item {key}.{index}.{c_key} is a null value', f'vr_io_domain-vr_io_domain_{key}-vr_io_domain_{key}_{index}',f'vr_io_{key}_items_{index}_{c_key}')
    #                                 self.__bco_object__['io_domain'][key][index] = [osd,"fail","red",f'item {key}.{index} fail','',f'vr_io_domain_{key}_{index}']
    #                                 self.__bco_object__['io_domain'][key] = [value,"fail","red",f'item {key} fail','',f'vr_io_domain_{key}']
    #                                 io_domain_status = ("Fail", "red")

    #         self.__bco_object__.update({"io_domain_status":io_domain_status})
    #         print(self.__bco_object__['io_domain'])

    #     except Exception as e:
    #         logger.error(f"Cannot validate io domain -- {repr(e)}")