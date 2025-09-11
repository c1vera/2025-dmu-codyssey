import socket
import threading
import time


class ChatServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.clients = []
        self.client_names = {}
        self.server_socket = None
        self.running = False

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        print(f'채팅 서버가 {self.host}:{self.port}에서 시작되었습니다.')
        
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
            except socket.error:
                break

    def handle_client(self, client_socket, client_address):
        client_name = None
        try:
            client_name = client_socket.recv(1024).decode('utf-8').strip()
            if not client_name:
                client_name = f'사용자{len(self.clients) + 1}'
            
            self.clients.append(client_socket)
            self.client_names[client_socket] = client_name
            
            join_message = f'{client_name}님이 입장하셨습니다.'
            self.broadcast_message(join_message, client_socket)
            print(join_message)
            
            while self.running:
                try:
                    message = client_socket.recv(1024).decode('utf-8').strip()
                    if not message:
                        break
                    
                    if message == '/q':
                        break
                    
                    if message.startswith('/w '):
                        self.handle_whisper(client_socket, message)
                    else:
                        formatted_message = f'{client_name}> {message}'
                        self.broadcast_message(formatted_message, client_socket)
                        print(formatted_message)
                        
                except socket.error:
                    break
                    
        except Exception as e:
            print(f'클라이언트 처리 중 오류: {e}')
        finally:
            self.remove_client(client_socket, client_name)

    def handle_whisper(self, sender_socket, message):
        try:
            parts = message.split(' ', 2)
            if len(parts) < 3:
                sender_socket.send('귓속말 형식이 잘못되었습니다. /w [받는사람] [메시지]'.encode('utf-8'))
                return
            
            target_name = parts[1]
            whisper_message = parts[2]
            sender_name = self.client_names[sender_socket]
            
            target_socket = None
            for socket_obj, name in self.client_names.items():
                if name == target_name:
                    target_socket = socket_obj
                    break
            
            if target_socket:
                whisper_to_send = f'[귓속말] {sender_name}님이 {target_name}님에게: {whisper_message}'
                target_socket.send(whisper_to_send.encode('utf-8'))
                sender_socket.send(f'[귓속말] {target_name}님에게 전송했습니다.'.encode('utf-8'))
            else:
                sender_socket.send(f'{target_name}님을 찾을 수 없습니다.'.encode('utf-8'))
                
        except Exception as e:
            sender_socket.send('귓속말 전송 중 오류가 발생했습니다.'.encode('utf-8'))

    def broadcast_message(self, message, sender_socket=None):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except socket.error:
                    self.remove_client(client, self.client_names.get(client))

    def remove_client(self, client_socket, client_name):
        if client_socket in self.clients:
            self.clients.remove(client_socket)
            if client_name:
                leave_message = f'{client_name}님이 퇴장하셨습니다.'
                self.broadcast_message(leave_message)
                print(leave_message)
            if client_socket in self.client_names:
                del self.client_names[client_socket]
            client_socket.close()

    def stop_server(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        for client in self.clients:
            client.close()


def main():
    server = ChatServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        print('\n서버를 종료합니다...')
        server.stop_server()


if __name__ == '__main__':
    main()

