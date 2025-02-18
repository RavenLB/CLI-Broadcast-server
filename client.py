import socket
import threading

def register_username(client_socket):
    """
    Handle username registration with the server
    """
    while True:
        try:
            username = input("Enter your username: ")
            if username and username.strip():
                # Send username to server for validation
                client_socket.send(f"USERNAME:{username}".encode())
                response = client_socket.recv(1024).decode()
                
                if response == "USERNAME_TAKEN":
                    print("Username already taken. Please choose another one.")
                elif response == "USERNAME_ACCEPTED":
                    print(f"Welcome, {username}!")
                    return username
            else:
                print("Username cannot be empty. Please try again.")
        except Exception as e:
            print(f"Error during registration: {e}")
            return None

def receive_messages(client_socket):
    """
    Listen for messages from the server and display them.
    """
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                # Clear current line and move to beginning
                print('\033[2K\r', end='')  # Clear the current line
                print(f"{message}")  # Print the received message
                # Print the prompt on a new line
                print("You: ", end='', flush=True)
            else:
                print("\nServer connection closed")
                break
        except socket.error:
            # Socket was closed by send_messages
            break
        except Exception as e:
            print(f"\nError receiving message: {e}")
            break

def send_messages(client_socket, username):
    while True:
        try:
            message = input("You: ")
            if message.lower() == 'exit':
                print("\nDisconnecting from server...")
                client_socket.shutdown(socket.SHUT_RDWR)
                break
            client_socket.send(message.encode())
        except Exception as e:
            print(f"\nError sending message: {e}")
            break
    try:
        client_socket.close()
    except:
        pass

def start_client():
    host = "localhost"
    port = 4444

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print("Connected to the server!")
        
        # Register username
        username = register_username(client_socket)
        if not username:
            print("Registration failed. Disconnecting...")
            client_socket.close()
            return

        print("Type 'exit' to disconnect")

        # Start a thread to listen for messages from the server
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
        receive_thread.start()

        # Main loop for sending messages to the server
        send_messages(client_socket, username)

    except ConnectionRefusedError:
        print("Could not connect to the server. Make sure the server is running.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            client_socket.close()
        except:
            pass

if __name__ == "__main__":
    start_client()