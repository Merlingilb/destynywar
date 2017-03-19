var chatroom;
function hide(){
    document.getElementById("log").style.display="none";
    document.getElementById("clear").style.display="none";
    document.getElementById("change_room").style.display="none";
    document.getElementById("roomdiv").style.display="none";
    document.getElementById("broadcast").style.display="none";
}
function show(){
    document.getElementById("log").style.display="inline";
    document.getElementById("clear").style.display="inline";
    document.getElementById("change_room").style.display="inline";
    document.getElementById("roomdiv").style.display="inline";
    document.getElementById("broadcast").style.display="inline";
}
function roomhide(){
    document.getElementById("changeroom").style.display="none";
}
function roomshow(){
    document.getElementById("changeroom").style.display="inline";
}
function minimize(){
    sessionStorage.setItem('chatmin', '1');
    hide();
}
function maximize(){
    sessionStorage.setItem('chatmin', '0');
    show();
}
function clear_history(){
    sessionStorage.setItem('chatlog', '');
    document.getElementById("log").innerHTML='';
}
function change_room_show(){
    sessionStorage.setItem('viewchangeroom', '0');
    roomshow();
}
$(document).ready(function(){
    var chatmin = sessionStorage.getItem("chatmin");
    if (chatmin=='null') sessionStorage.setItem("chatmin", 0);
    if (chatmin=='1') {
        hide();
    }
    if (chatmin=='0') {
        show();
    }
    var viewchangeroom = sessionStorage.getItem("viewchangeroom");
    if (viewchangeroom=='null' || viewchangeroom=='' || viewchangeroom==null) {
        sessionStorage.setItem("viewchangeroom", 1);
        roomhide();
    }
    if (viewchangeroom=='1') {
        roomhide();
    }
    if (viewchangeroom=='0') {
        roomshow();
    }
    chatroom = sessionStorage.getItem("chatroom");
    if (chatroom=='null' || chatroom=='' || chatroom==null) {
        chatroom="main";
        sessionStorage.setItem("chatroom", chatroom);
    }
    $('#roomdiv').append(chatroom);
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.emit('join', {
        room: chatroom,
        user: getusername(),
        date: new Date().toLocaleString('de-DE')
    });
    socket.on('ServerResponse',
        function(msg) {
            if (msg.user!="Server")
                {($('#log').append('<p>' + msg.user + ': ' + msg.data + '<br><h9 align="right">' + msg.date + ' - Raum:"' + msg.raum + '"</h9></p>'))};
            var element = document.getElementById("log");
            element.scrollTop = element.scrollHeight;
        });
    $('form#broadcast').submit(
        function(event) {
            socket.emit('RoomBroadcast', {
                data: $('#broadcast_data').val(),
                user: getusername(),
                date: new Date().toLocaleString('de-DE'),
                room: chatroom
            });
            document.getElementById("broadcast").reset();
            return false;
        }
    );
    $('form#changeroom').submit(
        function(event) {
            socket.emit('join', {
                room: $('#changeroom_data').val(),
                user: getusername(),
                date: new Date().toLocaleString('de-DE')
            });
            chatroom = $('#changeroom_data').val();
            sessionStorage.setItem("chatroom", chatroom);
            sessionStorage.setItem('viewchangeroom', '1');
            roomhide();
            window.location.reload();
            return false;
        }
    );
});