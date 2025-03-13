def show_industry_trend():
    st.title("반도체 산업 동향")
    
    try:
        # 데이터 로드
        market_data = load_semiconductor_data('market_data.csv')
        supply_chain_data = load_semiconductor_data('supply_chain.json')
        
        if market_data is None or supply_chain_data is None:
            return
        
        # 시장 점유율 섹션
        st.header("시장 점유율")
        
        # 연도 선택
        years = sorted(market_data['Year'].unique())
        selected_year = st.selectbox('연도 선택', years, index=len(years)-1)
        
        # 선택된 연도의 데이터
        year_data = market_data[market_data['Year'] == selected_year]
        
        # 시장 점유율 파이 차트
        fig_market_share = px.pie(
            year_data,
            values='Market_Share',
            names='Company',
            title=f'{selected_year}년 기업별 시장 점유율',
            template=set_plotly_theme()
        )
        
        # 소수점 첫째 자리까지만 표시하도록 수정
        fig_market_share.update_traces(
            textinfo='percent+label',
            texttemplate='%{label}<br>%{percent:.1f}%',
            hovertemplate='%{label}<br>점유율: %{percent:.1f}%'
        )
        
        st.plotly_chart(fig_market_share, use_container_width=True)
        
        # 공급망 분석 섹션
        st.header("공급망 분석")
        
        # 공급망 데이터 표시
        for category, items in supply_chain_data.items():
            st.subheader(category)
            
            # 카테고리별 데이터 표시
            cols = st.columns(len(items))
            for i, (company, details) in enumerate(items.items()):
                with cols[i]:
                    # 카드 스타일로 정보 표시
                    st.markdown(
                        f"""
                        <div style="padding: 1rem; border-radius: 0.5rem; border: 1px solid #e0e0e0; margin: 0.5rem 0;">
                            <h3 style="margin: 0; color: #1f77b4;">{company}</h3>
                            <p style="margin: 0.5rem 0;"><b>국가:</b> {details['country']}</p>
                            <p style="margin: 0.5rem 0;"><b>점유율:</b> {details['share']:.1f}%</p>
                            <p style="margin: 0.5rem 0;"><b>주요제품:</b> {details['products']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        
        # 연도별 추이 차트
        st.header("연도별 시장 점유율 추이")
        fig_trend = px.line(
            market_data,
            x='Year',
            y='Market_Share',
            color='Company',
            title='기업별 시장 점유율 추이',
            template=set_plotly_theme()
        )
        
        # y축을 퍼센트로 표시하고 소수점 첫째 자리까지 표시
        fig_trend.update_layout(
            yaxis=dict(
                tickformat='.1f',
                ticksuffix='%'
            )
        )
        
        # 호버 템플릿 수정
        fig_trend.update_traces(
            hovertemplate='%{x}년<br>%{y:.1f}%<extra>%{fullData.name}</extra>'
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
        
    except Exception as e:
        st.error(f'데이터를 불러오는 중 오류가 발생했습니다: {str(e)}') 