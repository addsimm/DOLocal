;(function () {
    var ChatMessage, ChatUI, Chat, ChatWidget, opentok_text_chat;

    ChatMessage = function () {
        /**
         * A representation of a chat message.
         */

        function ChatMessage(senderId, senderAlias, text) {
            Object.defineProperties(this, {
                senderId: {value: senderId},
                senderAlias: {value: senderAlias},
                text: {value: text},
                dateTime: {value: new Date()}
            });
        }

        return ChatMessage;
    }();


    ChatUI = function (ChatMessage) {

        var uiLayout = [
            '<div class="ot-bubbles">',
            '</div>',
            '<div class="ot-input" style="padding: 15px  0;">',
            '  <div>',
            '    <p class="ot-error-zone" hidden>Error sending the message!</p>',
            '    <p class="ot-new-messages" hidden>\u25BE&nbsp;Click to scroll to new messages</p>',
            '    <textarea placeholder="Contribute a thought&hellip;" class="ot-composer">' + '</textarea>',

            '      <p class="ot-character-counter"><span></span> characters left</p>',
            '      <button class="btn btn-default" style="float: right; padding: 6px 12px;">Send</button>',
            '    </div>',

            '</div>'
        ].join('\n');

        var bubbleLayout = [
            '<div>',

            '</div>'
        ].join('\n');

        /**
         * User interface for a basic chat client.
         */

        var senderAlias = 'xxx';
        function ChatUI(options) {
            options = options || {};

            this._messages = [];

            this.senderId =     options.senderId || ('' + Math.random()).substr(2);
            senderAlias =       options.senderAlias || 'xxx';
            this.maxTextLength = options.maxTextLength || 140;
            this.groupDelay =   options.groupDelay || 2 * 60 * 1000; // 2 min
            this.timeout =      options.timeout || 5000;

            this._watchScrollAtTheBottom = this._watchScrollAtTheBottom.bind(this);


            this._setupTemplates();
            this._setupUI(options.container);
            this._updateCharCounter();
        }

        ChatUI.prototype = {
            constructor: ChatUI,

            _setupTemplates: function () {
                this._bubbleTemplate = document.createElement('div');
                this._bubbleTemplate.innerHTML = bubbleLayout;
                this._bubbleTemplate.classList.add('ot-bubble');
            },

            _setupUI: function (parent) {
                parent = document.querySelector(parent) || document.body;

                var chatView = document.createElement('div');
                chatView.innerHTML = uiLayout;
                chatView.classList.add('ot-textchat');

                var sendButton = chatView.querySelector('.btn');
                var composer = chatView.querySelector('.ot-composer');
                var charCounter = chatView.querySelector('.ot-character-counter > span');
                var errorZone = chatView.querySelector('.ot-error-zone');
                var newMessages = chatView.querySelector('.ot-new-messages');

                this._composer = composer;
                this._sendButton = sendButton;
                this._charCounter = charCounter;
                this._bubbles = chatView.firstElementChild;
                this._errorZone = errorZone;
                this._newMessages = newMessages;
                this._bubbles.onscroll = this._watchScrollAtTheBottom;
                this._sendButton.onclick = this._sendMessage.bind(this);
                this._composer.onkeyup = this._updateCharCounter.bind(this);
                this._composer.onkeydown = this._controlComposerInput.bind(this);
                this._newMessages.onclick = this._goToNewMessages.bind(this);

                parent.appendChild(chatView);
            },

            _watchScrollAtTheBottom: function () {
                if (this._isAtBottom()) {
                    this._hideNewMessageAlert();
                }
            },

            _sendMessage: function () {
                var _this = this;
                var contents = this._composer.value;
                if (contents.length > _this.maxTextLength) {
                    _this._showTooLongTextError();
                } else {
                    _this._hideErrors();
                    if (typeof _this.onMessageReadyToSend === 'function') {
                        _this.disableSending();

                        var timeout = setTimeout(function () {
                            _this._showError();
                            _this.enableSending();
                        }, _this.timeout);

                        var sent = _this.onMessageReadyToSend(contents, function (err) {
                            clearTimeout(timeout);
                            if (err) {
                                _this._showError();

                            } else {

                                _this.addMessage(new ChatMessage(_this.senderId, senderAlias, contents));
                                _this._composer.value = '';
                                _this._updateCharCounter();
                                _this._hideErrors();
                            }
                            _this.enableSending();
                        });
                    }
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
            _showError: function () {
                this._errorZone.hidden = false;
            },
            _hideErrors: function () {
                this._errorZone.hidden = true;
                this._hideTooLongTextError();
            },
            _controlComposerInput: function (evt) {
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
            /**
             * Adds a message to the conversation.
             */
            addMessage: function (message) {
                var shouldGroup = this._shouldGroup(message);
                var shouldScroll = this._shouldScroll();
                this[shouldGroup ? '_groupBubble' : '_addNewBubble'](message);
                if (shouldScroll) {
                    this._scrollToBottom();
                } else {
                    this._showNewMessageAlert();
                }
                this._messages.push(message);
            },

            // Transform the message before displaying it be careful - safe html.
            renderMessage: function (raw, isGrouping) {
                return raw;
            },

            // Enable input area and sending button.
            enableSending: function () {
                this._sendButton.removeAttribute('disabled');
                this._composer.removeAttribute('disabled');
                this._composer.focus();
            },

            // Disable input area and sending button.
            disableSending: function () {
                this._sendButton.disabled = true;
                this._composer.disabled = true;
            },
            _shouldGroup: function (message) {
                if (this._lastMessage && this._lastMessage.senderId === message.senderId) {
                    var reference = this._lastMessage.dateTime.getTime();
                    var newDate = message.dateTime.getTime();
                    return newDate - reference < this.groupDelay;
                }
                return false;
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
                var contents = this.renderMessage(message.text, true);
                this._lastBubble.appendChild(this._getBubbleContent(contents));
                // this._lastTimestamp.textContent = this.humanizeDate(message.dateTime);
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
            get _lastTimestamp() {
                return this._bubbles.lastElementChild.querySelector('.ot-message-timestamp');
            },
            _getBubbleContent: function (safeHtml) {
                var div = document.createElement('DIV');
                div.classList.add('ot-message-content');
                div.innerHTML = safeHtml;
                return div;
            },
            _getBubble: function (message) {
                var bubble = this._bubbleTemplate.cloneNode(true);
                var wrapper = bubble.querySelector('div');
                var sender = wrapper.querySelector('.ot-message-sender');
                var timestamp = wrapper.querySelector('.ot-message-timestamp');
                // Sender & alias
                bubble.dataset.senderId = message.senderId;
                // alert("message.senderId: " + message.sessionId);
                // sender_alias = 'Missing name';
                // alert("three message.sender_alias: " + message.senderAlias);
                sender_alias = message.senderAlias;
                //if (message.senderId === this.senderId) {
                //    bubble.classList.add('mine');
                //    sender_alias = "Me";
                //} else {
                //    sender_alias = message.senderAlias;
                //}
                // Content
                var contents = this.renderMessage(message.text, false);
                wrapper.appendChild(this._getBubbleContent(contents));
                wrapper.innerHTML = "<span class='ot-message-sender'>" + sender_alias + '</span>' + contents;

                return bubble;
            },

            // humanizeDate
            humanizeDate: function (date) {
                var hours = date.getHours();
                var isAM = hours < 12;
                var hours12 = hours > 12 ? hours - 12 : hours;
                var minutes = date.getMinutes();
                minutes = (minutes < 10 ? '0' : '') + minutes;
                return hours + ':' + minutes + (isAM ? ' AM' : ' PM');
            }
        };
        return ChatUI;
    }(ChatMessage);

    Chat = function () {

        /**
         * OpenTok signal based Chat client.
         */
        function Chat(options) {
            if (!options || !options.session) {
                throw new Error('No session provided.');
            }
            this._session = options.session;
            var signalName = options.signalName || 'TextChat';
            this._session.on('signal:' + signalName, this._handleChatSignal.bind(this));
            Object.defineProperty(this, 'signalName', {value: signalName});
        }

        Chat.prototype = {
            constructor: Chat,
            /**
             * Sends a message though the chat.
             */
            ///////////////////////////////////////////////////////////////////////////////////////
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
                ///////////////////////////////////////////////////////////////////////////////////////
                return {
                    type: this.signalName,
                    data: text
                };
            }
        };
        return Chat;
    }();

    ChatWidget = function (Chat, ChatUI, ChatMessage) {
        // This regular expression detect text fragments looking like URLs.
        var links = /https?:\/\/[^.]+\..+/g;

        /**
         * An HTML widget enabling basic chat capabilities. Pass a `session` object the `options` hash.
         */

        // ChatWidget combines `ChatUI` and `ChatMessage` classes with `Chat` library.
        function ChatWidget(options) {

            if (!options || !options.session) {
                throw new Error('The key session must be present and set to a valid OpenTok session.');
            }
            this._chatBox = new ChatUI(options); //// NEW CHAT UI <<<<


            // Overriding transforms message before showing in chat.
            this._chatBox.renderMessage = this.renderMessage.bind(this);

            // If connected, create chat session
            if (options.session.connection) {
                this._start(options);
            }

            // otherwise wait for connection.
            else {
                options.session.once('sessionConnected', this._start.bind(this, options));
            }

            this._chatBox.disableSending();
        }

        ChatWidget.prototype = {
            constructor: ChatWidget,

            // START Connect the chat.
            _start: function (options) {
                if (!this._chat) {
                    this._chat = new Chat(options); //// CREATE CHAT <<<<

                    // Received messages handled by library
                    this._chat.onMessageReceived = this.onMessageReceived.bind(this);
                    // Sending messages handled by UI.
                    this._chatBox.onMessageReadyToSend = this.onMessageReadyToSend.bind(this);
                    // This set the sender information, id to messages - alias to other users.
                    this._chatBox.senderId = options.session.connection.connectionId;
                    this._chatBox.senderAlias = options.session.connection.data;
                    // Finally, enable message area and send buttons.
                    this._chatBox.enableSending();
                }
            },

            /**
             * Called when the user clicks send. Receives contents of input area and a callback.
             */

            // After the user click on the send button, sends contents through the `Chat` instance.
            onMessageReadyToSend: function (contents, callback) {
                // ("send: " + contents + " callback: " + callback);
                this._chat.send(contents, callback);
            },

            // Called when the chat receives a message. Also extracts id and alias from the connection.
            // After a message is received, simply create a new `ChatMessage` instance and add it to the UI.

            /////////////////////////////////////////////////////

            onMessageReceived: function (contents, from) {

                seen = [];

                json = JSON.stringify(from, function (key, val) {
                    if (typeof val == "object") {
                        if (seen.indexOf(val) >= 0)
                            return;
                        seen.push(val)
                    }
                    return val
                });


                // alert("from object: " + json);
                  var message = new ChatMessage(from.connectionId, from.data, contents);
                // alert("from.connectionId: " + from.connectionId + ", from.data: " + from.data + ", contents: "  + contents);
                this._chatBox.addMessage(message);
            },

            // Transform the text from message into content. Override for further transformations.
            // Transformations implemented by default: detecting URLs and allowing multiline messages.
            renderMessage: function (raw) {
                var output;
                // Allow multiline
                output = raw.replace(/(\r\n|\r|\n)/g, '<br/>');
                // Detect links
                output = output.replace(links, function (href) {
                    return '<a href="' + href + '" target="_blank">' + href + '</a>';
                });
                return output;
            }
        };

        return ChatWidget;

    }(Chat, ChatUI, ChatMessage);

    opentok_text_chat = function (Chat, ChatUI, ChatMessage, ChatWidget) {
        window.OTSolution = window.OTSolution || {};
        window.OTSolution.TextChat = {
            Chat: Chat,
            ChatUI: ChatUI,
            ChatMessage: ChatMessage,
            ChatWidget: ChatWidget
        };
    }(Chat, ChatUI, ChatMessage, ChatWidget);
}());