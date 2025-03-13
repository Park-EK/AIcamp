import streamlit as st
import os
import sys

# 상위 디렉토리 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def show_information():
    """
    정보 페이지를 표시하는 함수
    """
    st.title("반도체 산업 동향 분석 대시보드 정보")
    
    # 탭 생성
    tabs = st.tabs(["소개", "주요 기능", "데이터 출처", "연락처"])
    
    # 소개 탭
    with tabs[0]:
        st.header("대시보드 소개")
        
        st.markdown("""
        ### 반도체 산업 동향 분석 대시보드
        
        이 대시보드는 반도체 산업의 주요 동향을 시각적으로 분석하고 이해하기 위한 도구입니다. 
        반도체 제조사의 판매 현황, 생산 현황, 건설 산업 동향, 그리고 최신 뉴스를 한눈에 볼 수 있도록 설계되었습니다.
        
        #### 대시보드의 목적
        
        - 반도체 산업의 주요 지표를 시각화하여 트렌드 파악
        - 제조사별 시장 점유율 및 성과 비교 분석
        - 반도체 공급망 구조 이해
        - 반도체 관련 건설 산업 동향 모니터링
        - 최신 반도체 뉴스 및 정보 제공
        
        이 대시보드는 반도체 산업 관계자, 투자자, 연구원 및 학생들에게 유용한 정보를 제공합니다.
        """)
        
        st.image("https://via.placeholder.com/800x400?text=Semiconductor+Industry+Dashboard", 
                 caption="반도체 산업 동향 분석 대시보드 개요")
    
    # 주요 기능 탭
    with tabs[1]:
        st.header("주요 기능")
        
        st.markdown("""
        ### 반도체 산업 동향
        - **판매 현황**: 제조사별 판매량 및 시장 점유율 분석
        - **생산 현황**: 월별 생산량 및 생산 효율성 추이 분석
        - **공급망 분석**: 반도체 산업 공급망 구조 시각화
        
        ### 반도체 건설 산업 동향
        - **수주 현황**: 건설사별 반도체 관련 수주 현황
        - **공사 현장**: 주요 반도체 공장 건설 현장 정보
        
        ### 반도체 뉴스
        - **카테고리별 뉴스**: 반도체 산업, 기술, 시장, 정책 관련 최신 뉴스
        - **뉴스 요약**: AI 기반 뉴스 내용 요약 제공
        
        ### 기타 기능
        - **데이터 새로고침**: 최신 데이터로 대시보드 업데이트
        - **SWOT 분석**: 반도체 산업 및 주요 시나리오에 대한 SWOT 분석
        """)
        
        # 기능 아이콘 표시
        cols = st.columns(4)
        with cols[0]:
            st.markdown("#### 📊 데이터 시각화")
            st.markdown("다양한 차트와 그래프를 통한 직관적인 데이터 시각화")
        
        with cols[1]:
            st.markdown("#### 🔍 데이터 필터링")
            st.markdown("연도, 제조사, 모델 등 다양한 기준으로 데이터 필터링")
        
        with cols[2]:
            st.markdown("#### 📰 뉴스 분석")
            st.markdown("최신 반도체 관련 뉴스 제공 및 AI 기반 요약")
        
        with cols[3]:
            st.markdown("#### 🔄 실시간 업데이트")
            st.markdown("데이터 새로고침을 통한 최신 정보 업데이트")
    
    # 데이터 출처 탭
    with tabs[2]:
        st.header("데이터 출처")
        
        st.markdown("""
        ### 데이터 출처 및 참고 자료
        
        이 대시보드에서 사용된 데이터는 다음과 같은 출처에서 수집되었습니다:
        
        #### 반도체 산업 데이터
        - 한국반도체산업협회 (KSIA)
        - 세계반도체무역통계기구 (WSTS)
        - 각 제조사 분기/연간 보고서
        
        #### 건설 산업 데이터
        - 대한건설협회
        - 건설산업연구원
        - 주요 건설사 공시 자료
        
        #### 뉴스 데이터
        - News API를 통한 글로벌 뉴스 소스
        - 주요 기술 미디어 및 경제 뉴스 플랫폼
        
        > 참고: 현재 대시보드에 표시된 데이터는 교육 및 시연 목적의 샘플 데이터입니다.
        > 실제 프로덕션 환경에서는 위 출처의 실제 데이터를 연동하여 사용할 수 있습니다.
        """)
        
        # 데이터 업데이트 주기
        st.info("데이터 업데이트 주기: 판매/생산 데이터 - 월간, 건설 데이터 - 분기간, 뉴스 데이터 - 일간")
    
    # 연락처 탭
    with tabs[3]:
        st.header("연락처 및 피드백")
        
        st.markdown("""
        ### 개발팀 연락처
        
        이 대시보드에 대한 문의사항이나 피드백이 있으시면 아래 연락처로 연락해 주세요:
        
        📧 **이메일**: semiconductor.dashboard@example.com  
        📞 **전화번호**: 02-123-4567  
        🌐 **웹사이트**: https://example.com/semiconductor-dashboard  
        
        ### 피드백 제출
        
        아래 양식을 통해 피드백을 제출해 주세요:
        """)
        
        # 피드백 양식
        with st.form("feedback_form"):
            name = st.text_input("이름")
            email = st.text_input("이메일")
            feedback_type = st.selectbox("피드백 유형", ["기능 제안", "버그 신고", "데이터 문의", "기타"])
            feedback = st.text_area("피드백 내용")
            
            submitted = st.form_submit_button("제출")
            if submitted:
                st.success("피드백이 제출되었습니다. 감사합니다!")
        
        # 버전 정보
        st.markdown("---")
        st.caption("반도체 산업 동향 분석 대시보드 v1.0.0")
        st.caption("© 2023-2024 반도체 대시보드 개발팀. All rights reserved.")

if __name__ == "__main__":
    show_information() 