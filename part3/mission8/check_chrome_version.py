#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chrome 브라우저 버전 확인 스크립트
ChromeDriver 다운로드 시 필요한 Chrome 버전을 확인합니다.
"""

import subprocess
import sys
import os


def get_chrome_version():
    """Chrome 브라우저 버전 확인"""
    try:
        # Windows 환경에서 Chrome 버전 확인
        if sys.platform.startswith('win'):
            # 레지스트리를 통한 Chrome 버전 확인
            try:
                result = subprocess.run([
                    'reg', 'query', 
                    'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon',
                    '/v', 'version'
                ], capture_output=True, text=True, check=True)
                
                # 버전 정보 추출
                for line in result.stdout.split('\n'):
                    if 'version' in line.lower():
                        version = line.split()[-1]
                        print(f'Chrome 버전: {version}')
                        return version
                        
            except subprocess.CalledProcessError:
                print('레지스트리에서 Chrome 버전을 찾을 수 없습니다.')
        
        # 대안 방법: Chrome 실행 파일에서 버전 확인
        chrome_paths = [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            r'C:\Users\%USERNAME%\AppData\Local\Google\Chrome\Application\chrome.exe'
        ]
        
        for chrome_path in chrome_paths:
            if os.path.exists(chrome_path):
                try:
                    result = subprocess.run([
                        chrome_path, '--version'
                    ], capture_output=True, text=True, check=True)
                    
                    version = result.stdout.strip().split()[-1]
                    print(f'Chrome 버전: {version}')
                    return version
                    
                except subprocess.CalledProcessError:
                    continue
        
        print('Chrome 버전을 확인할 수 없습니다.')
        print('수동으로 확인하는 방법:')
        print('1. Chrome 브라우저 열기')
        print('2. 주소창에 chrome://version/ 입력')
        print('3. 버전 정보 확인')
        
        return None
        
    except Exception as e:
        print(f'Chrome 버전 확인 중 오류 발생: {e}')
        return None


def get_chromedriver_download_url(version):
    """ChromeDriver 다운로드 URL 생성"""
    if not version:
        return None
    
    # 메이저 버전만 추출 (예: 131.0.6778.108 -> 131)
    major_version = version.split('.')[0]
    
    # ChromeDriver 다운로드 URL
    base_url = f'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}'
    
    print(f'\nChromeDriver 다운로드 정보:')
    print(f'Chrome 버전: {version}')
    print(f'메이저 버전: {major_version}')
    print(f'다운로드 URL: https://chromedriver.chromium.org/downloads')
    print(f'또는: https://googlechromelabs.github.io/chrome-for-testing/')
    
    return base_url


def main():
    """메인 함수"""
    print('Chrome 버전 확인 중...')
    
    version = get_chrome_version()
    
    if version:
        get_chromedriver_download_url(version)
        
        print(f'\n설치 방법:')
        print(f'1. 위 URL에서 Chrome 버전 {version}에 맞는 ChromeDriver 다운로드')
        print(f'2. 다운로드한 chromedriver.exe를 crawling_KBS.py와 같은 폴더에 저장')
        print(f'3. python crawling_KBS.py 실행')
    else:
        print('\nChrome이 설치되어 있지 않거나 버전을 확인할 수 없습니다.')
        print('Chrome 브라우저를 설치한 후 다시 실행해주세요.')


if __name__ == '__main__':
    main()
