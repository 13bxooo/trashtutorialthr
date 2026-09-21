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
# 2. 기본 설정
# ============================================================

NAVY = "#14213D"
BLACK = "#0A0A0A"
WHITE = "#FFFFFF"
GRAY = "#858A93"

BOXOFFICE_URL = (
    "https://www.kobis.or.kr/"
    "kobisopenapi/webservice/rest/boxoffice/"
    "searchDailyBoxOfficeList.json"
)

MOVIE_INFO_URL = (
    "https://www.kobis.or.kr/"
    "kobisopenapi/webservice/rest/movie/"
    "searchMovieInfo.json"
)


# ============================================================
# 3. HTML 출력 함수
# ============================================================

def render_html(html):
    """
    Streamlit에서 HTML을 코드가 아니라 실제 화면으로 표시합니다.
    """
    st.html(html)


# ============================================================
# 4. 전체 CSS
# ============================================================

st.html(
    f"""
    <style>

    .stApp {{
        background: #FFFFFF;
    }}

    .block-container {{
        max-width: 1400px;
        padding-top: 2.5rem;
        padding-bottom: 5rem;
    }}

    /* -------------------------
       제목
       ------------------------- */

    .main-title {{
        font-family: Arial, sans-serif;
        font-size: 3.3rem;
        font-weight: 900;
        line-height: 0.92;
        letter-spacing: -0.065em;
        color: {BLACK};
    }}

    .sub-title {{
        margin-top: 18px;
        color: {GRAY};
        font-family: Arial, sans-serif;
        font-size: 0.78rem;
        letter-spacing: 0.12em;
    }}

    .navy-line {{
        width: 55px;
        height: 4px;
        background: {NAVY};
        border-radius: 20px;
        margin-top: 20px;
    }}

    /* -------------------------
       섹션
       ------------------------- */

    .section-title {{
        font-family: Arial, sans-serif;
        font-size: 1.35rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        color: {BLACK};
        margin: 32px 0 14px 0;
    }}

    .section-sub {{
        color: {GRAY};
        font-size: 0.82rem;
        margin-bottom: 16px;
    }}

    /* -------------------------
       Hero
       ------------------------- */

    .hero-card {{
        background: {BLACK};
        border-radius: 26px;
        padding: 38px;
        margin-top: 32px;
        margin-bottom: 32px;
    }}

    .hero-rank {{
        color: #AAB0BA;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.15em;
    }}

    .hero-movie {{
        color: white;
        font-size: 2.6rem;
        font-weight: 900;
        letter-spacing: -0.065em;
        margin-top: 12px;
        margin-bottom: 18px;
    }}

    .hero-info {{
        color: #B8BDC6;
        font-size: 0.84rem;
        margin-top: 20px;
    }}

    /* -------------------------
       Badge
       ------------------------- */

    .badge {{
        display: inline-block;
        background: {NAVY};
        color: white;
        padding: 7px 13px;
        border-radius: 999px;
        font-size: 0.68rem;
        font-weight: 900;
        letter-spacing: 0.07em;
    }}

    /* -------------------------
       KPI
       ------------------------- */

    .kpi-card {{
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 18px;
        padding: 24px;
        min-height: 145px;
        box-shadow: 0 5px 22px rgba(0,0,0,0.035);
    }}

    .kpi-label {{
        color: {GRAY};
        font-size: 0.68rem;
        font-weight: 900;
        letter-spacing: 0.08em;
        margin-bottom: 10px;
    }}

    .kpi-value {{
        color: {BLACK};
        font-size: 1.65rem;
        font-weight: 900;
        letter-spacing: -0.055em;
    }}

    .kpi-desc {{
        color: {GRAY};
        font-size: 0.76rem;
        margin-top: 8px;
        line-height: 1.5;
    }}

    /* -------------------------
       Analysis
       ------------------------- */

    .analysis-card {{
        background: #F7F8FA;
        border-left: 5px solid {NAVY};
        border-radius: 0 16px 16px 0;
        padding: 20px 25px;
        margin: 10px 0;
    }}

    .analysis-title {{
        color: {NAVY};
        font-size: 0.72rem;
        font-weight: 900;
        letter-spacing: 0.09em;
        margin-bottom: 8px;
    }}

    .analysis-text {{
        color: #242424;
        font-size: 0.9rem;
        line-height: 1.65;
    }}

    /* -------------------------
       Index
       ------------------------- */

    .index-card {{
        background: {BLACK};
        border-radius: 22px;
        padding: 30px;
        color: white;
        min-height: 250px;
    }}

    .index-number {{
        font-size: 4.2rem;
        font-weight: 900;
        letter-spacing: -0.08em;
        line-height: 1;
        margin: 10px 0;
    }}

    .index-label {{
        color: #AEB3BD;
        font-size: 0.7rem;
        letter-spacing: 0.1em;
        font-weight: 800;
    }}

    /* -------------------------
       Hidden performer
       ------------------------- */

    .hidden-card {{
        border: 1px solid #E5E7EB;
        border-radius: 20px;
        padding: 28px;
        background: #FFFFFF;
        box-shadow: 0 5px 20px rgba(0,0,0,0.03);
    }}

    .hidden-rank {{
        color: {NAVY};
        font-size: 0.7rem;
        font-weight: 900;
        letter-spacing: 0.1em;
    }}

    .hidden-name {{
        font-size: 1.6rem;
        font-weight: 900;
        margin-top: 8px;
    }}

    .hidden-number {{
        font-size: 2.6rem;
        font-weight: 900;
        letter-spacing: -0.06em;
        margin-top: 18px;
    }}

    /* -------------------------
       Profile
       ------------------------- */

    .profile-card {{
        border: 1px solid #E5E7EB;
        border-radius: 20px;
        padding: 28px;
        background: white;
        min-height: 260px;
    }}

    .profile-title {{
        font-size: 1.45rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        margin-bottom: 20px;
    }}

    .profile-item {{
        margin: 12px 0;
    }}

    .profile-label {{
        color: {GRAY};
        font-size: 0.67rem;
        font-weight: 900;
        letter-spacing: 0.08em;
    }}

    .profile-value {{
        color: {BLACK};
        font-size: 0.9rem;
        margin-top: 3px;
    }}

    /* -------------------------
       Footer
       ------------------------- */

    .footer {{
        text-align: center;
        color: #999;
        font-size: 0.72rem;
        line-height: 1.8;
        padding: 35px;
    }}

    </style>
    """
)


# ============================================================
# 5. 제목
# ============================================================

render_html(
    """
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
# 6. 한국 시간 기준 날짜
# ============================================================

KST = ZoneInfo("Asia/Seoul")

now_kst = datetime.now(KST)

yesterday = now_kst - timedelta(days=1)

target_date = yesterday.strftime("%Y%m%d")

display_date = yesterday.strftime(
    "%Y년 %m월 %d일"
)


# ============================================================
# 7. API KEY
# ============================================================

try:

    KOBIS_KEY = st.secrets["KOBIS_KEY"]

except Exception:

    st.error("KOBIS API 인증키를 찾을 수 없습니다.")

    st.info(
        "Streamlit Cloud의 Settings → Secrets에서 "
        "`KOBIS_KEY`가 등록되어 있는지 확인하세요."
    )

    st.stop()


# ============================================================
# 8. KOBIS API 요청 함수
# ============================================================

@st.cache_data(ttl=3600)
def get_daily_boxoffice(date_str, api_key):

    response = requests.get(
        BOXOFFICE_URL,
        params={
            "key": api_key,
            "targetDt": date_str
        },
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    if "faultInfo" in data:

        fault = data["faultInfo"]

        message = fault.get(
            "errorMessage",
            "KOBIS API 오류"
        )

        raise RuntimeError(message)

    return data


# ============================================================
# 9. 오늘 데이터 가져오기
# ============================================================

try:

    today_data = get_daily_boxoffice(
        target_date,
        KOBIS_KEY
    )

except Exception as e:

    st.error(
        "KOBIS 박스오피스 데이터를 가져오지 못했습니다."
    )

    st.info(
        "다음 사항을 확인해 주세요.\n\n"
        "• KOBIS_KEY가 정확한지\n"
        "• KOBIS API 서버가 정상인지\n"
        "• 해당 날짜의 박스오피스 데이터가 존재하는지\n\n"
        f"오류 내용: {e}"
    )

    st.stop()


movie_list = (
    today_data
    .get("boxOfficeResult", {})
    .get("dailyBoxOfficeList", [])
)


if not movie_list:

    st.warning(
        f"{display_date} 박스오피스 데이터가 없습니다."
    )

    st.info(
        "KOBIS에서 해당 날짜의 데이터가 아직 집계되지 않았거나 "
        "API 응답을 확인할 필요가 있습니다."
    )

    st.stop()


# ============================================================
# 10. 일일 데이터 → DataFrame
# ============================================================

def convert_movies(movie_list):

    rows = []

    for movie in movie_list:

        def to_int(value):

            try:
                return int(value)
            except:
                return 0

        audi = to_int(
            movie.get("audiCnt")
        )

        screen = to_int(
            movie.get("scrnCnt")
        )

        show = to_int(
            movie.get("showCnt")
        )

        per_screen = (
            audi / screen
            if screen > 0
            else 0
        )

        per_show = (
            audi / show
            if show > 0
            else 0
        )

        rows.append(
            {
                "순위": to_int(movie.get("rank")),
                "순위변화": to_int(
                    movie.get("rankInten")
                ),
                "영화명": movie.get(
                    "movieNm",
                    "-"
                ),
                "개봉일": movie.get(
                    "openDt",
                    "-"
                ),
                "관객수": audi,
                "누적관객": to_int(
                    movie.get("audiAcc")
                ),
                "스크린수": screen,
                "상영횟수": show,
                "스크린당 관객수": per_screen,
                "회차당 관객수": per_show,
                "영화코드": movie.get(
                    "movieCd",
                    ""
                )
            }
        )

    return (
        pd.DataFrame(rows)
        .sort_values("순위")
        .reset_index(drop=True)
    )


df = convert_movies(movie_list)


# ============================================================
# 11. 7일치 데이터 가져오기
# ============================================================

@st.cache_data(ttl=3600)
def get_week_data(api_key, yesterday_date):

    result = []

    base_date = datetime.strptime(
        yesterday_date,
        "%Y%m%d"
    )

    for i in range(7):

        date_obj = (
            base_date
            - timedelta(days=i)
        )

        date_str = date_obj.strftime(
            "%Y%m%d"
        )

        try:

            data = get_daily_boxoffice(
                date_str,
                api_key
            )

            movies = (
                data
                .get("boxOfficeResult", {})
                .get("dailyBoxOfficeList", [])
            )

            for movie in movies:

                try:
                    audience = int(
                        movie.get(
                            "audiCnt",
                            0
                        )
                    )
                except:
                    audience = 0

                try:
                    rank = int(
                        movie.get(
                            "rank",
                            0
                        )
                    )
                except:
                    rank = 0

                try:
                    screen = int(
                        movie.get(
                            "scrnCnt",
                            0
                        )
                    )
                except:
                    screen = 0

                result.append(
                    {
                        "날짜": date_str,
                        "영화명": movie.get(
                            "movieNm",
                            "-"
                        ),
                        "관객수": audience,
                        "순위": rank,
                        "스크린수": screen
                    }
                )

        except Exception:
            continue

    return pd.DataFrame(result)


week_df = get_week_data(
    KOBIS_KEY,
    target_date
)


# ============================================================
# 12. 1위 영화
# ============================================================

first_movie = df.iloc[0]


# ============================================================
# 13. 분석 함수
# ============================================================

def analyze_movie(movie, all_movies):

    rank = movie["순위"]

    rank_change = movie["순위변화"]

    audience = movie["관객수"]

    efficiency = movie[
        "스크린당 관객수"
    ]

    median_audience = (
        all_movies["관객수"].median()
    )

    median_efficiency = (
        all_movies[
            "스크린당 관객수"
        ].median()
    )

    insights = []

    # 순위
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

    # 관객
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

    # 효율
    if efficiency >= median_efficiency * 1.5:

        insights.append(
            "스크린당 관객수가 매우 높은 편으로, "
            "상영관 대비 관객 집중도가 높게 나타납니다."
        )

    elif efficiency >= median_efficiency:

        insights.append(
            "스크린당 관객수가 전체 영화의 중앙값 이상입니다."
        )

    else:

        insights.append(
            "스크린당 관객수는 상대적으로 낮은 편입니다."
        )

    # 상태
    if (
        rank <= 3
        and efficiency >= median_efficiency
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
# 14. BOX OFFICE INDEX
# ============================================================

def calculate_index(movie, all_movies):

    # 관객수 상대값
    audience_score = (
        movie["관객수"]
        / all_movies["관객수"].max()
        * 100
    )

    # 스크린 효율 상대값
    efficiency_max = (
        all_movies[
            "스크린당 관객수"
        ].max()
    )

    if efficiency_max > 0:

        efficiency_score = (
            movie["스크린당 관객수"]
            / efficiency_max
            * 100
        )

    else:

        efficiency_score = 0

    # 순위 점수
    rank_score = max(
        0,
        100 - (
            movie["순위"] - 1
        ) * 5
    )

    # 순위 변화
    momentum_score = min(
        100,
        max(
            0,
            50 + movie["순위변화"] * 10
        )
    )

    score = (
        audience_score * 0.35
        + efficiency_score * 0.25
        + rank_score * 0.25
        + momentum_score * 0.15
    )

    return round(
        min(100, score)
    )


first_index = calculate_index(
    first_movie,
    df
)


# ============================================================
# 15. HERO
# ============================================================

hero_status, hero_insights = analyze_movie(
    first_movie,
    df
)

render_html(
    f"""
    <div class="hero-card">

        <div class="hero-rank">
            NO. 01 · {display_date}
        </div>

        <div class="hero-movie">
            {first_movie["영화명"]}
        </div>

        <span class="badge">
            {hero_status}
        </span>

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

c1, c2, c3, c4 = st.columns(4)


with c1:

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


with c2:

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


with c3:

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


with c4:

    if first_movie["순위변화"] > 0:
        change = f"▲ {first_movie['순위변화']}"

    elif first_movie["순위변화"] < 0:
        change = f"▼ {abs(first_movie['순위변화'])}"

    else:
        change = "—"

    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                RANK CHANGE
            </div>

            <div class="kpi-value">
                {change}
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

    <div class="section-sub">
        KOBIS 데이터를 기반으로 관객수·순위·스크린 효율을 분석합니다.
    </div>
    """
)


for i, insight in enumerate(
    hero_insights
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

    <div class="section-sub">
        오늘의 관객수 상위 5편과 전체 관객 집중도를 확인합니다.
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
# 19. 관객 집중도
# ============================================================

total_audience = df["관객수"].sum()

top5_audience = top5["관객수"].sum()

if total_audience > 0:

    concentration = (
        top5_audience
        / total_audience
        * 100
    )

else:

    concentration = 0


cc1, cc2 = st.columns(2)


with cc1:

    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                TOP 5 AUDIENCE SHARE
            </div>

            <div class="kpi-value">
                {concentration:.1f}%
            </div>

            <div class="kpi-desc">
                전체 집계 영화 관객 중
                상위 5편이 차지하는 비율
            </div>

        </div>
        """
    )


with cc2:

    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                DAILY MARKET
            </div>

            <div class="kpi-value">
                {total_audience:,}
            </div>

            <div class="kpi-desc">
                집계된 영화의 총 일일 관객수
            </div>

        </div>
        """
    )


# ============================================================
# 20. 7-DAY TREND
# ============================================================

st.markdown("---")

render_html(
    """
    <div class="section-title">
        7-DAY TREND
    </div>

    <div class="section-sub">
        최근 7일 동안 선택한 영화의 관객수와 순위 변화를 추적합니다.
    </div>
    """
)


week_movies = sorted(
    week_df["영화명"].unique().tolist()
)


default_movie = first_movie["영화명"]

if default_movie in week_movies:

    default_index = (
        week_movies.index(default_movie)
    )

else:

    default_index = 0


trend_movie = st.selectbox(
    "추이를 확인할 영화를 선택하세요.",
    week_movies,
    index=default_index,
    key="trend_movie"
)


selected_week = (
    week_df[
        week_df["영화명"]
        == trend_movie
    ]
    .copy()
)


selected_week["날짜표시"] = pd.to_datetime(
    selected_week["날짜"],
    format="%Y%m%d"
).dt.strftime("%m/%d")


selected_week = (
    selected_week
    .sort_values("날짜")
)


t1, t2 = st.columns(2)


with t1:

    st.caption("DAILY AUDIENCE")

    audience_chart = (
        selected_week
        .set_index("날짜표시")
        [["관객수"]]
    )

    st.line_chart(
        audience_chart
    )


with t2:

    st.caption("RANK TREND")

    rank_chart = (
        selected_week
        .set_index("날짜표시")
        [["순위"]]
    )

    st.line_chart(
        rank_chart
    )


# ============================================================
# 21. HIDDEN PERFORMER
# ============================================================

st.markdown("---")

render_html(
    """
    <div class="section-title">
        HIDDEN PERFORMER
    </div>

    <div class="section-sub">
        단순 관객수 순위와 다른 관점에서 스크린 효율이 높은 영화를 찾습니다.
    </div>
    """
)


hidden = (
    df
    .sort_values(
        "스크린당 관객수",
        ascending=False
    )
    .iloc[0]
)


hc1, hc2 = st.columns([1, 2])


with hc1:

    render_html(
        f"""
        <div class="hidden-card">

            <div class="hidden-rank">
                HIGHEST AUDIENCE / SCREEN
            </div>

            <div class="hidden-name">
                {hidden["영화명"]}
            </div>

            <div class="hidden-number">
                {hidden["스크린당 관객수"]:,.1f}
            </div>

            <div class="kpi-desc">
                스크린당 관객수
            </div>

        </div>
        """
    )


with hc2:

    render_html(
        f"""
        <div class="hidden-card">

            <div class="hidden-rank">
                WHY IT STANDS OUT
            </div>

            <div style="font-size:1.15rem;font-weight:800;margin-top:10px;">
                {hidden["순위"]}위 영화지만
                {hidden["스크린수"]:,}개 스크린에서
                스크린당 {hidden["스크린당 관객수"]:,.1f}명의
                관객을 기록했습니다.
            </div>

            <div class="kpi-desc" style="margin-top:15px;">
                전체 박스오피스 순위와
                상영 효율은 서로 다른 모습을 보일 수 있습니다.
            </div>

        </div>
        """
    )


# ============================================================
# 22. BOX OFFICE INDEX
# ============================================================

st.markdown("---")

render_html(
    """
    <div class="section-title">
        BOX OFFICE INDEX
    </div>

    <div class="section-sub">
        관객수·스크린 효율·순위·순위 변화를 조합한 데이터 기반 지표입니다.
    </div>
    """
)


index_movie_name = st.selectbox(
    "지수를 확인할 영화를 선택하세요.",
    df["영화명"].tolist(),
    key="index_movie"
)


index_movie = (
    df[
        df["영화명"]
        == index_movie_name
    ]
    .iloc[0]
)


movie_index = calculate_index(
    index_movie,
    df
)


idx1, idx2 = st.columns([1, 2])


with idx1:

    render_html(
        f"""
        <div class="index-card">

            <div class="index-label">
                BOX OFFICE INDEX
            </div>

            <div class="index-number">
                {movie_index}
            </div>

            <div class="index-label">
                / 100
            </div>

        </div>
        """
    )


with idx2:

    # 세부 지표
    audience_component = round(
        index_movie["관객수"]
        / df["관객수"].max()
        * 100
    )

    efficiency_component = round(
        index_movie["스크린당 관객수"]
        / max(
            df["스크린당 관객수"].max(),
            1
        )
        * 100
    )

    rank_component = max(
        0,
        100 - (
            index_movie["순위"] - 1
        ) * 5
    )

    render_html(
        f"""
        <div class="profile-card">

            <div class="profile-title">
                {index_movie["영화명"]}
            </div>

            <div class="profile-item">

                <div class="profile-label">
                    AUDIENCE
                </div>

                <div class="profile-value">
                    {audience_component}/100
                </div>

            </div>

            <div class="profile-item">

                <div class="profile-label">
                    SCREEN EFFICIENCY
                </div>

                <div class="profile-value">
                    {efficiency_component}/100
                </div>

            </div>

            <div class="profile-item">

                <div class="profile-label">
                    RANK
                </div>

                <div class="profile-value">
                    {rank_component}/100
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# 23. MOVIE DEEP ANALYSIS
# ============================================================

st.markdown("---")

render_html(
    """
    <div class="section-title">
        MOVIE DEEP ANALYSIS
    </div>

    <div class="section-sub">
        특정 영화를 선택하여 현재 흥행 상태를 자세히 분석합니다.
    </div>
    """
)


selected_name = st.selectbox(
    "분석할 영화를 선택하세요.",
    df["영화명"].tolist(),
    key="deep_movie"
)


selected = (
    df[
        df["영화명"]
        == selected_name
    ]
    .iloc[0]
)


selected_status, selected_insights = (
    analyze_movie(
        selected,
        df
    )
)


dc1, dc2 = st.columns(2)


with dc1:

    render_html(
        f"""
        <div class="profile-card">

            <div class="profile-title">
                {selected["영화명"]}
            </div>

            <span class="badge">
                {selected_status}
            </span>

            <div class="profile-item">
                <div class="profile-label">
                    CURRENT RANK
                </div>

                <div class="profile-value">
                    {selected["순위"]}위
                </div>
            </div>

            <div class="profile-item">
                <div class="profile-label">
                    RELEASE
                </div>

                <div class="profile-value">
                    {selected["개봉일"]}
                </div>
            </div>

        </div>
        """
    )


with dc2:

    render_html(
        f"""
        <div class="profile-card">

            <div class="profile-title">
                AUDIENCE EFFICIENCY
            </div>

            <div class="index-number"
                 style="font-size:3rem;color:{BLACK};">
                {selected["스크린당 관객수"]:,.1f}
            </div>

            <div class="profile-item">
                <div class="profile-label">
                    DAILY AUDIENCE
                </div>

                <div class="profile-value">
                    {selected["관객수"]:,}명
                </div>
            </div>

            <div class="profile-item">
                <div class="profile-label">
                    SCREENS
                </div>

                <div class="profile-value">
                    {selected["스크린수"]:,}개
                </div>
            </div>

        </div>
        """
    )


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
# 24. 영화 상세정보 API
# ============================================================

st.markdown("---")

render_html(
    """
    <div class="section-title">
        MOVIE PROFILE
    </div>

    <div class="section-sub">
        KOBIS 영화정보 API에서 제공하는 작품 정보를 표시합니다.
    </div>
    """
)


@st.cache_data(ttl=86400)
def get_movie_info(movie_code, api_key):

    if not movie_code:

        return None

    response = requests.get(
        MOVIE_INFO_URL,
        params={
            "key": api_key,
            "movieCd": movie_code
        },
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    if "faultInfo" in data:

        return None

    return (
        data
        .get("movieInfoResult", {})
        .get("movieInfo")
    )


movie_info = get_movie_info(
    selected["영화코드"],
    KOBIS_KEY
)


if movie_info:

    directors = ", ".join(
        [
            person.get(
                "peopleNm",
                ""
            )
            for person in movie_info.get(
                "directors",
                []
            )
        ]
    )

    actors = ", ".join(
        [
            person.get(
                "peopleNm",
                ""
            )
            for person in movie_info.get(
                "actors",
                []
            )[:5]
        ]
    )

    genres = ", ".join(
        [
            genre.get(
                "genreNm",
                ""
            )
            for genre in movie_info.get(
                "genres",
                []
            )
        ]
    )

    countries = ", ".join(
        [
            country.get(
                "nationNm",
                ""
            )
            for country in movie_info.get(
                "nations",
                []
            )
        ]
    )

    runtime = movie_info.get(
        "showTm",
        "-"
    )

    production_year = movie_info.get(
        "prdtYear",
        "-"
    )

    p1, p2, p3 = st.columns(3)


    with p1:

        render_html(
            f"""
            <div class="profile-card">

                <div class="profile-title">
                    BASIC INFO
                </div>

                <div class="profile-item">
                    <div class="profile-label">
                        TITLE
                    </div>

                    <div class="profile-value">
                        {movie_info.get("movieNm", "-")}
                    </div>
                </div>

                <div class="profile-item">
                    <div class="profile-label">
                        YEAR
                    </div>

                    <div class="profile-value">
                        {production_year}
                    </div>
                </div>

                <div class="profile-item">
                    <div class="profile-label">
                        RUNTIME
                    </div>

                    <div class="profile-value">
                        {runtime}분
                    </div>
                </div>

            </div>
            """
        )


    with p2:

        render_html(
            f"""
            <div class="profile-card">

                <div class="profile-title">
                    CREATIVE
                </div>

                <div class="profile-item">
                    <div class="profile-label">
                        DIRECTOR
                    </div>

                    <div class="profile-value">
                        {directors or "-"}
                    </div>
                </div>

                <div class="profile-item">
                    <div class="profile-label">
                        ACTORS
                    </div>

                    <div class="profile-value">
                        {actors or "-"}
                    </div>
                </div>

            </div>
            """
        )


    with p3:

        render_html(
            f"""
            <div class="profile-card">

                <div class="profile-title">
                    CLASSIFICATION
                </div>

                <div class="profile-item">
                    <div class="profile-label">
                        GENRE
                    </div>

                    <div class="profile-value">
                        {genres or "-"}
                    </div>
                </div>

                <div class="profile-item">
                    <div class="profile-label">
                        COUNTRY
                    </div>

                    <div class="profile-value">
                        {countries or "-"}
                    </div>
                </div>

            </div>
            """
        )

else:

    st.info(
        "선택한 영화의 상세정보를 KOBIS에서 가져오지 못했습니다. "
        "박스오피스 데이터 자체에는 영향을 주지 않습니다."
    )


# ============================================================
# 25. FULL DATA
# ============================================================

st.markdown("---")

render_html(
    """
    <div class="section-title">
        FULL DATA
    </div>

    <div class="section-sub">
        어제의 전체 일일 박스오피스 데이터입니다.
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
# 26. Footer
# ============================================================

render_html(
    """
    <div class="footer">
        BOX OFFICE AI ANALYST<br>
        Data source · KOBIS Daily Box Office & Movie Information
    </div>
    """
)
