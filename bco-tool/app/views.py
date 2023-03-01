import copy
import json
import os
import subprocess
from collections import OrderedDict

from app.services.bco_db import BcoDB
from app.services.cwl import CWL
from app.services.dataservices.bco_data_service import \
    BcoDataService, ComparisonBcoDataService
from app.services.dataservices.bco_editor_export_service import BcoCleanUp
from app.services.dataservices.bco_editor_validation_service import \
    BcoEditorValidation
from app.services.dataservices.bco_validation_service import \
    BcoValidationService
from app.services.dnanexus import DNAnexus
from app.services.min_wdl_parse import Min_WDL_Parser
from app.services.pfda import PFDAClient
from django.conf import settings
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from script import CompileWorkflow

# from app.services.wdl import WDL
BCO_BASE = "app/schemas/biocompute.json"
COMPARISON_BCO = "app/schemas/biocompute_compare.json"
bco_comparison_file = ""


def load_bco():
    with open('app/schemas/biocompute.json','r') as f:
        return json.load(f)

def load_comparison_bco():
    with open("app/schemas/biocompute_compare.json", "r") as f:
        return json.load(f)

def load_bco_meta():
    with open('app/schemas/biocompute_meta.json','r') as f:
        return json.load(f)

def load_bco_skeleton():
    with open('app/schemas/biocompute_skeleton.json','r') as f:
        return json.load(f)

def create_export_bco():
    with open('app/schemas/biocompute.json','r') as f:
        export_bco = json.load(f)
    BcoCleanUp(export_bco).cleanup_bco_json()
    with open('app/schemas/biocompute_export.json', 'w') as outfile:
        json.dump(export_bco, outfile, indent=4)


def rename_export_bco(filename):
    with open('app/schemas/biocompute.json','r') as f:
        export_bco = json.load(f)
    BcoCleanUp(export_bco).cleanup_bco_json()
    export_file_dir = "app/schemas/export_files"
    os.makedirs(export_file_dir, exist_ok=True)
    with open(f'{export_file_dir}/{filename}.json', 'w') as outfile:
        json.dump(export_bco, outfile, indent=4)


def remove_bco_empty_rows():
    try:
        clean_up_usability_domain()
        clean_up_parametric_domain()
        clean_up_io_domain()
        clean_up_execution_domain()
        clean_up_description_domain()
        clean_up_provenance_domain()
    except Exception as e:
        pass

def clean_up_provenance_domain():
    review = copy.deepcopy(bco_obj['provenance_domain']['review'])
    for rev in review:
        count = len([value for keys, value in rev.items() if (value and keys != ("reviewer"))]) + len([value for value in rev['reviewer']['contribution'] if (value)]) + len([value for keys, value in rev['reviewer'].items() if (keys != "contribution") and (value)])
        if count == 0:
            bco_obj['provenance_domain']['review'].remove(rev)


    contributors = copy.deepcopy(bco_obj['provenance_domain']['contributors'])
    for con in contributors:
        count = len([value for value in con['contribution'] if (value)]) + len([value for keys, value in con.items() if (keys != "contribution") and (value)])
        if count == 0:
            bco_obj['provenance_domain']['contributors'].remove(con)

    save_bco(bco_obj)


def clean_up_usability_domain():
    usability = copy.deepcopy(bco_obj['usability_domain'])
    for usb in usability:
        if not usb:
            bco_obj['usability_domain'].remove(usb)
    save_bco(bco_obj)

def clean_up_parametric_domain():
    parameters = copy.deepcopy(bco_obj['parametric_domain'])
    for parameter in parameters:
        count = len([value for keys, value in parameter.items() if (value)])
        if count == 0:
            bco_obj['parametric_domain'].remove(parameter)
    save_bco(bco_obj)

def clean_up_io_domain():
    input_subdomain = copy.deepcopy(bco_obj['io_domain']['input_subdomain'])
    for isd in input_subdomain:
        count = len([value for keys, value in isd["uri"].items() if (value)])
        if count == 0:
            bco_obj['io_domain']['input_subdomain'].remove(isd)

    output_subdomain = copy.deepcopy(bco_obj['io_domain']['output_subdomain'])
    for osd in output_subdomain:
        count = len([value for keys, value in osd.items() if (value and keys != "uri")]) + len([value for keys, value in osd['uri'].items() if (value)])
        if count == 0:
            bco_obj['io_domain']['output_subdomain'].remove(osd)

    save_bco(bco_obj)

def clean_up_execution_domain():
    scripts = copy.deepcopy(bco_obj['execution_domain']['script'])
    for script in scripts:
        count = len([value for keys, value in script['uri'].items() if (value)])
        if count == 0:
            bco_obj['execution_domain']['script'].remove(script)

    software_prerequisites =  copy.deepcopy(bco_obj['execution_domain']['software_prerequisites'])
    for sw_pre_req in software_prerequisites:
        count = len([value for keys, value in sw_pre_req.items() if (value and keys != "uri")]) + len([value for keys, value in sw_pre_req['uri'].items() if (value)])
        if count == 0:
            bco_obj['execution_domain']['software_prerequisites'].remove(sw_pre_req)

    endpoints = copy.deepcopy(bco_obj['execution_domain']['external_data_endpoints'])
    for ext_data_ep in endpoints:
        count = len([value for keys, value in ext_data_ep.items() if (value)])
        if count == 0:
            bco_obj['execution_domain']['external_data_endpoints'].remove(ext_data_ep)
    save_bco(bco_obj)

def clean_up_description_domain():
    keywords = copy.deepcopy(bco_obj['description_domain']['keywords'])
    for keyword in keywords:
        if not keyword:
            bco_obj['description_domain']['keywords'].remove(keyword)

    platform = copy.deepcopy(bco_obj['description_domain']['platform'])
    for pl in platform:
        if not pl:
            bco_obj['description_domain']['platform'].remove(pl)

    for step_index, xr in enumerate(bco_obj['description_domain']['xref']):
        ids = copy.deepcopy(bco_obj['description_domain']['xref'][step_index]['ids'])
        for id in ids:
            for id in ids:
                if not id:
                    bco_obj['description_domain']['xref'][step_index]['ids'].remove(id)

    xref = copy.deepcopy(bco_obj['description_domain']['xref'])
    for xr in xref:
        count = len([value for key, value in xr.items() if (value)])
        if count == 0:
            bco_obj['description_domain']['xref'].remove(xr)

    for step_index, pipeline_step in enumerate(bco_obj['description_domain']['pipeline_steps']):

        prereqs = copy.deepcopy(bco_obj['description_domain']['pipeline_steps'][step_index]['prerequisite'])
        for prereq in prereqs:
            count = len([value for keys, value in prereq.items() if (value and keys != "uri")]) + len([value for keys, value in prereq['uri'].items() if (value)])
            if count == 0:
                bco_obj['description_domain']['pipeline_steps'][step_index]['prerequisite'].remove(prereq)

        input_list = copy.deepcopy(bco_obj['description_domain']['pipeline_steps'][step_index]['input_list'])
        for input in input_list:
            count = len([value for keys, value in input.items() if (value)])
            if count == 0:
                bco_obj['description_domain']['pipeline_steps'][step_index]['input_list'].remove(input)

        output_list = copy.deepcopy(bco_obj['description_domain']['pipeline_steps'][step_index]['output_list'])
        for output in output_list:
            count = len([value for keys, value in output.items() if (value)])
            if count == 0:
                bco_obj['description_domain']['pipeline_steps'][step_index]['output_list'].remove(output)

    pipeline_steps = copy.deepcopy(bco_obj['description_domain']['pipeline_steps'])
    for pipeline_step in pipeline_steps:
        count = len([value for key, value in pipeline_step.items() if value])
        if count == 0:
            bco_obj['description_domain']['pipeline_steps'].remove(pipeline_step)

    save_bco(bco_obj)



bco_obj = load_bco()
bco_obj_meta = load_bco_meta()
bco_reset_obj = load_bco_skeleton()

def reset_bco_obj(bco_reset_object):
    with open('app/schemas/biocompute.json', 'w') as outfile:
        json.dump(bco_reset_object, outfile, indent=4)

def reset_comparison_bco_obj(bco_reset_object):
    with open("app/schemas/biocompute_compare.json", "w") as outfile:
        json.dump(bco_reset_object, outfile, indent=4)

def save_bco(bco_json_object):
    with open('app/schemas/biocompute.json', 'w') as outfile:
        json.dump(bco_json_object, outfile, indent=4)

def upload_bco(request):
    try:
        if request.method == "POST":
            override = True if request.POST.get("override") == "true" else False
            bco_file = request.FILES["bcofile"]
            if override:
                reset_bco_obj(bco_reset_obj)
            BcoDataService().load_bco(bco_file, override)
            global bco_obj, bco_comparison_file
            bco_obj = load_bco()
            bco_comparison_file = ""
            return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)


def upload_comparison_bco(request):
    try:
        if request.method == "POST":
            override = True if request.POST.get("override") == "true" else False
            global bco_comparison_file
            bco_comparison_file = request.FILES["bcofile"]
            if override:
                reset_comparison_bco_obj(bco_reset_obj)
            ComparisonBcoDataService().load_bco(bco_comparison_file, override)
            is_valid = validate_comparison_bco()
            if is_valid:
                messages.success(request, "Successfully uploaded")
            else:
                messages.info(
                    request, "Note: The uploaded file did not pass validation"
                )
            return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)


# Define your data
def bcoobject(request):
    return JsonResponse({'ObjectInformation':bco_obj})

def index(request):
    context = {"bco_meta":bco_obj_meta}
    return render(request, "base.html", context)

def bco(request):
    context = {"bco_meta":bco_obj_meta}
    return render(request, "bco.html", context)

def review(request):
    return render(request, "review.html",{})

def export(request):
    return render(request, "export.html",{})

#2791 object info
def objectinfo(request):
    if request.method == "PUT":
        params = QueryDict(request.body)
        value = params.get("value")
        update_key = params.get("key")
        bco_obj[update_key] = value
        save_bco(bco_obj)

    context = {'object_id':bco_obj['object_id'], 'spec_version':bco_obj['spec_version'], 'etag':bco_obj['etag'], 'bco_meta':bco_obj_meta}
    return render(request, "2791/2791object.html",context)

#description domain
def description_domain(request):
    # clean_up_description_domain()
    context = {'description_domain': bco_obj['description_domain'], 'description_domain_meta':bco_obj_meta['description_domain']}
    return  render(request, "description/description_domain.html", context)

@csrf_protect
def keywords(request):
    if request.method == 'POST':
        bco_obj['description_domain']['keywords'].append("")
        save_bco(bco_obj)

    if request.method == "PUT":
        params = QueryDict(request.body)
        value = params.get('value').strip(' \t\n\r')
        index = int(params.get('index'))
        bco_obj['description_domain']['keywords'][index] = value
        save_bco(bco_obj)

    if request.method == "GET":
        keywords = copy.deepcopy(bco_obj['description_domain']['keywords'])
        for keyword in keywords:
            if not keyword:
                bco_obj['description_domain']['keywords'].remove(keyword)
        save_bco(bco_obj)

    context = {'keywords': bco_obj['description_domain']['keywords'], 'keywords_meta':bco_obj_meta['description_domain']['properties']['keywords']}
    return  render(request, "description/keywords.html", context)


def platform(request):
    if request.method == 'POST':
        bco_obj['description_domain']['platform'].append("")
        save_bco(bco_obj)

    if request.method == "PUT":
        params = QueryDict(request.body)
        value = params.get('value').strip(' \t\n\r')
        index = int(params.get('index'))
        bco_obj['description_domain']['platform'][index] = value
        save_bco(bco_obj)

    if request.method == "GET":
        platform = copy.deepcopy(bco_obj['description_domain']['platform'])
        for pl in platform:
            if not pl:
                bco_obj['description_domain']['platform'].remove(pl)
        save_bco(bco_obj)

    context = {'platform': bco_obj['description_domain']['platform']}
    return  render(request, "description/platform.html", context)

def xref(request):
    if request.method == "PUT":
        params = QueryDict(request.body)
        update_key = params.get('key')
        value = params.get('value').strip(' \t\n\r')
        index = int(params.get('index'))
        bco_obj['description_domain']['xref'][index][update_key] = value
        save_bco(bco_obj)
    if request.method == "POST":
        xref = {"namespace":"","name":"","ids":[],"access_time":""}
        bco_obj['description_domain']['xref'].append(xref)
        save_bco(bco_obj)

    if request.method == "GET":
        xref = copy.deepcopy(bco_obj['description_domain']['xref'])
        for xr in xref:
            count = len([value for key, value in xr.items() if (value)])
            if count == 0:
                bco_obj['description_domain']['xref'].remove(xr)
        save_bco(bco_obj)

    context = { 'xrefs': bco_obj['description_domain']['xref'], 'xref_meta':bco_obj_meta['description_domain']['properties']['xref']}
    return  render(request, "description/xref.html", context)

@csrf_protect
def ids(request):
    if request.method == "POST":
        step_index = int(request.POST.get('parentIndex'))
        bco_obj['description_domain']['xref'][step_index]['ids'].append("")
        save_bco(bco_obj)

    if request.method == "PUT":
        params = QueryDict(request.body)
        value = params.get('value').strip(' \t\n\r')
        index = int(params.get('index'))
        step_index = int(params.get('parentIndex'))
        bco_obj['description_domain']['xref'][step_index]['ids'][index] = value
        save_bco(bco_obj)

    if request.method == "GET":
        step_index = int(request.GET.get('step_index'))
        ids = copy.deepcopy(bco_obj['description_domain']['xref'][step_index]['ids'])
        for id in ids:
            if not id:
                bco_obj['description_domain']['xref'][step_index]['ids'].remove(id)
        save_bco(bco_obj)

    context = {'ids': bco_obj['description_domain']['xref'][step_index]['ids'], "step_index":step_index, "ids_meta": bco_obj_meta['description_domain']['properties']['xref']['items']['properties']['ids']}
    return  render(request, "description/ids.html", context)


def pipeline_steps(request):
    if request.method == "PUT":
        params = QueryDict(request.body)
        update_key = params.get('key')
        value = params.get('value').strip(' \t\n\r')
        index = int(params.get('index'))
        bco_obj['description_domain']['pipeline_steps'][index][update_key] = int(value) if update_key == "step_number" else value if value else value
        save_bco(bco_obj)

    if request.method == "POST":
        pipeline_step = {"step_number":"","name":"","description":"","version":"","prerequisite":[],"input_list":[], "output_list":[]}
        bco_obj['description_domain']['pipeline_steps'].append(pipeline_step)
        save_bco(bco_obj)

    if request.method == "GET":
        pipeline_steps = copy.deepcopy(bco_obj['description_domain']['pipeline_steps'])
        for pipeline_step in pipeline_steps:
            count = len([value for key, value in pipeline_step.items() if value])
            if count == 0:
                bco_obj['description_domain']['pipeline_steps'].remove(pipeline_step)
        save_bco(bco_obj)
        # clean_up_description_domain()

    context = { 'pipeline_steps': bco_obj['description_domain']['pipeline_steps'], 'pipeline_steps_meta':bco_obj_meta['description_domain']['properties']['pipeline_steps']['items']['properties']}
    return  render(request, "description/pipeline_steps.html", context)



def reset_bco(request):
    reset_bco_obj(bco_reset_obj)
    global bco_obj
    bco_obj = load_bco()
    wdl_dir = 'app/uploaded_files/wdl/'
    if os.path.exists(wdl_dir):
        for filename in os.listdir(wdl_dir):
            if filename.endswith('.wdl'):
                os.remove(os.path.join(wdl_dir, filename))
    context = {"bco_meta":bco_obj_meta}
    return render(request, "base.html", context)


def prerequisite(request):
    if request.method == "PUT":
        params = QueryDict(request.body)
        update_key = params.get('key')
        uri_update_key = update_key.split(".")
        value = params.get('value').strip(' \t\n\r')
        index = int(params.get('index'))
        step_index = int(params.get('parentIndex'))
        if len(uri_update_key) == 1:
            bco_obj['description_domain']['pipeline_steps'][step_index]['prerequisite'][index][update_key] = value
        elif len(uri_update_key) > 1:
            bco_obj['description_domain']['pipeline_steps'][step_index]['prerequisite'][index][uri_update_key[0]][uri_update_key[1]] = value
        save_bco(bco_obj)

    if request.method == "POST":
        step_index = int(request.POST.get('parentIndex'))
        pre_req = {"name":"", "uri":{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}}
        bco_obj['description_domain']['pipeline_steps'][step_index]['prerequisite'].append(pre_req)
        save_bco(bco_obj)

    if request.method == "GET":
        step_index = int(request.GET.get('step_index'))
        prereqs = copy.deepcopy(bco_obj['description_domain']['pipeline_steps'][step_index]['prerequisite'])
        for prereq in prereqs:
            count = len([value for keys, value in prereq.items() if (value and keys != "uri")]) + len([value for keys, value in prereq['uri'].items() if (value)])
            if count == 0:
                bco_obj['description_domain']['pipeline_steps'][step_index]['prerequisite'].remove(prereq)

    prerequisite =  bco_obj['description_domain']['pipeline_steps'][step_index]['prerequisite']
    context = {'prequisites':prerequisite, "step_index":step_index, 'prerequisite_meta':bco_obj_meta['description_domain']['properties']['pipeline_steps']['items']['properties']['prerequisite']['items']['properties'] }
    return render(request, "description/prerequisite.html", context)

def input_list(request):
    if request.method == "PUT":
        params = QueryDict(request.body)
        update_key = params.get('key')
        value = params.get('value').strip(' \t\n\r')
        index = int(params.get('index'))
        step_index = int(params.get('parentIndex'))
        bco_obj['description_domain']['pipeline_steps'][step_index]['input_list'][index][update_key] = value
        save_bco(bco_obj)

    if request.method == "POST":
        step_index = int(request.POST.get('parentIndex'))
        input = {"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}
        bco_obj['description_domain']['pipeline_steps'][step_index]['input_list'].append(input)
        save_bco(bco_obj)

    if request.method == "GET":
        step_index = int(request.GET.get('step_index'))
        input_list = copy.deepcopy(bco_obj['description_domain']['pipeline_steps'][step_index]['input_list'])
        for input in input_list:
            count = len([value for keys, value in input.items() if (value)])
            if count == 0:
                bco_obj['description_domain']['pipeline_steps'][step_index]['input_list'].remove(input)

    input_list =  bco_obj['description_domain']['pipeline_steps'][step_index]['input_list']

    context = {'input_list':input_list, "step_index":step_index, "input_list_meta":bco_obj_meta['description_domain']['properties']['pipeline_steps']['items']['properties']['input_list']['items']}
    return render(request, "description/input_list.html", context)

def output_list(request):
    if request.method == "PUT":
        params = QueryDict(request.body)
        update_key = params.get('key')
        value = params.get('value').strip(' \t\n\r')
        index = int(params.get('index'))
        step_index = int(params.get('parentIndex'))
        bco_obj['description_domain']['pipeline_steps'][step_index]['output_list'][index][update_key] = value
        save_bco(bco_obj)

    if request.method == "POST":
        step_index = int(request.POST.get('parentIndex'))
        output = {"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}
        bco_obj['description_domain']['pipeline_steps'][step_index]['output_list'].append(output)
        save_bco(bco_obj)

    if request.method == "GET":
        step_index = int(request.GET.get('step_index'))
        output_list = copy.deepcopy(bco_obj['description_domain']['pipeline_steps'][step_index]['output_list'])
        for output in output_list:
            count = len([value for keys, value in output.items() if (value)])
            if count == 0:
                bco_obj['description_domain']['pipeline_steps'][step_index]['output_list'].remove(output)

    output_list =  bco_obj['description_domain']['pipeline_steps'][step_index]['output_list']

    context = {'output_list':output_list, "step_index":step_index, "output_list_meta":bco_obj_meta['description_domain']['properties']['pipeline_steps']['items']['properties']['output_list']['items']}
    return render(request, "description/output_list.html", context)


#error domain
def error_domain(request):
    context = {"error_domain":bco_obj['error_domain'], "error_domain_meta":bco_obj_meta['error_domain']}
    return  render(request, "error/error_domain.html", context)

def empirical_error(request):
    if request.method == "PUT":
        params = QueryDict(request.body)
        update_key = params.get('key')
        value = params.get('value').strip(' \t\n\r')
        obj_identifier = params.get('obj_identifier')
        index = int(params.get('index'))

        if update_key == "key":
            new_ev = OrderedDict((value if (obj_value == obj_identifier and obj_index == index) else obj_key, obj_value) for obj_index, (obj_key, obj_value) in enumerate(bco_obj['error_domain']['empirical_error'].items()))
            bco_obj['error_domain']['empirical_error'] = new_ev
        if update_key == "value":
            new_ev = OrderedDict((obj_key, value if (obj_key == obj_identifier and obj_index == index) else obj_value) for obj_index, (obj_key, obj_value) in enumerate(bco_obj['error_domain']['empirical_error'].items()))
            bco_obj['error_domain']['empirical_error'] = new_ev
        save_bco(bco_obj)
    if request.method == "POST":
        bco_obj['error_domain']['empirical_error'][""]=""
        save_bco(bco_obj)
    if request.method == "GET":
        new_ev = OrderedDict((obj_key, obj_value) for index, (obj_key, obj_value) in enumerate(bco_obj['error_domain']['empirical_error'].items()) if(obj_key != "" or obj_value != ""))
        bco_obj['error_domain']['empirical_error'] = new_ev
        save_bco(bco_obj)
    context = {"empirical_error":bco_obj['error_domain']['empirical_error'], "error_domain_meta":bco_obj_meta['error_domain']}
    return  render(request, "error/empirical_error.html", context)

def algorithmic_error(request):
    if request.method == "PUT":
        params = QueryDict(request.body)
        update_key = params.get('key')
        value = params.get('value').strip(' \t\n\r')
        obj_identifier = params.get('obj_identifier')
        index = int(params.get('index'))

        if update_key == "key":
            new_ev = OrderedDict((value if (obj_value == obj_identifier and obj_index == index) else obj_key, obj_value) for obj_index, (obj_key, obj_value) in enumerate(bco_obj['error_domain']['algorithmic_error'].items()))
            bco_obj['error_domain']['algorithmic_error'] = new_ev
        if update_key == "value":
            new_ev = OrderedDict((obj_key, value if (obj_key == obj_identifier and obj_index == index) else obj_value) for obj_index, (obj_key, obj_value) in enumerate(bco_obj['error_domain']['algorithmic_error'].items()))
            bco_obj['error_domain']['algorithmic_error'] = new_ev
        save_bco(bco_obj)
    if request.method == "POST":
        bco_obj['error_domain']['algorithmic_error'][""]=""
        save_bco(bco_obj)
    if request.method == "GET":
        new_ev = OrderedDict((obj_key, obj_value) for index, (obj_key, obj_value) in enumerate(bco_obj['error_domain']['algorithmic_error'].items()) if(obj_key != "" or obj_value != ""))
        bco_obj['error_domain']['algorithmic_error'] = new_ev
        save_bco(bco_obj)


    context = {"algorithmic_error":OrderedDict(bco_obj['error_domain']['algorithmic_error']), "error_domain_meta":bco_obj_meta['error_domain']}
    return  render(request, "error/algorithmic_error.html", context)

#execution domain
def execution_domain(request):
    if request.method == "PUT":
        params = QueryDict(request.body)
        value = params.get("value")
        update_key = params.get("key")
        bco_obj['execution_domain'][update_key] = value
        save_bco(bco_obj)

    context = { 'execution': bco_obj['execution_domain'], "execution_domain_meta":bco_obj_meta['execution_domain']}
    return  render(request, "execution/execution_domain.html", context)

def script(request):
    if request.method == "PUT":
        params = QueryDict(request.body)
        update_key = params.get('key')
        update_uri_key = update_key.split(".")
        value = params.get('value').strip(' \t\n\r')
        index = int(params.get('index'))
        bco_obj['execution_domain']['script'][index][update_uri_key[0]][update_uri_key[1]] = value
        save_bco(bco_obj)

    if request.method == "POST":
        script = {"uri":{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}}
        bco_obj['execution_domain']['script'].append(script)
        save_bco(bco_obj)

    if request.method == "GET":
        scripts = copy.deepcopy(bco_obj['execution_domain']['script'])
        for script in scripts:
            count = len([value for keys, value in script['uri'].items() if (value)])
            if count == 0:
                bco_obj['execution_domain']['script'].remove(script)
        save_bco(bco_obj)

    script =  bco_obj['execution_domain']['script']

    context = {'script': script, "execution_domain_meta":bco_obj_meta['execution_domain']}
    return  render(request, "execution/script.html", context)

def software_prerequisites(request):
    if request.method == "PUT":
        params = QueryDict(request.body)
        update_key = params.get('key')
        uri_update_key = update_key.split(".")
        value = params.get('value').strip(' \t\n\r')
        index = int(params.get('index'))

        if len(uri_update_key) == 1:
            bco_obj['execution_domain']['software_prerequisites'][index][update_key] = value
        elif len(uri_update_key) > 1:
            bco_obj['execution_domain']['software_prerequisites'][index][uri_update_key[0]][uri_update_key[1]] = value
        save_bco(bco_obj)

    if request.method == "POST":
        sw_pre_req = {"name":"", "version":"", "uri":{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}}
        bco_obj['execution_domain']['software_prerequisites'].append(sw_pre_req)
        save_bco(bco_obj)

    if request.method == "GET":
        software_prerequisites =  copy.deepcopy(bco_obj['execution_domain']['software_prerequisites'])
        for sw_pre_req in software_prerequisites:
            count = len([value for keys, value in sw_pre_req.items() if (value and keys != "uri")]) + len([value for keys, value in sw_pre_req['uri'].items() if (value)])
            if count == 0:
                bco_obj['execution_domain']['software_prerequisites'].remove(sw_pre_req)
        save_bco(bco_obj)

    software_prerequisites =  bco_obj['execution_domain']['software_prerequisites']

    context = { 'software_prerequisites': software_prerequisites, "execution_domain_meta":bco_obj_meta['execution_domain']}
    return  render(request, "execution/software_prerequisites.html", context)

def external_data_endpoints(request):
    if request.method == "PUT":
        params = QueryDict(request.body)
        update_key = params.get('key')
        value = params.get('value').strip(' \t\n\r')
        index = int(params.get('index'))
        bco_obj['execution_domain']['external_data_endpoints'][index][update_key] = value
        save_bco(bco_obj)

    if request.method == "POST":
        ext_data_ep = {"name":"", "url":""}
        bco_obj['execution_domain']['external_data_endpoints'].append(ext_data_ep)
        save_bco(bco_obj)

    if request.method == "GET":
        endpoints = copy.deepcopy(bco_obj['execution_domain']['external_data_endpoints'])
        for ext_data_ep in endpoints:
            count = len([value for keys, value in ext_data_ep.items() if (value)])
            if count == 0:
                bco_obj['execution_domain']['external_data_endpoints'].remove(ext_data_ep)
        save_bco(bco_obj)

    external_data_endpoints =  bco_obj['execution_domain']['external_data_endpoints']

    context = { 'external_data_endpoints': external_data_endpoints, "execution_domain_meta":bco_obj_meta['execution_domain']}
    return  render(request, "execution/external_data_endpoints.html", context)

def environment_variables(request):
    if request.method == "PUT":
        params = QueryDict(request.body)
        update_key = params.get('key')
        value = params.get('value').strip(' \t\n\r')
        obj_identifier = params.get('obj_identifier')
        index = int(params.get('index'))

        if update_key == "key":
            new_ev = OrderedDict((value if (obj_value == obj_identifier and obj_index == index) else obj_key, obj_value) for obj_index, (obj_key, obj_value) in enumerate(bco_obj['execution_domain']['environment_variables'].items()))
            bco_obj['execution_domain']['environment_variables'] = new_ev
        if update_key == "value":
            new_ev = OrderedDict((obj_key, value if (obj_key == obj_identifier and obj_index == index) else obj_value) for obj_index, (obj_key, obj_value) in enumerate(bco_obj['execution_domain']['environment_variables'].items()))
            bco_obj['execution_domain']['environment_variables'] = new_ev
        save_bco(bco_obj)

    if request.method == "POST":
        bco_obj['execution_domain']['environment_variables'][""]=""
        save_bco(bco_obj)

    if request.method == "GET":
        new_ev = OrderedDict((obj_key, obj_value) for index, (obj_key, obj_value) in enumerate(bco_obj['execution_domain']['environment_variables'].items()) if(obj_key != "" or obj_value != ""))
        bco_obj['execution_domain']['environment_variables'] = new_ev
        save_bco(bco_obj)

    environment_variables =  OrderedDict(bco_obj['execution_domain']['environment_variables'])

    context = { 'environment_variables': environment_variables, "execution_domain_meta":bco_obj_meta['execution_domain']}
    return  render(request, "execution/environment_variables.html", context)

#io domain
def io_domain(request):
    context = {"io_domain":bco_obj['io_domain'], "io_domain_meta":bco_obj_meta["io_domain"]}
    return render(request, "io/io_domain.html", context)

def input_subdomain(request):
    if request.method == "PUT":
        params = QueryDict(request.body)
        update_key = params.get('key')
        uri_update_key = update_key.split(".")
        value = params.get('value').strip(' \t\n\r')
        index = int(params.get('index'))
        bco_obj['io_domain']['input_subdomain'][index][uri_update_key[0]][uri_update_key[1]] = value
        save_bco(bco_obj)

    if request.method == "POST":
        isd = {"uri":{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}}
        bco_obj['io_domain']['input_subdomain'].append(isd)
        save_bco(bco_obj)

    if request.method == "GET":
        input_subdomain = copy.deepcopy(bco_obj['io_domain']['input_subdomain'])
        for isd in input_subdomain:
            count = len([value for keys, value in isd["uri"].items() if (value)])
            if count == 0:
                bco_obj['io_domain']['input_subdomain'].remove(isd)
        save_bco(bco_obj)

    input_subdomain = bco_obj['io_domain']['input_subdomain']
    context = {'input_subdomain':input_subdomain, 'io_domain_meta':bco_obj_meta['io_domain']}
    return render(request, "io/input_subdomain.html", context)


def output_subdomain(request):
    if request.method == "PUT":
        params = QueryDict(request.body)
        update_key = params.get('key')
        uri_update_key = update_key.split(".")
        value = params.get('value').strip(' \t\n\r')
        index = int(params.get('index'))
        if len(uri_update_key) == 1:
            bco_obj['io_domain']['output_subdomain'][index][update_key] = value
        elif len(uri_update_key) > 1:
            bco_obj['io_domain']['output_subdomain'][index][uri_update_key[0]][uri_update_key[1]] = value
        save_bco(bco_obj)

    if request.method == "POST":
        osd = {"mediatype":"", "uri":{"filename":"", "uri":"", "access_time":"", "sha1_checksum":""}}
        bco_obj['io_domain']['output_subdomain'].append(osd)
        save_bco(bco_obj)

    if request.method == "GET":
        output_subdomain = copy.deepcopy(bco_obj['io_domain']['output_subdomain'])
        for osd in output_subdomain:
            count = len([value for keys, value in osd.items() if (value and keys != "uri")]) + len([value for keys, value in osd['uri'].items() if (value)])
            if count == 0:
                bco_obj['io_domain']['output_subdomain'].remove(osd)
        save_bco(bco_obj)

    output_subdomain = bco_obj['io_domain']['output_subdomain']
    context = {'output_subdomain':output_subdomain, 'io_domain_meta':bco_obj_meta['io_domain']}
    return render(request, "io/output_subdomain.html", context)


#parametric domain
def parametric_domain(request):
    if request.method == "PUT":
        params = QueryDict(request.body)
        update_key = params.get('key')
        value = params.get('value').strip(' \t\n\r')
        index = int(params.get('index'))

        bco_obj['parametric_domain'][index][update_key] = value
        save_bco(bco_obj)

    if request.method == "POST":
        parameter = {"param":"", "value":"", "step":""}
        bco_obj['parametric_domain'].append(parameter)
        save_bco(bco_obj)

    if request.method == "GET":
        parameters = copy.deepcopy(bco_obj['parametric_domain'])
        for parameter in parameters:
            count = len([value for keys, value in parameter.items() if (value)])
            if count == 0:
                bco_obj['parametric_domain'].remove(parameter)
        save_bco(bco_obj)

    context = {'parameters':bco_obj['parametric_domain'], 'parametric_domain_meta':bco_obj_meta['parametric_domain']}
    return  render(request, "parametric/parametric_domain.html", context)

#provenance domain
def provenance_domain(request):
    if request.method == "PUT":
        params = QueryDict(request.body)
        value = params.get("value")
        update_key = params.get("key")
        bco_obj['provenance_domain'][update_key] = value
        save_bco(bco_obj)

    if request.method == "GET":
        clean_up_provenance_domain()

    context = { 'provenance': bco_obj['provenance_domain'], 'provenance_domain_meta':bco_obj_meta['provenance_domain']}
    return  render(request, "provenance/provenance_domain.html", context)

def review(request):

    if request.method == "PUT":
        params = QueryDict(request.body)
        update_key = params.get('key')
        uri_update_key = update_key.split(".")
        value = params.get('value').strip(' \t\n\r')
        index = int(params.get('index'))
        if len(uri_update_key) == 1:
            bco_obj['provenance_domain']['review'][index][update_key] = value
        elif len(uri_update_key) > 1:
            bco_obj['provenance_domain']['review'][index][uri_update_key[0]][uri_update_key[1]] = value
        save_bco(bco_obj)

    if request.method == "POST":
        review = {"date":"", "reviewer":{"name":"", "affiliation":"", "email":"", "contribution":[], "orcid":""}, "reviewer_comment":"","status":""}
        bco_obj['provenance_domain']['review'].append(review)
        save_bco(bco_obj)

    if request.method == "GET":
        reviews = copy.deepcopy(bco_obj['provenance_domain']['review'])
        for review in reviews:
            count = len([value for keys, value in review.items() if (value and keys != "reviewer")]) + len([value for keys, value in review['reviewer'].items() if (value)])
            if count == 0:
                bco_obj['provenance_domain']['review'].remove(review)
        save_bco(bco_obj)

    context = {'reviews': bco_obj['provenance_domain']['review'], 'provenance_domain_meta':bco_obj_meta['provenance_domain'], 'status_enum':bco_obj_meta['provenance_domain']['properties']['review']['items']['properties']['status']['enum']}
    return  render(request, "provenance/review.html", context)


def review_contribution(request):

    if request.method == "POST":
        step_index = int(request.POST.get('parentIndex'))
        bco_obj['provenance_domain']['review'][step_index]['reviewer']['contribution'].append("")
        save_bco(bco_obj)

    if request.method == "PUT":
        params = QueryDict(request.body)
        value = params.get('value').strip(' \t\n\r')
        index = int(params.get('index'))
        step_index = int(params.get('parentIndex'))
        bco_obj['provenance_domain']['review'][step_index]['reviewer']['contribution'][index] = value
        save_bco(bco_obj)

    if request.method == "GET":
        step_index = int(request.GET.get('step_index'))
        contributions = copy.deepcopy(bco_obj['provenance_domain']['review'][step_index]['reviewer']['contribution'])
        for contrib in contributions:
            if not contrib:
                bco_obj['provenance_domain']['review'][step_index]['reviewer']['contribution'].remove(contrib)
        save_bco(bco_obj)

    context = {'review_contribution': bco_obj['provenance_domain']['review'][step_index]['reviewer']['contribution'], "step_index":step_index, 'provenance_domain_meta':bco_obj_meta['provenance_domain'], 'contribution_enum': bco_obj_meta['provenance_domain']['properties']['review']['items']['properties']['reviewer']['properties']['contribution']['items']['enum']}
    return  render(request, "provenance/review_contribution.html", context)

def contributors_contribution(request):

    if request.method == "POST":
        step_index = int(request.POST.get('parentIndex'))
        bco_obj['provenance_domain']['contributors'][step_index]['contribution'].append("")
        save_bco(bco_obj)

    if request.method == "PUT":
        params = QueryDict(request.body)
        value = params.get('value').strip(' \t\n\r')
        index = int(params.get('index'))
        step_index = int(params.get('parentIndex'))
        bco_obj['provenance_domain']['contributors'][step_index]['contribution'][index] = value
        save_bco(bco_obj)

    if request.method == "GET":
        step_index = int(request.GET.get('step_index'))
        contributions = copy.deepcopy(bco_obj['provenance_domain']['contributors'][step_index]['contribution'])
        for contrib in contributions:
            if not contrib:
                bco_obj['provenance_domain']['contributors'][step_index]['contribution'].remove(contrib)
        save_bco(bco_obj)

    context = {'contributor_contribution': bco_obj['provenance_domain']['contributors'][step_index]['contribution'], 'step_index':step_index,'provenance_domain_meta':bco_obj_meta['provenance_domain'], 'contribution_enum':bco_obj_meta['provenance_domain']['properties']['contributors']['contributor']['properties']['contribution']['items']['enum']}
    return  render(request, "provenance/contributors_contribution.html", context)

def contributors(request):
    if request.method == "PUT":
        params = QueryDict(request.body)
        update_key = params.get('key')
        value = params.get('value').strip(' \t\n\r')
        index = int(params.get('index'))
        bco_obj['provenance_domain']['contributors'][index][update_key] = value
        save_bco(bco_obj)

    if request.method == "POST":
        contributor = {"name":"", "affiliation":"", "email":"", "contribution":[], "orcid":""}
        bco_obj['provenance_domain']['contributors'].append(contributor)
        save_bco(bco_obj)

    if request.method == "GET":
        contributors = copy.deepcopy(bco_obj['provenance_domain']['contributors'])
        for contributor in contributors:
            count = len([value for key, value in contributor.items() if (value)])
            if count == 0:
                bco_obj['provenance_domain']['contributors'].remove(contributor)
        save_bco(bco_obj)

    context = { 'contributors': bco_obj['provenance_domain']['contributors'], 'provenance_domain_meta':bco_obj_meta['provenance_domain']}
    return  render(request, "provenance/contributors.html", context)


def embargo(request):

    if request.method == "PUT":
        params = QueryDict(request.body)
        update_key = params.get('key')
        value = params.get('value')
        bco_obj['provenance_domain']['embargo'][update_key] = value
        save_bco(bco_obj)

    context = { 'embargo': bco_obj['provenance_domain']['embargo'], 'provenance_domain_meta':bco_obj_meta['provenance_domain']}
    return  render(request, "provenance/embargo.html", context)

#usability domain
def usability_domain(request):

    if request.method == "POST":
        bco_obj['usability_domain'].append("")
        save_bco(bco_obj)

    if request.method == "PUT":
        params = QueryDict(request.body)
        value = params.get('value').strip(' \t\n\r')
        index = int(params.get('index'))
        bco_obj['usability_domain'][index] = value
        save_bco(bco_obj)

    if request.method == "GET":
        usability = copy.deepcopy(bco_obj['usability_domain'])
        for usb in usability:
            if not usb:
                bco_obj['usability_domain'].remove(usb)
        save_bco(bco_obj)

    context={'items':bco_obj['usability_domain'], "items_meta":bco_obj_meta['usability_domain']['items']}
    return render(request, 'usability/usability_domain.html',context)


def get_spaces(request):
    try:
        if request.method == "GET":
            access_token = request.GET.get('access_token')
            spaces_list = PFDAClient(access_token=access_token).get_spaces_list()
            context = {"spaces": spaces_list}
            return JsonResponse(context, status = 200)
        return HttpResponse(status = 400)
    except Exception as e:
        print(f'{repr(e)}')
        return HttpResponse(status = 400)


def get_folders(request):
    try:
        if request.method == "GET":
            access_token = request.GET.get('access_token')
            space_id = request.GET.get('space_id')
            folders_list = PFDAClient(access_token=access_token).get_folders_list(space_id=space_id)
            context = {"folders": folders_list}
            return JsonResponse(context, status = 200)
        return HttpResponse(status = 400)
    except Exception as e:
        print(f'{repr(e)}')
        return HttpResponse(status = 400)


# DNAnexus workflow views

def get_dnanexus_projects(request):
    try:
        if request.method == "GET":
            access_token = request.GET.get('access_token')
            # if access_token:
            project_list = DNAnexus(access_token=access_token).get_projects_list()
            context = {"projects":project_list}
                # context = {"projects":json.dump(project_list)}

            return JsonResponse(context, status = 200)
            #   return HttpResponse(status = 400)
        return HttpResponse(status = 400)
    except Exception as e:
        print(f'{repr(e)}')
        return HttpResponse(status = 400)


def get_project_workflows(request):
    try:
        if request.method == "GET":
            project_id = request.GET.get('project_id')
            if project_id:
                # workflow_list = DNAnexus().get_workflow_list(project_id)
                workflow_list = DNAnexus().get_workflow_list(project_id)
                analysis_list = DNAnexus().get_analysis_list(project_id)
                context = {"workflows_list":workflow_list,"analysis_list":analysis_list}
                return JsonResponse(context, status = 200)
            return HttpResponse(status = 400)
        return HttpResponse(status = 400)
    except Exception as e:
        print(f'{repr(e)}')
        return HttpResponse(status = 400)

def load_dna_workflow(request):
    try:
        if request.method == "POST":
            workflow_id = request.POST.get("workflow_id")
            analysis_id = request.POST.get("analysis_id")
            override = True if request.POST.get("override") == "true" else False
            if workflow_id and analysis_id:
                if override:
                    reset_bco_obj(bco_reset_obj)
                BcoDataService().load_dnanexus_workflow(
                    override, workflow_id, analysis_id
                )
                global bco_obj, bco_comparison_file
                bco_obj = load_bco()
                bco_comparison_file = ""
                return HttpResponse(status=200)
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(status=400)


def load_comparison_dna_workflow(request):
    try:
        if request.method == "POST":
            workflow_id = request.POST.get("workflow_id")
            analysis_id = request.POST.get("analysis_id")
            global bco_comparison_file
            bco_comparison_file = f"{workflow_id} : {analysis_id}"
            override = True if request.POST.get("override") == "true" else False
            if workflow_id and analysis_id:
                if override:
                    reset_comparison_bco_obj(bco_reset_obj)
                ComparisonBcoDataService().load_dnanexus_workflow(
                    override, workflow_id, analysis_id
                )
                is_valid = validate_comparison_bco()
                if is_valid:
                    messages.success(request, "Successfully uploaded")
                else:
                    messages.info(
                        request, "Note: The uploaded file did not pass validation"
                    )
                return HttpResponse(status=200)
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(status=400)


def load_cwl(request):
    try:
        if request.method == "POST":
            override = True if request.POST.get('override') == "true" else False
            cwl_file = request.FILES['cwlfile']
            if override:
                reset_bco_obj(bco_reset_obj)
            BcoDataService().load_cwl(cwl_file, override)
            global bco_obj, bco_comparison_file
            bco_obj = load_bco()
            bco_comparison_file = ""
            return HttpResponse(status = 200)
        return HttpResponse(status = 400)
    except Exception as e:
        return HttpResponse(status = 400)


def load_comparison_cwl(request):
    try:
        if request.method == "POST":
            override = True if request.POST.get("override") == "true" else False
            global bco_comparison_file
            bco_comparison_file = request.FILES["cwlfile"]
            if override:
                reset_comparison_bco_obj(bco_reset_obj)
            ComparisonBcoDataService().load_cwl(bco_comparison_file, override)
            is_valid = validate_comparison_bco()
            if is_valid:
                messages.success(request, "Successfully uploaded")
            else:
                messages.info(
                    request, "Note: The uploaded file did not pass validation"
                )
            return HttpResponse(status=200)
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(status=400)



def load_wdl(request):
    try:
        if request.method == "POST":
            override = True if request.POST.get("override") == "true" else False
            wdl_file = request.FILES["wdlfile"]
            wdl_dir = "app/uploaded_files/wdl"
            if not os.path.exists(wdl_dir):
                os.makedirs(wdl_dir)

            if override:
                reset_bco_obj(bco_reset_obj)
                for filename in os.listdir(wdl_dir):
                    if filename.endswith(".wdl"):
                        os.remove(os.path.join(wdl_dir, filename))

            with open(f"{wdl_dir}/{wdl_file.name}", "wb") as new_file:
                new_file.write(wdl_file.file.read())

            BcoDataService().load_wdl(
                wdl_file=f"{wdl_dir}/{wdl_file.name}", override=override
            )
            global bco_obj, bco_comparison_file
            bco_obj = load_bco()
            bco_comparison_file = ""
            return HttpResponse(status=200)
        return HttpResponse(status=400)
    except Exception as e:
        print(f"error-{repr(e)}")
        return HttpResponse(status=400)


def load_comparison_wdl(request):
    try:
        if request.method == "POST":
            override = True if request.POST.get("override") == "true" else False
            global bco_comparison_file
            bco_comparison_file = request.FILES["wdlfile"]

            wdl_dir = "app/uploaded_files/wdl"
            if not os.path.exists(wdl_dir):
                os.makedirs(wdl_dir)

            if override:
                reset_comparison_bco_obj(bco_reset_obj)

            with open(f"{wdl_dir}/{bco_comparison_file.name}", "wb") as new_file:
                new_file.write(bco_comparison_file.file.read())
            ComparisonBcoDataService().load_wdl(
                f"{wdl_dir}/{bco_comparison_file.name}", override=override
            )
            is_valid = validate_comparison_bco()
            if is_valid:
                messages.success(request, "Successfully uploaded")
            else:
                messages.info(
                    request, "Note: The uploaded file did not pass validation"
                )
            return HttpResponse(status=200)
        return HttpResponse(status=400)
    except Exception as e:
        print(f"error-{repr(e)}")
        return HttpResponse(status=400)


def valid_review(request):
    try:
        remove_bco_empty_rows()
        validated_bco = BcoValidationService().validate_bco()
        context={'bco':validated_bco}
        return render(request, 'valid_review.html',context)
    except Exception as e:
        return HttpResponse(status = 400)

def validate_editor_bco():
    try:
        global bco_obj
        bco_obj = load_bco()
        BcoEditorValidation(bco_obj).validate_bco_editor_json()
        return True
    except Exception as e:
        return False


def validate_comparison_bco():
    try:
        comparison_bco_obj = load_comparison_bco()
        BcoEditorValidation(comparison_bco_obj).validate_bco_editor_json()
        return True
    except Exception as e:
        return False


def json_editor(request):
    try:
        # remove_bco_empty_rows()
        # validated_bco = BcoValidationService().validate_bco()
        global bco_obj
        bco_obj = load_bco()
        status = validate_editor_bco()
        context={'bco': json.dumps(bco_obj, indent=4), "is_valid":status}
        return render(request, 'editor.html',context)
    except Exception as e:
        return HttpResponse(status = 400)


def compare_jsons(request):
    try:

        subprocess.run(
            f"git diff --no-index -U$(wc -l {BCO_BASE} | awk '{{print $1}}') {BCO_BASE} {COMPARISON_BCO} > diff.txt",
            shell=True,
        )
        global bco_comparison_file
        with open("diff.txt", "r") as fp:
            context = {
                "diff_str": fp.read().replace(r"`", r"\`"),
                "first_comparison": bco_comparison_file == "",
                "bco_comparison_file": bco_comparison_file,
            }
        return render(request, "diff.html", context)
    except BaseException as e:
        return HttpResponse(status=400)


def export_dowload_bco(request):
    try:
        create_export_bco()
        file_location = 'app/schemas/biocompute_export.json'
        # bco_name = request.GET.get('bco_name')
        with open(file_location, 'r') as file:
            file_data = file.read()
        response = HttpResponse(file_data, content_type ='application/json', status=200)
        response['Content-Disposition'] = 'attachment; filename="bco_download.json"'
        return response

    except Exception as e:
        print(f"{repr(e)}")
        return HttpResponse(status = 400)


def export_bco_to_pfda(request):
    try:
        if request.method == "GET":
            access_token = request.GET.get('access_token')
            space_id = request.GET.get('space_id')
            folder_id = request.GET.get('folder_id')
            bco_name = request.GET.get('bco_name')
            export_file_dir = "app/schemas/export_files"
            rename_export_bco(filename=bco_name)
            PFDAClient(access_token=access_token).upload_local_file(filepath=f"{export_file_dir}/{bco_name}.json", folder_id=folder_id, space_id=space_id)
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)


def export_bco_to_dnanexus(request):
    try:
        if request.method == "GET":
            project_id = request.GET.get('project_id')
            bco_name = request.GET.get('bco_name')
            CompileWorkflow(project_id).run_script()
            create_export_bco()
            DNAnexus().upload_file_to_project(project_id, bco_name)
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)


def export_to_bco_db(request):
    try:
        if request.method == "GET":
            create_export_bco()
            bco_url = request.GET.get("bco_url")
            prefix = request.GET.get("prefix")
            owner_group = request.GET.get("owner_group")
            user_token = request.GET.get("user_token")
            upload_status = BcoDB(host_url=bco_url, prefix=prefix, owner_group=owner_group, access_token=user_token).upload()
            if upload_status:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(status=400)

def save_bco_editor(request):
    try:
        if request.method == "POST":
            bco= request.POST.get('bco')
            save_bco(json.loads(bco))
            global bco_obj
            bco_obj = load_bco()
            status = validate_editor_bco()
            context={'bco': json.dumps(bco_obj, indent=4), "is_valid": status}
            return render(request, 'editor.html', context)
    except Exception as e:
        context = {'message':f'{repr(e)}'}
        return JsonResponse(data=context, status = 400)

def validate_bco_editor(request):
    try:
        if request.method == "POST":
            global bco_obj
            bco_obj = load_bco()
            BcoEditorValidation(bco_obj).validate_bco_editor_json()
            context={'bco': json.dumps(bco_obj, indent=4), "is_valid": True}
            return render(request, 'editor.html',context)
    except Exception as e:
        context = {'message':f'{repr(e).replace("Exception(","").replace(")","")}'}
        return JsonResponse(data=context, status = 400)


def search(request):
    try:
        if request.method == "POST":
            received_json_data=json.loads(request.body)
            search_term = received_json_data.get("search_term")
            bread_crumb_list = received_json_data.get("bread_crumb_list")
            new_list = []
            domain_key_list = ["description_domain", "error_domain", "execution_domain", "io_domain", "parametric_domain", "provenance_domain", "usability_domain","object_id", "spec_version", "etag", "2791"]

            description_domain_list = ["pipeline_steps", "step_number", "name", "description", "version", "prerequisite", "input_list", "output_list", "platform", "xref", "namespace", "name", "ids","access_time","keywords", "uri", "filename", "sha1_checksum"]
            pipeline_steps_list = ["step_number", "name", "description", "version", "prerequisite", "input_list", "output_list", "uri", "filename", "access_time", "sha1_checksum"]
            xref_list = ["namespace", "name", "ids","access_time"]
            ps_prerequisite_list = ["name", "uri", "filename", "access_time", "sha1_checksum"]
            ps_input_list = ["uri", "filename", "access_time", "sha1_checksum"]
            ps_output_list = ["uri", "filename", "access_time", "sha1_checksum"]

            execution_domain_list = ["script","uri", "filename", "access_time", "sha1_checksum", "script_driver", "software_prerequisites", "name", "version", "external_data_endpoints", "name", "url", "environment_variables"]
            script_list = ["uri", "filename", "access_time", "sha1_checksum"]
            software_prerequisites_list = ["name", "version", "uri", "filename", "access_time", "sha1_checksum"]
            external_data_endpoints_list = ["name","url"]

            io_domain_list = ["input_subdomain", "output_subdomain", "uri", "filename", "access_time", "sha1_checksum", "mediatype"]
            input_subdomain_list = ["uri", "filename", "access_time", "sha1_checksum"]
            output_subdomain_list = ["uri", "filename", "access_time", "sha1_checksum", "mediatype"]

            parametric_domain_list = ["param", "step", "value"]

            error_domain_list = ["algorithmic_error", "empirical_error"]

            provenance_domain_list = ["contributor.name", "contributor.affiliation", "contributor.email", "contributor.contribution", "contributor.orcid","start_time", "end_time","name", "version", "review", "date", "reviewer.name", "reviewer.affiliation", "reviewer.email", "reviewer.contribution", "reviewer.orcid", "reviewer_comment", "status","derived_from", "obsolete_after", "embargo", "created", "modified", "contributors", "license"]
            review_list = ["date", "reviewer.name", "reviewer.affiliation", "reviewer.email", "reviewer.contribution", "reviewer.orcid", "reviewer_comment", "status"]
            embargo_list = ["start_time", "end_time"]
            contributors_list = ["contributor.name", "contributor.affiliation", "contributor.email", "contributor.contribution", "contributor.orcid"]

            if len(bread_crumb_list) == 0:
                if search_term in domain_key_list:
                    if search_term in ["object_id", "spec_version", "etag", "2791"]:
                        new_list.append("objectinfo")
                    else:
                        new_list.append(search_term)
                elif search_term in description_domain_list:
                    new_list.append("description_domain")
                    if search_term in pipeline_steps_list:
                        new_list.append("pipeline_steps")
                        if search_term in ps_input_list:
                            for index, step in enumerate(bco_obj['description_domain']['pipeline_steps']):
                                if step['input_list']:
                                    new_list.append("input_list")
                                    new_list.append(int(f"{index}"))
                                    new_list.append(step["name"])
                                    break
                        elif search_term in ps_output_list:
                            for index, step in enumerate(bco_obj['description_domain']['pipeline_steps']):
                                if step['output_list']:
                                    new_list.append("output_list")
                                    new_list.append(int(f"{index}"))
                                    new_list.append(step["name"])
                                    break
                        elif search_term in ps_prerequisite_list:
                            for index, step in enumerate(bco_obj['description_domain']['pipeline_steps']):
                                if step['prerequisite']:
                                    new_list.append("prerequisite")
                                    new_list.append(int(f"{index}"))
                                    new_list.append(step["name"])
                                    break
                        # else:
                        #     if search_term not in [""]:

                    elif search_term in xref_list:
                        new_list.append("xref")
                        if search_term == "ids":
                            for index, xr in enumerate(bco_obj['description_domain']['xref']):
                                if xr['ids']:
                                    new_list.append("ids")
                                    new_list.append(int(f"{index}"))
                                    new_list.append(xr["name"])
                                    break
                    else:
                        new_list.append(search_term)

                elif search_term in execution_domain_list:
                    new_list.append("execution_domain")
                    if search_term in script_list:
                        new_list.append("script")
                    elif search_term in software_prerequisites_list:
                        new_list.append("software_prerequisites")
                    elif search_term in external_data_endpoints_list:
                        new_list.append("external_data_endpoints")
                    else:
                        if search_term != "script_driver":
                            new_list.append(search_term)

                elif search_term in io_domain_list:
                    new_list.append("io_domain")
                    if search_term in input_subdomain_list:
                        new_list.append("input_subdomain")
                    elif search_term in output_subdomain_list:
                        new_list.append("output_subdomain")
                    else:
                        new_list.append(search_term)

                elif search_term in parametric_domain_list:
                    new_list.append("parametric_domain")

                elif search_term in error_domain_list:
                    new_list.append("error_domain")
                    new_list.append(search_term)

                elif search_term in provenance_domain_list:
                    new_list.append("provenance_domain")
                    if search_term in review_list:
                        new_list.append("review")
                        if search_term == "reviewer.contribution":
                            for index, r in enumerate(bco_obj['provenance_domain']['review']):
                                if r["reviewer"]['contribution']:
                                    new_list.append("review_contribution")
                                    new_list.append(int(f"{index}"))
                                    new_list.append(r["reviewer"]["name"])
                                    break
                    elif search_term in embargo_list:
                        new_list.append("embargo")
                    elif search_term in contributors_list:
                        new_list.append("contributors")
                        if search_term == "contributor.contribution":
                            for index, c in enumerate(bco_obj['provenance_domain']['contributors']):
                                if c['contribution']:
                                    new_list.append("contributors_contribution")
                                    new_list.append(int(f"{index}"))
                                    new_list.append(c["name"])
                                    break
                    else:
                        new_list.append(search_term)
            elif len(bread_crumb_list) == 1:
                if bread_crumb_list[0] == "description_domain":
                    if search_term in description_domain_list:
                        if search_term in pipeline_steps_list:
                            new_list.append("pipeline_steps")
                            if search_term in ps_input_list:
                                for index, step in enumerate(bco_obj['description_domain']['pipeline_steps']):
                                    if step['input_list']:
                                        new_list.append("input_list")
                                        new_list.append(int(f"{index}"))
                                        new_list.append(step["name"])
                                        break
                            elif search_term in ps_output_list:
                                for index, step in enumerate(bco_obj['description_domain']['pipeline_steps']):
                                    if step['output_list']:
                                        new_list.append("output_list")
                                        new_list.append(int(f"{index}"))
                                        new_list.append(step["name"])
                                        break
                            elif search_term in ps_prerequisite_list:
                                for index, step in enumerate(bco_obj['description_domain']['pipeline_steps']):
                                    if step['prerequisite']:
                                        new_list.append("prerequisite")
                                        new_list.append(int(f"{index}"))
                                        new_list.append(step["name"])
                                        break
                        elif search_term in xref_list:
                            new_list.append("xref")
                            if search_term == "ids":
                                for index, xr in enumerate(bco_obj['description_domain']['xref']):
                                    if xr['ids']:
                                        new_list.append("ids")
                                        new_list.append(int(f"{index}"))
                                        new_list.append(xr["name"])
                                        break
                        else:
                            new_list.append(search_term)

                elif bread_crumb_list[0] == "execution_domain":
                    if search_term in execution_domain_list:
                        if search_term in script_list:
                            new_list.append("script")
                        elif search_term in software_prerequisites_list:
                            new_list.append("software_prerequisites")
                        elif search_term in external_data_endpoints_list:
                            new_list.append("external_data_endpoints")
                        else:
                            if search_term != "script_driver":
                                new_list.append(search_term)

                elif bread_crumb_list[0] == "io_domain":
                    if search_term in io_domain_list:
                        if search_term in input_subdomain_list:
                            new_list.append("input_subdomain")
                        elif search_term in output_subdomain_list:
                            new_list.append("output_subdomain")
                        else:
                            new_list.append(search_term)

                elif bread_crumb_list[0] == "error_domain":
                    if search_term in error_domain_list:
                        new_list.append(search_term)

                elif bread_crumb_list[0] == "provenance_domain":
                    if search_term in provenance_domain_list:
                        if search_term in review_list:
                            new_list.append("review")
                            if search_term == "reviewer.contribution":
                                for index, r in enumerate(bco_obj['provenance_domain']['review']):
                                    if r["reviewer"]['contribution']:
                                        new_list.append("review_contribution")
                                        new_list.append(int(f"{index}"))
                                        new_list.append(r["reviewer"]["name"])
                                        break
                        elif search_term in embargo_list:
                            new_list.append("embargo")
                        elif search_term in contributors_list:
                            new_list.append("contributors")
                            if search_term == "contributor.contribution":
                                for index, c in enumerate(bco_obj['provenance_domain']['contributors']):
                                    if c['contribution']:
                                        new_list.append("contributors_contribution")
                                        new_list.append(int(f"{index}"))
                                        new_list.append(c["name"])
                                        break
                        else:
                            new_list.append(search_term)

            elif len(bread_crumb_list) == 2:
                if bread_crumb_list[0] == "description_domain" and bread_crumb_list[1] == "pipeline_steps":
                    if search_term in ps_input_list:
                        for index, step in enumerate(bco_obj['description_domain']['pipeline_steps']):
                            if step['input_list']:
                                new_list.append("input_list")
                                new_list.append(int(f"{index}"))
                                new_list.append(step["name"])
                                break
                    elif search_term in ps_output_list:
                        for index, step in enumerate(bco_obj['description_domain']['pipeline_steps']):
                            if step['input_list']:
                                new_list.append("output_list")
                                new_list.append(int(f"{index}"))
                                new_list.append(step["name"])
                                break
                    elif search_term in ps_prerequisite_list:
                        for index, step in enumerate(bco_obj['description_domain']['pipeline_steps']):
                            if step['prerequisite']:
                                new_list.append("prerequisite")
                                new_list.append(int(f"{index}"))
                                new_list.append(step["name"])
                                break

                elif bread_crumb_list[0] == "description_domain" and bread_crumb_list[1] == "xref":
                    if search_term == "ids":
                        for index, xr in enumerate(bco_obj['description_domain']['xref']):
                            if xr['ids']:
                                new_list.append("ids")
                                new_list.append(int(f"{index}"))
                                new_list.append(xr["name"])
                                break

                elif bread_crumb_list[0] == "provenance_domain" and bread_crumb_list[1] == "review":
                    if search_term == "reviewer.contribution":
                        for index, r in enumerate(bco_obj['provenance_domain']['review']):
                            if r["reviewer"]['contribution']:
                                new_list.append("review_contribution")
                                new_list.append(int(f"{index}"))
                                new_list.append(r["reviewer"]["name"])
                                break
                elif bread_crumb_list[0] == "provenance_domain" and bread_crumb_list[1] == "contributors":
                    if search_term == "contributor.contribution":
                        for index, c in enumerate(bco_obj['provenance_domain']['contributors']):
                            if c['contribution']:
                                new_list.append("contributors_contribution")
                                new_list.append(int(f"{index}"))
                                new_list.append(c["name"])
                                break
            return JsonResponse(data={"bread_crumb_list":new_list},status=200)
    except Exception as e:
        print(f"{repr(e)}")
        return JsonResponse(data={},status=400)
