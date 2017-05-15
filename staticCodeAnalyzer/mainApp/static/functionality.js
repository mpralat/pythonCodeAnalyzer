/**
 * Created by marta on 07.05.17.
 */
function sendCloneRequest(project_id){
    console.log(project_id);
    $('#project_state').text('Cloning the repository...');
    document.getElementById("report_button").disabled = true;
    $.ajax({
        url: /clone_project/,
        type: "POST",
        data: {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                'project_id' : project_id},
        dataType: "json",
        statusCode: {
            201: function () {
                $('#project_state').text('Detected some new commits. Cloned the repository again.');
                document.getElementById("report_button").disabled = false;
            },
            202: function () {
                $('#project_state').text('Latest version already cloned. Not cloning again.');
                document.getElementById("report_button").disabled = false;
            },
            203: function () {
                $('#project_state').text('Made first, fresh clone.');
                document.getElementById("report_button").disabled = false;
            }
        }
    }).done(function () {
        console.log("done");
        document.getElementById("report_button").disabled = false;
    });
}

function sendReportRequest(project_id){
    console.log(project_id);
     $('#project_state').text('Generating the report...');
     document.getElementById("clone_button").disabled = true;
     checked_flake_options = [];
     $('#flake_options').find('input:checked').each(function () {
            checked_flake_options.push($(this).attr('value'));
        });
    var jsonArr = JSON.stringify(checked_flake_options);
    $.ajax({
        url: '/generate_report/',
        type: "POST",
        data: {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                'project_id' : project_id,
                'flake_options' : jsonArr},
        dataType: "json",
        statusCode: {
            204: function () {
                $('#project_state').text('Report generated.');
            },
            205: function () {
                $('#project_state').text('No changes detected. Not generating the report again.');
            }
        }
    }).done(function () {
        console.log("done");
        document.getElementById("clone_button").disabled = false;
        window.location.reload();
    });
}
