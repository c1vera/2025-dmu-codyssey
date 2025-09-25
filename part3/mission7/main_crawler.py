#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
통합 웹 크롤링 프로그램
KBS 뉴스, 날씨 정보, 주식 가격 정보를 통합하여 크롤링하는 프로그램
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crawling_KBS import get_kbs_headlines, display_headlines
from crawling_stock import get_stock_prices, display_stock_prices


def main():
    """
    통합 메인 함수
    """
    print('=' * 60)
    print('통합 웹 크롤링 프로그램')
    print('=' * 60)
    print()
    
    while True:
        print('크롤링할 정보를 선택하세요:')
        print('1. KBS 뉴스 헤드라인')
        print('2. 주식 가격 정보')
        print('3. 모든 정보')
        print('4. 종료')
        print()
        
        try:
            choice = input('선택 (1-4): ').strip()
            
            if choice == '1':
                print('\n[KBS 뉴스 헤드라인 크롤링]')
                headlines = get_kbs_headlines()
                display_headlines(headlines)
                
            elif choice == '2':
                print('\n[주식 가격 정보 크롤링]')
                stock_prices = get_stock_prices()
                display_stock_prices(stock_prices)
                
            elif choice == '3':
                print('\n[모든 정보 크롤링]')
                print('\n1. KBS 뉴스 헤드라인:')
                headlines = get_kbs_headlines()
                display_headlines(headlines)
                
                print('\n2. 주식 가격 정보:')
                stock_prices = get_stock_prices()
                display_stock_prices(stock_prices)
                
            elif choice == '4':
                print('프로그램을 종료합니다.')
                break
                
            else:
                print('잘못된 선택입니다. 1-4 중에서 선택해주세요.')
            
            print('\n' + '=' * 60)
            print()
            
        except KeyboardInterrupt:
            print('\n\n프로그램이 사용자에 의해 중단되었습니다.')
            break
        except Exception as e:
            print(f'\n오류가 발생했습니다: {e}')
            print()


if __name__ == '__main__':
    main()
