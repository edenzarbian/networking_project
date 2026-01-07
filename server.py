import socket
import threading

# Connection Constants
HOST = '127.0.0.1'
PORT = 65432
clients = {} # Dictionary to store {username: socket_connection}

def handle_client(conn, addr):
    username = None
    try:
        # Step 1: Receive the unique username upon connection
        username = conn.recv(1024).decode('utf-8')
        clients[username] = conn
        print(f"[LOG] {username} connected from {addr}")

        while True:
            # Step 2: Listen for messages in format "target:message"
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            
            if ":" in data:
                target, message = data.split(":", 1)
                # Step 3: Specific Routing (Unicast)
                if target in clients:
                    clients[target].send(f"{username}: {message}".encode('utf-8'))
                else:
                    conn.send(f"SERVER: User '{target}' is not online.".encode('utf-8'))
            else:
                conn.send("SERVER: Invalid format. Use 'target:message'".encode('utf-8'))
    except Exception as e:
        print(f"[ERROR] Connection error with {username}: {e}")
    finally:
        # Step 4: Handle unexpected disconnection
        if username in clients:
            del clients[username]
            print(f"[LOG] {username} disconnected.")
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5) # Support at least 5 clients
    print(f"[*] Server is listening on {HOST}:{PORT}...")
    
    while True:
        conn, addr = server.accept()
        # Create a new thread for each client
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
    