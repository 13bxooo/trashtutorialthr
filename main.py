import streamlit as st
import pandas as pd
import requests

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


# ============================================================
# 1. 기본 페이지 설정
# ============================================================

st.set_page_config(
    page_title="어제의 박스오피스",
    page_icon="🎬",
    layout="wide"
)


# ============================================================
# 2. 화면 제목
# ============================================================

st.title("🎬 어제의 박스오피스")
st.caption("영화진흥위원회 영화관입장권통합전산망(KOBIS) 기준")


# ============================================================
# 3. 한국 시간 기준으로 '어제' 계산
# ============================================================
# Streamlit Cloud 서버가 한국 시간이 아닐 수 있기 때문에
# 서버의 현재 시간을 그대로 사용하지 않고 한국 시간(KST)을 사용합니다.

kst = ZoneInfo("Asia/Seoul")

now_kst = datetime.now(kst)
yesterday = now_kst - timedelta(days=1)

# KOBIS API가 요구하는 날짜 형식: YYYYMMDD
target_date = yesterday.strftime("%Y%m%d")

# 화면에 보여줄 날짜
display_date = yesterday.strftime("%Y년 %m월 %d일")


# ============================================================
# 4. KOBIS API 주소
# ============================================================

API_URL = (
    "https://www.kobis.or.kr/"
    "kobisopenapi/webservice/rest/boxoffice/"
    "searchDailyBoxOfficeList.json"
)


# ============================================================
# 5. Secrets에서 API 인증키 가져오기
# ============================================================
# Streamlit Cloud의 Secrets에 다음과 같이 저장해야 합니다.
#
# KOBIS_KEY = "발급받은_인증키"
#
# 실제 인증키를 코드에 직접 적으면 안 됩니다.

try:
    KOBIS_KEY = st.secrets["KOBIS_KEY"]

except Exception:
    st.error("⚠️ KOBIS API 인증키를 불러오지 못했습니다.")

    st.info(
        "다음을 확인해 주세요.\n\n"
        "1. Streamlit Cloud의 앱 설정에서 Secrets를 열었는지 확인하세요.\n"
        "2. Secret 이름이 정확히 `KOBIS_KEY`인지 확인하세요.\n"
        "3. 인증키를 큰따옴표 안에 넣었는지 확인하세요.\n\n"
        "예시:\n"
        "KOBIS_KEY = \"발급받은_인증키\""
    )

    st.stop()


# ============================================================
# 6. KOBIS API 요청
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

    # HTTP 오류가 발생했는지 확인
    response.raise_for_status()

    # JSON으로 변환
    data = response.json()

except requests.exceptions.Timeout:
    st.error("⚠️ KOBIS API 요청 시간이 초과되었습니다.")

    st.info(
        "잠시 후 다시 접속해 보세요. "
        "계속 문제가 발생한다면 KOBIS API 서버 상태나 "
        "인터넷 연결 상태를 확인해 주세요."
    )

    st.stop()

except requests.exceptions.RequestException as e:
    st.error("⚠️ KOBIS API에 접속하지 못했습니다.")

    st.info(
        "다음 항목을 확인해 주세요.\n\n"
        "• 인터넷 연결 상태\n"
        "• KOBIS API 서버 상태\n"
        "• API 주소가 올바른지 여부\n\n"
        f"오류 내용: {e}"
    )

    st.stop()

except ValueError:
    st.error("⚠️ KOBIS API의 응답을 JSON으로 읽지 못했습니다.")

    st.info(
        "KOBIS API 서버에서 정상적인 JSON 응답을 보내고 있는지 "
        "확인해 주세요."
    )

    st.stop()


# ============================================================
# 7. KOBIS API 자체 오류 확인
# ============================================================
# KOBIS는 인증키가 잘못되어도 HTTP 상태코드가 200으로
# 올 수 있습니다.
#
# 따라서 response.raise_for_status()만으로는 인증키 오류를
# 잡을 수 없고, 응답 안에 있는 faultInfo를 확인해야 합니다.

if "faultInfo" in data:

    fault_info = data["faultInfo"]

    st.error("⚠️ KOBIS API에서 오류를 반환했습니다.")

    # KOBIS가 보내준 오류 메시지를 사용자에게 보여줍니다.
    if isinstance(fault_info, dict):

        fault_code = fault_info.get("errorCode", "알 수 없음")
        fault_message = fault_info.get(
            "errorMessage",
            "오류 메시지가 없습니다."
        )

        st.info(
            f"오류 코드: {fault_code}\n\n"
            f"오류 내용: {fault_message}\n\n"
            "특히 인증키를 확인해 주세요. "
            "Streamlit Cloud의 Secrets에서 `KOBIS_KEY`가 "
            "정확하게 설정되어 있는지도 확인하세요."
        )

    else:
        st.info(
            "KOBIS API에서 오류 정보를 반환했습니다. "
            "API 인증키와 Secrets 설정을 확인해 주세요."
        )

    st.stop()


# ============================================================
# 8. boxOfficeResult 확인
# ============================================================

if "boxOfficeResult" not in data:

    st.error("⚠️ 박스오피스 데이터를 찾을 수 없습니다.")

    st.info(
        "KOBIS API의 응답 형식을 확인해 주세요. "
        "잠시 후 다시 시도하거나 KOBIS API 상태를 확인해 주세요."
    )

    st.stop()


boxoffice = data["boxOfficeResult"]


# ============================================================
# 9. 영화 목록 가져오기
# ============================================================

movie_list = boxoffice.get("dailyBoxOfficeList", [])


# 영화 목록이 비어 있는 경우
if not movie_list:

    st.warning("📭 어제의 박스오피스 영화 목록이 없습니다.")

    st.info(
        f"조회 날짜: {display_date}\n\n"
        "다음 항목을 확인해 주세요.\n\n"
        "• KOBIS에서 해당 날짜의 일일 박스오피스가 집계되었는지\n"
        "• KOBIS API가 정상적으로 응답했는지\n"
        "• API 인증키가 정상적으로 작동하는지\n"
        "• 잠시 후 다시 요청했을 때도 같은 결과인지\n\n"
        "특히 서버 오류나 데이터 집계 지연이 있는 경우 "
        "영화 목록이 비어 있을 수 있습니다."
    )

    st.stop()


# ============================================================
# 10. 데이터를 표 형태로 변환
# ============================================================

rows = []

for movie in movie_list:

    rows.append(
        {
            "순위": int(movie.get("rank", 0)),
            "영화명": movie.get("movieNm", "-"),
            "개봉일": movie.get("openDt", "-"),
            "관객수": int(movie.get("audiCnt", 0)),
            "누적관객": int(movie.get("audiAcc", 0)),
            "스크린수": int(movie.get("scrnCnt", 0)),
        }
    )


df = pd.DataFrame(rows)


# ============================================================
# 11. 날짜 표시
# ============================================================

st.subheader(f"📅 {display_date} 박스오피스")

st.caption(
    "KOBIS 일일 박스오피스 기준 · 한국 시간으로 어제 날짜를 자동 계산했습니다."
)


# ============================================================
# 12. 1위 영화 정보
# ============================================================

first_movie = df.iloc[0]


st.markdown("### 🏆 1위 영화")


# 세 개의 지표 카드를 나란히 배치
col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        label="영화",
        value=first_movie["영화명"]
    )


with col2:
    st.metric(
        label="어제 관객수",
        value=f"{first_movie['관객수']:,}명"
    )


with col3:
    st.metric(
        label="누적 관객",
        value=f"{first_movie['누적관객']:,}명"
    )


# ============================================================
# 13. 관객수 상위 5편 막대그래프
# ============================================================

st.markdown("### 📊 관객수 상위 5편")

top5 = (
    df
    .sort_values("관객수", ascending=False)
    .head(5)
    .copy()
)

# 영화명을 인덱스로 사용하면 Streamlit에서
# 가로 막대그래프로 표시하기 편합니다.
chart_data = top5.set_index("영화명")[["관객수"]]

st.bar_chart(
    chart_data,
    horizontal=True
)


# ============================================================
# 14. 전체 박스오피스 표
# ============================================================

st.markdown("### 🎞️ 전체 순위")


# 숫자에 천 단위 쉼표를 넣어서 보기 좋게 표시
display_df = df.copy()

display_df["관객수"] = display_df["관객수"].map(
    lambda x: f"{x:,}"
)

display_df["누적관객"] = display_df["누적관객"].map(
    lambda x: f"{x:,}"
)

display_df["스크린수"] = display_df["스크린수"].map(
    lambda x: f"{x:,}"
)


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 15. 하단 안내
# ============================================================

st.divider()

st.caption(
    "※ 관객수·누적관객·스크린수 등의 값은 KOBIS API에서 제공하는 "
    "일일 박스오피스 데이터를 사용합니다."
)
