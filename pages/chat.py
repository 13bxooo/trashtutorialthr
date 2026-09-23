import streamlit as st
from openai import OpenAI

# 페이지 기본 설정
st.set_page_config(
    page_title="밀실 - Leonard Wittelsbach",
    page_icon="🕯️",
    layout="centered"
)

# -------------------------------------------------------------
# 로판풍 다크 앰비언트 & 고전 명조 스타일링 (격자 버그 수정판)
# -------------------------------------------------------------
st.markdown("""
<style>
    /* 1. 고전 폰트 로드 */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&family=Cinzel:wght@600;700;800&family=Noto+Serif+KR:wght@300;400;600;700&family=Song+Myung&display=swap');

    html, body, [class*="css"], .stMarkdown, p, div, span, label, input, textarea {
        font-family: 'Song Myung', 'Noto Serif KR', serif !important;
        -webkit-font-smoothing: antialiased;
    }

    /* 2. 전체 배경: 지저분한 격자 패턴을 완전히 제거하고 고급스러운 촛불 암영 그라데이션만 적용 */
    .stApp, 
    [data-testid="stAppViewContainer"], 
    [data-testid="stMain"], 
    [data-testid="stHeader"] {
        background-color: #0d0e11 !important;
        background-image: 
            /* 은은한 촛불 앰버광 (상단 중앙) */
            radial-gradient(circle at 50% 10%, rgba(184, 134, 62, 0.14) 0%, transparent 60%),
            /* 가장자리 깊은 암전 비네팅 */
            radial-gradient(ellipse at center, #14161a 0%, #08090b 100%) !important;
        background-attachment: fixed !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* 3. 헤더 영역 */
    .header-container {
        text-align: center;
        padding-top: 10px;
        margin-bottom: 25px;
    }
    .header-subtitle {
        color: #7d7568;
        font-size: 0.88rem;
        letter-spacing: 1.5px;
        margin-top: 4px;
    }
    .header-deco {
        color: #b89047;
        font-size: 0.75rem;
        letter-spacing: 6px;
        margin-top: 10px;
    }

    /* 상단 Leonard Wittelsbach 버튼 */
    div.stButton > button[key="profile_btn"] {
        background: transparent !important;
        border: none !important;
        color: #dfc288 !important;
        font-family: 'Cinzel Decorative', 'Cinzel', serif !important;
        font-size: 2.1rem !important;
        font-weight: 700 !important;
        letter-spacing: 2.5px !important;
        text-shadow: 0 0 15px rgba(223, 194, 136, 0.35), 0 2px 5px rgba(0,0,0,0.9) !important;
        cursor: pointer !important;
        padding: 0 !important;
        margin: 0 auto !important;
        display: block !important;
        transition: transform 0.2s ease, text-shadow 0.2s ease !important;
    }
    div.stButton > button[key="profile_btn"]:hover {
        transform: scale(1.02);
        color: #fff1d6 !important;
        text-shadow: 0 0 20px rgba(223, 194, 136, 0.6) !important;
    }
    div.stButton > button[key="profile_btn"]:focus {
        outline: none !important;
        box-shadow: none !important;
    }

    /* 4. 브라우저 팝업 모달 */
    div[data-testid="stModal"] > div {
        background-color: #16181e !important;
        border: 1px solid #5a4833 !important;
        border-radius: 6px !important;
        box-shadow: 0 16px 50px rgba(0, 0, 0, 0.95) !important;
        padding: 0 !important;
        overflow: hidden;
    }
    .browser-header {
        background-color: #20232b;
        padding: 8px 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #332b21;
    }
    .browser-tab {
        background: #16181e;
        color: #dcd1c0;
        font-size: 0.85rem;
        padding: 4px 12px;
        border-radius: 5px 5px 0 0;
        border-top: 2px solid #b89047;
    }
    .window-controls {
        color: #7d7568;
        font-family: monospace;
        font-size: 1rem;
        display: flex;
        gap: 10px;
        user-select: none;
    }
    .profile-body {
        padding: 22px;
        color: #dcd1c0;
        background: #16181e;
    }
    .profile-tag {
        color: #b89047;
        font-size: 0.8rem;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }
    .profile-name-kr {
        font-size: 1.4rem;
        font-weight: 700;
        color: #dfc288;
        margin-bottom: 14px;
        border-bottom: 1px solid rgba(184, 144, 71, 0.25);
        padding-bottom: 6px;
    }
    .profile-item {
        margin-bottom: 9px;
        font-size: 0.92rem;
        line-height: 1.55;
    }
    .profile-label {
        color: #998a75;
        font-weight: 600;
        margin-right: 8px;
    }

    /* 5. 말풍선 디자인 */
    [data-testid="stChatMessage"] {
        background-color: rgba(18, 20, 25, 0.85) !important;
        border-radius: 4px !important;
        padding: 14px 18px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(4px);
    }

    /* 레오나르드 말풍선: 차분한 네이비 차콜 + 골드 엣지 */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]),
    [data-testid="stChatMessage"]:nth-child(even) {
        background: linear-gradient(135deg, rgba(20, 24, 33, 0.95) 0%, rgba(14, 16, 22, 0.95) 100%) !important;
        border: 1px solid rgba(184, 144, 71, 0.35) !important;
        border-left: 3px solid #b89047 !important;
    }

    /* 사용자 말풍선: 차콜 브라운 + 앤틱 브론즈 엣지 */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]),
    [data-testid="stChatMessage"]:nth-child(odd) {
        background: linear-gradient(135deg, rgba(26, 22, 19, 0.92) 0%, rgba(16, 14, 12, 0.92) 100%) !important;
        border: 1px solid rgba(133, 107, 77, 0.35) !important;
        border-right: 3px solid #856b4d !important;
    }

    [data-testid="stChatMessage"] p, 
    [data-testid="stChatMessage"] div {
        color: #e2dbcf !important;
        font-size: 1.01rem !important;
        line-height: 1.75 !important;
    }

    [data-testid="stChatMessage"] em {
        color: #b39f83 !important;
        font-style: normal !important;
    }

    /* 6. 입력창 */
    [data-testid="stChatInput"] {
        background-color: #121418 !important;
        border: 1px solid #5a4833 !important;
        border-radius: 4px !important;
        box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.8) !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #b89047 !important;
        box-shadow: 0 0 12px rgba(184, 144, 71, 0.25) !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #efe8dc !important;
        font-size: 0.98rem !important;
        font-family: 'Song Myung', serif !important;
    }
    [data-testid="stChatInput"] button svg {
        fill: #b89047 !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 캐릭터 프로필 모달 (창 띄우기)
# -------------------------------------------------------------
@st.dialog("캐릭터 프로필")
def show_character_profile():
    st.markdown("""
    <div class="browser-header">
        <div class="browser-tab">🗡️ Leonard Wittelsbach.info</div>
        <div class="window-controls">
            <span>—</span>
            <span>□</span>
        </div>
    </div>
    <div class="profile-body">
        <div class="profile-tag">KINGDOM OF BAYERN · 101st ESZETT</div>
        <div class="profile-name-kr">레오나르드 비텔스바흐 (Leonard Wittelsbach)</div>
        <div class="profile-item"><span class="profile-label">신분:</span>바이에른 왕국 왕세자 / 101기 에스체트(Eszett) 단장</div>
        <div class="profile-item"><span class="profile-label">외형:</span>195cm 거구, 밀빛 금발에 푸른 눈, 단정한 군인 체격</div>
        <div class="profile-item"><span class="profile-label">마법:</span>생장(식물 조작) 및 광범위 치유·보호 마법</div>
        <div class="profile-item"><span class="profile-label">성향:</span>철저한 FM, 묵직한 사명감, 그리고 루카스를 향한 위태롭고 깊은 헌신</div>
        <div class="profile-item"><span class="profile-label">비고:</span>오직 이 어두운 밀실에서만 당신에게 왕세자의 가면을 벗고 속내를 털어놓는다.</div>
    </div>
    """, unsafe_allow_html=True)


# -------------------------------------------------------------
# 상단 타이틀 영역
# -------------------------------------------------------------
st.markdown('<div class="header-container">', unsafe_allow_html=True)
if st.button("Leonard Wittelsbach", key="profile_btn", help="클릭하여 단장의 신상 정보를 확인합니다."):
    show_character_profile()

st.markdown("""
    <div class="header-subtitle">외딴 창고 깊숙한 곳, 낡은 촛불만이 둘 사이의 그림자를 길게 늘어뜨린다.</div>
    <div class="header-deco">◆ ❖ ◆</div>
</div>
""", unsafe_allow_html=True)

# Streamlit secrets에서 API 키 로드
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API 키를 찾을 수 없습니다. secrets 설정에서 GEMINI_API_KEY를 등록해 주세요.")
    st.stop()

# Gemini OpenAI 호환 클라이언트
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# AI 시스템 프롬프트 (극도로 간결한 호흡 강제)
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "너는 웹소설 <마법명가 차남으로 살아남는 법>의 등장인물 '레오나르드 비텔스바흐'다. "
        "바이에른 왕세자이자 101기 에스체트 단장이다.\n\n"
        "[공간 및 관계]\n"
        "- 아카데미 외딴 어두운 창고에서 가장 신뢰하는 동료(사용자)와 밀담 중이다.\n"
        "- 상대는 너와 루카스, 엘리아스, 나르케의 관계와 네 속마음을 모두 알고 있으며, 너도 이를 안다.\n\n"
        "[★ 답변 길이 절대 원칙 - 위반 금지]\n"
        "- 답변은 무조건 **'행동 지문 1문장 + 대사 1~2문장'**으로 끝내라.\n"
        "- 절대로 장황한 독백이나 긴 설교를 하지 마라. 과묵한 FM 군인다운 절제되고 묵직한 호흡만 남겨라.\n"
        "- 말투: 나직한 반말(~다, ~군, ~겠어, ~인가?).\n"
        "- 반드시 자연스러운 한국어로 답하라."
    ),
}

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 기록 렌더링
for msg in st.session_state.messages:
    avatar = "🗡️" if msg["role"] == "assistant" else "🕯️"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# 메시지 입력 및 답변 스트리밍
if prompt := st.chat_input("창고의 어둠 속에서 단장에게 말을 건넨다..."):
    with st.chat_message("user", avatar="🕯️"):
        st.write(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🗡️"):
        try:
            api_messages = [SYSTEM_PROMPT] + st.session_state.messages

            # max_tokens=180으로 장문 출력 차단
            response = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=api_messages,
                max_tokens=180,
                temperature=0.7,
                stream=True,
            )

            full_response = st.write_stream(response)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

        except Exception:
            st.error("어둠 속에서 목소리가 흩어졌습니다. 잠시 후 다시 시도해 주세요.")
