/**
 * Created by marta on 07.05.17.
 */
function sendFormRequest(){
    var request_url = '/add_project/';
   $.ajax({
        url: request_url,
        type: "POST",
        data: $('#repository_form').serialize(),
        success : function () {
            response_args = arguments[0];
            console.log(response_args);
            window.location = window.location + response_args + '/';
        }
    });
}
