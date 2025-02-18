import socket
import threading

host = "localhost"
port = 4444
clients = []  # List of connected clients
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
print("Server Started.")
server.listen(5)

def broadcast(message, sender_client):
    """
    Send the message to all connected clients except the sender.
    """
    disconnected_clients = []
    for client in clients:
        if client != sender_client:  # Skip the sender
            try:
                formatted_message = f"{message}"
                client.send(bytes(formatted_message, "utf-8"))
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
            clients.remove(client)

def handle_client(client, client_address):
    """
    Handle communication with a single client.
    """
    print(f"New connection: {client_address}")
    try:
        while True:
            try:
                message = client.recv(1024).decode("utf-8")
                if message:
                    print(f"Message from {client_address}: {message}")
                    broadcast(message, client)
                else:
                    break
            except ConnectionResetError:
                break
            except Exception as e:
                print(f"Error with client {client_address}: {e}")
                break
    finally:
        print(f"Client {client_address} disconnected.")
        try:
            client.close()
        except:
            pass
        if client in clients:
            clients.remove(client)

# Function to accept incoming connections
def start_server():
    while True:
        client, client_address = server.accept()
        clients.append(client)
        threading.Thread(target=handle_client, args=(client, client_address)).start()

if __name__ == "__main__":
    threading.Thread(target=start_server).start()
    while True:
        user_input = input("Type 'exit' to shut down the server: ")
        if user_input.lower() == "exit":
            print("Shutting down server...")
            server.close()
            break