import socket
import threading


HOST = "0.0.0.0"
PORT = 8080


clients = []




def broadcast(message, exclude=None):
   for client in clients:
       if client != exclude:
           try:
               client.sendall(message.encode("utf-8"))
           except:
               pass




def handle_client(sock):
   buffer = ""


   while True:
       try:
           data = sock.recv(4096)
           if not data:
               break


           buffer += data.decode("utf-8")


           while "\n" in buffer:
               line, buffer = buffer.split("\n", 1)
               broadcast(line + "\n", exclude=sock)


       except:
           break


   if sock in clients:
       clients.remove(sock)


   sock.close()




def main():
   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   server.bind((HOST, PORT))
   server.listen()


   print(f"✅ Сервер запущено: {HOST}:{PORT}")


   while True:
       client, addr = server.accept()
       print("🔌 Підключився:", addr)
       clients.append(client)


       threading.Thread(
           target=handle_client,
           args=(client,),
           daemon=True
       ).start()




if __name__ == "__main__":
   main()
