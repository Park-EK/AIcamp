import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import random

# 데이터 디렉토리 경로
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

# 샘플 데이터 생성 함수
def generate_sample_data():
    """
    샘플 데이터를 생성하는 함수
    """
    try:
        # 데이터 디렉토리 생성
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        # 반도체 판매 데이터 생성
        companies = ['삼성전자', 'SK하이닉스', 'TSMC', 'Intel', 'Micron']
        models = ['DRAM', 'NAND', 'SSD', 'CPU']
        years = [2020, 2021, 2022, 2023, 2024, 2025]
        
        sales_data = []
        
        for year in years:
            for company in companies:
                for model in models:
                    # 2024년과 2025년은 증가 추세로 데이터 생성
                    if year >= 2024:
                        growth_factor = 1.2 if year == 2024 else 1.5  # 2025년은 더 큰 성장
                        sales_volume = int(random.uniform(100, 500) * growth_factor)
                        market_share = random.uniform(5, 25) * growth_factor
                        if market_share > 30:  # 최대 30%로 제한
                            market_share = 30
                    else:
                        sales_volume = int(random.uniform(100, 500))
                        market_share = random.uniform(5, 25)
                    
                    sales_data.append({
                        'Year': year,
                        'Company': company,
                        'Model': model,
                        'Sales_Volume': sales_volume,
                        'Market_Share': market_share
                    })
        
        sales_df = pd.DataFrame(sales_data)
        
        # 각 연도별로 Market_Share 합계가 100이 되도록 조정
        for year in years:
            for model in models:
                mask = (sales_df['Year'] == year) & (sales_df['Model'] == model)
                sales_df.loc[mask, 'Market_Share'] = sales_df.loc[mask, 'Market_Share'] / sales_df.loc[mask, 'Market_Share'].sum() * 100
        
        sales_df.to_csv(os.path.join(data_dir, 'semiconductor_sales.csv'), index=False)
        
        # 반도체 생산 데이터 생성
        production_data = []
        
        for year in years:
            for month in range(1, 13):
                for company in companies:
                    for model in models:
                        # 2024년과 2025년은 생산량과 효율성 증가
                        if year >= 2024:
                            efficiency_boost = 5 if year == 2024 else 10  # 2025년은 더 높은 효율성
                            production_volume = int(random.uniform(50, 200) * (1.2 if year == 2024 else 1.4))
                            efficiency = min(95, random.uniform(70, 85) + efficiency_boost)  # 최대 95%로 제한
                        else:
                            production_volume = int(random.uniform(50, 200))
                            efficiency = random.uniform(70, 85)
                        
                        production_data.append({
                            'Year': year,
                            'Month': month,
                            'Company': company,
                            'Model': model,
                            'Production_Volume': production_volume,
                            'Efficiency': efficiency
                        })
        
        production_df = pd.DataFrame(production_data)
        production_df.to_csv(os.path.join(data_dir, 'semiconductor_production.csv'), index=False)
        
        # 반도체 건설 산업 데이터 생성
        construction_companies = ['삼성물산', '현대건설', 'GS건설', '대우건설', '포스코건설']
        regions = ['경기도', '충청남도', '경상북도', '전라남도', '인천광역시']
        
        orders_data = []
        
        for year in years:
            for quarter in range(1, 5):
                for company in construction_companies:
                    # 2024년과 2025년은 수주 금액 증가
                    if year >= 2024:
                        order_amount = int(random.uniform(5000, 20000) * (1.3 if year == 2024 else 1.6))
                    else:
                        order_amount = int(random.uniform(5000, 20000))
                    
                    orders_data.append({
                        'Year': year,
                        'Quarter': quarter,
                        'Company': company,
                        'Order_Amount': order_amount
                    })
        
        orders_df = pd.DataFrame(orders_data)
        orders_df.to_csv(os.path.join(data_dir, 'construction_orders.csv'), index=False)
        
        # 건설 현장 데이터 생성
        sites_data = []
        
        for year in years:
            for company in construction_companies:
                for region in regions:
                    # 2024년과 2025년은 더 많은 현장과 인력
                    if year >= 2024:
                        site_count = int(random.uniform(2, 8) * (1.2 if year == 2024 else 1.5))
                        worker_count = int(random.uniform(500, 2000) * (1.2 if year == 2024 else 1.5))
                    else:
                        site_count = int(random.uniform(2, 8))
                        worker_count = int(random.uniform(500, 2000))
                    
                    sites_data.append({
                        'Year': year,
                        'Company': company,
                        'Region': region,
                        'Site_Count': site_count,
                        'Worker_Count': worker_count
                    })
        
        sites_df = pd.DataFrame(sites_data)
        sites_df.to_csv(os.path.join(data_dir, 'construction_sites.csv'), index=False)
        
        # SWOT 분석 데이터 생성
        swot_data = {
            "반도체 산업 SWOT 분석": {
                "strengths": [
                    "글로벌 시장 점유율 상위권 유지",
                    "첨단 공정 기술 보유",
                    "안정적인 공급망 구축",
                    "높은 수익성"
                ],
                "weaknesses": [
                    "높은 초기 투자 비용",
                    "기술 격차 존재",
                    "인력 확보의 어려움",
                    "환경 규제 대응 비용 증가"
                ],
                "opportunities": [
                    "AI, 자율주행차 등 신규 시장 확대",
                    "정부의 산업 지원 정책",
                    "디지털 전환 가속화",
                    "친환경 반도체 수요 증가"
                ],
                "threats": [
                    "글로벌 경쟁 심화",
                    "원자재 가격 상승",
                    "지정학적 리스크",
                    "기술 유출 위험"
                ]
            },
            "트럼프 2기 가정 시나리오 SWOT 분석": {
                "strengths": [
                    "미국 내 반도체 생산기지 확대",
                    "미국 정부의 자국 기업 우대 정책",
                    "세금 감면 혜택",
                    "규제 완화로 인한 비용 절감"
                ],
                "weaknesses": [
                    "관세 부과로 인한 원자재 비용 상승",
                    "글로벌 인재 확보의 어려움",
                    "미국 중심 공급망 재편 비용",
                    "불확실한 정책 환경"
                ],
                "opportunities": [
                    "미국 시장 내 점유율 확대 기회",
                    "미국 정부의 반도체 산업 투자 확대",
                    "중국 의존도 감소를 위한 지원",
                    "미국 기업과의 전략적 제휴 가능성"
                ],
                "threats": [
                    "중국과의 관계 악화",
                    "글로벌 공급망 분열",
                    "보호무역주의 강화",
                    "국제 협력 약화로 인한 기술 발전 저해"
                ]
            }
        }
        
        with open(os.path.join(data_dir, 'swot_analysis.json'), 'w', encoding='utf-8') as f:
            json.dump(swot_data, f, ensure_ascii=False, indent=4)
        
        print("샘플 데이터 생성 완료")
        return True
    except Exception as e:
        print(f"샘플 데이터 생성 중 오류 발생: {str(e)}")
        return False

# 데이터 로드 함수
def load_data(file_name):
    """
    저장된 데이터를 로드하는 함수
    """
    file_path = os.path.join(DATA_DIR, file_name)
    
    if not os.path.exists(file_path):
        print(f"파일이 존재하지 않습니다: {file_path}")
        return None
    
    if file_name.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_name.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"지원하지 않는 파일 형식입니다: {file_path}")
        return None

# 웹 스크래핑 함수 (예시)
def scrape_material_prices():
    """
    원자재 가격 정보를 웹에서 스크래핑하는 함수 (예시)
    실제 구현 시 적절한 웹사이트와 API를 사용해야 함
    """
    try:
        # 예시 URL (실제 구현 시 변경 필요)
        url = "https://www.investing.com/commodities/copper"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 여기에 실제 파싱 로직 구현
            # 예: price = soup.select_one('span#last_last').text
            
            # 임시 데이터 반환 (실제 구현 시 변경 필요)
            return {
                'material': '구리',
                'price': 10250.50,
                'unit': 'USD/톤',
                'date': datetime.now().strftime('%Y-%m-%d')
            }
        else:
            print(f"스크래핑 실패: 상태 코드 {response.status_code}")
            return None
    except Exception as e:
        print(f"스크래핑 중 오류 발생: {str(e)}")
        return None

# 데이터 업데이트 함수
def update_data():
    """
    최신 데이터로 업데이트하는 함수
    실제 구현 시 적절한 API 또는 웹 스크래핑 사용
    """
    # 여기에 실제 데이터 업데이트 로직 구현
    print("데이터 업데이트 기능은 아직 구현되지 않았습니다.")
    pass

# 메인 함수
if __name__ == "__main__":
    # 샘플 데이터 생성
    generate_sample_data()
    
    # 데이터 로드 테스트
    df = load_data('semiconductor_sales.csv')
    if df is not None:
        print(df.head())

def load_semiconductor_data(filename):
    """
    반도체 관련 데이터를 로드하는 함수
    
    Parameters:
    -----------
    filename : str
        로드할 파일 이름
        
    Returns:
    --------
    pandas.DataFrame or dict
        로드된 데이터
    """
    try:
        # 파일 경로 설정
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        file_path = os.path.join(data_dir, filename)
        
        # 파일이 존재하지 않으면 샘플 데이터 생성
        if not os.path.exists(file_path):
            if not generate_sample_data():
                raise Exception("샘플 데이터 생성 실패")
        
        # 파일 확장자에 따라 다른 방식으로 로드
        if filename.endswith('.csv'):
            return pd.read_csv(file_path, encoding='utf-8-sig')
        elif filename.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            raise ValueError(f"지원하지 않는 파일 형식입니다: {filename}")
            
    except Exception as e:
        print(f"데이터 로드 중 오류 발생: {str(e)}")
        return None 