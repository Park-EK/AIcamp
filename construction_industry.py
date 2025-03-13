import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import sys
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import folium
from streamlit_folium import folium_static
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from utils.data_utils import load_semiconductor_data
from utils.visualization_utils import (
    create_line_chart, 
    create_bar_chart, 
    create_pie_chart, 
    create_pydeck_map,
    create_folium_map,
    create_card, 
    create_swot_analysis,
    COLOR_PALETTE,
    set_plotly_theme
)

# 상위 디렉토리 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_construction_data():
    """건설 산업 데이터를 로드하는 함수"""
    try:
        # 프로젝트 데이터 로드
        projects_df = pd.read_csv('data/construction_projects.csv')
        # 매출액 데이터 로드
        revenue_df = pd.read_csv('data/construction_revenue.csv')
        # 데이터 소스 정보 로드
        with open('data/data_sources.json', 'r', encoding='utf-8') as f:
            sources_info = json.load(f)
        
        return projects_df, revenue_df, sources_info
    except Exception as e:
        st.error(f"데이터 로드 중 오류가 발생했습니다: {str(e)}")
        return None, None, None

def show_aggrid(df, key=None):
    """
    AgGrid를 사용하여 데이터프레임을 표시하는 함수
    """
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
    gb.configure_side_bar()
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren=True)
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
    
    # 숫자 형식 지정
    for col in df.select_dtypes(include=['float64', 'int64']).columns:
        gb.configure_column(col, type=["numericColumn", "numberColumnFilter"], precision=0)
    
    grid_options = gb.build()
    
    return AgGrid(
        df,
        gridOptions=grid_options,
        data_return_mode='AS_INPUT',
        update_mode='MODEL_CHANGED',
        fit_columns_on_grid_load=True,
        theme='streamlit',
        enable_enterprise_modules=False,
        height=400,
        width='100%',
        key=key
    )

def show_construction_industry(section="overview"):
    """
    반도체 건설 산업 동향 페이지를 표시하는 함수
    """
    st.title("반도체 건설 산업 동향")
    
    try:
        # 데이터 로드
        projects_df, revenue_df, sources_info = load_construction_data()
        
        if projects_df is None or revenue_df is None:
            return
        
        # 탭 생성
        tabs = st.tabs(["프로젝트 현황", "매출액 분석", "지역별 분포", "데이터 출처"])
        
        with tabs[0]:
            st.header("반도체 건설 프로젝트 현황")
            
            # 필터 옵션
            col1, col2, col3 = st.columns(3)
            with col1:
                selected_year = st.selectbox(
                    "연도 선택",
                    sorted(projects_df['Year'].unique()),
                    index=len(projects_df['Year'].unique())-1
                )
            with col2:
                selected_country = st.selectbox(
                    "국가 선택",
                    ['전체'] + sorted(projects_df['Country'].unique())
                )
            with col3:
                selected_status = st.selectbox(
                    "진행 상태",
                    ['전체'] + sorted(projects_df['Status'].unique())
                )
            
            # 데이터 필터링
            filtered_df = projects_df.copy()
            if selected_country != '전체':
                filtered_df = filtered_df[filtered_df['Country'] == selected_country]
            if selected_status != '전체':
                filtered_df = filtered_df[filtered_df['Status'] == selected_status]
            
            # 프로젝트 테이블 표시
            st.subheader("프로젝트 목록")
            show_aggrid(filtered_df, key='projects_table')
            
            # 투자금액 차트
            st.subheader("국가별 투자금액")
            fig_investment = px.bar(
                filtered_df.groupby(['Country', 'Year'])['Investment_Amount'].sum().reset_index(),
                x='Country',
                y='Investment_Amount',
                color='Year',
                title='국가별 연도별 투자금액',
                labels={
                    'Country': '국가',
                    'Investment_Amount': '투자금액 (억원)',
                    'Year': '연도'
                }
            )
            st.plotly_chart(fig_investment, use_container_width=True)
        
        with tabs[1]:
            st.header("건설사 매출액 분석")
            
            # 연도 선택
            selected_year_revenue = st.selectbox(
                "연도 선택",
                sorted(revenue_df['Year'].unique()),
                index=len(revenue_df['Year'].unique())-1,
                key='revenue_year'
            )
            
            # 매출액 데이터 필터링
            revenue_filtered = revenue_df[revenue_df['Year'] == selected_year_revenue]
            
            # 매출액 테이블
            st.subheader(f"{selected_year_revenue}년 기업별 매출액")
            show_aggrid(revenue_filtered, key='revenue_table')
            
            # 매출액 추이 차트
            st.subheader("기업별 매출액 추이")
            fig_revenue = px.line(
                revenue_df,
                x='Year',
                y='Revenue',
                color='Company',
                title='기업별 연도별 매출액 추이',
                labels={
                    'Year': '연도',
                    'Revenue': '매출액 (억원)',
                    'Company': '기업명'
                }
            )
            st.plotly_chart(fig_revenue, use_container_width=True)
        
        with tabs[2]:
            st.header("건설 프로젝트 지역별 분포")
            
            # 지도에 프로젝트 위치 표시
            st.subheader("프로젝트 위치")
            
            # 위도/경도가 있는 데이터만 선택
            map_data = projects_df[['Latitude', 'Longitude', 'Project_Name', 'Company', 'Investment_Amount']].copy()
            map_data = map_data.dropna(subset=['Latitude', 'Longitude'])
            
            if not map_data.empty:
                # 컬럼명 변경
                map_data.rename(columns={
                    'Latitude': 'lat',
                    'Longitude': 'lon'
                }, inplace=True)
                st.map(map_data)
            else:
                st.warning("지도에 표시할 위치 데이터가 없습니다.")
            
            # 지역별 프로젝트 수
            st.subheader("국가별 프로젝트 현황")
            fig_projects = px.pie(
                projects_df.groupby('Country').size().reset_index(name='count'),
                values='count',
                names='Country',
                title='국가별 프로젝트 비중'
            )
            st.plotly_chart(fig_projects, use_container_width=True)
        
        with tabs[3]:
            st.header("데이터 출처 및 참고사항")
            
            st.subheader("시장 보고서")
            for report in sources_info['market_reports']:
                st.markdown(f"- **{report['name']}** ({report['year']})")
                st.markdown(f"  - 발행: {report['publisher']}")
                st.markdown(f"  - 설명: {report['description']}")
            
            st.subheader("기업 보고서")
            for report in sources_info['company_reports']:
                st.markdown(f"- **{report['name']}** ({min(report['years'])}~{max(report['years'])})")
                st.markdown(f"  - 기업: {report['company']}")
                st.markdown(f"  - 유형: {report['type']}")
            
            st.subheader("데이터 수집 방법론")
            st.markdown(f"- {sources_info['methodology']['data_collection']}")
            st.markdown(f"- {sources_info['methodology']['forecast']}")
            st.markdown(f"- {sources_info['methodology']['verification']}")
            
            st.warning(sources_info['methodology']['disclaimer'])
    
    except Exception as e:
        st.error(f'데이터를 불러오는 중 오류가 발생했습니다: {str(e)}')

if __name__ == "__main__":
    show_construction_industry() 