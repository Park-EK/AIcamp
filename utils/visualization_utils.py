import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import pydeck as pdk
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import io
import base64

# 색상 팔레트 정의
COLOR_PALETTE = {
    'primary': '#1E40AF',    # 진한 파란색
    'secondary': '#60A5FA',  # 밝은 파란색
    'accent1': '#DC2626',    # 진한 빨간색
    'accent2': '#FB923C',    # 주황색
    'accent3': '#059669',    # 진한 초록색
    'accent4': '#818CF8',    # 밝은 보라색
    'accent5': '#4C1D95',    # 진한 보라색
    'neutral': '#6B7280',    # 회색
    'background': '#F8FAFC', # 매우 밝은 회색
    'text': '#1E293B',       # 진한 회색
}

def apply_custom_css():
    """
    커스텀 CSS 스타일을 적용하는 함수
    """
    st.markdown("""
        <style>
            /* 전체 배경 및 텍스트 색상 */
            .stApp {
                background-color: #F8FAFC;
                color: #1E293B;
            }
            
            /* 사이드바 스타일 */
            .css-1d391kg {
                background-color: #F1F5F9;
            }
            
            /* 헤더 스타일 */
            h1, h2, h3, h4, h5, h6 {
                color: #1E3A8A;
            }
            
            /* 버튼 스타일 */
            .stButton>button {
                background-color: #1E40AF;
                color: white;
                border: none;
                border-radius: 0.375rem;
                padding: 0.5rem 1rem;
                font-weight: 500;
            }
            
            .stButton>button:hover {
                background-color: #1E3A8A;
            }
            
            /* 선택 위젯 스타일 */
            .stSelectbox>div>div {
                background-color: #F8FAFC;
                border: 1px solid #CBD5E1;
                border-radius: 0.375rem;
            }
            
            /* 데이터프레임 스타일 */
            .dataframe {
                border: 1px solid #E2E8F0;
                border-radius: 0.375rem;
            }
            
            .dataframe th {
                background-color: #F1F5F9;
                color: #1E293B;
                font-weight: 600;
                padding: 0.5rem;
            }
            
            .dataframe td {
                padding: 0.5rem;
                border-top: 1px solid #E2E8F0;
            }
            
            /* 카드 스타일 */
            .card {
                background-color: white;
                border-radius: 0.5rem;
                padding: 1rem;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                margin-bottom: 1rem;
            }
            
            .card-title {
                font-size: 1.25rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
                color: #1E3A8A;
            }
            
            .card-value {
                font-size: 2rem;
                font-weight: 700;
                color: #1E40AF;
            }
            
            .card-subtitle {
                font-size: 0.875rem;
                color: #64748B;
            }
        </style>
    """, unsafe_allow_html=True)

def set_plotly_theme():
    """
    Plotly 차트 테마를 설정하는 함수
    """
    return 'plotly_white'

def create_line_chart(data, x, y, title, color=None, hover_data=None):
    """
    라인 차트를 생성하는 함수
    """
    fig = px.line(
        data, 
        x=x, 
        y=y, 
        title=title,
        color=color,
        hover_data=hover_data,
        template=set_plotly_theme(),
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        title_font_size=20,
        title_font_family="Pretendard",
        legend_title_font_size=14,
        legend_title_font_family="Pretendard",
        legend_font_size=12,
        legend_font_family="Pretendard",
        xaxis_title_font_size=14,
        xaxis_title_font_family="Pretendard",
        yaxis_title_font_size=14,
        yaxis_title_font_family="Pretendard"
    )
    
    return fig

def create_bar_chart(data, x, y, title, color=None, barmode='group'):
    """
    바 차트를 생성하는 함수
    """
    fig = px.bar(
        data, 
        x=x, 
        y=y, 
        title=title,
        color=color,
        barmode=barmode,
        template=set_plotly_theme(),
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        title_font_size=20,
        title_font_family="Pretendard",
        legend_title_font_size=14,
        legend_title_font_family="Pretendard",
        legend_font_size=12,
        legend_font_family="Pretendard",
        xaxis_title_font_size=14,
        xaxis_title_font_family="Pretendard",
        yaxis_title_font_size=14,
        yaxis_title_font_family="Pretendard"
    )
    
    return fig

def create_pie_chart(data, values, names, title):
    """
    파이 차트를 생성하는 함수
    """
    fig = px.pie(
        data, 
        values=values, 
        names=names, 
        title=title,
        template=set_plotly_theme(),
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        title_font_size=20,
        title_font_family="Pretendard",
        legend_title_font_size=14,
        legend_title_font_family="Pretendard",
        legend_font_size=12,
        legend_font_family="Pretendard"
    )
    
    fig.update_traces(
        textinfo='percent+label',
        textfont_size=12,
        textfont_family="Pretendard"
    )
    
    return fig

def create_card(title, value, subtitle=None):
    """
    카드 형태의 UI 요소를 생성하는 함수
    """
    html = f"""
        <div class="card">
            <div class="card-title">{title}</div>
            <div class="card-value">{value}</div>
    """
    
    if subtitle:
        html += f'<div class="card-subtitle">{subtitle}</div>'
    
    html += "</div>"
    
    return html

def create_swot_analysis(data, title):
    """
    SWOT 분석 UI를 생성하는 함수
    """
    st.subheader(title)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div style="background-color: #DCFCE7; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
                <h3 style="color: #166534; margin-top: 0;">강점 (Strengths)</h3>
                <ul style="margin-bottom: 0;">
                    {"".join([f"<li>{item}</li>" for item in data["strengths"]])}
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="background-color: #FEF3C7; padding: 1rem; border-radius: 0.5rem;">
                <h3 style="color: #92400E; margin-top: 0;">기회 (Opportunities)</h3>
                <ul style="margin-bottom: 0;">
                    {"".join([f"<li>{item}</li>" for item in data["opportunities"]])}
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style="background-color: #FEE2E2; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
                <h3 style="color: #991B1B; margin-top: 0;">약점 (Weaknesses)</h3>
                <ul style="margin-bottom: 0;">
                    {"".join([f"<li>{item}</li>" for item in data["weaknesses"]])}
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="background-color: #E0E7FF; padding: 1rem; border-radius: 0.5rem;">
                <h3 style="color: #3730A3; margin-top: 0;">위협 (Threats)</h3>
                <ul style="margin-bottom: 0;">
                    {"".join([f"<li>{item}</li>" for item in data["threats"]])}
                </ul>
            </div>
        """, unsafe_allow_html=True)

# 지도 시각화 함수 (PyDeck)
def create_pydeck_map(df, lat_col, lon_col, color_col=None, size_col=None, tooltip_cols=None, title=None):
    """
    PyDeck을 사용하여 지도 시각화를 생성하는 함수
    
    Parameters:
    -----------
    df : pandas.DataFrame
        데이터프레임
    lat_col : str
        위도 열 이름
    lon_col : str
        경도 열 이름
    color_col : str, optional
        색상 구분을 위한 열 이름
    size_col : str, optional
        크기 구분을 위한 열 이름
    tooltip_cols : list, optional
        툴팁에 표시할 열 이름 목록
    title : str, optional
        지도 제목
        
    Returns:
    --------
    pydeck.Deck
        생성된 PyDeck 지도
    """
    if title:
        st.subheader(title)
    
    # 기본 위치 설정 (데이터의 중심)
    center_lat = df[lat_col].mean()
    center_lon = df[lon_col].mean()
    
    # 색상 설정
    if color_col:
        # 색상 매핑 (예시)
        color_mapping = {
            '진행 중': [0, 128, 255],  # 파란색
            '완공': [0, 204, 102],     # 녹색
            '계회': [255, 153, 51]     # 주황색
        }
        
        # 색상 열이 범주형인 경우
        if df[color_col].dtype == 'object':
            df['color'] = df[color_col].map(lambda x: color_mapping.get(x, [100, 100, 100]))
        # 색상 열이 수치형인 경우
        else:
            min_val = df[color_col].min()
            max_val = df[color_col].max()
            df['color'] = df[color_col].apply(
                lambda x: [
                    int(255 * (x - min_val) / (max_val - min_val)),
                    int(100 + 155 * (1 - (x - min_val) / (max_val - min_val))),
                    int(255 * (1 - (x - min_val) / (max_val - min_val)))
                ]
            )
    else:
        df['color'] = [[0, 128, 255]] * len(df)  # 기본 파란색
    
    # 크기 설정
    if size_col:
        min_size = df[size_col].min()
        max_size = df[size_col].max()
        df['size'] = df[size_col].apply(lambda x: 5000 * (x - min_size) / (max_size - min_size) + 5000)
    else:
        df['size'] = 10000  # 기본 크기
    
    # 툴팁 설정
    if tooltip_cols:
        tooltip = {
            "html": " ".join([f"<b>{col}:</b> {{{col}}}<br>" for col in tooltip_cols]),
            "style": {
                "backgroundColor": "white",
                "color": "black"
            }
        }
    else:
        tooltip = None
    
    # 레이어 생성
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=[lon_col, lat_col],
        get_color="color",
        get_radius="size",
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=0.05,
        radius_min_pixels=5,
        radius_max_pixels=100,
        line_width_min_pixels=1
    )
    
    # 뷰 상태 설정
    view_state = pdk.ViewState(
        longitude=center_lon,
        latitude=center_lat,
        zoom=3,
        pitch=0
    )
    
    # 지도 생성
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/light-v10",
        tooltip=tooltip
    )
    
    return deck

# 지도 시각화 함수 (Folium)
def create_folium_map(df, lat_col, lon_col, popup_col=None, color_col=None, size_col=None, title=None):
    """
    Folium을 사용하여 지도 시각화를 생성하는 함수
    
    Parameters:
    -----------
    df : pandas.DataFrame
        데이터프레임
    lat_col : str
        위도 열 이름
    lon_col : str
        경도 열 이름
    popup_col : str, optional
        팝업에 표시할 열 이름
    color_col : str, optional
        색상 구분을 위한 열 이름
    size_col : str, optional
        크기 구분을 위한 열 이름
    title : str, optional
        지도 제목
        
    Returns:
    --------
    folium.Map
        생성된 Folium 지도
    """
    if title:
        st.subheader(title)
    
    # 기본 위치 설정 (데이터의 중심)
    center_lat = df[lat_col].mean()
    center_lon = df[lon_col].mean()
    
    # 지도 생성
    m = folium.Map(location=[center_lat, center_lon], zoom_start=3, tiles="CartoDB positron")
    
    # 색상 설정
    if color_col:
        # 색상 매핑 (예시)
        color_mapping = {
            '진행 중': 'blue',
            '완공': 'green',
            '계회': 'orange'
        }
        
        # 색상 열이 범주형인 경우
        if df[color_col].dtype == 'object':
            df['marker_color'] = df[color_col].map(lambda x: color_mapping.get(x, 'gray'))
        # 색상 열이 수치형인 경우
        else:
            # 수치형 데이터를 3개 구간으로 나누어 색상 지정
            bins = [df[color_col].min(), df[color_col].quantile(0.33), df[color_col].quantile(0.66), df[color_col].max()]
            labels = ['blue', 'purple', 'red']
            df['marker_color'] = pd.cut(df[color_col], bins=bins, labels=labels, include_lowest=True)
    else:
        df['marker_color'] = 'blue'  # 기본 파란색
    
    # 크기 설정
    if size_col:
        min_size = df[size_col].min()
        max_size = df[size_col].max()
        df['marker_size'] = df[size_col].apply(lambda x: 5 * (x - min_size) / (max_size - min_size) + 5)
    else:
        df['marker_size'] = 8  # 기본 크기
    
    # 마커 추가
    for idx, row in df.iterrows():
        # 팝업 내용 설정
        if popup_col:
            popup_text = f"{popup_col}: {row[popup_col]}"
        else:
            popup_text = f"위치: {row[lat_col]}, {row[lon_col]}"
        
        # 마커 추가
        folium.CircleMarker(
            location=[row[lat_col], row[lon_col]],
            radius=row['marker_size'],
            color=row['marker_color'],
            fill=True,
            fill_color=row['marker_color'],
            fill_opacity=0.7,
            popup=popup_text
        ).add_to(m)
    
    return m

# 메인 함수
if __name__ == "__main__":
    # 테스트 데이터
    df = pd.DataFrame({
        'x': range(10),
        'y1': [i**2 for i in range(10)],
        'y2': [i**3 for i in range(10)]
    })
    
    # 라인 차트 테스트
    fig = create_line_chart(df, 'x', ['y1', 'y2'], '테스트 라인 차트')
    fig.show() 