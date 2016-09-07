

// Input Area
var HTML =
    '    <p class="ot-new-messages" hidden>\u25BE&nbsp;Click to scroll to new messages</p>' +
    '    <p class="ot-character-counter"><span></span> characters left</p>';


    // defaults
    maxTextLength = options.maxTextLength || 140;
    groupDelay = options.groupDelay || 2 * 60 * 1000; // 2 min
    timeout = options.timeout || 5000;
    

    
    updateCharCounter();
    
       
    _bubbles = chatView.firstElementChild;

    
    _charCounter = charCounter;
    

    _composer.onkeyup = _updateCharCounter.bind(this);
    
    
    _newMessages = newMessages;
    _newMessages.onclick = _goToNewMessages.bind(this);



    _showTooLongTextError = function () {
        _charCounter.parentElement.classList.add('error');
    };
    _hideTooLongTextError = function () {
        _charCounter.parentElement.classList.remove('error');
    };

    _updateCharCounter = function () {
        var remaining = maxTextLength - _composer.value.length;
        var isValid = remaining >= 0;
        if (isValid) {
            _hideTooLongTextError();
        } else {
            _showTooLongTextError();
        }
        _charCounter.textContent = remaining;
    };

    // Adds a message to the conversation.
    addMessage = function (message) {

        var shouldGroup = _shouldGroup(message); //// Key
        var shouldScroll = _shouldScroll();      //// Key
        this[shouldGroup ? '_groupBubble' : '_addNewBubble'](message);


        _messages.push(message); /// ???
    };
    _shouldGroup = function (message) {
        return (_lastMessage && _lastMessage.senderId === message.senderId);
    };

    _groupBubble = function (message) {
        var contents = 'contents';
        _lastBubble.appendChild(_getBubbleContent(contents));
    };
    _addNewBubble = function (message) {
        _bubbles.appendChild(_getBubble(message));
    };
    _lastMessage = function() {
        return _messages[_messages.length - 1];
    };
    _lastBubble = function () {
        return _bubbles.lastElementChild.querySelector('div');
    };






