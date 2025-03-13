import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import sys
import plotly.express as px
import plotly.graph_objects as go
from st_cytoscape import cytoscape
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from utils.data_utils import load_semiconductor_data
from utils.visualization_utils import (
    create_line_chart, 
    create_bar_chart, 
    create_pie_chart, 
    create_card, 
    create_swot_analysis,
    COLOR_PALETTE,
    set_plotly_theme
)

# 상위 디렉토리 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_supply_chain_elements():
    nodes = [
        # 제조사
        {"data": {"id": "삼성전자", "label": "삼성전자", "type": "제조사"}},
        {"data": {"id": "SK하이닉스", "label": "SK하이닉스", "type": "제조사"}},
        {"data": {"id": "TSMC", "label": "TSMC", "type": "제조사"}},
        {"data": {"id": "Intel", "label": "Intel", "type": "제조사"}},
        # 부품사
        {"data": {"id": "삼성전기", "label": "삼성전기", "type": "부품사"}},
        # 소재사
        {"data": {"id": "SK머티리얼즈", "label": "SK머티리얼즈", "type": "소재사"}},
        # 장비사
        {"data": {"id": "원익IPS", "label": "원익IPS", "type": "장비사"}},
        {"data": {"id": "ASML", "label": "ASML", "type": "장비사"}},
        {"data": {"id": "Applied Materials", "label": "Applied Materials", "type": "장비사"}},
    ]
    
    edges = [
        {"data": {"source": "ASML", "target": "삼성전자"}},
        {"data": {"source": "ASML", "target": "SK하이닉스"}},
        {"data": {"source": "ASML", "target": "TSMC"}},
        {"data": {"source": "ASML", "target": "Intel"}},
        {"data": {"source": "Applied Materials", "target": "삼성전자"}},
        {"data": {"source": "Applied Materials", "target": "SK하이닉스"}},
        {"data": {"source": "원익IPS", "target": "삼성전자"}},
        {"data": {"source": "원익IPS", "target": "SK하이닉스"}},
        {"data": {"source": "삼성전기", "target": "삼성전자"}},
        {"data": {"source": "SK머티리얼즈", "target": "SK하이닉스"}},
    ]
    
    return nodes + edges

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
    for col in df.select_dtypes(include=['float64']).columns:
        gb.configure_column(col, type=["numericColumn", "numberColumnFilter"], precision=2)
    
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

def show_semiconductor_industry(section="sales"):
    """
    반도체 산업 데이터를 표시하는 함수
    """
    try:
        if section == "sales":
            # 판매 현황 데이터 로드
            sales_data = load_semiconductor_data('semiconductor_sales.csv')
            
            # 연도 선택
            years = sorted(sales_data['Year'].unique())
            selected_year = st.selectbox('연도 선택', years, key='sales_year')
            
            # 필터링된 데이터
            filtered_data = sales_data[sales_data['Year'] == selected_year]
            
            # 데이터 테이블 표시 (AgGrid 사용)
            st.subheader(f"{selected_year}년 반도체 판매 데이터")
            
            # 데이터 단위 변환 (억원 단위로 통일)
            display_data = filtered_data.copy()
            display_data['Sales_Volume'] = display_data['Sales_Volume'] * 100  # 백만 개 -> 억원 단위로 변환
            display_data.rename(columns={
                'Company': '기업명',
                'Model': '모델',
                'Sales_Volume': '판매액(억원)',
                'Market_Share': '시장점유율(%)'
            }, inplace=True)
            
            show_aggrid(display_data, key='sales_table')
            
            # 판매량 차트
            fig_sales = px.bar(
                filtered_data,
                x='Company',
                y='Sales_Volume',
                color='Model',
                title=f'{selected_year}년 제조사별 판매액',
                template=set_plotly_theme(),
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_sales.update_layout(
                xaxis_title="제조사",
                yaxis_title="판매액 (억원)",
            )
            # 판매량을 억원 단위로 표시
            fig_sales.update_traces(
                hovertemplate="제조사: %{x}<br>모델: %{fullData.name}<br>판매액: %{y:.0f}억원"
            )
            # y축 값에 100을 곱해서 억원 단위로 표시
            fig_sales.update_yaxes(tickprefix="", ticksuffix="억원")
            fig_sales.update_layout(yaxis=dict(tickformat=",d"))
            
            st.plotly_chart(fig_sales, use_container_width=True)
            
            # 점유율 파이 차트
            fig_share = px.pie(
                filtered_data,
                values='Market_Share',
                names='Company',
                title=f'{selected_year}년 시장 점유율',
                template=set_plotly_theme(),
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_share.update_traces(
                textinfo='percent+label',
                hovertemplate="회사: %{label}<br>점유율: %{percent}<br>매출액: %{value:.1f}%"
            )
            st.plotly_chart(fig_share, use_container_width=True)
            
        elif section == "production":
            # 생산 현황 데이터 로드
            production_data = load_semiconductor_data('semiconductor_production.csv')
            
            # 연도 및 모델 선택
            years = sorted(production_data['Year'].unique())
            models = sorted(production_data['Model'].unique())
            
            col1, col2 = st.columns(2)
            with col1:
                selected_year = st.selectbox('연도 선택', years, key='prod_year')
            with col2:
                selected_model = st.selectbox('모델 선택', models, key='prod_model')
            
            # 필터링된 데이터
            filtered_data = production_data[
                (production_data['Year'] == selected_year) &
                (production_data['Model'] == selected_model)
            ]
            
            # 데이터 테이블 표시 (AgGrid 사용)
            st.subheader(f"{selected_year}년 {selected_model} 생산 데이터")
            
            # 데이터 단위 변환 (억원 단위로 통일)
            display_data = filtered_data.copy()
            display_data['Production_Volume'] = display_data['Production_Volume'] * 100  # 백만 개 -> 억원 단위로 변환
            display_data.rename(columns={
                'Company': '기업명',
                'Month': '월',
                'Production_Volume': '생산액(억원)',
                'Efficiency': '효율성(%)'
            }, inplace=True)
            
            show_aggrid(display_data, key='production_table')
            
            # 생산량 차트
            fig_production = px.bar(
                filtered_data,
                x='Month',
                y='Production_Volume',
                color='Company',
                title=f'{selected_year}년 {selected_model} 월별 생산액',
                template=set_plotly_theme(),
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            # x축을 1월부터 12월까지 표시
            fig_production.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=list(range(1, 13)),
                    ticktext=[f"{i}월" for i in range(1, 13)]
                ),
                xaxis_title="월",
                yaxis_title="생산액 (억원)",
            )
            
            # 생산량을 억원 단위로 표시
            fig_production.update_traces(
                hovertemplate="월: %{x}월<br>기업: %{fullData.name}<br>생산액: %{y:.0f}억원"
            )
            # y축 값에 100을 곱해서 억원 단위로 표시
            fig_production.update_yaxes(tickprefix="", ticksuffix="억원")
            fig_production.update_layout(yaxis=dict(tickformat=",d"))
            
            st.plotly_chart(fig_production, use_container_width=True)
            
            # 생산 효율성 라인 차트
            fig_efficiency = go.Figure()
            
            for company in filtered_data['Company'].unique():
                company_data = filtered_data[filtered_data['Company'] == company]
                fig_efficiency.add_trace(
                    go.Scatter(
                        x=company_data['Month'],
                        y=company_data['Efficiency'],
                        name=company,
                        mode='lines+markers'
                    )
                )
            
            # x축을 1월부터 12월까지 표시
            fig_efficiency.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=list(range(1, 13)),
                    ticktext=[f"{i}월" for i in range(1, 13)]
                ),
                title=f'{selected_year}년 {selected_model} 생산 효율성',
                template=set_plotly_theme(),
                showlegend=True,
                xaxis_title="월",
                yaxis_title="생산 효율성 (%)",
            )
            
            # 효율성을 퍼센트로 표시
            fig_efficiency.update_traces(
                hovertemplate="월: %{x}월<br>기업: %{fullData.name}<br>효율성: %{y:.1f}%"
            )
            fig_efficiency.update_yaxes(ticksuffix="%")
            
            st.plotly_chart(fig_efficiency, use_container_width=True)
            
    except Exception as e:
        st.error(f'데이터를 불러오는 중 오류가 발생했습니다: {str(e)}')

def show_supply_chain():
    """
    반도체 산업 공급망을 시각화하는 함수
    """
    st.header("반도체 산업 공급망 분석")
    
    # 공급망 설명
    st.markdown("""
    반도체 산업의 공급망은 크게 장비사, 소재사, 부품사, 제조사로 구성됩니다. 
    각 기업들은 복잡한 네트워크를 형성하여 최종 제품 생산에 기여합니다.
    
    ### 주요 공급망 구성
    - **장비사**: 반도체 제조 장비를 공급 (ASML, Applied Materials, 원익IPS 등)
    - **소재사**: 웨이퍼, 화학물질 등 원자재 공급 (SK머티리얼즈 등)
    - **부품사**: 기판, PCB 등 부품 공급 (삼성전기 등)
    - **제조사**: 최종 반도체 제품 생산 (삼성전자, SK하이닉스, TSMC, Intel 등)
    """)
    
    # Cytoscape 스타일 정의
    stylesheet = [
        {
            "selector": "node",
            "style": {
                "label": "data(label)",
                "text-valign": "center",
                "text-halign": "center",
                "width": "60px",
                "height": "60px",
                "font-size": "10px",
                "background-color": "#fff",
                "border-width": "2px",
                "border-color": "#000",
                "color": "#000"
            }
        },
        {
            "selector": 'node[type = "제조사"]',
            "style": {
                "background-color": "#8dd3c7",
                "border-color": "#6bab9f"
            }
        },
        {
            "selector": 'node[type = "부품사"]',
            "style": {
                "background-color": "#ffffb3",
                "border-color": "#d9d98f"
            }
        },
        {
            "selector": 'node[type = "소재사"]',
            "style": {
                "background-color": "#bebada",
                "border-color": "#9a96b6"
            }
        },
        {
            "selector": 'node[type = "장비사"]',
            "style": {
                "background-color": "#fb8072",
                "border-color": "#d9655a"
            }
        },
        {
            "selector": "edge",
            "style": {
                "width": 2,
                "line-color": "#b3b3b3",
                "target-arrow-color": "#b3b3b3",
                "target-arrow-shape": "triangle",
                "curve-style": "bezier"
            }
        }
    ]
    
    # 레이아웃 선택
    layout_options = {
        "원형 레이아웃": "circle",
        "그리드 레이아웃": "grid",
        "동심원 레이아웃": "concentric",
        "힘 기반 레이아웃": "cose"
    }
    
    selected_layout = st.selectbox(
        "레이아웃 선택",
        options=list(layout_options.keys()),
        key="supply_chain_layout"
    )
    
    # Cytoscape 그래프 표시
    elements = create_supply_chain_elements()
    cytoscape(
        elements=elements,
        stylesheet=stylesheet,
        layout={"name": layout_options[selected_layout]},
        height="600px"
    )
    
    # 범례 표시
    st.markdown("### 범례")
    cols = st.columns(4)
    with cols[0]:
        st.markdown(
            """
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #8dd3c7; margin-right: 10px;"></div>
                <span>제조사</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with cols[1]:
        st.markdown(
            """
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #ffffb3; margin-right: 10px;"></div>
                <span>부품사</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with cols[2]:
        st.markdown(
            """
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #bebada; margin-right: 10px;"></div>
                <span>소재사</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with cols[3]:
        st.markdown(
            """
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #fb8072; margin-right: 10px;"></div>
                <span>장비사</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # 공급망 분석 인사이트
    st.markdown("### 공급망 분석 인사이트")
    
    with st.expander("주요 인사이트 보기"):
        st.markdown("""
        1. **장비사 의존성**: 첨단 반도체 제조에 필수적인 EUV 장비는 ASML이 독점하고 있어, 모든 주요 제조사가 ASML에 의존하는 구조입니다.
        
        2. **지역적 집중**: 반도체 제조는 대만(TSMC), 한국(삼성, SK하이닉스), 미국(Intel) 등 특정 지역에 집중되어 있어 지정학적 리스크가 존재합니다.
        
        3. **수직 계열화**: 삼성은 삼성전기를 통해 부품 공급을, SK는 SK머티리얼즈를 통해 소재 공급을 수직 계열화하여 공급망 안정성을 확보하고 있습니다.
        
        4. **병목 현상**: 특정 장비나 소재의 공급 부족은 전체 산업에 병목 현상을 일으킬 수 있으며, 이는 최근 글로벌 반도체 부족 사태의 원인 중 하나입니다.
        """)

def show_semiconductor_industry_main():
    """
    반도체 산업 동향을 표시하는 함수
    """
    st.title("반도체 산업 동향")
    
    # 탭 생성
    tabs = st.tabs(["판매 현황", "생산 현황"])
    
    # 판매 현황 탭
    with tabs[0]:
        show_semiconductor_industry("sales")
    
    # 생산 현황 탭
    with tabs[1]:
        show_semiconductor_industry("production")
    
    # SWOT 분석 표시
    try:
        # SWOT 분석 데이터 로드
        swot_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'swot_analysis.json')
        
        if os.path.exists(swot_file):
            with open(swot_file, 'r', encoding='utf-8') as f:
                swot_data = json.load(f)
            
            st.markdown("---")
            st.header("SWOT 분석")
            
            # 반도체 산업 SWOT 분석
            if "반도체 산업 SWOT 분석" in swot_data:
                st.subheader("반도체 산업 SWOT 분석")
                
                swot = swot_data["반도체 산업 SWOT 분석"]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 강점 (Strengths)")
                    for item in swot["strengths"]:
                        st.markdown(f"- {item}")
                    
                    st.markdown("#### 약점 (Weaknesses)")
                    for item in swot["weaknesses"]:
                        st.markdown(f"- {item}")
                
                with col2:
                    st.markdown("#### 기회 (Opportunities)")
                    for item in swot["opportunities"]:
                        st.markdown(f"- {item}")
                    
                    st.markdown("#### 위협 (Threats)")
                    for item in swot["threats"]:
                        st.markdown(f"- {item}")
            
            # 트럼프 2기 가정 시나리오 SWOT 분석
            if "트럼프 2기 가정 시나리오 SWOT 분석" in swot_data:
                st.markdown("---")
                st.subheader("트럼프 2기 가정 시나리오 SWOT 분석")
                
                swot = swot_data["트럼프 2기 가정 시나리오 SWOT 분석"]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 강점 (Strengths)")
                    for item in swot["strengths"]:
                        st.markdown(f"- {item}")
                    
                    st.markdown("#### 약점 (Weaknesses)")
                    for item in swot["weaknesses"]:
                        st.markdown(f"- {item}")
                
                with col2:
                    st.markdown("#### 기회 (Opportunities)")
                    for item in swot["opportunities"]:
                        st.markdown(f"- {item}")
                    
                    st.markdown("#### 위협 (Threats)")
                    for item in swot["threats"]:
                        st.markdown(f"- {item}")
    
    except Exception as e:
        st.warning(f"SWOT 분석 데이터를 불러오는 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    show_semiconductor_industry_main() 