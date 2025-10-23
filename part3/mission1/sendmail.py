#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gmail SMTP 메일 전송 프로그램
Python 기본 라이브러리만 사용하여 Gmail을 통해 메일을 전송합니다.
"""

import smtplib
import ssl
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
        print('2. 첨부파일이 있는 메일 (보너스 과제)')
        
        choice = input('선택 (1 또는 2): ')
        
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
        else:
            print('잘못된 선택입니다. 1 또는 2를 입력해주세요.')
    
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
