import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 상위 디렉토리 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 유틸리티 모듈 임포트
from utils.visualization_utils import apply_custom_css, COLOR_PALETTE
from utils.data_utils import generate_sample_data
from components.semiconductor_industry import show_semiconductor_industry_main, show_supply_chain
from components.construction_industry import show_construction_industry
from components.information import show_information
from components.news_component import show_news

# 페이지 설정
st.set_page_config(
    page_title="반도체 산업 동향 분석 대시보드",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일 추가
st.markdown("""
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css" rel="stylesheet" />
<style>
    /* 전체 폰트 스타일 */
    * {
        font-family: 'Pretendard', sans-serif !important;
    }
    
    /* 제목 스타일 */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background-color: #F8FAFC;
        border-radius: 10px;
    }
    
    /* Streamlit 요소 스타일 */
    .stMarkdown, .stButton, .stSelectbox, .stMultiSelect {
        font-family: 'Pretendard', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

# 메인 제목 추가
st.markdown('<h1 class="main-title">반도체 산업 동향 분석 대시보드</h1>', unsafe_allow_html=True)

# 커스텀 CSS 적용
apply_custom_css()

# 사이드바 설정
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <h1 style='font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem;'>반도체 산업 동향 대시보드</h1>
            <p style='color: #64748B; font-size: 0.875rem;'>실시간 데이터 기반 분석</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 1rem 0; border-color: #E2E8F0;'>", unsafe_allow_html=True)
    
    # 메뉴 선택
    menu = st.radio(
        "분석 항목 선택",
        ["반도체 산업 동향", "반도체 건설 산업 동향", "반도체 뉴스", "정보"]
    )
    
    st.markdown("<hr style='margin: 1rem 0; border-color: #E2E8F0;'>", unsafe_allow_html=True)
    
    # 데이터 업데이트 버튼
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
            <p style='color: #64748B; font-size: 0.875rem; margin-bottom: 0.5rem;'>
                데이터 업데이트
            </p>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("새로고침"):
            with st.spinner("데이터를 업데이트하는 중..."):
                generate_sample_data()
                st.success("✅ 완료")
    
    # 사이드바 푸터
    st.markdown("<hr style='margin: 1rem 0; border-color: #E2E8F0;'>", unsafe_allow_html=True)
    st.markdown("""
        <div style='position: fixed; bottom: 0; padding: 1rem;'>
            <p style='color: #64748B; font-size: 0.75rem; margin-bottom: 0.25rem;'>
                © 2025 반도체 산업 동향 대시보드
            </p>
            <p style='color: #94A3B8; font-size: 0.75rem;'>
                데이터 출처: 각 기업 연간 보고서, 시장 조사 기관 보고서
            </p>
        </div>
    """, unsafe_allow_html=True)

# 현재 시간 표시
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.sidebar.markdown(f"마지막 업데이트: {current_time}")

# 메인 컨텐츠
if menu == "반도체 산업 동향":
    show_semiconductor_industry_main()
    
    # 공급망 분석 표시 여부
    if st.checkbox("공급망 분석 보기", value=False):
        show_supply_chain()
elif menu == "반도체 건설 산업 동향":
    show_construction_industry()
elif menu == "반도체 뉴스":
    show_news()
elif menu == "정보":
    show_information()

# 앱 실행
if __name__ == "__main__":
    # 샘플 데이터가 없는 경우 자동 생성
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    sample_file = os.path.join(data_dir, 'semiconductor_sales.csv')
    
    if not os.path.exists(sample_file):
        with st.spinner("초기 샘플 데이터를 생성 중입니다..."):
            generate_sample_data() 