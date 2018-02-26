$("#games").attr('class', 'active');
$(document).ready(function () {
  'use strict';
  var win_url = window.location;
  var game_id = win_url.pathname;
  game_id = game_id.replace("/play/", '');



  $(window).on('message', function (event) {
    var data = event.originalEvent.data;
    // https://stackoverflow.com/questions/133925/javascript-post-request-like-a-form-submit
    // A function for posting data to target URL
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

    // Source reference: https://stackoverflow.com/questions/1184624/convert-form-data-to-javascript-object-with-jquery
    // Helper function to make JSON out of form data
    function formToJSON( selector ){
       var form = {};
       $(selector).find(':input[name]:enabled').each( function() {
               var self = $(this);
               var name = self.attr('name');
               if (form[name]) {
                form[name] = form[name] + ',' + self.val();
            }
            else {
                form[name] = self.val();
            }
        });

       return form;
    }

    // Handling of different POST messages received from the game
    if(data.messageType == 'SETTING'){

      $('#encoder_iframe').attr('width', data.options.width);
      $('#encoder_iframe').attr('height', data.options.height);

    } else if(data.messageType == "SCORE"){
      post('/play/savescore/'+ game_id , data );


    } else if(data.messageType == "SAVE"){
      alert("Game Saved!");
      post('', {'messageType': data.messageType, 'gameState': JSON.stringify(data.gameState)});

    } else if(data.messageType == 'ERROR'){

    } else if(data.messageType == 'LOAD_REQUEST'){

      var form = formToJSON('#load_form');
      try{
        var load_data = {'messageType': 'LOAD', 'gameState': JSON.parse(form.gameState)};
        document.getElementById("encoder_iframe").contentWindow.postMessage(load_data, '*');
        alert("Game Loaded!");
      }catch(e){
        var error_data = {'messageType': 'ERROR', 'info': "Could not load a gamestate."};
        document.getElementById("encoder_iframe").contentWindow.postMessage(error_data, '*');
      }




    }
  });
});
