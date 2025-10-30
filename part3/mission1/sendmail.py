#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 메일 전송 프로그램

요구사항 요약:
- HTML 형식으로 메일 전송 지원
- 수신자 CSV 목록(`mail_target_list.csv`, 헤더: 이름, 이메일) 읽기
- 전송 방식 2가지 제공: 개별 전송, 일괄 전송
- Python 표준 라이브러리만 사용 (smtplib, email, csv 등)

권장 기본값:
- 전송 방식 기본값은 개별 전송 (프라이버시/수신 성공률 고려)

보너스:
- 네이버 SMTP(smtp.naver.com:587) 지원 (앱 비밀번호/IMAP·SMTP 사용 설정 필요)
"""

import smtplib
import ssl
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os


class GmailSender:
    """Gmail 메일 전송 클래스"""
    
    def __init__(self):
        """Gmail 전송자 초기화"""
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.sender_email = ''
        self.sender_password = ''
        self.receiver_email = ''
    
    def set_naver_config(self):
        """네이버 메일 설정 (보너스 과제).

        사전 준비:
        - 네이버 계정 보안 설정에서 2단계 인증 및 앱 비밀번호 생성
        - 메일 환경설정에서 IMAP/SMTP 사용 허용
        - 보내는 주소는 네이버 계정 이메일을 사용
        """
        self.smtp_server = 'smtp.naver.com'
        self.smtp_port = 587
    
    def set_email_config(self, sender_email, sender_password, receiver_email):
        """이메일 설정"""
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_email = receiver_email
    
    def send_simple_email(self, subject, body):
        """간단한 텍스트 메일 전송"""
        try:
            # MIMEText 객체 생성
            message = MIMEText(body, 'plain', 'utf-8')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = self.receiver_email
            
            # SSL 컨텍스트 생성
            context = ssl.create_default_context()
            
            # SMTP 서버에 연결 및 메일 전송
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.receiver_email, message.as_string())
            
            print('메일 전송 성공!')
            return True
            
        except smtplib.SMTPAuthenticationError:
            print('인증 오류: 이메일 주소나 앱 비밀번호를 확인해주세요.')
            return False
        except smtplib.SMTPRecipientsRefused:
            print('수신자 오류: 수신자 이메일 주소를 확인해주세요.')
            return False
        except smtplib.SMTPServerDisconnected:
            print('서버 연결 오류: SMTP 서버와의 연결이 끊어졌습니다.')
            return False
        except smtplib.SMTPException as e:
            print(f'SMTP 오류: {e}')
            return False
        except Exception as e:
            print(f'예상치 못한 오류: {e}')
            return False
    
    def send_html_email(self, subject, html_body, receiver_email=None):
        """HTML 형식의 메일 전송"""
        try:
            # 수신자 이메일 설정
            target_email = receiver_email if receiver_email else self.receiver_email
            
            # MIMEText 객체 생성 (HTML 형식)
            message = MIMEText(html_body, 'html', 'utf-8')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = target_email
            
            # SSL 컨텍스트 생성
            context = ssl.create_default_context()
            
            # SMTP 서버에 연결 및 메일 전송
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, target_email, message.as_string())
            
            print(f'HTML 메일 전송 성공! 수신자: {target_email}')
            return True
            
        except smtplib.SMTPAuthenticationError:
            print('인증 오류: 이메일 주소나 앱 비밀번호를 확인해주세요.')
            return False
        except smtplib.SMTPRecipientsRefused:
            print('수신자 오류: 수신자 이메일 주소를 확인해주세요.')
            return False
        except smtplib.SMTPServerDisconnected:
            print('서버 연결 오류: SMTP 서버와의 연결이 끊어졌습니다.')
            return False
        except smtplib.SMTPException as e:
            print(f'SMTP 오류: {e}')
            return False
        except Exception as e:
            print(f'예상치 못한 오류: {e}')
            return False
    
    def read_csv_recipients(self, csv_file_path):
        """CSV 파일에서 수신자 목록 읽기 (UTF-8 BOM 대응, 헤더 유연 처리)."""
        recipients = []
        try:
            with open(csv_file_path, 'r', encoding='utf-8-sig', newline='') as file:
                csv_reader = csv.DictReader(file)
                if not csv_reader.fieldnames:
                    print('CSV 헤더를 찾을 수 없습니다. "이름,이메일" 형식을 확인하세요.')
                    return []

                # 헤더 정규화: 소문자/공백 제거
                normalized = [h.strip().lower() for h in csv_reader.fieldnames]

                # 한국어/영어 헤더 모두 허용
                try:
                    name_key = csv_reader.fieldnames[normalized.index('이름')] if '이름' in normalized else csv_reader.fieldnames[normalized.index('name')]
                except ValueError:
                    print('CSV에 "이름" 또는 "name" 헤더가 없습니다.')
                    return []

                try:
                    email_key = csv_reader.fieldnames[normalized.index('이메일')] if '이메일' in normalized else csv_reader.fieldnames[normalized.index('email')]
                except ValueError:
                    print('CSV에 "이메일" 또는 "email" 헤더가 없습니다.')
                    return []

                for row in csv_reader:
                    name_value = (row.get(name_key) or '').strip()
                    email_value = (row.get(email_key) or '').strip()
                    if not email_value:
                        continue
                    recipients.append({'name': name_value, 'email': email_value})

            print(f'CSV 파일에서 {len(recipients)}명의 수신자를 읽었습니다.')
            return recipients
        except FileNotFoundError:
            print(f'CSV 파일을 찾을 수 없습니다: {csv_file_path}')
            return []
        except Exception as e:
            print(f'CSV 파일 읽기 오류: {e}')
            return []
    
    def send_html_email_to_multiple_recipients(self, subject, html_body, csv_file_path, method='individual'):
        """CSV 파일의 수신자들에게 HTML 메일 전송"""
        recipients = self.read_csv_recipients(csv_file_path)
        if not recipients:
            return False
        
        success_count = 0
        
        if method == 'individual':
            # 한 명씩 개별 전송
            print('개별 전송 방식으로 메일을 보냅니다...')
            for recipient in recipients:
                print(f'전송 중: {recipient["name"]} ({recipient["email"]})')
                # {name} 플레이스홀더 개인화 처리 (없으면 그대로 사용)
                personalized_html = html_body.replace('{name}', recipient['name'] or '')
                if self.send_html_email(subject, personalized_html, recipient['email']):
                    success_count += 1
                else:
                    print(f'전송 실패: {recipient["name"]} ({recipient["email"]})')
        
        elif method == 'bulk':
            # 여러 명에게 한 번에 전송
            print('일괄 전송 방식으로 메일을 보냅니다...')
            try:
                # MIMEText 객체 생성 (HTML 형식)
                message = MIMEText(html_body, 'html', 'utf-8')
                message['Subject'] = subject
                message['From'] = self.sender_email
                
                # 수신자 이메일 목록 생성
                recipient_emails = [recipient['email'] for recipient in recipients]
                message['To'] = ', '.join(recipient_emails)
                
                # SSL 컨텍스트 생성
                context = ssl.create_default_context()
                
                # SMTP 서버에 연결 및 메일 전송
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls(context=context)
                    server.login(self.sender_email, self.sender_password)
                    server.sendmail(self.sender_email, recipient_emails, message.as_string())
                
                success_count = len(recipients)
                print(f'일괄 전송 성공! {success_count}명에게 전송 완료')
                
            except Exception as e:
                print(f'일괄 전송 오류: {e}')
                return False
        
        print(f'전송 완료: {success_count}/{len(recipients)}명')
        return success_count > 0


def try_read_text(path):
    """경로에서 텍스트를 읽어 반환. 실패 시 빈 문자열 반환."""
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception:
        return ''


def build_default_story_html(name=''):
    """기본 스토리 HTML 템플릿을 생성한다. {name} 치환을 지원한다."""
    safe_name = name or ''
    return (
        '<!doctype html>'
        '<html lang="en">'
        '<head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Message from Mars</title>'
        '<style>body{font-family:Arial,Helvetica,sans-serif;line-height:1.6;color:#222;padding:24px;}'
        '.box{max-width:640px;margin:0 auto;border:1px solid #eee;border-radius:8px;padding:24px;}'
        'h1{font-size:20px;margin:0 0 8px;} p{margin:12px 0;}</style>'
        '</head><body>'
        '<div class="box">'
        f'<h1>To {safe_name if safe_name else "Team"},</h1>'
        '<p>Dr. Han, we received your message. We could not understand the situation at first; '
        'we froze, then cried as we hugged each other. We are so grateful that you are alive. '
        'We will do our best too. Just in case your condition is not good, we are sending this '
        'message in English.</p>'
        '<p>Across the silence of Mars, being connected to Earth is itself a blessing. We will '
        'share your message with those who can help most effectively, and we will continue to '
        'reach out until you are safely home.</p>'
        '<p>With hope,<br>The Support Team</p>'
        '</div></body></html>'
    )
    
    def send_email_with_attachment(self, subject, body, attachment_path):
        """첨부파일이 있는 메일 전송 (보너스 과제)"""
        try:
            # MIMEMultipart 객체 생성
            message = MIMEMultipart()
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = self.receiver_email
            
            # 메일 본문 추가
            message.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # 첨부파일 추가
            if os.path.exists(attachment_path):
                with open(attachment_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                # Base64 인코딩
                encoders.encode_base64(part)
                
                # 첨부파일 헤더 설정
                filename = os.path.basename(attachment_path)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {filename}'
                )
                
                message.attach(part)
                print(f'첨부파일 추가: {filename}')
            else:
                print(f'첨부파일을 찾을 수 없습니다: {attachment_path}')
                return False
            
            # SSL 컨텍스트 생성
            context = ssl.create_default_context()
            
            # SMTP 서버에 연결 및 메일 전송
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.receiver_email, message.as_string())
            
            print('첨부파일이 포함된 메일 전송 성공!')
            return True
            
        except smtplib.SMTPAuthenticationError:
            print('인증 오류: 이메일 주소나 앱 비밀번호를 확인해주세요.')
            return False
        except smtplib.SMTPRecipientsRefused:
            print('수신자 오류: 수신자 이메일 주소를 확인해주세요.')
            return False
        except smtplib.SMTPServerDisconnected:
            print('서버 연결 오류: SMTP 서버와의 연결이 끊어졌습니다.')
            return False
        except smtplib.SMTPException as e:
            print(f'SMTP 오류: {e}')
            return False
        except FileNotFoundError:
            print(f'파일을 찾을 수 없습니다: {attachment_path}')
            return False
        except Exception as e:
            print(f'예상치 못한 오류: {e}')
            return False


def get_user_input():
    """사용자로부터 이메일 정보 입력받기"""
    print('=' * 50)
    print('Gmail 메일 전송 프로그램')
    print('=' * 50)
    print()
    print('주의사항:')
    print('1. Gmail 계정에서 2단계 인증을 활성화해야 합니다.')
    print('2. 앱 비밀번호를 생성하여 사용해야 합니다.')
    print('3. 일반 비밀번호는 사용할 수 없습니다.')
    print()
    
    sender_email = input('보내는 사람 Gmail 주소: ')
    sender_password = input('앱 비밀번호 (16자리): ')
    receiver_email = input('받는 사람 이메일 주소: ')
    
    return sender_email, sender_password, receiver_email


def main():
    """메인 함수"""
    try:
        # 사용자 입력 받기
        sender_email, sender_password, receiver_email = get_user_input()
        
        # Gmail 전송자 객체 생성
        gmail_sender = GmailSender()
        gmail_sender.set_email_config(sender_email, sender_password, receiver_email)
        
        print()
        print('메일 전송 옵션을 선택하세요:')
        print('1. 간단한 텍스트 메일')
        print('2. HTML 형식 메일')
        print('3. CSV 파일을 통한 다중 수신자 HTML 메일')
        print('4. 첨부파일이 있는 메일 (보너스 과제)')
        print('5. 네이버 메일을 통한 전송 (보너스 과제)')
        
        choice = input('선택 (1-5): ')
        
        if choice == '1':
            # 간단한 텍스트 메일
            subject = input('메일 제목: ')
            body = input('메일 내용: ')
            
            print()
            print('메일 전송 중...')
            success = gmail_sender.send_simple_email(subject, body)
            
            if success:
                print('메일이 성공적으로 전송되었습니다!')
            else:
                print('메일 전송에 실패했습니다.')
        
        elif choice == '2':
            # HTML 형식 메일
            subject = input('메일 제목: ')
            html_path = input('HTML 파일 경로(선택, 엔터 시 직접 입력): ').strip()
            if html_path:
                html_body = try_read_text(html_path) or build_default_story_html()
            else:
                print('HTML 메일 내용을 입력하세요 (HTML 태그 사용 가능):')
                html_body = input()
                if not html_body.strip():
                    html_body = build_default_story_html()
            
            print()
            print('HTML 메일 전송 중...')
            success = gmail_sender.send_html_email(subject, html_body)
            
            if success:
                print('HTML 메일이 성공적으로 전송되었습니다!')
            else:
                print('HTML 메일 전송에 실패했습니다.')
        
        elif choice == '3':
            # CSV 파일을 통한 다중 수신자 HTML 메일
            subject = input('메일 제목: ')
            html_path = input('HTML 파일 경로(선택, 엔터 시 직접 입력/기본 템플릿 사용): ').strip()
            if html_path:
                html_body = try_read_text(html_path) or build_default_story_html()
            else:
                print('HTML 메일 내용을 입력하세요 (HTML 태그 사용 가능, 비우면 기본 템플릿):')
                html_body = input()
                if not html_body.strip():
                    html_body = build_default_story_html()
            
            csv_file_path = input('CSV 파일 경로 (기본값: mail_target_list.csv): ')
            if not csv_file_path:
                csv_file_path = 'mail_target_list.csv'
            
            print()
            print('전송 방식을 선택하세요:')
            print('1. 개별 전송 (한 명씩) [권장]')
            print('2. 일괄 전송 (여러 명에게 한 번에)')
            method_choice = input('선택 (1 또는 2, 엔터 시 1): ').strip()

            method = 'individual' if method_choice in ('', '1') else 'bulk'
            
            print()
            print('다중 수신자 HTML 메일 전송 중...')
            success = gmail_sender.send_html_email_to_multiple_recipients(
                subject, html_body, csv_file_path, method
            )
            
            if success:
                print('다중 수신자 HTML 메일이 성공적으로 전송되었습니다!')
            else:
                print('다중 수신자 HTML 메일 전송에 실패했습니다.')
        
        elif choice == '4':
            # 첨부파일이 있는 메일
            subject = input('메일 제목: ')
            body = input('메일 내용: ')
            attachment_path = input('첨부파일 경로: ')
            
            print()
            print('첨부파일이 포함된 메일 전송 중...')
            success = gmail_sender.send_email_with_attachment(subject, body, attachment_path)
            
            if success:
                print('첨부파일이 포함된 메일이 성공적으로 전송되었습니다!')
            else:
                print('메일 전송에 실패했습니다.')
        
        elif choice == '5':
            # 네이버 메일을 통한 전송 (보너스 과제)
            print('네이버 메일을 통한 전송을 시도합니다.')
            print('- 네이버 보안 설정에서 2단계 인증과 앱 비밀번호를 사용하세요.')
            print('- 메일 환경설정에서 IMAP/SMTP 사용을 허용해야 합니다.')
            print('- 보내는 주소는 반드시 네이버 계정 이메일이어야 합니다.')
            gmail_sender.set_naver_config()

            print()
            print('전송 모드를 선택하세요:')
            print('1. 단일 HTML 전송 (현재 입력한 수신자에게)')
            print('2. CSV 기반 다중 HTML 전송 (mail_target_list.csv 등)')
            naver_mode = input('선택 (1 또는 2, 엔터 시 1): ').strip() or '1'

            if naver_mode == '2':
                # CSV 다중 전송 (네이버)
                subject = input('메일 제목: ')
                html_path = input('HTML 파일 경로(선택, 엔터 시 직접 입력/기본 템플릿 사용): ').strip()
                if html_path:
                    html_body = try_read_text(html_path) or build_default_story_html()
                else:
                    print('HTML 메일 내용을 입력하세요 (HTML 태그 사용 가능, 비우면 기본 템플릿):')
                    html_body = input()
                    if not html_body.strip():
                        html_body = build_default_story_html()

                csv_file_path = input('CSV 파일 경로 (기본값: mail_target_list.csv): ').strip()
                if not csv_file_path:
                    csv_file_path = 'mail_target_list.csv'

                print('전송 방식을 선택하세요:')
                print('1. 개별 전송 (한 명씩) [권장]')
                print('2. 일괄 전송 (여러 명에게 한 번에)')
                method_choice = input('선택 (1 또는 2, 엔터 시 1): ').strip()
                method = 'individual' if method_choice in ('', '1') else 'bulk'

                print()
                print('네이버 메일(다중 수신자) 전송 중...')
                success = gmail_sender.send_html_email_to_multiple_recipients(
                    subject, html_body, csv_file_path, method
                )

                if success:
                    print('네이버 메일(다중) 전송이 성공적으로 완료되었습니다!')
                else:
                    print('네이버 메일(다중) 전송에 실패했습니다.')
            else:
                # 단일 전송 (네이버)
                subject = input('메일 제목: ')
                html_path = input('HTML 파일 경로(선택, 엔터 시 직접 입력): ').strip()
                if html_path:
                    html_body = try_read_text(html_path) or build_default_story_html()
                else:
                    print('HTML 메일 내용을 입력하세요 (HTML 태그 사용 가능):')
                    html_body = input()
                    if not html_body.strip():
                        html_body = build_default_story_html()

                print()
                print('네이버 메일 전송 중...')
                success = gmail_sender.send_html_email(subject, html_body)

                if success:
                    print('네이버 메일이 성공적으로 전송되었습니다!')
                else:
                    print('네이버 메일 전송에 실패했습니다.')
        
        else:
            print('잘못된 선택입니다. 1-5 중에서 선택해주세요.')
    
    except KeyboardInterrupt:
        print()
        print('사용자에 의해 프로그램이 중단되었습니다.')
    
    except Exception as e:
        print(f'프로그램 실행 중 오류 발생: {e}')
    
    finally:
        print()
        print('프로그램을 종료합니다.')


if __name__ == '__main__':
    main()
