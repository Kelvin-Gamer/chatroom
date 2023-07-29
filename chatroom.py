from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

messages = []

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat Room</title>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    </head>
    <body>
        <h1>Chat Room</h1>
        <div id="chat">
            <div id="message-area"></div>
            <input type="text" id="username" placeholder="Username">
            <input type="text" id="message" placeholder="Type your message">
            <button id="send-btn">Send</button>
        </div>

        <script>
            function appendMessage(username, message) {
                $('#message-area').append('<p><strong>' + username + '</strong>: ' + message + '</p>');
            }

            function sendMessage() {
                var username = $('#username').val();
                var message = $('#message').val();

                if (!username || !message) {
                    alert('Please enter both username and message.');
                    return;
                }

                $.ajax({
                    type: 'POST',
                    url: '/send_message',
                    contentType: 'application/json',
                    data: JSON.stringify({username: username, message: message}),
                    success: function(response) {
                        appendMessage(username, message);
                        $('#message').val('');
                    },
                    error: function(error) {
                        alert('Failed to send message. Please try again.');
                    }
                });
            }

            function getMessages() {
                $.ajax({
                    type: 'GET',
                    url: '/get_messages',
                    success: function(response) {
                        $('#message-area').empty();
                        for (var i = 0; i < response.length; i++) {
                            appendMessage(response[i]['username'], response[i]['message']);
                        }
                    },
                    error: function(error) {
                        console.log('Failed to retrieve messages.');
                    }
                });
            }

            $(document).ready(function() {
                $('#send-btn').on('click', sendMessage);
                setInterval(getMessages, 1000);
            });
        </script>
    </body>
    </html>
    """

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    username = data['username']
    message = data['message']
    messages.append({'username': username, 'message': message})
    return jsonify({'status': 'success'})

@app.route('/get_messages')
def get_messages():
    return jsonify(messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
