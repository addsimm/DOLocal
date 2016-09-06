

ChatUI = function (ChatMessage) {

    var uiLayout = [

        // Messages
        '<div class="ot-bubbles">',
        '</div>',

        // Input Area
        '<div class="ot-input" style="padding: 15px  0;">',
        '    <div>',
        '    <p class="ot-new-messages" hidden>\u25BE&nbsp;Click to scroll to new messages</p>',
        '    <textarea placeholder="Contribute a thought&hellip;" class="ot-composer">' + '</textarea>',
        '    <p class="ot-character-counter"><span></span> characters left</p>',
        '    <button class="btn btn-default" style="float: right; padding: 6px 12px;">Send</button>',
        '    </div>',
        '</div>'
    ].join('\n');

    // User interface for a basic chat client.
    function ChatUI(options) {
        options = options || {};

        this._messages = [];

        // defaults
        this.maxTextLength = options.maxTextLength || 140;
        this.groupDelay = options.groupDelay || 2 * 60 * 1000; // 2 min
        this.timeout = options.timeout || 5000;

        this._watchScrollAtTheBottom = this._watchScrollAtTheBottom.bind(this);

        this._updateCharCounter();
    }

    ChatUI.prototype = {
        constructor: ChatUI,

        _setupUI: function (parent) {

            //// >>>>  Layout Chat Area

            this._bubbles = chatView.firstElementChild;
            this._bubbles.onscroll = this._watchScrollAtTheBottom;

            this._charCounter = charCounter;

            this._composer = composer;
            this._composer.onkeydown = this._controlComposerInput.bind(this);
            this._composer.onkeyup = this._updateCharCounter.bind(this);

            this._errorZone = errorZone;

            this._newMessages = newMessages;
            this._newMessages.onclick = this._goToNewMessages.bind(this);

            this._sendButton = sendButton;
            this._sendButton.onclick = this._sendMessage.bind(this);

            parent.appendChild(chatView);
        },
        _watchScrollAtTheBottom: function () {
            if (this._isAtBottom()) {
                this._hideNewMessageAlert();
            }
        },
        _sendMessage: function () {
            var contents = this._composer.value; //// <<< get contents

            if (contents.length > _this.maxTextLength) {

                _this._showTooLongTextError();

            } else {

                _this._hideErrors();
                //// >> Send MEessage
            }
        },
        _showTooLongTextError: function () {
            this._charCounter.parentElement.classList.add('error');
        },
        _hideTooLongTextError: function () {
            this._charCounter.parentElement.classList.remove('error');
        },
        _showNewMessageAlert: function () {
            this._newMessages.removeAttribute('hidden');
        },
        _hideNewMessageAlert: function () {
            this._newMessages.hidden = true;
        },
        _controlComposerInput: function (evt) {  /// INTERESTING
            var isEnter = evt.which === 13 || evt.keyCode === 13;
            if (!evt.shiftKey && isEnter) {
                evt.preventDefault();
                this._sendMessage();
            }
        },
        _goToNewMessages: function () {
            this._scrollToBottom();
            this._hideNewMessageAlert();
        },
        _updateCharCounter: function () {
            var remaining = this.maxTextLength - this._composer.value.length;
            var isValid = remaining >= 0;
            if (isValid) {
                this._hideTooLongTextError();
            } else {
                this._showTooLongTextError();
            }
            this._charCounter.textContent = remaining;
        },
        // Adds a message to the conversation.
        addMessage: function (message) {

            var shouldGroup = this._shouldGroup(message); //// Key
            var shouldScroll = this._shouldScroll();      //// Key
            this[shouldGroup ? '_groupBubble' : '_addNewBubble'](message);

            if (shouldScroll) {
                this._scrollToBottom();
            } else {
                this._showNewMessageAlert();
            }
            this._messages.push(message); /// ???
        },
        _shouldGroup: function (message) {
            return (this._lastMessage && this._lastMessage.senderId === message.senderId);
        },
        _shouldScroll: function () {
            return this._isAtBottom();
        },
        _isAtBottom: function () {
            var bubbles = this._bubbles;
            return bubbles.scrollHeight - bubbles.scrollTop === bubbles.clientHeight;
        },
        _scrollToBottom: function () {
            this._bubbles.scrollTop = this._bubbles.scrollHeight;
        },
        _groupBubble: function (message) {
            var contents = 'contents';
            this._lastBubble.appendChild(this._getBubbleContent(contents));
        },
        _addNewBubble: function (message) {
            this._bubbles.appendChild(this._getBubble(message));
        },
        get _lastMessage() {
            return this._messages[this._messages.length - 1];
        },
        get _lastBubble() {
            return this._bubbles.lastElementChild.querySelector('div');
        },
        _getBubbleContent: function (content) {
            var div = document.createElement('DIV');
            div.classList.add('ot-message-content');
            div.innerHTML = content;
            return div;
        },
        _getBubble: function (message) {
            // >>>>  Put Message SOMEWWHERE
            var wrapper = bubble.querySelector('div');
            var sender = wrapper.querySelector('.ot-message-sender');

            bubble.dataset.senderId = message.senderId;

            // sender_alias
            if (message.senderId === this.senderId) {
                bubble.classList.add('mine');
                sender_alias = "Me";
            } else {
                sender_alias = message.senderAlias;
            }

            //// >>>>  Content
            var contents = 'contents';
            wrapper.appendChild(this._getBubbleContent(contents));
            wrapper.innerHTML = "<span class='ot-message-sender'>" + sender_alias + '</span>' + contents;

            return bubble;
        }
    };


    Chat = function () {

        Chat.prototype = {
            constructor: Chat,
            // Sends a message though the chat.
            send: function (text, callback) {
                var signal = this._getMessageSignal(text);
                this._session.signal(signal, callback);
            },

            // Called when receiving a new message from the chat
            onMessageReceived: function (contents, from) {
            },

            _handleChatSignal: function (signal) {
                var me = this._session.connection.connectionId;
                var from = signal.from.connectionId;
                if (from !== me) {
                    var handler = this.onMessageReceived;
                    if (handler && typeof handler === 'function') {
                        handler(signal.data, signal.from);
                    }
                }
            },

            _getMessageSignal: function (text) {
                return {
                    type: this.signalName,
                    data: text
                };
            }
        };
        return Chat;
    }
};
