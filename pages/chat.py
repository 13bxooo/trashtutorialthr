import streamlit as st
from openai import OpenAI

# 페이지 기본 설정
st.set_page_config(
    page_title="밀실 - Leonard Wittelsbach",
    page_icon="🕯️",
    layout="centered"
)

# -------------------------------------------------------------
# 로판풍 어두운 석조 창고 & 고전 양식 + 브라우저 팝업 스타일링
# -------------------------------------------------------------
st.markdown("""
<style>
    /* 1. 고전 앤틱 & 클래식 명조 웹폰트 로드 */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&family=Cinzel:wght@600;700;800&family=Noto+Serif+KR:wght@300;400;600;700&family=Song+Myung&display=swap');

    /* 모든 텍스트 기본 폰트를 고전 명조체로 지정 */
    html, body, [class*="css"], .stMarkdown, p, div, span, label, input, textarea {
        font-family: 'Song Myung', 'Noto Serif KR', serif !important;
        -webkit-font-smoothing: antialiased;
    }

    /* 2. 전체 배경: 촛불 조명 + 석조 벽돌 패턴 + 다크 차콜 */
    .stApp, 
    [data-testid="stAppViewContainer"], 
    [data-testid="stMain"], 
    [data-testid="stHeader"] {
        background-color: #121316 !important;
        background-image: 
            radial-gradient(circle at 50% 8%, rgba(212, 163, 89, 0.18) 0%, rgba(18, 19, 22, 0) 55%),
            radial-gradient(circle at 50% 50%, transparent 20%, rgba(5, 5, 7, 0.85) 100%),
            url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 0h40v40H0V0zm20 20h20v20H20V20zM0 20h20v20H0V20zm20 0H0V0h20v20z' fill='%23ffffff' fill-opacity='0.015' fill-rule='evenodd'/%3E%3C/svg%3E") !important;
        background-attachment: fixed !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* 3. 상단 헤더 컨테이너 */
    .header-container {
        text-align: center;
        padding-top: 10px;
        margin-bottom: 25px;
    }
    .header-subtitle {
        color: #8c8273;
        font-size: 0.88rem;
        letter-spacing: 1.5px;
        margin-top: 4px;
    }
    .header-deco {
        color: #c5a059;
        font-size: 0.75rem;
        letter-spacing: 6px;
        margin-top: 10px;
    }

    /* 상단 영문 이름 버튼 스타일 커스텀 */
    div.stButton > button[key="profile_btn"] {
        background: transparent !important;
        border: none !important;
        color: #dfc288 !important;
        font-family: 'Cinzel Decorative', 'Cinzel', serif !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        letter-spacing: 3px !important;
        text-shadow: 0 0 15px rgba(223, 194, 136, 0.45), 0 2px 5px rgba(0,0,0,0.9) !important;
        cursor: pointer !important;
        padding: 0 !important;
        margin: 0 auto !important;
        display: block !important;
        transition: transform 0.2s ease, text-shadow 0.2s ease !important;
    }
    div.stButton > button[key="profile_btn"]:hover {
        transform: scale(1.03);
        text-shadow: 0 0 22px rgba(223, 194, 136, 0.75) !important;
        color: #fff0d0 !important;
    }
    div.stButton > button[key="profile_btn"]:focus {
        outline: none !important;
        box-shadow: none !important;
    }

    /* 4. 브라우저 창 팝업 (모달) 스타일 */
    div[data-testid="stModal"] > div {
        background-color: #181a20 !important;
        border: 1px solid #755f3f !important;
        border-radius: 8px !important;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.95) !important;
        padding: 0 !important;
        overflow: hidden;
    }

    /* 브라우저 상단 타이틀 바 */
    .browser-header {
        background-color: #242730;
        padding: 10px 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #3d3429;
    }
    .browser-tab {
        background: #181a20;
        color: #dcd1c0;
        font-size: 0.85rem;
        padding: 4px 14px;
        border-radius: 6px 6px 0 0;
        border-top: 2px solid #c5a059;
        font-family: 'Song Myung', serif;
    }
    .window-controls {
        color: #8c8273;
        font-family: monospace;
        font-size: 1.1rem;
        display: flex;
        gap: 12px;
        user-select: none;
    }

    /* 프로필 카드 본문 디자인 */
    .profile-body {
        padding: 24px;
        color: #dcd1c0;
        background: radial-gradient(circle at top, rgba(35, 30, 25, 0.3) 0%, rgba(18, 19, 23, 0.95) 100%);
    }
    .profile-tag {
        color: #c5a059;
        font-size: 0.82rem;
        letter-spacing: 2px;
        margin-bottom: 6px;
    }
    .profile-name-kr {
        font-size: 1.5rem;
        font-weight: 700;
        color: #dfc288;
        margin-bottom: 16px;
        border-bottom: 1px solid rgba(197, 160, 89, 0.3);
        padding-bottom: 8px;
    }
    .profile-item {
        margin-bottom: 10px;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .profile-label {
        color: #a39580;
        font-weight: 600;
        margin-right: 8px;
    }

    /* 5. 말풍선 기본 구조 */
    [data-testid="stChatMessage"] {
        background-color: rgba(18, 19, 23, 0.88) !important;
        border-radius: 4px !important;
        padding: 14px 18px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.75) !important;
        backdrop-filter: blur(5px);
    }

    /* 레오나르드 말풍선: 네이비 차콜 + 고전 골드 테두리 */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]),
    [data-testid="stChatMessage"]:nth-child(even) {
        background: linear-gradient(135deg, rgba(20, 26, 38, 0.95) 0%, rgba(13, 16, 24, 0.95) 100%) !important;
        border: 1px solid rgba(197, 160, 89, 0.45) !important;
        border-left: 4px solid #c5a059 !important;
    }

    /* 사용자 말풍선: 차콜 브라운 + 앤틱 브론즈 테두리 */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]),
    [data-testid="stChatMessage"]:nth-child(odd) {
        background: linear-gradient(135deg, rgba(30, 25, 22, 0.92) 0%, rgba(18, 15, 13, 0.92) 100%) !important;
        border: 1px solid rgba(143, 114, 82, 0.4) !important;
        border-right: 4px solid #8f7252 !important;
    }

    [data-testid="stChatMessage"] p, 
    [data-testid="stChatMessage"] div {
        color: #e5ded2 !important;
        font-size: 1.02rem !important;
        line-height: 1.7 !important;
    }

    [data-testid="stChatMessage"] em {
        color: #bda888 !important;
        font-style: normal !important;
    }

    /* 6. 입력창 */
    [data-testid="stChatInput"] {
        background-color: #121418 !important;
        border: 1px solid #755f3f !important;
        border-radius: 4px !important;
        box-shadow: 0 -4px 25px rgba(0, 0, 0, 0.9) !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #c5a059 !important;
        box-shadow: 0 0 15px rgba(197, 160, 89, 0.3) !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #f0e6d6 !important;
        font-size: 0.98rem !important;
        font-family: 'Song Myung', serif !important;
    }
    [data-testid="stChatInput"] button svg {
        fill: #c5a059 !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 캐릭터 프로필 모달 (창 띄우기)
# -------------------------------------------------------------
@st.dialog("캐릭터 프로필")
def show_character_profile():
    # 브라우저 타이틀바 모양 장식 (— □ ✕)
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
        <div class="profile-item"><span class="profile-label">외형:</span>195cm를 상회하는 거구, 밀빛 금발에 선한 푸른 눈, 단정한 군인 체격</div>
        <div class="profile-item"><span class="profile-label">마법 특성:</span>생장(식물 조작) 및 광범위 치유·보호 마법</div>
        <div class="profile-item"><span class="profile-label">성향:</span>철저한 원칙주의(FM), 깊은 의무감, 그리고 소중한 사람(루카스 등)을 향한 위태롭고 무거운 헌신</div>
        <div class="profile-item"><span class="profile-label">비고:</span>타인의 시선 앞에서는 완벽한 왕세자이자 단장이지만, 밀실에서는 깊은 신뢰를 나누는 동료에게만 속내를 내비침.</div>
    </div>
    """, unsafe_allow_html=True)


# -------------------------------------------------------------
# 상단 타이틀 영역 (이름 클릭 시 모달 열림)
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

# AI 시스템 프롬프트 (간결한 호흡 유지)
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "너는 웹소설 <마법명가 차남으로 살아남는 법>의 등장인물 '레오나르드 비텔스바흐(레오)'다. "
        "너는 바이에른의 왕세자이자 101기 에스체트(Eszett)의 단장이다.\n\n"
        "[공간 배경]\n"
        "- 둘은 아카데미 외딴 곳의 어두운 석조 창고에서 은밀히 밀담을 나누고 있다.\n\n"
        "[상대(사용자)와의 관계]\n"
        "- 상대는 네가 가장 신뢰하는 에스체트의 핵심 동료다.\n"
        "- 상대는 너와 루카스 아스카니엔, 엘리아스, 나르케 사이의 모든 내막과 감정선을 전부 알고 있으며, 너도 이를 인지하고 있다.\n"
        "- 따라서 격식이나 방어적인 태도를 풀고 솔직한 속내를 털어놓는다.\n\n"
        "[★ 답변 길이 및 연출 규칙]\n"
        "1. 절대로 말을 길게 늘어놓지 마라. 답변 전체는 '짧은 행동 지문 1줄 + 대사 2~3문장' 내외로 극도로 간결하게 끊어라.\n"
        "2. 과묵하고 묵직한 FM 군인 특유의 절제된 호흡을 유지하라. 한마디에 무게감을 실어라.\n"
        "3. 나직하고 낮은 반말(~다, ~군, ~겠어, ~인가?)을 사용하라.\n"
        "4. 반드시 자연스러운 한국어로 답하라."
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

            response = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=api_messages,
                max_tokens=300,
                temperature=0.7,
                stream=True,
            )

            full_response = st.write_stream(response)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

        except Exception:
            st.error("어둠 속에서 목소리가 흩어졌습니다. 잠시 후 다시 시도해 주세요.")
