import socket
import threading
import sys


class ChatClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.client_socket = None
        self.running = False
        self.client_name = None

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.running = True
            return True
        except socket.error as e:
            print(f'서버 연결 실패: {e}')
            return False

    def send_name(self, name):
        try:
            self.client_socket.send(name.encode('utf-8'))
            self.client_name = name
            return True
        except socket.error:
            return False

    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(message)
            except socket.error:
                break

    def send_message(self, message):
        try:
            self.client_socket.send(message.encode('utf-8'))
            return True
        except socket.error:
            return False

    def disconnect(self):
        self.running = False
        if self.client_socket:
            self.client_socket.close()

    def start_chat(self):
        if not self.connect_to_server():
            return
        
        name = input('사용자 이름을 입력하세요: ').strip()
        if not name:
            name = '익명사용자'
        
        if not self.send_name(name):
            print('이름 전송 실패')
            self.disconnect()
            return
        
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
        print('채팅을 시작합니다. "/q"를 입력하면 연결이 끊어집니다.')
        print('귓속말을 보내려면 "/w [받는사람] [메시지]" 형식으로 입력하세요.')
        print('-' * 50)
        
        try:
            while self.running:
                message = input().strip()
                if message == '/q':
                    self.send_message('/q')
                    break
                elif message:
                    if not self.send_message(message):
                        print('메시지 전송 실패')
                        break
        except KeyboardInterrupt:
            print('\n연결을 종료합니다...')
            self.send_message('/q')
        finally:
            self.disconnect()


def main():
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = 'localhost'
    
    if len(sys.argv) > 2:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print('포트 번호가 올바르지 않습니다.')
            return
    else:
        port = 12345
    
    client = ChatClient(host, port)
    client.start_chat()


if __name__ == '__main__':
    main()

