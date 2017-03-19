var chatroom;
$(document).ready(function(){
    function hide(){
        $('#log').hide();
        $('#clear').hide();
        $('#change_room').hide();
        $('#roomdiv').hide();
        $('#broadcast').hide();
    }
    function show(){
        $('#log').show();
        $('#clear').show();
        $('#change_room').show();
        $('#roomdiv').show();
        $('#broadcast').show();
    }
    function roomhide(){
        $('#changeroom').hide();
    }
    function roomshow(){
        $('#changeroom').show();
    }
    var chatmin = sessionStorage.getItem("chatmin");
    if (chatmin=='null') sessionStorage.setItem("chatmin", 0);
    if (chatmin=='1') {
        hide();
    }
    if (chatmin=='0') {
        show();
    }
    var viewchangeroom = sessionStorage.getItem("viewchangeroom");
    if (viewchangeroom=='null') {
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
    $('form#clear').submit(
        function(){
            sessionStorage.setItem('chatlog', '');
            $('#log').html('');
        }
    );
    $('form#change_room').submit(
        function(){
            sessionStorage.setItem('viewchangeroom', '0');
            roomshow();
        }
    );
    $('form#minimize').submit(
        function(){
            sessionStorage.setItem('chatmin', '1');
            hide();
        }
    );
    $('form#maximize').submit(
        function(){
            sessionStorage.setItem('chatmin', '0');
            show();
        }
    );
});