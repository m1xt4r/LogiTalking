import threading
import socket
from customtkinter import *




class MainWindow(CTk):
   def __init__(self):
       super().__init__()


       self.title("Chat")
       self.geometry("700x420")


       self.username = "User"


       # ================= MAIN =================
       self.main_frame = CTkFrame(self)
       self.main_frame.pack(fill="both", expand=True)


       # ================= MENU =================
       self.menu_closed = 40
       self.menu_opened = 220
       self.menu_open = False


       self.menu_frame = CTkFrame(self.main_frame, width=self.menu_closed)
       self.menu_frame.pack(side="left", fill="y")
       self.menu_frame.pack_propagate(False)


       self.menu_btn = CTkButton(
           self.menu_frame,
           text="▶",
           width=30,
           command=self.toggle_menu
       )
       self.menu_btn.pack(pady=5)


       self.name_label = CTkLabel(self.menu_frame, text="Ваше імʼя:")
       self.name_entry = CTkEntry(self.menu_frame)
       self.save_btn = CTkButton(
           self.menu_frame,
           text="Зберегти",
           command=self.save_username
       )


       # ================= CHAT =================
       self.chat_frame = CTkFrame(self.main_frame)
       self.chat_frame.pack(side="left", fill="both", expand=True)


       self.chat = CTkTextbox(
           self.chat_frame,
           state="disabled",
           font=("Arial", 14)
       )
       self.chat.pack(fill="both", expand=True, padx=10, pady=10)


       bottom = CTkFrame(self.chat_frame)
       bottom.pack(fill="x")


       self.entry = CTkEntry(bottom, placeholder_text="Введіть повідомлення...")
       self.entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)


       self.send_btn = CTkButton(
           bottom,
           text="▶",
           width=50,
           command=self.send_message
       )
       self.send_btn.pack(side="right", padx=5)


       # ================= SOCKET =================
       try:
           self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           self.sock.connect(("localhost", 8080))


           hello = f"TEXT@SYSTEM@{self.username} приєднався до чату\n"
           self.sock.sendall(hello.encode())


           threading.Thread(
               target=self.recv_message,
               daemon=True
           ).start()


       except Exception as e:
           self.add_message(f"❌ Помилка підключення: {e}")


   # =================================================
   # MENU (БЕЗ АНІМАЦІЇ — 100% стабільно)
   # =================================================


   def toggle_menu(self):
       self.menu_open = not self.menu_open


       if self.menu_open:
           self.menu_frame.configure(width=self.menu_opened)
           self.menu_btn.configure(text="◀")
           self.show_menu_widgets()
       else:
           self.menu_frame.configure(width=self.menu_closed)
           self.menu_btn.configure(text="▶")
           self.hide_menu_widgets()


   def show_menu_widgets(self):
       self.name_label.pack(pady=(30, 5))
       self.name_entry.delete(0, END)
       self.name_entry.insert(0, self.username)
       self.name_entry.pack(padx=10, fill="x")
       self.save_btn.pack(pady=10)


   def hide_menu_widgets(self):
       self.name_label.pack_forget()
       self.name_entry.pack_forget()
       self.save_btn.pack_forget()


   def save_username(self):
       name = self.name_entry.get().strip()
       if name:
           self.username = name
           self.add_message(f"🔔 Тепер ваше імʼя: {self.username}")


   # =================================================
   # CHAT
   # =================================================


   def add_message(self, text):
       self.chat.configure(state="normal")
       self.chat.insert("end", text + "\n")
       self.chat.configure(state="disabled")
       self.chat.see("end")


   def send_message(self):
       msg = self.entry.get().strip()
       if not msg:
           return


       data = f"TEXT@{self.username}@{msg}\n"
       self.sock.sendall(data.encode())


       self.add_message(f"{self.username}: {msg}")
       self.entry.delete(0, END)


   def recv_message(self):
       buffer = ""
       while True:
           try:
               data = self.sock.recv(4096)
               if not data:
                   break


               buffer += data.decode()


               while "\n" in buffer:
                   line, buffer = buffer.split("\n", 1)
                   self.after(0, self.handle_line, line)


           except:
               break


   def handle_line(self, line):
       parts = line.split("@", 2)
       if len(parts) < 3:
           return


       _, author, message = parts
       self.add_message(f"{author}: {message}")




if __name__ == "__main__":
   app = MainWindow()
   app.mainloop()
