function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function update_panel(uri, filter = null, custom_value = null){
    var step_index = null
    var url = uri
    if(filter != null){

        step_index = filter.split("=")[1]
        url = uri + filter;
    }

    return $.ajax({
        type: 'GET',
        url: url,
        success: function (data) {

            $('#main').html(data);
            update_breadcrumb(uri, custom_value, step_index);
            return false;
        }
    });
    // update_breadcrumb(uri, custom_value, step_index);
    // return false;
}

function breadcrumb_navigation(element){
    uri = $(element).text()
    $.ajax({
        type: 'GET',
        url: uri,
        success: function (data) {

            $('#main').html(data);
        }
    });
    update_breadcrumb(uri);
}

function update_breadcrumb(uri, custom_value = null, step_index=null){

    // var $this = $('.breadcrumb');
    var links = $('.breadcrumb > li')

    var canremove = false
    for (const link of links){
        breadcrumb = $(link).find('button')

        if(canremove){
            var text = breadcrumb.text()
            $("li:has('button'):contains('"+text+"')").remove()

        }
        else if(breadcrumb.text() !== uri){
            breadcrumb.removeAttr("style")
            breadcrumb.attr('disabled', false)
            breadcrumb.attr('onClick', 'breadcrumb_navigation(this)')
        }
        else{
            canremove = true

            var text = uri
            $("li:has('button'):contains('"+text+"')").remove()

        }
    }
    if (custom_value !== null){
        if(step_index !== null){
            $('.breadcrumb').append('<li class="breadcrumb-item"><button type=button key='+uri+' step_index='+step_index+' class="btn btn-link">'+custom_value+'</button></li>');
        }
        else{
            $('.breadcrumb').append('<li class="breadcrumb-item"><button type=button key='+uri+' class="btn btn-link">'+custom_value+'</button></li>');
        }
    }
    else{
        if(step_index !== null){
            $('.breadcrumb').append('<li class="breadcrumb-item"><button type=button key='+uri+' step_index='+step_index+' class="btn btn-link">'+uri+'</button></li>');
        }
        else{
            $('.breadcrumb').append('<li class="breadcrumb-item"><button type=button key='+uri+' class="btn btn-link">'+uri+'</button></li>');
        }
    }

}

function update_bco(uri, request_type, json_data){
    $.ajax({
        type: request_type,
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        mode: 'same-origin',
        url: uri,
        data: json_data,
        success: function (data) {
            if (["environment_variables","algorithmic_error","empirical_error"].includes(uri)){

                $('#main').html(data);
            }
            //$('#main').html(data); //this doesnot allow the tabindex to move to the next element.
            return;
        }
    });
    return;
}


function load_comparison_bco(override) {
  var formData = new FormData();
  var files = $("#comparison_file_input").prop("files");
  if (!files || files.length == 0) {
    alert("File is not selected!");
    reset_comparison_modal_button();
    return;
  }
  var file = files[0]
  formData.append("bcofile", file, file.name);
  formData.append("override", override);
  if (file) {
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
      data: formData,
      cache: false,
      processData: false,
      contentType: false,
      url: "upload_comparison_bco",
      success: function (result) {
        $("#file_uploader_to_compare_container").modal("hide");
        compare();
      },
      error: function (result) {
        alert("File not Uploaded");
      },
    });
  } else {
      alert("please select a file");
      reset_comparison_modal_button();
  }
}

// function edit_bco(uri, json_data){
//     $.ajax({
//         type: 'POST',
//         headers: {'X-CSRFToken': getCookie('csrftoken')},
//         mode: 'same-origin',
//         url: uri,
//         data: json_data,
//         success: function (data) {
//             $('#main').html(data);
//         }
//     });
//     return true;
// }

function update_keywords(uri){
    json_data = { 'new_keyword': $('#txt-new-keyword').val()}
    update_bco(uri, json_data);
}

function update_usability(uri){
    json_data = { 'new_usability': $('#txt-new-usability').val()}
    update_bco(uri, json_data);
}

function update_ids(uri){
    json_data = { 'new_id': $('#txt-new-id').val()}
    update_bco(uri, json_data);
}

function load_bco_tree(){
    $.ajax({
        type: 'GET',
        url: 'bcoobject',
        success: function (treeData) {
            $('#json_viewer').html({
                data: treeData
            });

        }
    });
}

function load_bco(override){
  var formData = new FormData()
  var files = $('#file_input').prop("files")
  if (!files || files.length == 0) {
    alert("File is not selected!");
    reset_modal_button();
    return;
  }
  var file = files[0]
  formData.append("bcofile", file, file.name)
  formData.append("override", override)
  if (file) {
    $.ajax({
        type: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        url: 'upload_bco',
        success: function(result) {
            $('#file_uploader_container').modal('hide');
        },
        error: function(result) {
            alert('File not Uploaded');
        }
    }
    )
  } else {
    alert("please select a file");
    reset_modal_button();
  }
}

function load_cwl(override){
  var formData = new FormData()
  var files = $('#file_input').prop("files")
  if (!files || files.length == 0) {
    alert("File is not selected!");
    reset_modal_button();
    return;
  }
  var file = files[0]
  formData.append("cwlfile", file, file.name)
  formData.append("override", override)
  if (file) {
    $.ajax({
        type: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        url: 'load_cwl',
        success: function(result) {
            $('#file_uploader_container').modal('hide');
        },
        error: function(result) {
            alert('File not Uploaded');
        }
    })
  } else {
    alert("please select a file");
    reset_modal_button();
  }
}


function load_comparison_cwl(override) {
  var formData = new FormData();
  var files = $("#comparison_file_input").prop("files");
  if (!files || files.length == 0) {
    alert("File is not selected!");
    reset_comparison_modal_button();
    return;
  }
  var file = files[0]
  formData.append("cwlfile", file, file.name);
  formData.append("override", override);
  if (file) {
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
      data: formData,
      cache: false,
      processData: false,
      contentType: false,
      url: "load_comparison_cwl",
      success: function (result) {
        $("#file_uploader_to_compare_container").modal("hide");
        compare();
      },
      error: function (result) {
        alert("File not Uploaded");
      },
    });
  }
  else {
    reset_comparison_modal_button();
    alert("please select a file");
}
}

function load_wdl(override){
  var formData = new FormData()
  var files = $("#file_input").prop("files")
  if (!files || files.length == 0) {
    alert("File is not selected!");
    reset_modal_button();
    return;
  }
  var file = files[0]
  if (file) {
    formData.append("wdlfile", file, file.name)
    formData.append("override", override)
    $.ajax({
        type: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        url: 'load_wdl',
        success: function(result) {
            $('#file_uploader_container').modal('hide');
        },
        error: function(result) {
            alert('File not Uploaded');
        }
    }
    )
  }
  else{
    alert("Please select a file!")
    reset_modal_button()
  }
}


function load_comparison_wdl(override) {
  var formData = new FormData();
  var files = $("#comparison_file_input").prop("files");
  if (!files || files.length == 0) {
    alert("File is not selected!");
    reset_comparison_modal_button()
    return;
  }
  var file = files[0]
  if (file) {
    formData.append("wdlfile", file, file.name);
    formData.append("override", override);
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
      data: formData,
      cache: false,
      processData: false,
      contentType: false,
      url: "load_comparison_wdl",
      success: function (result) {
        $("#file_uploader_to_compare_container").modal("hide");
        compare();
      },
      error: function (result) {
        alert("File not Uploaded");
      },
    });
  } else {
    alert("please select a file");
    reset_comparison_modal_button()
  }

}


function load_dna_workflow(override){
  selected_workflow = $('#dna-workflows').val()
  selected_analysis = $('#dna-analysis').val()

  if (selected_workflow && selected_analysis) {
    json_data = {"workflow_id":selected_workflow, "analysis_id":selected_analysis, "override":override}
    $.ajax({
      type: 'POST',
      headers: {'X-CSRFToken': getCookie('csrftoken')},
      data: json_data,
      url: 'load_dna_workflow',
      success: function(result) {
          $('#file_uploader_container').modal('hide');
      },
      error: function(result) {
          alert('No Data found');
      }
    }
    )
  } else {
    alert("Please select project, workflow and analysis!")
    reset_modal_button()

  }
}


function load_comparison_dna_workflow(override) {
  selected_workflow = $("#comparison-dna-workflows").val();
  selected_analysis = $("#comparison-dna-analysis").val();

  if (selected_workflow && selected_analysis) {
    json_data = {
      "workflow_id": selected_workflow,
      "analysis_id": selected_analysis,
      "override": override,
    };

    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
      data: json_data,
      url: "load_comparison_dna_workflow",
      success: function (result) {
        $("#file_uploader_to_compare_container").modal("hide");
        compare();
      },
      error: function (result) {
        alert("No Data found");
      },
    });
  } else {
    alert("Please select project, workflow and analysis!");
    reset_comparison_modal_button();
  }
}


function openZoom(){
    console.log("you")
    $('#imagepreview').attr('src', $('#imageresource').attr('src')); // here asign the image to the modal when the user click the enlarge link
    $('#image_zoom_container').modal('show');
}


$(document).ready(function () {
  $("#upload_2nd_bco_button").off("click").click(function (event) {
      event.preventDefault();
      reset_comparison_modal_button();
      $("#comparison_file_input").val("");
      $("#dna-token").val("");
      $("#dna-token").css("visibility", "hidden");
      $("#file_uploader_to_compare_container").modal("show");
      $("#comparison_file_type_id").val("WDL").change();
      $("#comparison_dna_project_selector_div").css("visibility", "hidden");
      $("#comparison_dna_workflow_selector_div").css("visibility", "hidden");
      $("#comparison_dna_analysis_selector_div").css("visibility", "hidden");
    });
});


function reset_comparison_modal_button() {
  $("#upload-btn").prop("disabled", false);
  $("#upload-btn").html("Update");
}


function reset_modal_button() {
  $('#update').prop("disabled", false);
  $("#update").html("Update");
  $('#load').prop("disabled", false);
  $("#load").html("Load");
  $('#reset').prop("disabled", false);
  $("#reset").html("Reset");
}

function reset_modal() {
  // Resetting the modal-button status
  reset_modal_button()

  // Reset the input fields
  $("#file_input").val("")
  $("#dna-token").val("")
  $("#dna-token").css('visibility', 'hidden')
  $('#file_uploader_container').modal('show');
  $('#file_type_id').val("WDL").change()
  $('#dna_project_selector_div').css('visibility', 'hidden')
  $('#dna_workflow_selector_div').css('visibility', 'hidden')
  $('#dna_analysis_selector_div').css('visibility', 'hidden')
}

$(document).ready(function() {
    $(".btn-circle").off("click").click(function(event){
        url_val=$(this).attr('data-value');
        event.stopImmediatePropagation()
        // $(this).attr('disabled','disabled')

        if(url_val=='source'){

            reset_modal()
        }
        else if(url_val=='objectinfo'){

            update_panel(url_val, filter=null, custom_value="2791object");
            // $(this).attr('disabled','disabled')
        }
        else{

            update_panel(url_val);
            // $(this).attr('disabled','disabled')
        }
    });
    // $(".btn-primary").click(function(){
    //     $('#file_uploader_container').modal('hide');
    // })
});

$(document).ready(function() {
    $(".dropdown-item").off("click").click(function(){
        export_option=$(this).attr('data-value');

        if(export_option=='BCO File'){
            $('#file_downloader_container').modal('show');
        }
        else if (export_option=="DNAnexus BCO File"){
            $("#dna_export_project_selector_div").css("visibility", "hidden")
            $('#dna_export_container').modal('show')
        }
        else if (export_option=="BCO DB"){
            $("#bco_db_url").val("https://biocomputeobject.org/api/objects/drafts/create/")
            $("#prefix").val("DNAN")
            $("#owner_group").val("bco_drafter")
            $("#user_token").val("")
            $('#bco_db_export_container').modal('show')
        }
        else if (export_option=="PFDA BCO File"){
            $("#pfda_export_space_selector_div").css("visibility", "hidden")
            $("#pfda_export_folder_selector_div").css("visibility", "hidden")
            $("#pfda_export_container").modal('show')
        }
        else{
        }
    });
    // $(".btn-primary").click(function(){
    //     $('#file_uploader_container').modal('hide');
    // })
});

$(document).ready(function () {
  $("#upload-btn").off("click").click(function (event) {
      event.stopImmediatePropagation();
      $(this).prop("disabled", true);
      $(this).html("Uploading...");
      selected_type = $("#comparison_file_type_id").val();
      let override = true;
      if (selected_type === "DNAnexus Workflow") {
        load_comparison_dna_workflow(override);
      } else if (selected_type === "CWL") {
        load_comparison_cwl(override);
      } else if (selected_type === "WDL") {
        load_comparison_wdl(override);
      } else if (selected_type === "BCO") {
        load_comparison_bco(override);
      }
    });
});


$(document).ready(function() {
        $("#update").off("click").click(function(event){
            event.stopImmediatePropagation()
            $(this).prop("disabled", true);
            $(this).html("Updating...");
            selected_type = $('#file_type_id').val()
            let override = false
            if (selected_type === "DNAnexus Workflow"){

                load_dna_workflow(override)
            }
            else if(selected_type === "CWL"){
                load_cwl(override)
            }
            else if(selected_type === "WDL"){
                load_wdl(override)

            }
            else if(selected_type === "BCO"){
                load_bco(override)

            }
            else{

            }
        }
        )
        $("#load").off("click").click(function(event){
            event.stopImmediatePropagation()
            selected_type = $('#file_type_id').val()
            $(this).prop("disabled", true);
            $(this).html("Loading...");
            let override = true
            if (selected_type === "DNAnexus Workflow"){
                load_dna_workflow(override)
            }
            else if(selected_type === "CWL"){
                load_cwl(override)
            }
            else if(selected_type === "WDL"){
                load_wdl(override)

            }
            else if(selected_type === "BCO"){
                load_bco(override)

            }
            else{

            }
        })
        $("#reset").off("click").click(function(event){
            event.stopImmediatePropagation()
            $(this).prop("disabled", true);
            $(this).html("Resetting...");
            reset_bco()
            return;
        }
        )
    }
)

function reset_bco(){

    $.ajax({
        type: 'GET',
        url: 'reset_bco',
        success: function(result) {
            $('#file_uploader_container').modal('hide');
        },
        error: function(result) {
            alert('Error resetting the BCO');
        }
    }
    )
}


function edit_array_value(uri, element,index,parentIndex = null){
    setInterval(100);
    json_data = {'value': $(element).text(), 'index':index, 'parentIndex':parentIndex}
    const request_type = 'PUT'
    update_bco(uri, request_type, json_data);

    return;

}

function edit_array_dd_value(uri, element,index,parentIndex = null){
    setInterval(100);
    json_data = {'value': $(element).val(), 'index':index, 'parentIndex':parentIndex}
    const request_type = 'PUT'
    update_bco(uri, request_type, json_data);

    return;

}

function edit_array_object_value(uri,element,index = null, parentIndex = null, obj_identifier = null){
    value = $(element).text() || $(element).val()
    obj_identifier = $(element).attr('obj_identifier')
    json_data = {'key':$(element).attr('key') ,'value': value, 'obj_identifier':obj_identifier, 'index':index, 'parentIndex':parentIndex}
    const request_type = 'PUT'
    update_bco(uri, request_type, json_data);
    return;
}

function edit_array_object_dd_value(uri,element,index = null, parentIndex = null, obj_identifier = null){
    json_data = {'key':$(element).attr('key') ,'value': $(element).val(), 'obj_identifier':obj_identifier, 'index':index, 'parentIndex':parentIndex}
    const request_type = 'PUT'
    update_bco(uri, request_type, json_data);
    return;
}

function add_array_value(uri, element, parentIndex = null){
    json_data = {'value': $(element).text(), 'parentIndex':parentIndex}
    const request_type = 'POST'
    update_bco(uri, request_type, json_data);

    return;
}

function add_array_dd_value(uri, element, parentIndex = null){
    json_data = {'value': $(element).val(), 'parentIndex':parentIndex}
    const request_type = 'POST'
    update_bco(uri, request_type, json_data);

    return;
}

function add_array_object_value(uri,element, parentIndex=null){
    json_data = {'key':$(element).attr('key') ,'value': $(element).text(), 'parentIndex':parentIndex}
    const request_type = 'POST'
    update_bco(uri, request_type, json_data);

    return;
}

function hasClass(element, className) {
    return (' ' + element.className + ' ').indexOf(' ' + className+ ' ') > -1;
}
function make_editable(element){
        if ($(element).hasClass('watermark')){
            $(element).removeClass('watermark')
            $(element).empty()
        }
        $(element).attr('contenteditable', 'true')
}

function make_active(element){
    $(element).attr('class', 'nav-link active')
    $(element).attr('aria-selected', 'true')
}


function change_editor_file_type() {
  selected_type = $("#file_type_id").val();
  if (!selected_type) {
    alert("Please select Workflow type!")
    return
  }

  $("#file_selector_div").css("visibility", "visible");
  $("#dna_project_div").hide();

  if (selected_type === "CWL") {
    $("#file_input").attr("accept", ".cwl");
  } else if (selected_type === "WDL") {
    $("#file_input").attr("accept", ".wdl");
  } else if (selected_type === "BCO") {
    $("#file_input").attr("accept", ".json");
  } else if (selected_type === "DNAnexus Workflow") {
    $("#file_selector_div").css("visibility", "hidden");
    $("#dna_project_div").show();
  }
}

function change_comparison_file_type(){
  selected_type = $("#comparison_file_type_id").val();
  if (!selected_type) {
    alert("Please select Workflow type!")
    return
  }

  $("#comparison_file_selector_div").css("visibility", "visible");
  $("#comparison_dna_project_div").hide();

  if (selected_type === "CWL") {
    $("#comparison_file_input").attr("accept", ".cwl");
  } else if (selected_type === "WDL") {
    $("#comparison_file_input").attr("accept", ".wdl");
  } else if (selected_type === "BCO") {
    $("#comparison_file_input").attr("accept", ".json");
  } else if (selected_type === "DNAnexus Workflow") {
    $("#comparison_file_selector_div").css("visibility", "hidden");
    $("#comparison_dna_project_div").show();
  }
}



$(document).ready(function() {
    $("#get-projects").off("click").click(function(){
        load_cwl()
    }
    )
}
)

function get_dna_projects(){
    uri = 'get_dnanexus_projects'
    access_token = $("#dna-token").val()
    json_data = {"access_token":access_token}

    $.ajax({
        type: 'GET',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        mode: 'same-origin',
        // dataType:'json',
        url: uri,
        data: json_data,
        success: function (data){

            $('#dna-projects').empty()
            $.each(data.projects, function(i, project){
                $('#dna-projects').append('<option value='+project['id']+'>'+project['name']+'</option>')
            })

            $('#dna-projects').val('')
            $('#dna_project_selector_div').css('visibility', 'visible')
            $('#file_selector_div').css('visibility', 'hidden')
            $('#dna_project_div').css('visibility', 'visible')
            // $('#dna-token').val(access_token)
            // $('#file_uploader_container').modal('show')
        },
        error: function(result) {
            alert('DNAnexus access token is expired or not found. Please enter a token');
            $("#dna-token").css('visibility', 'visible')
        }
    });
}

// use select2 for select
$(document).ready(function() {
  $('#file_type_id').select2({
    placeholder: {
      id: '', // the value of the option
      text: 'Select a file type'
    },
    dropdownParent: $('#file_uploader_container'),
  });

  $('#dna-projects').select2({
    placeholder: {
      id: '', // the value of the option
      text: 'Select a project'
    },
    dropdownParent: $('#file_uploader_container')
  });

  $('#dna-workflows').select2({
    placeholder: {
      id: '', // the value of the option
      text: 'Select a workflow'
    },
    dropdownParent: $('#file_uploader_container')
  });

  $('#dna-analysis').select2({
    placeholder: {
      id: '', // the value of the option
      text: 'Select a analysis'
    },
    dropdownParent: $('#file_uploader_container')
  });

  $('#comparison_file_type_id').select2({
    placeholder: {
      id: '', // the value of the option
      text: 'Select a file type'
    },
    dropdownParent: $('#file_uploader_to_compare_container')
  });

  $('#comparison-dna-projects').select2({
    placeholder: {
      id: '', // the value of the option
      text: 'Select a project'
    },
    dropdownParent: $('#file_uploader_to_compare_container')
  });

  $('#comparison-dna-workflows').select2({
    placeholder: {
      id: '', // the value of the option
      text: 'Select a workflow'
    },
    dropdownParent: $('#file_uploader_to_compare_container')
  });

  $('#comparison-dna-analysis').select2({
    placeholder: {
      id: '', // the value of the option
      text: 'Select a analysis'
    },
    dropdownParent: $('#file_uploader_to_compare_container')
  });

  $('#dna-export-projects').select2({
    placeholder: {
      id: '',
      text: 'Select a project'
    },
    dropdownParent: $('#dna_export_container'),
  });

  $('#pfda-export-space').select2({
    placeholder: {
      text: 'Select a space'
    },
    dropdownParent: $('#pfda_export_container'),
  });

  $('#pfda-export-folder').select2({
    placeholder: {
      text: 'Select a folder'
    },
    dropdownParent: $('#pfda_export_container'),
  });
});


function get_spaces(element){
    uri = 'pfda/spaces'
    access_token = $("#pfda-export-token").val()
    json_data = {"access_token":access_token}
    $(element).prop("disabled", true)
    $(element).html("getting spaces...")
    $.ajax({
        type: 'GET',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        mode: 'same-origin',
        url: uri,
        data: json_data,
        success: function (data){
            $('#pfda-export-space').empty().append('<option selected="selected" value="">My Home</option>');
            $.each(data.spaces, function(i, space){
                $('#pfda-export-space').append('<option value='+space['id']+'>'+space['title']+'</option>')
            })
            get_folders()

            $('#pfda_export_space_selector_div').css('visibility', 'visible')
            $('#pfda_export_folder_selector_div').css('visibility', 'visible')

            $('#pfda_space_div').css('visibility', 'visible')
            $(element).prop("disabled", false)
            $(element).html("get spaces")

            $("#pfda-export-token").css('visibility', 'hidden')
        },
        error: function(result) {
            $(element).prop("disabled", false)
            $(element).html("get spaces")
            alert('PFDA access token is expired or not found. please enter a token');
            $("#pfda-export-token").css('visibility', 'visible')

        }

    });
}


function get_folders() {
    uri = 'pfda/folders'
    space_id = document.getElementById("pfda-export-space").value
    access_token = $("#pfda-export-token").val()
    json_data = {"access_token":access_token, "space_id":space_id}

    $.ajax({
        type: 'GET',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        mode: 'same-origin',
        url: uri,
        data: json_data,
        success: function (data){
            $('#pfda-export-folder').empty().append('<option selected="selected" value="">Root</option>');
            $.each(data.folders, function(i, folder){
                $('#pfda-export-folder').append('<option value='+folder['id']+'>'+folder['name']+'</option>')
            })
            $('#pfda_export_folder_selector_div').css('visibility', 'visible')
        },
        error: function(result) {
            alert('PFDA access token is expired or not found. please enter a token');
            $("#pfda-export-token").css('visibility', 'visible')

        }

    });
};


function get_comparison_dna_projects() {
  uri = "get_dnanexus_projects";
  access_token = $("#comparison-dna-token").val();
  json_data = { access_token: access_token };

  $.ajax({
    type: "GET",
    headers: { "X-CSRFToken": getCookie("csrftoken") },
    mode: "same-origin",
    url: uri,
    data: json_data,
    success: function (data) {
      $("#comparison-dna-projects").empty();
      $.each(data.projects, function (i, project) {
        $("#comparison-dna-projects").append(
          "<option value=" + project["id"] + ">" + project["name"] + "</option>"
        );
      });
      $("#comparison-dna-projects").val('');
      $("#comparison_dna_project_selector_div").css("visibility", "visible");
      $("#comparison_file_selector_div").css("visibility", "hidden");
      $("#comparison_dna_project_div").css("visibility", "visible");
    },
    error: function (result) {
      alert(
        "DNAnexus access token is expired or not found. Please enter a token"
      );
      $("#comparison-dna-token").css("visibility", "visible");
    },
  });
}


function get_dna_export_projects(element){
    uri = 'get_dnanexus_projects'
    access_token = $("#dna-export-token").val()
    json_data = {"access_token":access_token}
    $(element).prop("disabled", true)
    $(element).html("Getting projects...")
    $.ajax({
        type: 'GET',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        mode: 'same-origin',
        // dataType:'json',
        url: uri,
        data: json_data,
        success: function (data){

            $('#dna-export-projects').empty();
            $.each(data.projects, function(i, project){
                $('#dna-export-projects').append('<option value='+project['id']+'>'+project['name']+'</option>')
            })

            $('#dna-export-projects').val('');
            $('#dna_export_project_selector_div').css('visibility', 'visible')
            $('#file_selector_div').css('visibility', 'hidden')
            $('#dna_project_div').css('visibility', 'visible')
            $(element).prop("disabled", false)
            $(element).html("Get Projects")
            $("#dna-export-token").css('visibility', 'hidden')
            // $('#dna-token').val(access_token)
            // $('#file_uploader_container').modal('show')
        },
        error: function(result) {
            $(element).prop("disabled", false)
            $(element).html("Get Projects")
            alert('DNAnexus access token is expired or not found. Please enter a token');
            $("#dna-export-token").css('visibility', 'visible')

        }

    });
}


function get_project_workflows(){
    selected_project = $('#dna-projects').val()
    if (selected_project) {
      uri = 'get_project_workflows'
      json_data = {'project_id':selected_project}

      $.ajax({
        type: 'GET',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        mode: 'same-origin',
        url: uri,
        data: json_data,
        success: function (data){

            // $('#modal-div').html(data)
            $('#dna-workflows').empty();
            $('#dna-analysis').empty();

            $.each(data.workflows_list, function(i, workflow){
                $('#dna-workflows').append('<option value='+workflow['id']+'>'+workflow['name']+'</option>')
            })
            $.each(data.analysis_list, function(i, analyse){
                $('#dna-analysis').append('<option value='+analyse['id']+'>'+analyse['name']+'</option>')
            })

            $('#dna-workflows').val('');
            $('#dna-analysis').val('');
            $('#dna_workflow_selector_div').css('visibility', 'visible')
            $('#dna_analysis_selector_div').css('visibility', 'visible')
            // $('#file_selector_div').css('visibility', 'hidden')
            // $('#dna_project_div').css('visibility', 'visible')
            // $('#dna-token').val(access_token)
            // $('#file_uploader_container').modal('show')
        }
      });
    } else {
      alert("Please select a project!")
    }
}


function get_comparison_project_workflows() {
  selected_project = $("#comparison-dna-projects").val();
  uri = "get_project_workflows";
  json_data = { project_id: selected_project };

  $.ajax({
    type: "GET",
    headers: { "X-CSRFToken": getCookie("csrftoken") },
    mode: "same-origin",
    url: uri,
    data: json_data,
    success: function (data) {
      $("#comparison-dna-workflows").empty();
      $("#comparison-dna-analysis").empty();

      $.each(data.workflows_list, function (i, workflow) {
        $("#comparison-dna-workflows").append(
          "<option value=" + workflow["id"] + ">" + workflow["name"] + "</option>"
        );
      });
      $.each(data.analysis_list, function (i, analyse) {
        $("#comparison-dna-analysis").append(
          "<option value=" + analyse["id"] + ">" + analyse["name"] + "</option>"
        );
      });

      $("#comparison-dna-workflows").val('');
      $("#comparison-dna-analysis").val('');

      $("#comparison_dna_workflow_selector_div").css("visibility", "visible");
      $("#comparison_dna_analysis_selector_div").css("visibility", "visible");
    },
  });
}


$(document).ready(function() {
    $("#review-tab").off("click").click(function(){
        review()
    }
    )
}
)

$(document).ready(function() {
    $("#editor-tab").off("click").click(function(){
        editor()
    }
    )
}
)

$(document).ready(function () {
  $("#compare-tab").off("click").click(function () {
      compare()
    })
})


function review() {

    $.ajax({
        type: 'GET',
        url: 'valid_review',
        success: function (data) {

            $('#review_screen').html(data);
        }
    });

}

function editor() {

    $.ajax({
        type: 'GET',
        url: 'json_editor',
        success: function (data) {
            $('#editor_screen').html(data);
        }
    });
}

function enable_editor(e) {
    console.log($(e).text())
    if($(e).text() === "Edit"){
        $("#json_editor_text_box").attr('disabled', false)
        $(e).text("Reset")
        $('#save_button').attr('disabled', false)
        $("#validate_button").attr('disabled', true)
    }
    else if($(e).text() === "Reset"){
        $("#json_editor_text_box").attr('disabled', true)
        $("#validate_button").attr('disabled', false)
        $(e).text("Edit")

        editor()
    }
}

function beautify() {
    data = $("#json_editor_text_box").text()
    $("#json_editor_text_box").val(JSON.stringify(JSON.parse(data), null, 4))
    console.log($("#json_editor_text_box").text())
}


function export_file_to_pfda(element){
  bco_name = $('#pfda-export-bco-name').val()
  access_token = $("#pfda-export-token").val()
  selected_space = $('#pfda-export-space').val()
  selected_folder = $('#pfda-export-folder').val()
  json_data = {"access_token":access_token, "space_id":selected_space, "folder_id":selected_folder, "bco_name":bco_name}

  $(element).prop("disabled", true)
  $(element).html("Uploading...")

  if (bco_name){
      $.ajax({
          type: "GET",
          url: "pfda/export_bco",
          data: json_data,
          dataType: "text",
          success: function(data) {
              alert("File upload successful")
              $(element).prop("disabled", false)
              $(element).html("Upload to precisionFDA")
              $("#pfda_export_container").modal("hide")
          },
          error: function(){
              $(element).prop("disabled", false)
              $(element).html("Upload to precisionFDA")
              alert("Error uploading file to precisionFDA")
          }

      });
  }
  else{
      $(element).prop("disabled", false)
      $(element).html("Upload to precisionFDA")
      alert("please enter a name to upload and select a project BCO")
  }
}

function showNoDiff() {
  let data = `
    <p style="margin-top: 200px; font-size: large; color: dimgray; font-weight: normal;" >
    There is no change
    </p>
    `;
  $("#compare-panes").html(data);
}

function showDiff(diffString) {
  const targetElement = document.getElementById("compare-panes");
  if (!targetElement) {
    return;
  }
  const configuration = {
    drawFileList: false,
    matching: "lines",
    outputFormat: "side-by-side",
    stickyFileHeaders: false,
    renderNothingWhenEmpty: false,
  };
  const diff2htmlUi = new Diff2HtmlUI(targetElement, diffString, configuration);
  diff2htmlUi.draw();
}

function compare() {
  $.ajax({
    type: "GET",
    url: "compare_jsons",
    success: function (data) {
      $("#compare-screen").html(data);
      $(".d2h-file-header").hide();
    },
  });
}


function export_file_to_dnanexus(element){
    bco_name = $('#dna-export-bco-name').val()
    access_token = $("#dna-export-token").val()
    selected_project = $('#dna-export-projects').val()
    json_data = {"access_token":access_token,"project_id":selected_project, "bco_name":bco_name}
    $(element).prop("disabled", true)
    $(element).html("Uploading...")
    if (bco_name && selected_project){
        $.ajax({
            type: "GET",
            url: "export_bco_to_dnanexus",
            data: json_data,
            dataType: "text",
            success: function(data) {
                alert("File upload successful")
                $(element).prop("disabled", false)
                $(element).html("Upload to DNAnexus")

                $("#dna_export_container").modal("hide")
            },
            error: function(){
                $(element).prop("disabled", false)
                $(element).html("Upload to DNAnexus")
                alert("Error uploading file to DNAnexus")
            }

        });
    }
    else{
        $(element).prop("disabled", false)
        $(element).html("Upload to DNAnexus")
        alert("please enter a name to upload and select a project BCO")
    }
}


function file_download(element) {
    bco_name = $('#bco-name').val()
    json_data = {'bco_name':bco_name}
    if (bco_name){
        $(element).prop("disabled", true);
        // console.log(element)
        $(element).html("Downloading...");
        $.ajax({
            type: "GET",
            url: "export_dowload_bco",
            // headers: {'X-CSRF-TOKEN': getCookie('csrftoken')},
            // data: json_data,
            dataType: "text",
            success: function(data) {
                let blob = new Blob([data]);
                let link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download = bco_name+'.json';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                window.URL.revokeObjectURL(link.href);
                $(element).prop("disabled", false);
                $(element).html("Download BCO File");
                $("#file_downloader_container").modal('hide');
            },
            error: function(){
                alert("Error downloading the file")
            }
        });
    }
    else{
        alert("Please enter a name to download BCO")
    }
}


// $(document).ready(function () {
//     $("#download-link").click(function (e) {
//         e.preventDefault();

//         window.location.href = "file:///C:/Users/LAP-110/Downloads/bco_1.json";
//     });
// });


function description_modal(header, description) {

    $('#descriptionLabel').text(header)
    $('#description').text("description: "+description)
    $('#description_container').modal('show');

}


function updatestate(element){
    if ($(element).attr('data-before') === "+"){
        $(element).attr('data-before', '-')
    }
    else if ($(element).attr('data-before') === "-"){
        $(element).attr('data-before', '+')
    }
}


function expandNodes(element){
    nodes_to_expand = $(element).attr('nodes_to_expand')
    element_id_to_highlight = $(element).attr('element_id_to_highlight')

    nodes = nodes_to_expand.split("-")
    for(const node of nodes ){
        var is_expanded = $('#'+node+'').attr('aria-expanded')
        if (is_expanded === 'false'){
            $('#'+node+'').click()
        }
    }

    scrollToElement(element_id_to_highlight)
    highLightError(element_id_to_highlight)
}

function scrollToElement(element_id){

}

function highLightError(element_id){
    $('#'+element_id+'').effect("highlight",{"color":"lightpink"},1500)
}

function export_file_to_bco_db(element){
    bco_url = $('#bco_db_url').val()
    prefix = $("#prefix").val()
    owner_group = $('#owner_group').val()
    user_token = $('#user_token').val()
    json_data = {"bco_url":bco_url,"prefix":prefix, "owner_group":owner_group ,"user_token":user_token}
    if (bco_url && prefix && owner_group && user_token){
        $(element).prop("disabled",true)
        $(element).html("Submitting...")
        $.ajax({
                type: "GET",
                url: "export_to_bco_db",
                data: json_data,
                dataType: "text",
                success: function(data) {
                    $(element).prop("disabled",false)
                    $(element).html("Submit")
                    alert("File upload successful")
                    $("#bco_db_export_container").modal("hide")
                },
                error: function(result) {
                    $(element).prop("disabled",false)
                    $(element).html("Submit")
                    alert("Error uploading file")
                }
            });
    }
    else{
        alert("Please enter data for all fields to upload BCO")
    }
}

function insert_bco(uri, request_type, json_data){
    $.ajax({
        type: request_type,
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        mode: 'same-origin',
        url: uri,
        data: json_data,
        success: function (data) {

            $('#main').html(data); //this doesnot allow the tabindex to move to the next element.
            return;
        }
    });
    return;
}


function add_array_object_row(element){
    uri = $(element).attr("uri")
    parentIndex = $(element).attr("parentIndex")
    json_data = {"parentIndex": parentIndex}

    insert_bco(uri, "POST", json_data)

}


// $(document).bind("ajaxStop", function() {
//     // alert("loaed")
//
//     $(".autofocus").focus()
// })
// $(document).on("load", '#add_button', function(event) {
//     alert("new link clicked!");
//     $(".autofocus").focus();
//     return;
// });

// $(document).on("click", '#add_button',function(){
//     ele = document.getElementsByClassName("autofocus")
//     setInterval(function(ele){ $(ele).focus();
// }
// )


function search(){
    search_term = $("#search_text").val()
    breadcrumb_nav = $(".breadcrumb-item > button")
    var bread_crumb_list = []
    for (const breadcrumb of breadcrumb_nav){
        var attr  = $(breadcrumb).attr('step_index')
        if (attr) {
            var text = parseInt($(breadcrumb).attr('step_index'))
            bread_crumb_list.push(text)
            var key = $(breadcrumb).attr('key')
            bread_crumb_list.push(key)
        }
        else{
            var text = $(breadcrumb).attr('key')
            if(text !== "bco"){
                bread_crumb_list.push(text)
            }
        }
    }

    json_data = JSON.stringify({"search_term":search_term, "bread_crumb_list":bread_crumb_list})

    $.ajax({
        type: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: json_data,
        url: "search",
        dataType: "text",
        success: function(data) {
            res_data = JSON.parse(data)


            // bread_crumb_list = ["description_domain", "pipeline_steps"]
            display_search(res_data.bread_crumb_list)
        },
        error: function(result) {
            alert("No results found")
        }
    });
    return;
}

async function display_search(data){
    for (let i=0; i < data.length; i++){
        if (typeof data[i+1] === 'number') {
            await update_panel(data[i], "?step_index="+data[i+1], "name: "+data[i+2]);
            i = i+2;
        }
        else{
            await update_panel(data[i]);
        }
    }
}


function expand_all(){
    nodes_to_expand = $('.expandcollapse')
    for(const node of nodes_to_expand ){
        var is_expanded = $(node).attr('aria-expanded')
        if (is_expanded === 'false'){
            $(node).click()
        }
    }
}

function saveBcoEditor(e){
    try {
    bco = JSON.stringify(JSON.parse($("#json_editor_text_box").val()),null,4)
    $(e).attr('disabled', true)
    $('#validate_button').attr('disabled', true)
    $('#edit_button').attr('disabled', true)
    $('#beautify_button').attr('disabled', true)
    $("#json_editor_text_box").attr('disabled', true)
    $(e).text('Saving...')
    json_data = {"bco":bco}
    console.log(json_data)
    $.ajax({
        type: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: json_data,
        url: 'save_bco_editor',
        success: function(data) {
            $('#editor_screen').html(data);
        },
        error: function(data) {
            alert(data.responseJSON.message)
            $('#edit_button').attr('disabled', false)
            $('#beautify_button').attr('disabled', false)
            $("#json_editor_text_box").attr('disabled', false)
            $('#validate_button').attr('disabled', false)
            $(e).attr('disabled', false)
            $(e).text('Save')
        }
    }
    )
    }
    catch(err) {
        alert("Syntax Error, Please check and format the JSON properly: "+err)
    }
}


function validateBcoEditor(e){
    try {
        $(e).attr('disabled', true)
        $('#save_button').attr('disabled', true)
        $('#edit_button').attr('disabled', true)
        $('#beautify_button').attr('disabled', true)
        $("#json_editor_text_box").attr('disabled', true)
        $(e).text('Validating...')
        $.ajax({
            type: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            url: 'validate_bco_editor',
            success: function(data) {
                alert("BCO validation successful")
                $('#editor_screen').html(data);
            },
            error: function(data) {
                alert(data.responseJSON.message)
                $('#edit_button').attr('disabled', false)
                if ($('#edit_button').text() === 'Reset'){
                    $('#save_button').attr('disabled', false)
                    $("#json_editor_text_box").attr('disabled', false)
                }
                $('#beautify_button').attr('disabled', false)
                $(e).attr('disabled', false)
                $(e).text('Validate')
            }
        }
        )
        }
        catch(err) {
            console.log(err)
            alert("Syntax Error, Please check and format the JSON properly")
        }
}

function sendEmail() {
    $('#descriptionLabel').text("INFO")
    $('#description').text("If an email client(eg. Outlook) is configured on your system it will open up in a moment. " +
    "If not, please send your valuable feedback to the email_address: bco-feedback-noreply@dnanexus.com")
    $('#description_container').modal('show');
    var email = 'bco-feedback-noreply@dnanexus.com';
    window.location = "mailto:"+email;
}
