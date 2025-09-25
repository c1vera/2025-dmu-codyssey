#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
통합 웹 크롤링 프로그램
KBS 뉴스, 날씨 정보, 주식 가격 정보를 통합하여 크롤링하는 프로그램
"""

import requests
from bs4 import BeautifulSoup
import sys


def get_kbs_headlines():
    """
    KBS 뉴스 웹사이트에서 주요 헤드라인을 가져오는 함수
    
    Returns:
        list: 헤드라인 뉴스 리스트
    """
    try:
        # KBS 뉴스 메인 페이지 URL (실제 뉴스 페이지)
        url = 'http://news.kbs.co.kr/news/pc/main/main.html'
        
        # User-Agent 헤더 설정 (웹사이트 접근을 위한 기본 설정)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 웹페이지 요청
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # HTTP 오류가 있으면 예외 발생
        
        # HTML 파싱
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 헤드라인 뉴스 추출
        headlines = []
        
        # 모든 링크에서 뉴스 제목 추출
        links = soup.find_all('a', href=True)
        
        for link in links:
            text = link.get_text(strip=True)
            href = link.get('href', '')
            
            # 뉴스 제목 조건 확인
            if (text and 
                len(text) > 10 and 
                len(text) < 100 and
                not text.startswith('KBS') and
                not text.startswith('마이페이지') and
                not text.startswith('English') and
                not text.startswith('재난포털') and
                not text.startswith('06:') and
                not text.startswith('07:') and
                not text.startswith('09:') and
                not text.startswith('12:') and
                not text.startswith('22:') and
                not text.startswith('10:') and
                not text.startswith('18:') and
                not text.startswith('특파원 보고') and
                not text.startswith('경제콘서트')):
                
                # 뉴스 관련 키워드가 포함된 링크만 선택
                news_keywords = ['뉴스', '기자', '보도', '발생', '확인', '발표', '단독', '법원', '정부', '국회', '대통령', '조사', '수사', '재판', '혐의', '주가', '코인', '편입', '구속', '기소']
                if any(keyword in text for keyword in news_keywords):
                    headlines.append(text)
        
        # 중복 제거 및 최대 10개로 제한
        headlines = list(dict.fromkeys(headlines))[:10]
        
        # 디버깅을 위한 출력
        if not headlines:
            print("디버깅: 링크 개수:", len(links))
            sample_links = [link.get_text(strip=True) for link in links[:20] if link.get_text(strip=True)]
            print("샘플 링크:", sample_links)
        
        return headlines
        
    except requests.exceptions.RequestException as e:
        print(f'웹페이지 요청 중 오류 발생: {e}')
        return []
    except Exception as e:
        print(f'크롤링 중 오류 발생: {e}')
        return []



def get_stock_prices():
    """
    네이버 금융에서 주요 주식 가격 정보를 가져오는 함수
    
    Returns:
        list: 주식 가격 정보 리스트
    """
    try:
        # 네이버 금융 메인 페이지 URL
        url = 'https://finance.naver.com/sise/sise_market_sum.naver'
        
        # User-Agent 헤더 설정
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 웹페이지 요청
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # HTML 파싱
        soup = BeautifulSoup(response.content, 'html.parser')
        
        stock_prices = []
        
        # 주식 테이블에서 정보 추출
        try:
            # 주식 테이블 찾기
            table = soup.find('table', class_='type_2')
            if table:
                rows = table.find_all('tr')[1:11]  # 헤더 제외하고 상위 10개
                
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 4:
                        try:
                            # 종목명
                            name_cell = cells[1]
                            name_link = name_cell.find('a')
                            if name_link:
                                name = name_link.get_text(strip=True)
                            else:
                                name = name_cell.get_text(strip=True)
                            
                            # 현재가
                            price = cells[2].get_text(strip=True)
                            
                            # 등락률
                            change_rate = cells[4].get_text(strip=True)
                            
                            # 거래량
                            volume = cells[6].get_text(strip=True)
                            
                            if name and price:
                                stock_info = {
                                    'name': name,
                                    'price': price,
                                    'change_rate': change_rate,
                                    'volume': volume
                                }
                                stock_prices.append(stock_info)
                        
                        except Exception as e:
                            continue
            
        except Exception as e:
            print(f'주식 테이블 파싱 중 오류: {e}')
        
        # 대체 방법으로 주식 정보 찾기
        if not stock_prices:
            # 링크에서 주식 정보 추출
            links = soup.find_all('a', href=True)
            for link in links:
                href = link.get('href', '')
                if '/item/main.naver?code=' in href:
                    name = link.get_text(strip=True)
                    if name and len(name) < 20:
                        # 주변 텍스트에서 가격 정보 찾기
                        parent = link.parent
                        if parent:
                            text = parent.get_text(strip=True)
                            parts = text.split()
                            for part in parts:
                                if ',' in part and part.replace(',', '').replace('+', '').replace('-', '').isdigit():
                                    stock_info = {
                                        'name': name,
                                        'price': part,
                                        'change_rate': '',
                                        'volume': ''
                                    }
                                    stock_prices.append(stock_info)
                                    break
        
        return stock_prices[:10]  # 최대 10개로 제한
        
    except requests.exceptions.RequestException as e:
        print(f'웹페이지 요청 중 오류 발생: {e}')
        return []
    except Exception as e:
        print(f'주식 정보 크롤링 중 오류 발생: {e}')
        return []


def display_headlines(headlines):
    """
    헤드라인을 화면에 출력하는 함수
    
    Args:
        headlines (list): 출력할 헤드라인 리스트
    """
    if not headlines:
        print('헤드라인을 가져올 수 없습니다.')
        return
    
    print('=' * 60)
    print('KBS 주요 헤드라인 뉴스')
    print('=' * 60)
    
    for i, headline in enumerate(headlines, 1):
        print(f'{i:2d}. {headline}')
    
    print('=' * 60)
    print(f'총 {len(headlines)}개의 헤드라인을 가져왔습니다.')



def display_stock_prices(stock_prices):
    """
    주식 가격 정보를 화면에 출력하는 함수
    
    Args:
        stock_prices (list): 출력할 주식 가격 정보 리스트
    """
    if not stock_prices:
        print('주식 가격 정보를 가져올 수 없습니다.')
        return
    
    print('=' * 80)
    print('주요 주식 가격 정보')
    print('=' * 80)
    print(f'{"순위":<4} {"종목명":<15} {"현재가":<12} {"등락률":<10} {"거래량":<15}')
    print('-' * 80)
    
    for i, stock in enumerate(stock_prices, 1):
        name = stock.get('name', '')[:14]
        price = stock.get('price', '')
        change_rate = stock.get('change_rate', '')
        volume = stock.get('volume', '')
        
        print(f'{i:<4} {name:<15} {price:<12} {change_rate:<10} {volume:<15}')
    
    print('=' * 80)
    print(f'총 {len(stock_prices)}개의 주식 정보를 가져왔습니다.')


def main():
    """
    통합 메인 함수 - KBS 뉴스, 날씨, 주식 정보를 모두 표시
    """
    print('=' * 80)
    print('KBS 뉴스, 주식 가격 정보를 가져옵니다')
    print('=' * 80)
    print()
    
    # 1. KBS 뉴스 헤드라인
    print('📰 KBS 뉴스 헤드라인 크롤링 중...')
    headlines = get_kbs_headlines()
    display_headlines(headlines)
    print()
    
     
    # 3. 주식 가격 정보
    print('📈 주식 가격 정보 크롤링 중...')
    stock_prices = get_stock_prices()
    display_stock_prices(stock_prices)
    print()
    
    
    return {
        'headlines': headlines,
        'stocks': stock_prices
    }


if __name__ == '__main__':
    main()
