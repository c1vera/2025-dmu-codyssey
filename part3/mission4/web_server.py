

import http.server
import socketserver
import datetime
import os
import socket


def get_location_info(ip_address):
    """IP 주소를 기반으로 위치 정보를 조회하는 함수"""
    try:
        # 로컬 IP 주소 처리
        if ip_address in ['127.0.0.1', 'localhost', '::1']:
            return {
                'country': '대한민국',
                'city': '서울',
                'region': '서울특별시',
                'isp': '로컬호스트',
                'type': '로컬 접속'
            }
        
        # 사설 IP 대역 처리
        if ip_address.startswith('192.168.') or ip_address.startswith('10.') or ip_address.startswith('172.'):
            return {
                'country': '대한민국',
                'city': '사설 네트워크',
                'region': '내부 네트워크',
                'isp': '사설 IP',
                'type': '내부 네트워크'
            }
        
        # 간단한 IP 주소 분류 (실제로는 더 정교한 데이터베이스가 필요)
        ip_parts = ip_address.split('.')
        if len(ip_parts) == 4:
            first_octet = int(ip_parts[0])
            
            # 주요 국가별 IP 대역 분류 (간단한 예시)
            if 1 <= first_octet <= 14:
                return {
                    'country': '미국',
                    'city': '미국 서부',
                    'region': '캘리포니아',
                    'isp': '미국 ISP',
                    'type': '해외 접속'
                }
            elif 15 <= first_octet <= 31:
                return {
                    'country': '미국',
                    'city': '미국 동부',
                    'region': '뉴욕',
                    'isp': '미국 ISP',
                    'type': '해외 접속'
                }
            elif 32 <= first_octet <= 47:
                return {
                    'country': '중국',
                    'city': '베이징',
                    'region': '베이징시',
                    'isp': '중국 ISP',
                    'type': '해외 접속'
                }
            elif 48 <= first_octet <= 63:
                return {
                    'country': '일본',
                    'city': '도쿄',
                    'region': '도쿄도',
                    'isp': '일본 ISP',
                    'type': '해외 접속'
                }
            elif 64 <= first_octet <= 79:
                return {
                    'country': '독일',
                    'city': '베를린',
                    'region': '독일',
                    'isp': '독일 ISP',
                    'type': '해외 접속'
                }
            elif 80 <= first_octet <= 95:
                return {
                    'country': '영국',
                    'city': '런던',
                    'region': '잉글랜드',
                    'isp': '영국 ISP',
                    'type': '해외 접속'
                }
            elif 96 <= first_octet <= 111:
                return {
                    'country': '프랑스',
                    'city': '파리',
                    'region': '일드프랑스',
                    'isp': '프랑스 ISP',
                    'type': '해외 접속'
                }
            elif 112 <= first_octet <= 127:
                return {
                    'country': '러시아',
                    'city': '모스크바',
                    'region': '모스크바',
                    'isp': '러시아 ISP',
                    'type': '해외 접속'
                }
            elif 128 <= first_octet <= 143:
                return {
                    'country': '대한민국',
                    'city': '서울',
                    'region': '서울특별시',
                    'isp': '한국 ISP',
                    'type': '국내 접속'
                }
            elif 144 <= first_octet <= 159:
                return {
                    'country': '대한민국',
                    'city': '부산',
                    'region': '부산광역시',
                    'isp': '한국 ISP',
                    'type': '국내 접속'
                }
            elif 160 <= first_octet <= 175:
                return {
                    'country': '대한민국',
                    'city': '대구',
                    'region': '대구광역시',
                    'isp': '한국 ISP',
                    'type': '국내 접속'
                }
            elif 176 <= first_octet <= 191:
                return {
                    'country': '대한민국',
                    'city': '인천',
                    'region': '인천광역시',
                    'isp': '한국 ISP',
                    'type': '국내 접속'
                }
            elif 192 <= first_octet <= 207:
                return {
                    'country': '대한민국',
                    'city': '광주',
                    'region': '광주광역시',
                    'isp': '한국 ISP',
                    'type': '국내 접속'
                }
            elif 208 <= first_octet <= 223:
                return {
                    'country': '대한민국',
                    'city': '대전',
                    'region': '대전광역시',
                    'isp': '한국 ISP',
                    'type': '국내 접속'
                }
            elif 224 <= first_octet <= 239:
                return {
                    'country': '대한민국',
                    'city': '울산',
                    'region': '울산광역시',
                    'isp': '한국 ISP',
                    'type': '국내 접속'
                }
            else:
                return {
                    'country': '알 수 없음',
                    'city': '알 수 없음',
                    'region': '알 수 없음',
                    'isp': '알 수 없음',
                    'type': '알 수 없는 접속'
                }
        
        return {
            'country': '알 수 없음',
            'city': '알 수 없음',
            'region': '알 수 없음',
            'isp': '알 수 없음',
            'type': '알 수 없는 접속'
        }
        
    except Exception as e:
        return {
            'country': '오류',
            'city': '오류',
            'region': '오류',
            'isp': '오류',
            'type': f'위치 조회 실패: {str(e)}'
        }


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 접속 시간과 IP 주소 로깅
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_ip = self.client_address[0]
        
        # 위치 정보 조회
        location_info = get_location_info(client_ip)
        
        # 상세 로그 출력
        print(f'접속 시간: {current_time}, IP 주소: {client_ip}')
        print(f'위치 정보: {location_info["country"]} - {location_info["city"]} ({location_info["type"]})')
        print(f'ISP: {location_info["isp"]}')
        print('-' * 50)
        
        # index.html 파일이 요청된 경우
        if self.path == '/' or self.path == '/index.html':
            self.serve_index_html()
        else:
            # 다른 파일 요청에 대한 기본 처리
            super().do_GET()
    
    def serve_index_html(self):
        try:
            # 위치 정보 조회
            client_ip = self.client_address[0]
            location_info = get_location_info(client_ip)
            
            # index.html 파일 읽기
            with open('index.html', 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 위치 정보를 HTML에 삽입
            location_html = f'''
            <div class="location-info">
                <h2>🌍 접속자 위치 정보</h2>
                <div class="location-details">
                    <p><strong>IP 주소:</strong> {client_ip}</p>
                    <p><strong>국가:</strong> {location_info['country']}</p>
                    <p><strong>도시:</strong> {location_info['city']}</p>
                    <p><strong>지역:</strong> {location_info['region']}</p>
                    <p><strong>ISP:</strong> {location_info['isp']}</p>
                    <p><strong>접속 유형:</strong> {location_info['type']}</p>
                </div>
            </div>
            '''
            
            # HTML 내용에 위치 정보 삽입
            content = content.replace('<!-- LOCATION_INFO_PLACEHOLDER -->', location_html)
            
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
