"""bconexus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from app.views import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('index', index, name='index'),
    path('load_cwl', load_cwl, name='load_cwl'),
    path("load_comparison_cwl", load_comparison_cwl, name="load_comparison_cwl"),
    path('upload_bco', upload_bco, name='upload_bco'),
    path("upload_comparison_bco", upload_comparison_bco, name="upload_comparison_bco"),
    path('bco', bco, name='bco'),
    path('reset_bco', reset_bco, name='reset_bco'),
    path('bcoobject', bcoobject, name='bcoobject'),
    path('objectinfo', objectinfo, name='objectinfo'),
    path('description_domain', description_domain, name='description_domain'),
    path('keywords', keywords, name='keywords'),
    # path('add_keywords', add_keywords, name='add_keywords'),
    # path('edit_keywords', edit_keywords, name='edit_keywords'),
    path('pipeline_steps', pipeline_steps, name='pipeline_steps'),
    path('platform', platform, name='platform'),
    # path('add_platform', add_platform, name='add_platform'),
    # path('edit_platform', edit_platform, name='edit_platform'),
    path('xref', xref, name='xref'),
    # path('edit_xref', edit_xref, name='edit_xref'),
    # path('xref', xref, name='xref'),
    path('ids', ids, name='ids'),
    # path('edit_ids',edit_ids, name='edit_ids'),
    # path('add_ids', add_ids, name='add_ids'),
    path('prerequisite', prerequisite, name='prerequisite'),
    # path('add_prerequisite', add_prerequisite, name='add_prerequisite'),
    # path('edit_prerequisite', edit_prerequisite, name='edit_prerequisite'),
    path('input_list', input_list, name='input_list'),
    # path('edit_input_list', edit_input_list, name='edit_input_list'),
    # path('add_input_list', add_input_list, name='add_input_list'),
    path('output_list', output_list, name='output_list'),
    # path('edit_output_list', edit_output_list, name='edit_output_list'),
    # path('add_output_list', add_output_list, name='add_output_list'),
    path('error_domain', error_domain, name='error_domain'),
    path('empirical_error',empirical_error, name='empirical_error'),
    path('algorithmic_error',algorithmic_error, name='algorithmic_error'),
    path('execution_domain', execution_domain, name='execution_domain'),
    path('script', script, name='script'),
    path('software_prerequisites', software_prerequisites, name='software_prerequisites'),
    path('external_data_endpoints', external_data_endpoints, name='external_data_endpoints'),
    path('environment_variables', environment_variables, name='environment_variables'),
    path('io_domain', io_domain, name='io_domain'),
    path('input_subdomain', input_subdomain, name='input_subdomain'),
    path('output_subdomain', output_subdomain, name='output_subdomain'),
    # path('edit_io_isd', edit_io_isd, name="edit_io_isd"),
    # path('add_io_isd', add_io_isd, name="add_io_isd"),
    # path('edit_io_osd', edit_io_osd, name="edit_io_osd"),
    # path('add_io_osd', add_io_osd, name="add_io_osd"),
    path('parametric_domain', parametric_domain,name='parametric_domain'),
    # path('edit_pd', edit_pd,name='edit_pd'),
    # path('add_pd', add_pd,name='add_pd'),
    path('provenance_domain', provenance_domain,name='provenance_domain'),
    path('review', review,name='review'),
    path('review_contribution', review_contribution,name='review_contribution'),
    path('contributors_contribution', contributors_contribution,name='contributors_contribution'),
    path('contributors', contributors,name='contributors'),
    path('embargo', embargo,name='embargo'),
    path('usability_domain', usability_domain, name='usability_domain'),
    # path('add_usability', add_usability, name='usability'),
    # path('edit_usability', edit_usability, name='edit_usability'),
    path('get_dnanexus_projects', get_dnanexus_projects, name='get_dnanexus_projects'),
    path('get_project_workflows', get_project_workflows, name='get_project_workflows'),
    path('load_dna_workflow', load_dna_workflow, name='load_dna_workflow'),
    path("load_comparison_dna_workflow", load_comparison_dna_workflow, name="load_comparison_dna_workflow",),
    path('load_wdl', load_wdl, name='load_wdl'),
    path("load_comparison_wdl", load_comparison_wdl, name="load_comparison_wdl"),
    path('valid_review', valid_review, name='valid_review'),
    path('json_editor', json_editor, name='json_editor'),
    path("compare_jsons", compare_jsons, name="compare_jsons"),
    path('export_dowload_bco', export_dowload_bco, name='export_dowload_bco'),
    path('export_bco_to_dnanexus', export_bco_to_dnanexus, name='export_bco_to_dnanexus'),
    path('export_to_bco_db', export_to_bco_db, name='export_to_bco_db'),
    path('search', search, name='search'),
    path('save_bco_editor',save_bco_editor, name='save_bco_editor'),
    path('validate_bco_editor',validate_bco_editor, name='validate_bco_editor'),
    path('pfda/spaces', get_spaces, name='get_spaces'),
    path('pfda/folders', get_folders, name='get_folders'),
    path('pfda/export_bco', export_bco_to_pfda, name='export_bco_to_pfda'),

] + staticfiles_urlpatterns()