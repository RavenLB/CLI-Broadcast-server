import socket
import threading
from db_service import DatabaseService

class ChatServer:
    def __init__(self, host="localhost", port=8080):
        self.host = host
        self.port = port
        self.clients = {}  # Dictionary to store client sockets and usernames
        self.db = DatabaseService()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        print("Server Started.")
        self.server.listen(5)

    def broadcast(self, message, sender_client, is_system_message=False):
        """
        Send the message to all connected clients except the sender.
        is_system_message: True for join/leave notifications, False for user messages
        """
        if is_system_message:
            formatted_message = f"\n{message}"  # System messages don't need a prefix
        else:
            sender_username = self.clients.get(sender_client, "Unknown")
            formatted_message = f"\n{sender_username}: {message}"
        
        disconnected_clients = []
        
        for client in self.clients:
            if client != sender_client:  # Skip the sender
                try:
                    client.send(formatted_message.encode())
                except Exception as e:
                    print(f"Error sending message to a client: {e}")
                    disconnected_clients.append(client)
        
        # Remove disconnected clients outside the loop
        for client in disconnected_clients:
            self.disconnect_client(client)

    def disconnect_client(self, client):
        """Handle client disconnection and cleanup"""
        try:
            username = self.clients.get(client, "Unknown")
            print(f"Logging out user: {username}")  # Debug print
            self.db.remove_active_connection(username)
            self.broadcast(f"{username} has left the chat!", None, is_system_message=True)  # Notify other users
            client.close()
        except:
            pass
        finally:
            if client in self.clients:
                del self.clients[client]

    def handle_auth(self, client):
        while True:
            try:
                auth_message = client.recv(1024).decode()
                print(f"DEBUG: Received auth message: {auth_message}") # Debug print
                
                if auth_message.startswith("REGISTER:"):
                    _, username, password = auth_message.split(":", 2)
                    print(f"DEBUG: Registration attempt for user: {username}") # Debug print
                    if self.db.register_user(username, password):
                        client.send("REGISTRATION_SUCCESS".encode())
                        return self.handle_login(client, username)
                    else:
                        client.send("REGISTRATION_FAILED".encode())
                
                elif auth_message.startswith("LOGIN:"):
                    _, username, password = auth_message.split(":", 2)
                    print(f"DEBUG: Login attempt for user: {username}") # Debug print
                    if self.db.verify_user(username, password):
                        return self.handle_login(client, username)
                    else:
                        client.send("LOGIN_FAILED".encode())
            except Exception as e:
                print(f"Auth error: {e}")
                return False
        return False

    def handle_login(self, client, username):
        if username in self.db.get_active_users():
            client.send("ALREADY_LOGGED_IN".encode())
            self.clients[client] = username
            self.broadcast(f"{username} has rejoined the chat!", None, is_system_message=True)
            return True
        
        client.send("LOGIN_SUCCESS".encode())
        self.clients[client] = username
        self.db.add_active_connection(username)
        self.broadcast(f"{username} has joined the chat!", None, is_system_message=True)
        return True

    def handle_client(self, client, client_address):
        """Handle communication with a single client."""
        print(f"New connection from: {client_address}")
        
        if not self.handle_auth(client):
            self.disconnect_client(client)  # Added explicit disconnect
            return
        
        try:
            while True:
                try:
                    message = client.recv(1024).decode("utf-8")
                    if message:
                        print(f"{self.clients[client]}: {message}")
                        self.broadcast(message, client)
                    else:
                        # Client disconnected gracefully
                        break
                except ConnectionResetError:
                    # Client disconnected unexpectedly
                    break
                except Exception as e:
                    print(f"Error with client {self.clients[client]}: {e}")
                    break
        finally:
            self.disconnect_client(client)
            print(f"Client {self.clients.get(client, 'Unknown')} disconnected.")

    def start(self):
        while True:
            client, client_address = self.server.accept()
            threading.Thread(target=self.handle_client, args=(client, client_address)).start()

    def cleanup(self):
        """Clean up server resources and disconnect all clients"""
        # Disconnect all clients before shutting down
        for client in list(self.clients.keys()):
            self.disconnect_client(client)
        self.db.cleanup()
        self.server.close()

if __name__ == "__main__":
    server = ChatServer()
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    
    try:
        while True:
            cmd = input("Type 'exit' to shut down the server: ")
            if cmd.lower() == 'exit':
                break
    finally:
        print("Shutting down server...")
        server.cleanup()