import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ChatClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WhatsApp Clone")
        self.username = ""
        self.setup_login()

    def setup_login(self):
        self.login_label = tk.Label(self.root, text="Enter your Username:")
        self.login_label.pack(pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)
        self.login_btn = tk.Button(self.root, text="Connect", command=self.connect_to_server)
        self.login_btn.pack(pady=5)

    def connect_to_server(self):
        self.username = self.name_entry.get()
        if not self.username:
            messagebox.showwarning("Warning", "Please enter a username.")
            return
        
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(('127.0.0.1', 65432))
            self.client.send(self.username.encode('utf-8'))
            
            # Transition to Chat UI
            for widget in self.root.winfo_children():
                widget.destroy()
            self.setup_chat_window()
            
            # Start thread to receive messages
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", f"Could not connect to server: {e}")

    def setup_chat_window(self):
        self.root.title(f"Logged in as: {self.username}")
        
        self.chat_area = scrolledtext.ScrolledText(self.root, width=40, height=15)
        self.chat_area.pack(padx=10, pady=10)
        
        tk.Label(self.root, text="Send to (Recipient Name):").pack()
        self.target_entry = tk.Entry(self.root)
        self.target_entry.pack(fill=tk.X, padx=10)
        
        tk.Label(self.root, text="Message:").pack()
        self.msg_entry = tk.Entry(self.root)
        self.msg_entry.pack(fill=tk.X, padx=10)
        self.msg_entry.bind("<Return>", lambda x: self.send_message())
        
        self.send_btn = tk.Button(self.root, text="Send ✉", command=self.send_message, bg="#25D366", fg="white")
        self.send_btn.pack(pady=10)

    def send_message(self):
        target = self.target_entry.get()
        message = self.msg_entry.get()
        if target and message:
            full_msg = f"{target}:{message}"
            self.client.send(full_msg.encode('utf-8'))
            self.chat_area.insert(tk.END, f"You to {target}: {message}\n")
            self.msg_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                msg = self.client.recv(1024).decode('utf-8')
                if not msg: break
                self.chat_area.insert(tk.END, f"{msg}\n")
                self.chat_area.see(tk.END)
            except:
                break

if __name__ == "__main__":
    app = ChatClient()
    app.root.mainloop()