import socket
import threading
import getpass

class ChatClient:
    def __init__(self, host="localhost", port=8080):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None

    def get_password(self, prompt="Password: "):
        """Handle password input with proper warning handling"""
        import warnings
        
        # Temporarily catch warnings to prevent them from being printed
        with warnings.catch_warnings():
            warnings.filterwarnings("error", category=getpass.GetPassWarning)
            try:
                return getpass.getpass(prompt)
            except (getpass.GetPassWarning, Warning):
                print("\nSecure password input not available.")
                print("WARNING: Password will be visible when typing.")
                return input(prompt)

    def authenticate(self):
        while True:
            try:
                choice = input("1. Login\n2. Register\nChoice (1/2): ").strip()
                
                if choice == "1":
                    username = input("Username: ")
                    password = self.get_password("Password: ")
                    auth_message = f"LOGIN:{username}:{password}"
                    print(f"DEBUG: Sending login request")
                    try:
                        self.socket.send(auth_message.encode())
                    except (BrokenPipeError, ConnectionResetError):
                        print("Lost connection to server")
                        return False
                elif choice == "2":
                    username = input("Choose username: ")
                    password = self.get_password("Choose password: ")
                    auth_message = f"REGISTER:{username}:{password}"
                    print(f"DEBUG: Sending registration request")
                    try:
                        self.socket.send(auth_message.encode())
                    except (BrokenPipeError, ConnectionResetError):
                        print("Lost connection to server")
                        return False
                else:
                    print("Invalid choice")
                    continue

                try:
                    response = self.socket.recv(1024).decode()
                    print(f"DEBUG: Server response: {response}")
                    if response in ["LOGIN_SUCCESS", "REGISTRATION_SUCCESS", "ALREADY_LOGGED_IN"]:
                        self.username = username
                        if response == "ALREADY_LOGGED_IN":
                            print(f"Resuming session for {username}")
                        else:
                            print(f"Welcome, {username}!")
                        return True
                    else:
                        print("Authentication failed. Please try again.")
                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                    print("Lost connection to server during authentication")
                    return False
            except Exception as e:
                print(f"Authentication error: {e}")
                return False
            except KeyboardInterrupt:
                print("\nAuthentication cancelled by user")
                return False

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode()
                if message:
                    print('\033[2K\r', end='')  # Clear current line
                    print(f"{message}")
                    print("You: ", end='', flush=True)  # Add back the prompt
                else:
                    print("\nServer connection closed")
                    break
            except:
                break

    def start(self):
        try:
            self.socket.connect((self.host, self.port))
            print("Connected to server!")

            if not self.authenticate():
                print("Authentication failed, disconnecting...")
                return

            print("Type 'exit' to disconnect")

            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()

            while True:
                try:
                    message = input("You: ")
                    if message.lower() == 'exit':
                        break
                    self.socket.send(message.encode())
                except (BrokenPipeError, ConnectionResetError):
                    print("\nLost connection to server")
                    break

        except ConnectionRefusedError:
            print("Could not connect to the server. Make sure the server is running on port 8080.")
        except ConnectionResetError:
            print("Connection was reset by the server. Server might be down.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            try:
                self.socket.close()
            except:
                pass

if __name__ == "__main__":
    client = ChatClient()
    client.start()