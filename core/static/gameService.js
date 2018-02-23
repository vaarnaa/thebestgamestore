$("#games").attr('class', 'active');
$(document).ready(function () {
  'use strict';
  var win_url = window.location;
  var game_id = win_url.pathname;
  game_id = game_id.replace("/play/", '');



  $(window).on('message', function (event) {
    var data = event.originalEvent.data;

    // https://stackoverflow.com/questions/133925/javascript-post-request-like-a-form-submit
    function post(path, params, method) {
        method = method || "post"; // Set method to post by default if not specified.

        // The rest of this code assumes you are not using a library.
        // It can be made less wordy if you use one.
        var form = document.getElementById('form');
        form.setAttribute("method", method);
        form.setAttribute("action", path);

        for(var key in params) {
            if(params.hasOwnProperty(key)) {
                var hiddenField = document.createElement("input");
                hiddenField.setAttribute("type", "hidden");
                hiddenField.setAttribute("name", key);
                hiddenField.setAttribute("value", params[key]);

                form.appendChild(hiddenField);
            }
        }
        document.body.appendChild(form);
        form.submit();
    }

    if(data.messageType == "SCORE"){
      post('/play/savescore/'+ game_id , data );

    } else if(data.messageType == "SAVE"){
      console.log("Save");
      post('/play/savegame/'+ game_id , data );
    } else if(data.messageType == 'ERROR'){}
  });
});
