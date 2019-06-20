
  var chatsocket = new WebSocket(
    'ws://' + window.location.host +
    "/ws/chat/" + chat_room_name +'/'
  )

  chatsocket.onmessage = function(e){
    var data = JSON.parse(e.data);
    var message = data['message'];
    document.querySelector().value += (message + '\n');
  }

  chatsocket.onclose = function(e){
    console.error('chatsocket ended');

  }

  chatsocket.onopen = function(e){
    console.log("chatwebsocket is connected")
  }
}
