#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버 로그인 크롤링 프로그램
로그인 전후 콘텐츠 차이를 확인하고 로그인 후 콘텐츠를 크롤링합니다.
"""

import time
import os
import random
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class NaverLoginCrawler:
    """네이버 로그인 크롤링 클래스"""
    
    def __init__(self):
        """크롤러 초기화"""
        self.driver = None
        self.wait = None
        self.login_content = []
        self.clipboard = tk.Tk()
        self.clipboard.withdraw()  # tkinter 창을 숨김
    
    def copy_to_clipboard(self, text):
        """클립보드에 텍스트 복사"""
        self.clipboard.clipboard_clear()
        self.clipboard.clipboard_append(text)
        self.clipboard.update()  # 클립보드 업데이트
    
    def setup_driver(self):
        """셀레니움 드라이버 설정"""
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        # chrome_options.add_argument('--disable-javascript')  # JavaScript 비활성화 제거
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            driver_path = os.path.join(current_dir, 'chromedriver.exe')
            
            if os.path.exists(driver_path):
                service = Service(executable_path=driver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                self.driver = webdriver.Chrome(options=chrome_options)
            
            self.wait = WebDriverWait(self.driver, 10)
            
            # 자동화 탐지 우회
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print('Chrome 드라이버 설정 완료')
            
        except Exception as e:
            print(f'드라이버 설정 오류: {e}')
            raise
    
    def check_content_before_login(self):
        """로그인 전 콘텐츠 확인"""
        print('로그인 전 콘텐츠 확인 중...')
        self.driver.get('https://www.naver.com')
        time.sleep(3)
        
        try:
            login_button = self.driver.find_element(By.CLASS_NAME, 'link_login')
            print(f'로그인 버튼 발견: {login_button.text}')
            return True
        except NoSuchElementException:
            print('이미 로그인된 상태입니다.')
            return False
    
    def login_naver(self, user_id, user_pw):
        """네이버 로그인 수행 (클립보드 방식만 사용)"""
        print('네이버 로그인 시도 중... (클립보드 방식)')
        
        # 클립보드 방식만 사용
        return self._try_clipboard_login(user_id, user_pw)
    
    def _try_clipboard_login(self, user_id, user_pw):
        """클립보드 방식으로 로그인 시도"""
        print('클립보드 방식으로 로그인 시도...')
        
        try:
            self.driver.get('https://nid.naver.com/nidlogin.login')
            time.sleep(3)
            
            # 아이디 입력 (클립보드 방식)
            id_input = self.wait.until(
                EC.presence_of_element_located((By.ID, 'id'))
            )
            id_input.click()
            time.sleep(0.5)
            
            # 클립보드에 아이디 복사 후 붙여넣기
            self.copy_to_clipboard(user_id)
            id_input.send_keys(Keys.CONTROL + 'v')
            time.sleep(1)
            
            # 비밀번호 입력 (클립보드 방식)
            pw_input = self.driver.find_element(By.ID, 'pw')
            pw_input.click()
            time.sleep(0.5)
            
            # 클립보드에 비밀번호 복사 후 붙여넣기
            self.copy_to_clipboard(user_pw)
            pw_input.send_keys(Keys.CONTROL + 'v')
            time.sleep(1)
            
            # 로그인 버튼 클릭
            login_button = self.driver.find_element(By.ID, 'log.login')
            login_button.click()
            time.sleep(5)
            
            return self.check_login_success()
                
        except Exception as e:
            print(f'클립보드 로그인 실패: {e}')
            return False
    
    def check_login_success(self):
        """로그인 성공 여부 확인"""
        try:
            current_url = self.driver.current_url
            print(f'현재 URL: {current_url}')
            
            # URL 기반 확인
            if 'naver.com' in current_url and ('login' not in current_url or 'deviceConfirm' in current_url):
                print('URL 기반 로그인 성공 확인!')
                # 새 기기 등록 알림 처리
                self.handle_device_registration()
                return True
            
            # 페이지 요소 기반 확인
            try:
                # 로그아웃 버튼이나 사용자 메뉴가 있는지 확인
                logout_selectors = [
                    '[data-clk="svc.logout"]',
                    '.link_logout',
                    '.btn_logout',
                    '.gnb_my',
                    '.my_service'
                ]
                
                for selector in logout_selectors:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f'요소 기반 로그인 성공 확인: {selector}')
                        self.handle_device_registration()
                        return True
                        
            except Exception:
                pass
            
            # 에러 메시지 확인
            try:
                error_elements = self.driver.find_elements(By.CSS_SELECTOR, '.error_message, .err_msg, .alert')
                if error_elements:
                    for elem in error_elements:
                        if elem.is_displayed():
                            print(f'로그인 에러 메시지: {elem.text}')
            except Exception:
                pass
            
            print('로그인 실패')
            return False
            
        except Exception as e:
            print(f'로그인 상태 확인 중 오류: {e}')
            return False
    
    def handle_device_registration(self):
        """새 기기 등록 알림 처리"""
        print('새 기기 등록 알림 확인 중...')
        
        try:
            # 여러 선택자로 '등록안함' 버튼 찾기
            selectors = [
                "a#new\\.dontsave",  # 직접 ID 선택자
                "span.btn_cancel a#new\\.dontsave",  # 기존 선택자
                "a[href='#'][id='new.dontsave']",  # href와 id 조합
                ".btn_cancel a",  # 클래스 기반
                "a:contains('등록안함')"  # 텍스트 기반 (일부 브라우저에서만 작동)
            ]
            
            for selector in selectors:
                try:
                    print(f"선택자 시도: {selector}")
                    element = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    element.click()
                    print('기기 등록을 거부부했습니다.')
                    time.sleep(3)
                    return
                except TimeoutException:
                    continue
                except Exception as e:
                    print(f"선택자 {selector} 실패: {e}")
                    continue
            
            # JavaScript로 직접 클릭 시도
            try:
                print("JavaScript로 직접 클릭 시도...")
                self.driver.execute_script("document.getElementById('new.dontsave').click();")
                print('JavaScript로 기기 등록을 취소했습니다.')
                time.sleep(3)
                return
            except Exception as e:
                print(f"JavaScript 클릭 실패: {e}")
            
            print("기기 등록 '등록안함' 버튼을 찾을 수 없습니다.")
            
        except Exception as e:
            print(f'기기 등록 처리 중 오류: {e}')
    
    def crawl_login_content(self):
        """로그인 후 콘텐츠 크롤링"""
        print('로그인 후 콘텐츠 크롤링 중...')
        
        try:
            self.driver.get('https://www.naver.com')
            time.sleep(3)
            
            login_contents = []
            
            # 로그인 상태 확인
            login_status_selectors = [
                '[data-clk="svc.logout"]',
                '.link_logout',
                '.btn_logout',
                '.gnb_my',
                '.my_service'
            ]
            
            for selector in login_status_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        login_contents.append(f'로그인 상태 확인: {selector} 발견')
                        break
                except Exception:
                    continue
            
            # 개인화된 콘텐츠 찾기
            personal_content_selectors = [
                '.news_area a',
                '.mail a',
                '.my_service a',
                '.gnb_my a'
            ]
            
            for selector in personal_content_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for elem in elements[:3]:
                            try:
                                text = elem.text.strip()
                                if text and len(text) > 3:
                                    login_contents.append(f'개인화 콘텐츠: {text}')
                                    break
                            except:
                                continue
                except Exception:
                    continue
            
            # 개인화된 링크 찾기
            try:
                all_links = self.driver.find_elements(By.TAG_NAME, 'a')
                personal_keywords = ['내정보', '마이페이지', '로그아웃', '설정', '메일']
                
                for link in all_links[:20]:
                    try:
                        text = link.text.strip()
                        if any(keyword in text for keyword in personal_keywords):
                            if text and len(text) > 1:
                                login_contents.append(f'개인화 링크: {text}')
                    except:
                        continue
                        
            except Exception as e:
                print(f'링크 검색 중 오류: {e}')
            
            self.login_content = login_contents
            print(f'총 {len(login_contents)}개의 로그인 전용 콘텐츠를 발견했습니다.')
            
        except Exception as e:
            print(f'콘텐츠 크롤링 중 오류 발생: {e}')
    
    def crawl_naver_mail_titles(self):
        """네이버 메일 제목 크롤링 (보너스 과제)"""
        print('네이버 메일 제목 크롤링 중...')
        
        try:
            self.driver.get('https://mail.naver.com')
            time.sleep(3)
            
            mail_titles = []
            
            # 메일 제목 선택자들
            mail_title_selectors = [
                '.mail_list .subject a',
                '.mail_item .subject a',
                '.mail_title a',
                '.subject a'
            ]
            
            for selector in mail_title_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for element in elements[:10]:
                            try:
                                title = element.text.strip()
                                # "메일 제목"이라는 텍스트가 포함된 경우 제외
                                if title and len(title) > 2 and title != "메일 제목":
                                    mail_titles.append(title)
                            except:
                                continue
                        break
                except Exception:
                    continue
            
            print(f'총 {len(mail_titles)}개의 메일 제목을 수집했습니다.')
            return mail_titles
            
        except Exception as e:
            print(f'메일 크롤링 중 오류 발생: {e}')
            return []
    
    def display_results(self):
        """크롤링 결과 출력"""
        print('\n=== 크롤링 결과 ===')
        
        if self.login_content:
            print('\n[로그인 후 전용 콘텐츠]')
            for i, content in enumerate(self.login_content, 1):
                print(f'{i}. {content}')
        else:
            print('\n로그인 후 전용 콘텐츠를 찾을 수 없습니다.')
        
        # 보너스 과제: 메일 제목 출력
        mail_titles = self.crawl_naver_mail_titles()
        if mail_titles:
            print('\n[네이버 메일 제목 - 보너스 과제]')
            for i, title in enumerate(mail_titles, 1):
                print(f'{i}. {title}')
        else:
            print('\n메일 제목을 찾을 수 없습니다.')
    
    def close_driver(self):
        """드라이버 종료"""
        if self.driver:
            self.driver.quit()
            print('드라이버가 종료되었습니다.')
        
        # tkinter 클립보드 정리
        if hasattr(self, 'clipboard'):
            self.clipboard.destroy()


def main():
    """메인 함수"""
    print('=' * 50)
    print('네이버 로그인 크롤링 프로그램 시작')
    print('=' * 50)
    
    # 사용자 인증 정보 입력
    print('\n로그인 정보를 입력해주세요:')
    user_id = input('네이버 아이디: ')
    user_pw = input('네이버 비밀번호: ')
    
    print('\n브라우저 설정 중...')
    crawler = NaverLoginCrawler()
    
    try:
        # 드라이버 설정
        crawler.setup_driver()
        
        # 로그인 전 콘텐츠 확인
        print('\n로그인 전 콘텐츠 확인 중...')
        crawler.check_content_before_login()
        
        # 로그인 수행
        print('\n로그인 시도 중...')
        if crawler.login_naver(user_id, user_pw):
            # 로그인 후 콘텐츠 크롤링
            print('\n로그인 후 콘텐츠 크롤링 시작...')
            crawler.crawl_login_content()
            
            # 결과 출력
            crawler.display_results()
        else:
            print('\n로그인에 실패하여 크롤링을 진행할 수 없습니다.')
    
    except KeyboardInterrupt:
        print('\n사용자에 의해 프로그램이 중단되었습니다.')
    
    except Exception as e:
        print(f'\n프로그램 실행 중 오류 발생: {e}')
    
    finally:
        # 드라이버 종료
        print('\n프로그램을 종료합니다...')
        crawler.close_driver()
        print('프로그램이 정상적으로 종료되었습니다.')


if __name__ == '__main__':
    main()
