
//// CHAT

mc.onscroll = function () {
    var isAtBottom = (mc.scrollHeight - mc.scrollTop) === mc.clientHeight;
    if (isAtBottom) {
        $(newMessageButton).addClass('invisible').prop("disabled", true);
    }
};

function goToNewMessages() {
    mc.scrollTop = mc.scrollHeight;
    $(newMessageButton).addClass('invisible').prop("disabled", true);
}

function addMessage(usr, cntnt, clssnm) {
    console.log("addMessage: " + cntnt);

    var div = document.createElement('table');
    $(div).addClass('table ' + clssnm);

    var cntntClass = 'cntnt';
    if (usr == 'Me') {
        cntntClass = 'cntnt me';
    }

    chatMessage = [
        "<tr class='chat-message'>",
        "    <td class='usr' style='overflow-x: hidden; width: 12%; padding-left: 10px;'>" + usr + "</td>",
        "    <td class='" + cntntClass + "' style='overflow-x: hidden;'> '" + cntnt + "'</td>",
        "</tr>"
    ].join('\n');

    div.innerHTML = chatMessage;
    var isAtBottom = (mc.scrollHeight - mc.scrollTop) === mc.clientHeight;
    mc.appendChild(div);
    if (isAtBottom) {
        mc.scrollTop = mc.scrollHeight;
    } else {
        $(newMessageButton).removeClass('invisible').prop("disabled", false);
    }
}

function sendMessage() {
    JOSSkylink.sendP2PMessage(composeInput.value);
    console.log("sendMessage: " + composeInput.value);
    composeInput.value = '';
}

// sends message on return
$(composeInput).keypress(function (e) {
    if (e.which == 13) {
        sendMessage();
    }
});

JOSSkylink.on('incomingMessage', function (message, peerId, peerInfo, isSelf) {
    console.log("incomingMessage info: " + peerInfo);
    var user = 'Me', className = 'message';
    if (!isSelf) {
        user = JOSSkylink.getUserData(peerId)['name'];
        ;
    }
    addMessage(usr = user, cntnt = message.content, clssnm = className);
});

addMessage(usr = peerJOSName, cntnt = ' has joined chat', clssnm = 'action');

addMessage(usr = peerJOSName, cntnt = ' has left chat', clssnm = 'action');









