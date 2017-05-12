/**
 * Created by marta on 07.05.17.
 */
function sendFormRequest(){
    $('#project_state').text('Cloning the repository...');
    var url = window.location.href;
    var array = url.split('/');
    var lastsegment = array[array.length - 2];
    var request_url = '/clone_project/';
   $.ajax({
        url: request_url,
        type: "POST",
        data: {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                'project_id' : lastsegment},
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
    });
}
