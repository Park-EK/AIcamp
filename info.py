import streamlit as st

def show_info():
    # 소개
    st.markdown("""
    <div class='stBlock'>
        <h2 style='font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem;'>소개</h2>
        <p style='color: #475569; line-height: 1.6;'>
            이 대시보드는 반도체 산업과 반도체 건설 산업에 대한 데이터를 시각화하여 제공합니다.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 주요 기능
    st.markdown("""
    <div class='stBlock'>
        <h2 style='font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem;'>주요 기능</h2>

        <h3 style='font-size: 1.25rem; font-weight: 500; margin: 1.5rem 0 0.5rem;'>
            1. 반도체 산업 동향
        </h3>
        <ul style='color: #475569; line-height: 1.6; margin-left: 1.5rem;'>
            <li>Model별, 제작회사별 판매 현황 및 Supply Chain</li>
            <li>과거(2023~2024), 현재, 향후(2026~2027) 반도체 MODEL별 생산 현황</li>
            <li>"미국 트럼프 2기" 시나리오 하에 한국 반도체 회사에 미치는 영향(SWOT 분석)</li>
        </ul>

        <h3 style='font-size: 1.25rem; font-weight: 500; margin: 1.5rem 0 0.5rem;'>
            2. 반도체 건설 산업 동향
        </h3>
        <ul style='color: #475569; line-height: 1.6; margin-left: 1.5rem;'>
            <li>과거(2023~2024), 현재, 향후(2026~2027) 반도체 건설 산업 수주 현황</li>
            <li>지도(Map) 시각화(건설 사업장 위치, Clean Room 면적, 생산장비 금액, 전체 도급액 등)</li>
            <li>"미국 트럼프 2기" 시나리오 하에 반도체 건설사에 미치는 영향(SWOT 분석)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 데이터 소스
    st.markdown("""
    <div class='stBlock'>
        <h2 style='font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem;'>데이터 소스</h2>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;'>
            <div>
                <h4 style='font-size: 1rem; font-weight: 500; color: #64748B; margin-bottom: 0.5rem;'>
                    기본 데이터
                </h4>
                <ul style='color: #475569; line-height: 1.6; margin-left: 1.5rem;'>
                    <li>학술 논문</li>
                    <li>뉴스 기사</li>
                    <li>기업 보고서</li>
                    <li>정부 자료</li>
                </ul>
            </div>
            <div>
                <h4 style='font-size: 1rem; font-weight: 500; color: #64748B; margin-bottom: 0.5rem;'>
                    시장 데이터
                </h4>
                <ul style='color: #475569; line-height: 1.6; margin-left: 1.5rem;'>
                    <li>Investing.com</li>
                    <li>Trading Economics</li>
                    <li>Bloomberg</li>
                    <li>네이버 금융</li>
                </ul>
            </div>
            <div>
                <h4 style='font-size: 1rem; font-weight: 500; color: #64748B; margin-bottom: 0.5rem;'>
                    산업 데이터
                </h4>
                <ul style='color: #475569; line-height: 1.6; margin-left: 1.5rem;'>
                    <li>ENR</li>
                    <li>Platts</li>
                    <li>KOTRA</li>
                    <li>건설산업연구원</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 연락처
    st.markdown("""
    <div class='stBlock'>
        <h2 style='font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem;'>연락처</h2>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;'>
            <div>
                <p style='color: #475569; margin-bottom: 0.5rem;'>
                    <span style='color: #64748B;'>이메일:</span> example@example.com
                </p>
                <p style='color: #475569; margin-bottom: 0.5rem;'>
                    <span style='color: #64748B;'>웹사이트:</span> 
                    <a href="https://example.com" style='color: #4F46E5; text-decoration: none;'>
                        example.com
                    </a>
                </p>
            </div>
            <div>
                <p style='color: #475569; margin-bottom: 0.5rem;'>
                    <span style='color: #64748B;'>GitHub:</span>
                    <a href="https://github.com/example/semiconductor-dashboard" 
                       style='color: #4F46E5; text-decoration: none;'>
                        semiconductor-dashboard
                    </a>
                </p>
                <p style='color: #475569; margin-bottom: 0.5rem;'>
                    <span style='color: #64748B;'>LinkedIn:</span>
                    <a href="https://linkedin.com/in/example" 
                       style='color: #4F46E5; text-decoration: none;'>
                        /in/example
                    </a>
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_info() 