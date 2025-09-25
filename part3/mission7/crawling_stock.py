#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
주식 가격 정보 크롤링 프로그램
네이버 금융에서 주요 주식 가격 정보를 가져와서 출력하는 프로그램
"""

import requests
from bs4 import BeautifulSoup
import sys


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
    메인 함수
    """
    print('주식 가격 정보 크롤링을 시작합니다...')
    
    # 주식 가격 정보 가져오기
    stock_prices = get_stock_prices()
    
    # 주식 가격 정보 출력
    display_stock_prices(stock_prices)
    
    return stock_prices


if __name__ == '__main__':
    main()
