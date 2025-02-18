import socket
import threading

host = "localhost"
port = 4444
clients = {}  # Dictionary to store client sockets and usernames
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
print("Server Started.")
server.listen(5)

def broadcast(message, sender_client):
    """
    Send the message to all connected clients except the sender.
    """
    sender_username = clients.get(sender_client, "Unknown")
    disconnected_clients = []
    
    for client in clients:
        if client != sender_client:  # Skip the sender
            try:
                formatted_message = f"\nMessage from {sender_username}: {message}"
                client.send(formatted_message.encode())
            except Exception as e:
                print(f"Error sending message to a client: {e}")
                disconnected_clients.append(client)
    
    # Remove disconnected clients outside the loop
    for client in disconnected_clients:
        try:
            client.close()
        except:
            pass
        if client in clients:
            del clients[client]

def handle_username_registration(client, client_address):
    """
    Handle the username registration process for a new client
    """
    while True:
        try:
            message = client.recv(1024).decode()
            if message.startswith("USERNAME:"):
                username = message[9:]  # Remove "USERNAME:" prefix
                
                # Check if username is already taken
                if username in clients.values():
                    client.send("USERNAME_TAKEN".encode())
                else:
                    clients[client] = username
                    client.send("USERNAME_ACCEPTED".encode())
                    print(f"Username '{username}' registered for {client_address}")
                    return True
        except Exception as e:
            print(f"Error during registration for {client_address}: {e}")
            return False

def handle_client(client, client_address):
    """
    Handle communication with a single client.
    """
    print(f"New connection from: {client_address}")
    
    # Handle username registration first
    if not handle_username_registration(client, client_address):
        client.close()
        return
    
    try:
        while True:
            try:
                message = client.recv(1024).decode("utf-8")
                if message:
                    print(f"Message from {clients[client]}: {message}")
                    broadcast(message, client)
                else:
                    break
            except ConnectionResetError:
                break
            except Exception as e:
                print(f"Error with client {clients[client]}: {e}")
                break
    finally:
        username = clients.get(client, "Unknown")
        print(f"Client {username} disconnected.")
        try:
            client.close()
        except:
            pass
        if client in clients:
            del clients[client]

def start_server():
    while True:
        client, client_address = server.accept()
        threading.Thread(target=handle_client, args=(client, client_address)).start()

if __name__ == "__main__":
    threading.Thread(target=start_server).start()
    while True:
        user_input = input("Type 'exit' to shut down the server: ")
        if user_input.lower() == "exit":
            print("Shutting down server...")
            server.close()
            break