$(function () {
            // Correctly decide between ws:// and wss://
            var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
            var ws_path = ws_scheme + '://' + window.location.host + window.location.pathname;
            var socket = new ReconnectingWebSocket(ws_path);

            socket.onmessage = function(message){
            var data = JSON.parse(message.data);
            if(!data.score){
              if(!data.theme){
                var element = $([
                    "<tr>",
                    "<td>" + data.message + "</td>",
                    "<td>",
                    "<div class='center-block'>" + data.user + "</div>",
                    "</td>",
                    "</tr>"
                ].join("\n"));
              }
              else{
                var element = $([
                    "<tr>",
                    "<td>" + data.message + "</td>",
                    "<td>",
                    "<div class='center-block'>" + data.user + "</div>",
                    "</td>",
                    "</tr>"
                 ].join("\n"));
                 $("#theme").html(data.theme);
              }
              $("#chat_table tbody").append(element);
            }
            else {
            var element = $([
                "<tr>",
                "<td>" + data.user + "'s score is: " + data.score + "</td>",
                "<td>",
                "<div class='center-block'> DebateIT </div>",
                "</td>",
                "</tr>"
            ].join("\n"));
            $("#chat_table tbody").append(element);
            }}



             $('#arg_form').on('submit',function () {
                        socket.send(JSON.stringify({
                           "text": $('#argument').val()
                        }));
                        $('#argument').val("");
                        return false;
                        });
        });

