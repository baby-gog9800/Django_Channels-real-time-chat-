var add_chat_room ='/user/chat/chatroom/';
var add_chat = '/user/chat/';
// alert(document.getElementById("chat-room"))
var chat_room_name = document.getElementById('crn');
console.log(chat_room_name);

if (window.location.pathname == add_chat_room){
  // alert("js file imported");

    var chatsocket = new WebSocket(
      'ws://' + window.location.host +
      "/ws/chat/" + chat_room_name +'/'
    );

    chatsocket.onmessage = function(e){
      var data = JSON.parse(e.data);
      var message = data['message'];
      document.querySelector().value += (message + '\n');
    };

    chatsocket.onclose = function(e){
      console.error('chatsocket ended');

    };

    chatsocket.onopen = function(e){
      console.log("chatwebsocket is connected")
    };
  }

if (window.location.pathname == add_chat){
  let search_input = document.getElementById('search-form');
  let searchsocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/'
  );
  searchsocket.onopen = function(e){
    // searchsocket.send('{"hello":"hello"}')
    console.log("connected");
  };
  searchsocket.onclose = function(e) {
    console.error("disconnected");
  };

}
