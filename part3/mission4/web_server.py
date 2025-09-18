import http.server
import socketserver
import datetime
import os


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 접속 시간과 IP 주소 로깅
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_ip = self.client_address[0]
        print(f'접속 시간: {current_time}, IP 주소: {client_ip}')
        
        # index.html 파일이 요청된 경우
        if self.path == '/' or self.path == '/index.html':
            self.serve_index_html()
        else:
            # 다른 파일 요청에 대한 기본 처리
            super().do_GET()
    
    def serve_index_html(self):
        try:
            # index.html 파일 읽기
            with open('index.html', 'r', encoding='utf-8') as file:
                content = file.read()
            
            # HTTP 응답 헤더 전송 (200 상태 코드)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-length', str(len(content.encode('utf-8'))))
            self.end_headers()
            
            # HTML 내용 전송
            self.wfile.write(content.encode('utf-8'))
            
        except FileNotFoundError:
            # index.html 파일이 없는 경우 404 에러
            self.send_error(404, 'File not found: index.html')
        except Exception as e:
            # 기타 오류 처리
            self.send_error(500, f'Internal server error: {str(e)}')


def start_web_server(port=8080):
    """웹서버를 시작하는 함수"""
    try:
        with socketserver.TCPServer(('', port), CustomHTTPRequestHandler) as httpd:
            print(f'웹서버가 포트 {port}에서 시작되었습니다.')
            print(f'브라우저에서 http://localhost:{port}로 접속하세요.')
            print('서버를 종료하려면 Ctrl+C를 누르세요.')
            httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n웹서버를 종료합니다...')
    except Exception as e:
        print(f'서버 시작 중 오류 발생: {e}')


def main():
    """메인 함수"""
    start_web_server()


if __name__ == '__main__':
    main()
