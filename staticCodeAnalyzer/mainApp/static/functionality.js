/**
 * Created by marta on 07.05.17.
 */
function sendFormRequest(project_id, url){
    console.log(project_id);
    if(url === '/clone_project/'){
         $('#project_state').text('Cloning the repository...');
         document.getElementById("report_button").disabled = true;
    } else {
         $('#project_state').text('Generating the report...');
         document.getElementById("clone_button").disabled = true;
    }
    $.ajax({
        url: url,
        type: "POST",
        data: {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                'project_id' : project_id},
        dataType: "json",
        statusCode: {
            201: function () {
                $('#project_state').text('Detected some new commits. Cloned the repository again.');
            },
            202: function () {
                $('#project_state').text('Latest version already cloned. Not cloning again.');
            },
            203: function () {
                $('#project_state').text('Made first, fresh clone.');
            }

        }
    }).done(function () {
        console.log("done");
        document.getElementById("report_button").disabled = false;
        document.getElementById("clone_button").disabled = false;
    });
}
