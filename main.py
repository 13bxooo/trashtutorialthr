import streamlit as st
import pandas as pd
import requests

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


# ============================================================
# 1. 페이지 설정
# ============================================================

st.set_page_config(
    page_title="BOX OFFICE AI ANALYST",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 2. 색상
# ============================================================

NAVY = "#14213D"
BLACK = "#0A0A0A"
WHITE = "#FFFFFF"
GRAY = "#8A8F98"


# ============================================================
# 3. HTML 출력 함수
# ============================================================
# st.markdown()이 아니라 st.html()을 사용합니다.
# 따라서 <div> 등이 코드처럼 표시되지 않습니다.

def render_html(html):
    st.html(html)


# ============================================================
# 4. 전체 CSS
# ============================================================

st.html(
    f"""
    <style>

    .stApp {{
        background: {WHITE};
    }}

    .block-container {{
        max-width: 1400px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }}

    /* -----------------------------------------
       메인 제목
       ----------------------------------------- */

    .main-title {{
        font-family: Arial, sans-serif;
        font-size: 3.2rem;
        font-weight: 900;
        line-height: 0.95;
        letter-spacing: -0.06em;
        color: {BLACK};
    }}

    .sub-title {{
        margin-top: 18px;
        color: {GRAY};
        font-family: Arial, sans-serif;
        font-size: 0.85rem;
        letter-spacing: 0.08em;
    }}

    .navy-line {{
        width: 55px;
        height: 4px;
        background: {NAVY};
        border-radius: 10px;
        margin-top: 18px;
    }}

    /* -----------------------------------------
       섹션 제목
       ----------------------------------------- */

    .section-title {{
        font-family: Arial, sans-serif;
        font-size: 1.4rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        color: {BLACK};
        margin: 30px 0 15px 0;
    }}

    /* -----------------------------------------
       1위 영화 카드
       ----------------------------------------- */

    .hero-card {{
        background: {BLACK};
        border-radius: 24px;
        padding: 34px;
        margin-top: 30px;
        margin-bottom: 30px;
    }}

    .hero-rank {{
        color: #AEB5C1;
        font-family: Arial, sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.14em;
    }}

    .hero-movie {{
        color: white;
        font-family: Arial, sans-serif;
        font-size: 2.4rem;
        font-weight: 900;
        letter-spacing: -0.06em;
        margin-top: 10px;
        margin-bottom: 18px;
    }}

    .hero-info {{
        color: #B9BDC5;
        font-size: 0.88rem;
        margin-top: 18px;
    }}

    /* -----------------------------------------
       상태 배지
       ----------------------------------------- */

    .badge {{
        display: inline-block;
        background: {NAVY};
        color: white;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 0.7rem;
        font-weight: 800;
        letter-spacing: 0.05em;
    }}

    /* -----------------------------------------
       KPI 카드
       ----------------------------------------- */

    .kpi-card {{
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 18px;
        padding: 24px;
        min-height: 135px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.035);
    }}

    .kpi-label {{
        color: {GRAY};
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.06em;
        margin-bottom: 10px;
    }}

    .kpi-value {{
        color: {BLACK};
        font-size: 1.65rem;
        font-weight: 900;
        letter-spacing: -0.05em;
    }}

    .kpi-desc {{
        color: {GRAY};
        font-size: 0.78rem;
        margin-top: 8px;
    }}

    /* -----------------------------------------
       AI 분석 카드
       ----------------------------------------- */

    .analysis-card {{
        background: #F7F8FA;
        border-left: 5px solid {NAVY};
        border-radius: 0 16px 16px 0;
        padding: 20px 24px;
        margin: 10px 0;
    }}

    .analysis-title {{
        color: {NAVY};
        font-size: 0.76rem;
        font-weight: 900;
        letter-spacing: 0.08em;
        margin-bottom: 7px;
    }}

    .analysis-text {{
        color: #252525;
        font-size: 0.94rem;
        line-height: 1.65;
    }}

    /* -----------------------------------------
       하단
       ----------------------------------------- */

    .footer {{
        text-align: center;
        color: #999999;
        font-size: 0.75rem;
        line-height: 1.8;
        padding: 20px;
    }}

    </style>
    """
)


# ============================================================
# 5. 제목
# ============================================================

render_html(
    f"""
    <div class="main-title">
        BOX OFFICE<br>
        AI ANALYST
    </div>

    <div class="navy-line"></div>

    <div class="sub-title">
        KOBIS DAILY BOX OFFICE · DATA-DRIVEN MOVIE ANALYSIS
    </div>
    """
)


# ============================================================
# 6. 한국 시간 기준 어제 계산
# ============================================================

kst = ZoneInfo("Asia/Seoul")

now_kst = datetime.now(kst)

yesterday = now_kst - timedelta(days=1)

target_date = yesterday.strftime("%Y%m%d")

display_date = yesterday.strftime("%Y년 %m월 %d일")


# ============================================================
# 7. KOBIS API
# ============================================================

API_URL = (
    "https://www.kobis.or.kr/"
    "kobisopenapi/webservice/rest/boxoffice/"
    "searchDailyBoxOfficeList.json"
)


# ============================================================
# 8. 인증키
# ============================================================

try:

    KOBIS_KEY = st.secrets["KOBIS_KEY"]

except Exception:

    st.error("KOBIS API 인증키를 찾을 수 없습니다.")

    st.info(
        "Streamlit Cloud → Settings → Secrets에서 "
        "`KOBIS_KEY`가 등록되어 있는지 확인하세요."
    )

    st.stop()


# ============================================================
# 9. API 요청
# ============================================================

params = {
    "key": KOBIS_KEY,
    "targetDt": target_date
}


try:

    response = requests.get(
        API_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

except requests.exceptions.Timeout:

    st.error("KOBIS API 요청 시간이 초과되었습니다.")

    st.info(
        "KOBIS 서버가 응답하지 않았을 수 있습니다. "
        "잠시 후 다시 시도해 주세요."
    )

    st.stop()

except requests.exceptions.RequestException as e:

    st.error("KOBIS API에 연결할 수 없습니다.")

    st.info(
        "인터넷 연결 또는 KOBIS API 상태를 확인해 주세요.\n\n"
        f"오류 내용: {e}"
    )

    st.stop()

except ValueError:

    st.error("KOBIS API 응답을 읽을 수 없습니다.")

    st.info(
        "KOBIS API가 정상적인 JSON 데이터를 반환하는지 확인해 주세요."
    )

    st.stop()


# ============================================================
# 10. KOBIS 오류 확인
# ============================================================

if "faultInfo" in data:

    fault = data["faultInfo"]

    st.error("KOBIS API에서 오류를 반환했습니다.")

    if isinstance(fault, dict):

        code = fault.get(
            "errorCode",
            "알 수 없음"
        )

        message = fault.get(
            "errorMessage",
            "오류 메시지가 없습니다."
        )

        st.info(
            f"오류 코드: {code}\n\n"
            f"오류 내용: {message}\n\n"
            "KOBIS_KEY가 정확한지 확인해 주세요."
        )

    st.stop()


# ============================================================
# 11. 데이터 확인
# ============================================================

if "boxOfficeResult" not in data:

    st.error("박스오피스 데이터를 찾을 수 없습니다.")

    st.info(
        "KOBIS API의 응답 또는 서버 상태를 확인해 주세요."
    )

    st.stop()


movie_list = data[
    "boxOfficeResult"
].get(
    "dailyBoxOfficeList",
    []
)


if not movie_list:

    st.warning(
        f"{display_date} 박스오피스 데이터가 없습니다."
    )

    st.info(
        "다음 항목을 확인해 주세요.\n\n"
        "• 해당 날짜의 데이터가 KOBIS에서 집계되었는지\n"
        "• API 인증키가 정상인지\n"
        "• KOBIS API 서버에 문제가 없는지\n"
        "• 잠시 후 다시 시도했을 때도 같은지"
    )

    st.stop()


# ============================================================
# 12. 데이터 정리
# ============================================================

rows = []


for movie in movie_list:

    try:

        rank = int(movie.get("rank", 0))

        rank_inten = int(
            movie.get("rankInten", 0)
        )

        audi_cnt = int(
            movie.get("audiCnt", 0)
        )

        audi_acc = int(
            movie.get("audiAcc", 0)
        )

        scrn_cnt = int(
            movie.get("scrnCnt", 0)
        )

        show_cnt = int(
            movie.get("showCnt", 0)
        )

    except (ValueError, TypeError):

        rank = 0
        rank_inten = 0
        audi_cnt = 0
        audi_acc = 0
        scrn_cnt = 0
        show_cnt = 0


    # 스크린당 관객수
    if scrn_cnt > 0:

        audience_per_screen = (
            audi_cnt / scrn_cnt
        )

    else:

        audience_per_screen = 0


    # 회차당 관객수
    if show_cnt > 0:

        audience_per_show = (
            audi_cnt / show_cnt
        )

    else:

        audience_per_show = 0


    rows.append(
        {
            "순위": rank,
            "순위변화": rank_inten,
            "영화명": movie.get(
                "movieNm",
                "-"
            ),
            "개봉일": movie.get(
                "openDt",
                "-"
            ),
            "관객수": audi_cnt,
            "누적관객": audi_acc,
            "스크린수": scrn_cnt,
            "상영횟수": show_cnt,
            "스크린당 관객수": audience_per_screen,
            "회차당 관객수": audience_per_show
        }
    )


df = pd.DataFrame(rows)

df = (
    df
    .sort_values("순위")
    .reset_index(drop=True)
)


# ============================================================
# 13. 분석 함수
# ============================================================

def analyze_movie(movie, all_movies):

    rank = movie["순위"]

    rank_change = movie["순위변화"]

    audience = movie["관객수"]

    per_screen = movie[
        "스크린당 관객수"
    ]


    median_audience = (
        all_movies["관객수"].median()
    )

    median_per_screen = (
        all_movies[
            "스크린당 관객수"
        ].median()
    )


    insights = []


    # 순위 변화
    if rank_change > 0:

        insights.append(
            f"전날보다 {rank_change}계단 상승하며 "
            "순위 상승 흐름을 보이고 있습니다."
        )

    elif rank_change < 0:

        insights.append(
            f"전날보다 {abs(rank_change)}계단 하락했습니다."
        )

    else:

        insights.append(
            "전날과 동일한 순위를 유지하고 있습니다."
        )


    # 관객수
    if audience >= median_audience * 2:

        insights.append(
            "일일 관객수가 전체 영화의 중앙값보다 "
            "상당히 높아 높은 관객 집중도를 보입니다."
        )

    elif audience >= median_audience:

        insights.append(
            "일일 관객수가 전체 영화의 중앙값 이상입니다."
        )

    else:

        insights.append(
            "일일 관객수는 전체 영화의 중앙값보다 낮은 편입니다."
        )


    # 스크린 효율
    if per_screen >= median_per_screen * 1.5:

        insights.append(
            "스크린당 관객수가 높은 편으로, "
            "상영관 대비 관객 집중도가 높게 나타납니다."
        )

    elif per_screen >= median_per_screen:

        insights.append(
            "스크린당 관객수가 전체 영화의 중앙값 이상입니다."
        )

    else:

        insights.append(
            "스크린당 관객수는 상대적으로 낮은 편입니다."
        )


    # 종합 상태
    if (
        rank <= 3
        and per_screen >= median_per_screen
    ):

        status = "HIGH MOMENTUM"

    elif rank <= 5:

        status = "STABLE"

    elif rank_change > 2:

        status = "RISING"

    elif rank_change < -2:

        status = "FALLING"

    else:

        status = "NORMAL"


    return status, insights


# ============================================================
# 14. 1위 영화
# ============================================================

first_movie = df.iloc[0]

status, first_insights = analyze_movie(
    first_movie,
    df
)


# ============================================================
# 15. HERO
# ============================================================

render_html(
    f"""
    <div class="hero-card">

        <div class="hero-rank">
            NO. 01 · {display_date}
        </div>

        <div class="hero-movie">
            {first_movie["영화명"]}
        </div>

        <div>
            <span class="badge">
                {status}
            </span>
        </div>

        <div class="hero-info">
            개봉일 {first_movie["개봉일"]}
            &nbsp; · &nbsp;
            {first_movie["스크린수"]:,}개 스크린
            &nbsp; · &nbsp;
            누적 {first_movie["누적관객"]:,}명
        </div>

    </div>
    """
)


# ============================================================
# 16. KEY PERFORMANCE
# ============================================================

render_html(
    """
    <div class="section-title">
        KEY PERFORMANCE
    </div>
    """
)


col1, col2, col3, col4 = st.columns(4)


# ------------------------------------------------------------
# 카드 1
# ------------------------------------------------------------

with col1:

    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                DAILY AUDIENCE
            </div>

            <div class="kpi-value">
                {first_movie["관객수"]:,}
            </div>

            <div class="kpi-desc">
                어제 관객수
            </div>

        </div>
        """
    )


# ------------------------------------------------------------
# 카드 2
# ------------------------------------------------------------

with col2:

    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                TOTAL AUDIENCE
            </div>

            <div class="kpi-value">
                {first_movie["누적관객"]:,}
            </div>

            <div class="kpi-desc">
                누적 관객수
            </div>

        </div>
        """
    )


# ------------------------------------------------------------
# 카드 3
# ------------------------------------------------------------

with col3:

    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                AUDIENCE / SCREEN
            </div>

            <div class="kpi-value">
                {first_movie["스크린당 관객수"]:,.1f}
            </div>

            <div class="kpi-desc">
                스크린 1개당 관객수
            </div>

        </div>
        """
    )


# ------------------------------------------------------------
# 카드 4
# ------------------------------------------------------------

with col4:

    rank_change = first_movie["순위변화"]


    if rank_change > 0:

        change_text = (
            f"▲ {rank_change}"
        )

    elif rank_change < 0:

        change_text = (
            f"▼ {abs(rank_change)}"
        )

    else:

        change_text = "—"


    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                RANK CHANGE
            </div>

            <div class="kpi-value">
                {change_text}
            </div>

            <div class="kpi-desc">
                전일 대비 순위 변화
            </div>

        </div>
        """
    )


# ============================================================
# 17. AI ANALYSIS
# ============================================================

render_html(
    """
    <div class="section-title">
        AI ANALYSIS
    </div>
    """
)


st.caption(
    "KOBIS 데이터를 바탕으로 관객수·순위 변화·스크린 효율을 분석했습니다."
)


for i, insight in enumerate(
    first_insights
):

    render_html(
        f"""
        <div class="analysis-card">

            <div class="analysis-title">
                INSIGHT {i + 1:02d}
            </div>

            <div class="analysis-text">
                {insight}
            </div>

        </div>
        """
    )


# ============================================================
# 18. BOX OFFICE LANDSCAPE
# ============================================================

st.markdown("---")


render_html(
    """
    <div class="section-title">
        BOX OFFICE LANDSCAPE
    </div>
    """
)


top5 = (
    df
    .sort_values(
        "관객수",
        ascending=False
    )
    .head(5)
    .copy()
)


chart_data = (
    top5
    .set_index("영화명")
    [["관객수"]]
)


st.bar_chart(
    chart_data,
    horizontal=True
)


# ============================================================
# 19. MOVIE DEEP ANALYSIS
# ============================================================

render_html(
    """
    <div class="section-title">
        MOVIE DEEP ANALYSIS
    </div>
    """
)


movie_names = df[
    "영화명"
].tolist()


selected_movie_name = st.selectbox(
    "분석할 영화를 선택하세요.",
    movie_names
)


selected_movie = (
    df[
        df["영화명"]
        == selected_movie_name
    ]
    .iloc[0]
)


selected_status, selected_insights = (
    analyze_movie(
        selected_movie,
        df
    )
)


# ============================================================
# 20. 선택 영화 카드
# ============================================================

left, right = st.columns(2)


with left:

    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                SELECTED MOVIE
            </div>

            <div class="kpi-value">
                {selected_movie["영화명"]}
            </div>

            <div style="margin-top:15px;">
                <span class="badge">
                    {selected_status}
                </span>
            </div>

            <div class="kpi-desc">
                현재 순위 {selected_movie["순위"]}위
                · 개봉일 {selected_movie["개봉일"]}
            </div>

        </div>
        """
    )


with right:

    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                AUDIENCE EFFICIENCY
            </div>

            <div class="kpi-value">
                {selected_movie["스크린당 관객수"]:,.1f}
            </div>

            <div class="kpi-desc">
                스크린당 관객수
            </div>

            <div style="margin-top:12px; color:#777;">
                총 {selected_movie["스크린수"]:,}개 스크린
            </div>

        </div>
        """
    )


# ============================================================
# 21. 선택 영화 분석
# ============================================================

for i, insight in enumerate(
    selected_insights
):

    render_html(
        f"""
        <div class="analysis-card">

            <div class="analysis-title">
                ANALYST NOTE {i + 1:02d}
            </div>

            <div class="analysis-text">
                {insight}
            </div>

        </div>
        """
    )


# ============================================================
# 22. FULL DATA
# ============================================================

st.markdown("---")


render_html(
    """
    <div class="section-title">
        FULL DATA
    </div>
    """
)


display_df = df[
    [
        "순위",
        "영화명",
        "개봉일",
        "관객수",
        "누적관객",
        "스크린수",
        "상영횟수",
        "스크린당 관객수"
    ]
].copy()


display_df["관객수"] = (
    display_df["관객수"]
    .map(lambda x: f"{x:,}")
)


display_df["누적관객"] = (
    display_df["누적관객"]
    .map(lambda x: f"{x:,}")
)


display_df["스크린수"] = (
    display_df["스크린수"]
    .map(lambda x: f"{x:,}")
)


display_df["상영횟수"] = (
    display_df["상영횟수"]
    .map(lambda x: f"{x:,}")
)


display_df["스크린당 관객수"] = (
    display_df["스크린당 관객수"]
    .map(lambda x: f"{x:,.1f}")
)


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 23. FOOTER
# ============================================================

render_html(
    """
    <div class="footer">
        BOX OFFICE AI ANALYST<br>
        Data source · KOBIS Daily Box Office
    </div>
    """
)
