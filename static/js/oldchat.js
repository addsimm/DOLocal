

// Input Area
var HTML =
    '    <p class="ot-new-messages" hidden>\u25BE&nbsp;Click to scroll to new messages</p>' +
    '    <p class="ot-character-counter"><span></span> characters left</p>';


    // defaults
    maxTextLength = options.maxTextLength || 140;
    groupDelay = options.groupDelay || 2 * 60 * 1000; // 2 min
    timeout = options.timeout || 5000;
    
    watchScrollAtTheBottom = _watchScrollAtTheBottom.bind(this);
    
    updateCharCounter();
    
       
    _bubbles = chatView.firstElementChild;
    _bubbles.onscroll = _watchScrollAtTheBottom;
    
    _charCounter = charCounter;
    

    _composer.onkeyup = _updateCharCounter.bind(this);
    
    
    _newMessages = newMessages;
    _newMessages.onclick = _goToNewMessages.bind(this);


    _watchScrollAtTheBottom = function () {
        if (_isAtBottom()) {
            _hideNewMessageAlert();
        }
    }; 

    _showTooLongTextError = function () {
        _charCounter.parentElement.classList.add('error');
    };
    _hideTooLongTextError = function () {
        _charCounter.parentElement.classList.remove('error');
    };
    _showNewMessageAlert = function () {
        _newMessages.removeAttribute('hidden');
    };
    _hideNewMessageAlert = function () {
        _newMessages.hidden = true;
    };

    _goToNewMessages = function () {
        _scrollToBottom();
        _hideNewMessageAlert();
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

        if (shouldScroll) {
            _scrollToBottom();
        } else {
            _showNewMessageAlert();
        }
        _messages.push(message); /// ???
    };
    _shouldGroup = function (message) {
        return (_lastMessage && _lastMessage.senderId === message.senderId);
    };
    _shouldScroll = function () {
        return _isAtBottom();
    };
    _isAtBottom = function () {
        var bubbles = _bubbles;
        return bubbles.scrollHeight - bubbles.scrollTop === bubbles.clientHeight;
    };
    _scrollToBottom = function () {
        _bubbles.scrollTop = _bubbles.scrollHeight;
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






