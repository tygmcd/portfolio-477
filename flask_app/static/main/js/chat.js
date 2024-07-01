const sendButton = document.getElementById("msg-send");
const leaveButton = document.getElementById("chat-leave");

// SOCKET.IO
var socket;
$(document).ready(function(){
    
    // socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket = io.connect('https://' + document.domain + ':' + location.port + '/chat');
    socket.on('connect', function() {
        socket.emit('joined', {});
    });
    
    // Listen for status event
    socket.on('status', function(data) {     
        let tag  = document.createElement("p");
        let text = document.createTextNode(data.msg);
        let element = document.getElementById("chat");

        document.getElementById("online-count").innerHTML = "Currently Online: " + data.online;

        tag.appendChild(text);
        tag.style.cssText = data.style;
        element.appendChild(tag);
        $('#chat').scrollTop($('#chat')[0].scrollHeight);

    });

    // Listen for message received
    socket.on('message-received', function(data) {     
        let tag  = document.createElement("p");
        let text = document.createTextNode(data.msg);
        let element = document.getElementById("chat");
        tag.appendChild(text);
        tag.style.cssText = data.style;
        element.appendChild(tag);
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });       

});

// Allows enter key to act as button press
document.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendButton.click();
    }
});

// Perform when sendButton is clicked
sendButton.addEventListener('click', (event) => {
    const message = document.getElementById("msg-input");
    socket.emit('message-sent', {'msg': message.value});
    message.value = "";
});

// Perform when leaveButton is clicked
leaveButton.addEventListener('click', (event) => {
    socket.emit('leave-room', {});
    window.location.href = "/home";
});