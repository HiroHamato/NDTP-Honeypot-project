#!/usr/bin/env python3

import socket
import paramiko
import threading
import requests
from datetime import datetime

port = 22
TOKEN = "6454211004:AAGHjg0F8dCXneF7O7CzLTO0NRukE-_auq8"
chat_id = ""
server_key = paramiko.RSAKey.generate(2048)

class SSHServer(paramiko.ServerInterface):
	def check_auth_password(self, username, password):
		print(f"{username} : {password}")
		message = f"{datetime.now().isoformat(' ', 'seconds')} \n login: {username} \n password: {password}"
		url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
		requests.get(url)
		return paramiko.AUTH_FAILED

def handle_connection(client_sock):
	transport = paramiko.Transport(client_sock)
	# server_key = paramiko.RSAKey.from_private_key_file("C:/Users/Admin/Desktop/custom ssh honeypot v2/key")
	transport.add_server_key(server_key)
	ssh = SSHServer()
	transport.start_server(server=ssh)

def main():
	server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	server_sock.bind(('',port))
	server_sock.listen(223)
	while True:
		client_sock,client_addr = server_sock.accept()
		print(f"Connection from {client_addr[0]}:{client_addr[1]}")
		message = f"{datetime.now().isoformat(' ', 'seconds')} Connection from {client_addr[0]}:{client_addr[1]}"
		url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
		requests.get(url)
		t = threading.Thread(target=handle_connection,args=(client_sock,))
		t.start()

if __name__ == "__main__":
	chat_id=input("Write your telegram chatID: ")
	print("SSH honeypot started!")
	main()
