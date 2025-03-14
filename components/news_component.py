import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from newsapi import NewsApiClient

def get_sample_news():
    """샘플 뉴스 데이터를 생성하는 함수"""
    current_time = datetime.now()
    
    sample_news = [
        {
            "source": {"id": "news1", "name": "반도체 뉴스"},
            "author": "김기자",
            "title": "삼성전자, 4나노 반도체 양산 본격화",
            "description": "삼성전자가 4나노 반도체 공정의 양산을 본격화했다고 발표했습니다. 이번 양산을 통해 시스템 반도체 시장에서의 경쟁력을 한층 강화할 것으로 기대됩니다. 특히 AI 반도체 시장을 겨냥한 첨단 공정으로, 전력 효율과 성능이 크게 개선되었습니다.",
            "url": "https://example.com/news1",
            "publishedAt": (current_time - timedelta(hours=2)).isoformat()
        },
        {
            "source": {"id": "news2", "name": "테크 리포트"},
            "author": "이기자",
            "title": "SK하이닉스, 차세대 D램 개발 성공",
            "description": "SK하이닉스가 차세대 D램 개발에 성공했다고 발표했습니다. 이번에 개발된 D램은 기존 제품 대비 속도는 30% 향상되고 전력 소비량은 20% 감소했습니다. 2024년 하반기부터 본격적인 양산이 시작될 예정입니다.",
            "url": "https://example.com/news2",
            "publishedAt": (current_time - timedelta(hours=4)).isoformat()
        },
        {
            "source": {"id": "news3", "name": "글로벌 이코노미"},
            "author": "박기자",
            "title": "글로벌 반도체 시장, 2024년 회복세 전망",
            "description": "세계반도체시장통계기구(WSTS)는 2024년 글로벌 반도체 시장이 전년 대비 20% 성장할 것으로 전망했습니다. AI 반도체 수요 증가와 재고 조정 마무리가 주요 성장 동력으로 분석됩니다. 특히 메모리 반도체 시장의 반등이 두드러질 것으로 예상됩니다.",
            "url": "https://example.com/news3",
            "publishedAt": (current_time - timedelta(hours=6)).isoformat()
        },
        {
            "source": {"id": "news4", "name": "산업 동향"},
            "author": "최기자",
            "title": "미국, 추가 반도체 지원책 발표",
            "description": "미국 정부가 자국 내 반도체 산업 육성을 위한 추가 지원책을 발표했습니다. 이번 지원책에는 R&D 투자 확대와 인력 양성 프로그램이 포함되어 있습니다. 총 500억 달러 규모의 투자가 이루어질 예정이며, 첨단 패키징 기술 개발에 중점을 둘 계획입니다.",
            "url": "https://example.com/news4",
            "publishedAt": (current_time - timedelta(hours=8)).isoformat()
        },
        {
            "source": {"id": "news5", "name": "테크 인사이트"},
            "author": "정기자",
            "title": "TSMC, 미국 애리조나 공장 가동 임박",
            "description": "TSMC의 미국 애리조나 공장이 시험 가동을 시작했습니다. 2024년 상반기 중 본격적인 양산 체제에 돌입할 예정이며, 초기에는 5나노 공정을 중심으로 생산이 이루어질 전망입니다. 애플과 AMD가 주요 고객이 될 것으로 예상됩니다.",
            "url": "https://example.com/news5",
            "publishedAt": (current_time - timedelta(hours=10)).isoformat()
        }
    ]
    
    return pd.DataFrame(sample_news)

def fetch_news(api_key, category, days=7):
    """뉴스 데이터를 가져오는 함수"""
    try:
        newsapi = NewsApiClient(api_key=api_key)
        
        # 날짜 범위 설정
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days)
        
        # 카테고리별 검색어 설정 (한글 + 영문)
        search_queries = {
            "전체": "(반도체 OR 삼성전자 OR SK하이닉스) OR (semiconductor OR Samsung OR SK Hynix OR TSMC OR Intel)",
            "기업 동향": "(삼성전자 반도체 OR SK하이닉스) OR (Samsung semiconductor OR SK Hynix OR TSMC OR Intel)",
            "시장 동향": "(반도체 시장 OR 메모리 시장) OR (semiconductor market OR memory market)",
            "기술 동향": "(반도체 기술 OR 파운드리) OR (semiconductor technology OR foundry)",
            "정책": "(반도체 정책 OR 반도체 지원) OR (semiconductor policy OR CHIPS Act)"
        }
        
        # 뉴스 검색
        query = search_queries.get(category, search_queries["전체"])
        response = newsapi.get_everything(
            q=query,
            from_param=from_date.strftime('%Y-%m-%d'),
            to=to_date.strftime('%Y-%m-%d'),
            sort_by='publishedAt',
            page_size=30  # 한 번에 가져올 뉴스 수
        )
        
        if response['status'] == 'ok' and response['articles']:
            articles = response['articles']
            df = pd.DataFrame(articles)
            
            # 중복 제거 및 정렬
            df = df.drop_duplicates(subset=['title'])
            df = df.sort_values('publishedAt', ascending=False)
            
            # 한글 기사 우선 정렬 (description에 한글이 포함된 기사)
            def has_korean(text):
                if not isinstance(text, str):
                    return False
                return any(ord('가') <= ord(char) <= ord('힣') for char in text)
            
            df['is_korean'] = df['description'].apply(has_korean)
            df = df.sort_values(['is_korean', 'publishedAt'], ascending=[False, False])
            df = df.drop('is_korean', axis=1)
            
            return df
        else:
            st.warning(f"'{category}' 카테고리의 뉴스를 찾을 수 없습니다. 다른 카테고리를 선택해주세요.")
            return None
            
    except Exception as e:
        st.error(f"뉴스를 가져오는 중 오류가 발생했습니다: {str(e)}")
        return get_sample_news()  # 에러 발생 시 샘플 데이터 반환

def categorize_news(article):
    """뉴스 기사 카테고리 분류"""
    title = article['title'].lower()
    description = str(article['description']).lower()
    content = title + " " + description
    
    if any(keyword in content for keyword in ['실적', '매출', '영업이익', '투자', '주가']):
        return '기업/재무'
    elif any(keyword in content for keyword in ['기술', '공정', '개발', '나노', '연구']):
        return '기술/연구'
    elif any(keyword in content for keyword in ['시장', '수요', '공급', '전망', '예측']):
        return '시장/산업'
    elif any(keyword in content for keyword in ['정책', '규제', '지원', 'chips act', '보조금']):
        return '정책/규제'
    else:
        return '기타'

def simple_summarize(text, max_sentences=3):
    """간단한 텍스트 요약 함수"""
    try:
        if not text:
            return "내용이 없습니다."
            
        # 문장 단위로 분리
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        # 중요 문장 선택 (첫 번째 문장과 마지막 문장 포함)
        if len(sentences) <= max_sentences:
            return '. '.join(sentences) + '.'
        else:
            summary = [sentences[0]]
            if max_sentences > 2:
                middle = len(sentences) // 2
                summary.append(sentences[middle])
            if len(sentences) > 1:
                summary.append(sentences[-1])
            return '. '.join(summary) + '.'
            
    except Exception as e:
        st.warning(f"텍스트 요약 중 오류가 발생했습니다: {str(e)}")
        return text

def show_news():
    """반도체 관련 뉴스를 표시하는 함수"""
    st.title("반도체 산업 뉴스")
    
    # NewsAPI 키 설정
    api_key = st.secrets["NEWSAPI_KEY"]
    
    # 뉴스 카테고리 선택
    categories = [
        "전체",
        "기업 동향",
        "시장 동향",
        "기술 동향",
        "정책"
    ]
    
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_category = st.selectbox(
            "뉴스 카테고리 선택",
            categories
        )
    
    with col2:
        days = st.slider("조회 기간 (일)", 1, 30, 7)
    
    # 뉴스 데이터 가져오기
    with st.spinner("뉴스를 불러오는 중..."):
        news_df = fetch_news(api_key, selected_category, days)
        
        if news_df is not None and not news_df.empty:
            # 뉴스 카테고리 분류
            news_df['category'] = news_df.apply(categorize_news, axis=1)
            
            # 카테고리별 탭 생성
            unique_categories = sorted(news_df['category'].unique())
            tabs = st.tabs(unique_categories)
            
            # 각 카테고리별 뉴스 표시
            for tab, category in zip(tabs, unique_categories):
                with tab:
                    category_news = news_df[news_df['category'] == category]
                    for _, article in category_news.iterrows():
                        with st.expander(article['title']):
                            # 뉴스 정보 표시
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown(f"**출처**: {article['source']['name']}")
                            with col2:
                                published_at = pd.to_datetime(article['publishedAt']).strftime('%Y-%m-%d %H:%M')
                                st.markdown(f"**작성일**: {published_at}")
                            
                            # 원문과 요약문 탭으로 구분
                            content_tabs = st.tabs(["원문", "요약"])
                            
                            with content_tabs[0]:
                                if article['description']:
                                    st.markdown(article['description'])
                                if article['url']:
                                    st.markdown(f"[기사 원문 보기]({article['url']})")
                            
                            with content_tabs[1]:
                                if article['description']:
                                    summary = simple_summarize(article['description'])
                                    st.markdown(summary)
                                else:
                                    st.info("요약할 내용이 없습니다.")
        else:
            st.info("표시할 뉴스가 없습니다. 다른 카테고리나 기간을 선택해보세요.")
    
    # 주의사항 표시
    st.markdown("---")
    st.caption("* 뉴스 데이터는 NewsAPI를 통해 실시간으로 제공됩니다.")
    st.caption("* 뉴스는 제목과 내용을 기반으로 자동 분류됩니다.")
    st.caption("* 요약은 주요 문장을 추출하여 제공됩니다.") 