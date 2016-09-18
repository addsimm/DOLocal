skylink.on('incomingStream', function (peerId, stream, isSelf) {
    if (isSelf) {
        attachMediaStream($video, stream);
    }
    else {

        var $audio = document.createElement('audio');
        $audio.id = "audio_" + peerId;
        $audio.autoplay = true;
        $audio.volume = focussed ? 1 : 0.15;
        $users.appendChild($audio);
        attachMediaStream($audio, stream);
        peer_audios.push($audio);
    }
});

skylink.on('incomingMessage', function (message, peerId, peerInfo, isSelf) {
    if (message.content.substr(0, 1) === '/') {
        var msg = message.content.substr(1);
        if (msg === 'hail') {
            $alert.play();
            var $img = document.getElementById("img_" + peerId);
            $img.className = "hailing";
            setTimeout(function () {
                $img.className = "";
            }, 5000);

            if (!isSelf) {
                addMessage('hailed you', 'action', peerId);
            }
        }
        else if (msg.substr(0, 8) === 'getaroom') {
            var roomPeerId = msg.substr(9);
            var name = isSelf ? skylink.getPeerInfo(roomPeerId).userData.name : peerInfo.userData.name;

            addMessage('<a href="http://getaroom.io/' + roomPeerId + '" target="_blank">Get an audio/video meeting room with ' + name + '</a>',
                'action', isSelf ? roomPeerId : peerId);
        }
    }
    else {
        addMessage(message.content, "message", peerId, isSelf);
    }
});

skylink.on('peerJoined', function (peerId, peerInfo, isSelf) {
    if (isSelf) {
        online = true;
        skylink.setUserData(user);
        replay();
        if (mediaOK === false) {
            $pic.src = last_pic = "http://robohash.org/" + peerId;
            $pic.style.display = "inline";
        }
        addMessage('Welcome to ' + room + ', ' + user.name + '.', 'bot');
    }
    else {
        var info = skylink.getPeerInfo(peerId);
        var $img = addUserImage(peerId, info.userData.name);
        $img.src = peer_pics[peerId] = "http://robohash.org/" + peerId;
        addMessage('is in ' + room, 'action', peerId, false);
    }
});

skylink.on('peerLeft', function (peerId, peerInfo, isSelf) {
    if (isSelf) {
        online = false;
        addMessage('Bye', 'bot');
    }
    else {
        var $img = document.getElementById("img_" + peerId);
        var $span = document.getElementById("span_" + peerId);
        var $audio = document.getElementById("audio_" + peerId);
        $users.removeChild($img);
        $users.removeChild($span);
        $users.removeChild($audio);
        addMessage('left ' + room, 'action', peerId, false);
    }

});

skylink.init({
    //apiKey: '48f72309-6dd1-47bb-9dd2-aa43f4a6a14a',
    apiKey: '774b477f-dc20-4374-ba13-3eda09414c28',
    defaultRoom: hash
}, function () {
    skylink.getUserMedia({
        video: {
            resolution: {
                width: 160,
                height: 120
            }
        },
        audio: true
    });
    addMessage("Welcome" +
        "Please share your camera and microphone" +
        "pictures that update every 5 seconds. " +
        "Additionally there are a few more things you can do: " +
        "Your picture will blur to give you a little privacy if you're not actively following " +
        "/mute and /unmute do what you'd expect to your audio and give you more privacy. " +
        "It'll convert your picture into grayscale to indicate to others you're muted." +
        "Click on somebodies picture to hail that person" +
        "Type /hail to alert everybody in the office" +
        "Double-click somebodies picture to invite that person into a real-time audio/video meeting room</li><li>" +
        "Type /clear to empty your local chat history" +
        "Try '/share coffee' or other keywords to post random pictures of Flickr</" +
        "Join a room by typing /join roomname", 'bot');
});

//// Not in
skylink.on('dataTransferState', function (state, transferId, peerId, transferInfo, error) {
    if (state === skylink.DATA_TRANSFER_STATE.UPLOAD_REQUEST) {
        skylink.respondBlobRequest(peerId, true);
        console.log("Incoming Request from " + peerId);
    }
    else if (state === skylink.DATA_TRANSFER_STATE.DOWNLOAD_COMPLETED) {
        console.log("Download completed from " + peerId);
        var $img = document.getElementById("img_" + peerId);

        blob2dataURL(transferInfo.data, function (data) {
            peer_pics[peerId] = data;
            $img.src = data;
        });
    }
    else if (error && error.message) {
        console.log(error.message);
    }
});

//// Not in
skylink.on('mediaAccessSuccess', function (stream) {
    attachMediaStream($video, stream);
    if (!user.name) {
        capture_timeout = setTimeout(capture, 2000);
        addMessage("Thanks. May I now know your name?", 'bot');
        $msg.select();
        mediaOK = true;
    }
});

//// Not in
skylink.on('mediaAccessError', function (stream) {
    addMessage("If you don't want to share your camera and microphone, I'll make you a bot like me. Can I have your name tho?", 'bot');
    $msg.select();
    mediaOK = false;
});