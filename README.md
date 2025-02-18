# Simple Chat Application

A simple terminal-based chat application built with Python using sockets, threading, and SQLAlchemy for real-time communication between multiple clients through a central server.

## Features

### V1 Features
- Basic terminal-based chat interface
- Multiple client connections
- Real-time message broadcasting
- Clean message formatting
- Graceful connection handling
- Simple command system ('exit')
- Server-side connection management
- Automatic client cleanup on disconnect

### V2 Features
- User authentication system
  - Username/password registration
  - Secure password storage with hashing
  - Login session management
- Database integration (SQLAlchemy)
  - User account persistence
  - Active connection tracking
  - Session management
- Security improvements
  - Password hashing
  - Secure password input
  - Session validation

## Requirements

- Python 3.6 or higher
- SQLAlchemy
- SQLite3 (included with Python)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/RavenLB/CLI-Broadcast-server.git
cd simple-chat-app
```

2. Install dependencies:

```bash
pip install sqlalchemy
```

3. Initialize the database:

```bash
python init_db.py
```

## Usage

1. Start the server:

```bash
python server.py
```

2. Connect clients:

```bash
python client.py
```

3. Register or login:
   - Choose option 1 to login with existing account
   - Choose option 2 to register new account
   - Enter username and password when prompted

4. Chat commands:
   - Type messages and press Enter to send
   - Type 'exit' to disconnect

## Security Features

- Passwords are hashed using SHA-256
- Secure password input (hidden characters)
- Session tracking prevents duplicate logins
- Automatic session cleanup on disconnect

## Error Handling

The application handles various scenarios:
- Server disconnection
- Client disconnection
- Network errors
- Invalid messages
- Authentication failures
- Database errors
- Session conflicts
- Unexpected termination

## Future Improvements

1. User Features:
   - Private messaging
   - Message history
   - File sharing
   - Online user list
   - User profiles

2. Security:
   - End-to-end encryption
   - Password strength requirements
   - Rate limiting
   - IP blocking

3. Technical Enhancements:
   - GUI interface
   - Message persistence
   - Multiple chat rooms
   - Message timestamps
   - Message formatting

4. Administrative Features:
   - User moderation tools
   - Chat room management
   - Message filtering
   - User banning/muting
   - Activity logging

## Contributing

Feel free to submit issues and enhancement requests!

## License

[MIT License](LICENSE)