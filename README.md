# Simple Chat Application

A simple terminal-based chat application built with Python using sockets and threading for real-time communication between multiple clients through a central server.

## V1 Features

- Basic terminal-based chat interface
- Multiple client connections
- Real-time message broadcasting
- Clean message formatting (You/Them prefixes)
- Graceful connection handling and error recovery
- Simple command system ('exit')
- Server-side connection management
- Automatic client cleanup on disconnect

## Requirements

- Python 3.6 or higher

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/RavenLB/CLI-Broadcast-server.git
cd simple-chat-app
```

2. Start the server:

```bash
python server.py start
```

## Usage

1. Connect to the server:

```bash
python client.py
```

2. Send messages:

```bash
Type your message and press Enter to send.
Type 'exit' to disconnect.
```

3. Disconnect:

```bash
Type 'exit' to disconnect.
```

## Example Interaction

```bash
Server Terminal:
Server Started.
New connection: ('127.0.0.1', 52431)
Message from ('127.0.0.1', 52431): Hello everyone!

Client Terminal:
Connected to the server!
Type 'exit' to disconnect
You: Hello everyone!
Them: Hi there!
You:
```

## Error Handling

The application handles various scenarios:
- Server disconnection
- Client disconnection
- Network errors
- Invalid messages
- Unexpected client termination

## Future Improvements

1. User Features:
   - Username registration
   - Private messaging
   - Message history
   - File sharing
   - Emojis and rich text support
   - Online user list

2. Security:
   - End-to-end encryption
   - User authentication
   - Message validation
   - Rate limiting

3. Technical Enhancements:
   - GUI interface
   - Message persistence (database)
   - Server configuration file
   - Multiple chat rooms
   - Message timestamps
   - Server status monitoring
   - Client reconnection handling

4. Administrative Features:
   - User moderation tools
   - Chat room management
   - Message filtering
   - User banning/muting

## Contributing

Feel free to submit issues and enhancement requests