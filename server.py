import socket
import threading

HOST = '127.0.0.1'
PORT = 65432
clients = {} # {username: connection}

def broadcast_user_update():
    #שולח את רשימת המשתמשים המעודכנת לכל מי שכרגע מחובר
    user_list = ",".join(clients.keys())
    msg = f"USER_LIST_UPDATE:{user_list}"
    for conn in clients.values():
        try:
            conn.send(msg.encode('utf-8'))
        except:
            pass

def handle_client(conn, addr):
    username = None
    try:
        # קבלת שם המשתמש מיד עם החיבור
        username = conn.recv(1024).decode('utf-8').strip()
        
        if username:
            clients[username] = conn
            print(f"[SERVER] {username} connected.")
            # עדכון מיידי לכולם שהרשימה השתנתה
            broadcast_user_update()

        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data: break
            
            if ":" in data:
                target, message = data.split(":", 1)
                if target in clients:
                    clients[target].send(f"{username}:{message}".encode('utf-8'))
                else:
                    conn.send(f"SEND_FAILED:User {target} is no longer online.".encode('utf-8'))
                    
    except:
        pass
    finally:
        if username in clients:
            del clients[username]
            print(f"[SERVER] {username} disconnected.")
            # עדכון הרשימה לאחר עזיבה
            broadcast_user_update()
        conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)
print("Server is Up and listening")

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()