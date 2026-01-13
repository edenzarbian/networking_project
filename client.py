import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime

class ChatClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("EDEN & NETA'S CHAT💜")
        self.root.geometry("900x650")
        self.root.configure(bg="#E6E6FA")
        self.history = {} 
        self.username = ""
        self.current_chat = None 
        self.setup_login()

    def setup_login(self):
        self.login_frame = tk.Frame(self.root, bg="#E6E6FA")
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        tk.Label(self.login_frame, text="💜 Welcome 💜", bg="#E6E6FA", font=("Arial", 20, "bold"), fg="#4B0082").pack(pady=20)
        self.name_ent = tk.Entry(self.login_frame, font=("Arial", 14), justify='center')
        self.name_ent.pack(pady=10)
        tk.Button(self.login_frame, text="Connect", command=self.connect, bg="#4B0082", fg="white", font=("Arial", 12, "bold"), width=15).pack(pady=10)

    def connect(self):
        self.username = self.name_ent.get().strip()
        if not self.username: return
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(('127.0.0.1', 65432))
            self.client.send(self.username.encode('utf-8'))
            self.login_frame.destroy()
            self.setup_chat_ui()
            threading.Thread(target=self.receive, daemon=True).start()
        except:
            messagebox.showerror("Error", "Server not responding")

    def setup_chat_ui(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        header = tk.Label(self.root, text=f"Logged in as: {self.username}", bg="#4B0082", fg="white", font=("Arial", 11, "bold"))
        header.grid(row=0, column=0, columnspan=2, sticky="ew", ipady=10)

        #רשימת המשתמשים
        self.sidebar = tk.Frame(self.root, bg="#D8BFD8", width=200)
        self.sidebar.grid(row=1, column=0, sticky="ns")
        tk.Label(self.sidebar, text="ONLINE", bg="#D8BFD8", font=("Arial", 10, "bold")).pack(pady=10)
        self.user_list = tk.Listbox(self.sidebar, bg="#F3E5F5", font=("Arial", 11), borderwidth=0, selectbackground="#4B0082")
        self.user_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.user_list.bind('<<ListboxSelect>>', self.select_user)

        self.area = scrolledtext.ScrolledText(self.root, bg="#FDF5FF", state='disabled', font=("Arial", 11), spacing1=8)
        self.area.grid(row=1, column=1, sticky="nsew", padx=15, pady=15)
        self.area.tag_configure("me", background="#4B0082", foreground="white", lmargin1=150, lmargin2=150, rmargin=10)
        self.area.tag_configure("other", background="#D1C4E9", foreground="black", lmargin1=10, lmargin2=10, rmargin=150)
        self.area.tag_configure("error", justify='center', foreground="red", font=("Arial", 10, "bold"))

        input_frame = tk.Frame(self.root, bg="#E6E6FA")
        input_frame.grid(row=2, column=1, sticky="ew", padx=15, pady=15)
        self.target_lbl = tk.Label(input_frame, text="To: Select User", bg="#E6E6FA", fg="#4B0082", font=("Arial", 9, "bold"))
        self.target_lbl.pack(side=tk.LEFT)
        self.msg_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.msg_entry.bind("<Return>", lambda e: self.send())
        tk.Button(input_frame, text="SEND", command=self.send, bg="#4B0082", fg="white", font=("Arial", 10, "bold"), width=10).pack(side=tk.RIGHT)

    def select_user(self, event):
        selection = self.user_list.curselection()
        if selection:
            name = self.user_list.get(selection[0]).replace(" ● ", "").strip()
            self.current_chat = name
            self.target_lbl.config(text=f"Chatting with: {name}")
            self.refresh_display()

    def refresh_display(self):
        self.area.config(state='normal')
        self.area.delete('1.0', tk.END)
        if self.current_chat in self.history:
            for text, tag in self.history[self.current_chat]:
                self.area.insert(tk.END, f" {text} \n", tag)
                self.area.insert(tk.END, "\n")
        self.area.config(state='disabled')
        self.area.see(tk.END)

    def send(self):
        if not self.current_chat:
            messagebox.showwarning("Warning", "Please select a user first!")
            return
        msg = self.msg_entry.get().strip()
        if msg:
            time = datetime.now().strftime("%H:%M")
            self.client.send(f"{self.current_chat}:{msg}".encode('utf-8'))
            display_txt = f"You ({time}):\n{msg}"
            if self.current_chat not in self.history: self.history[self.current_chat] = []
            self.history[self.current_chat].append((display_txt, "me"))
            self.refresh_display()
            self.msg_entry.delete(0, tk.END)

    def receive(self):
        while True:
            try:
                data = self.client.recv(1024).decode('utf-8')
                if not data: break
                
                # עדכון הרשימה
                if data.startswith("USER_LIST_UPDATE:"):
                    users = data.split(":")[1].split(",")
                    self.user_list.delete(0, tk.END)
                    for u in users:
                        if u != self.username: self.user_list.insert(tk.END, f" ● {u}")
                
                elif data.startswith("SEND_FAILED:"):
                    self.area.config(state='normal')
                    self.area.insert(tk.END, f"\n--- {data.split(':', 1)[1]} ---\n", "error")
                    self.area.config(state='disabled')

                elif ":" in data:
                    sender, content = data.split(":", 1)
                    time = datetime.now().strftime("%H:%M")
                    if sender not in self.history: self.history[sender] = []
                    self.history[sender].append((f"{sender} ({time}):\n{content}", "other"))
                    if self.current_chat == sender: self.refresh_display()
            except: break

if __name__ == "__main__":
    ChatClient().root.mainloop()