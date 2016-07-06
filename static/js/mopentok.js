// Initialize OpenTok Session object
var session = TB.initSession(sessionId);

// Initialize a Publisher, and place it in id="publisher"
var publisher = TB.initPublisher(apiKey, 'publisher');

// Attach event handlers
session.on({

    // This runs when session.connect() asynchronously completes
    sessionConnected: function (event) {

        // Publish publisher initialzed earlier - triggers 'streamCreated' on other clients
        session.publish(publisher, function () {
            screenshare();
        });
    },

    // Runs when another client publishes stream (eg. session.publish())
    streamCreated: function (event) {

        // Creates new Subscriber container, assigns streamId to id and puts it inside id="subscribers"
        var subContainer = document.createElement('div');
        subContainer.id = 'stream-' + event.stream.streamId;
        document.getElementById('subscribers').appendChild(subContainer);

        // Subscribe to the stream that caused this event, put it inside the container we just made
        session.subscribe(event.stream, subContainer);
    }
});







