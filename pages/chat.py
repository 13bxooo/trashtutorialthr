import streamlit as st
from openai import OpenAI

# 페이지 기본 설정
st.set_page_config(
    page_title="밀실 - 레오나르드 비텔스바흐",
    page_icon="🕯️",
    layout="centered"
)

# -------------------------------------------------------------
# 로판풍 어두운 창고 / 석조 밀실 스타일링 (Custom CSS)
# -------------------------------------------------------------
st.markdown("""
<style>
    /* 전체 배경: 어두운 석조 벽돌 및 오래된 창고 느낌 */
    .stApp {
        background-color: #121316;
        background-image: 
            radial-gradient(ellipse at top, rgba(35, 30, 25, 0.6) 0%, rgba(10, 10, 12, 0.95) 80%),
            linear-gradient(to bottom, #141419, #0d0e11);
        color: #d6cbba;
        font-family: 'Nanum Myeongjo', 'Batang', serif;
    }

    /* 제목 및 부제 헤더 */
    .warehouse-title {
        text-align: center;
        color: #c9a96e;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 4px;
        text-shadow: 0 0 12px rgba(201, 169, 110, 0.3);
    }
    .warehouse-subtitle {
        text-align: center;
        color: #7b7468;
        font-size: 0.9rem;
        font-style: italic;
        margin-bottom: 25px;
        letter-spacing: 1px;
    }

    /* 말풍선 컨테이너 기본 스타일 */
    .stChatMessage {
        background-color: rgba(22, 23, 28, 0.75) !important;
        border: 1px solid rgba(139, 115, 85, 0.3) !important;
        border-radius: 6px !important;
        padding: 12px 16px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 12px !important;
        backdrop-filter: blur(4px);
    }

    /* AI(레오나르드) 말풍선 강조: 바이에른 제복을 연상시키는 묵직한 청회색/골드 */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: linear-gradient(135deg, rgba(20, 24, 33, 0.9) 0%, rgba(15, 17, 24, 0.9) 100%) !important;
        border-left: 3px solid #c9a96e !important;
    }

    /* 사용자 말풍선 강조: 낡은 양피지/가죽 느낌의 갈색빛 톤 */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: linear-gradient(135deg, rgba(28, 24, 20, 0.9) 0%, rgba(18, 16, 14, 0.9) 100%) !important;
        border-left: 3px solid #6b5840 !important;
    }

    /* 본문 글자색: 바랜 양피지 느낌의 아이보리 톤 */
    .stChatMessage p {
        color: #ded6c8 !important;
        line-height: 1.65;
        font-size: 0.98rem;
    }

    /* 지문 묘사(괄호, 이탤릭 등) 색상 은은하게 처리 */
    .stChatMessage em {
        color: #a39580 !important;
    }

    /* 하단 채팅 입력창 스타일 */
    div[data-testid="stChatInput"] {
        background-color: #14151a !important;
        border: 1px solid #5a4b38 !important;
        border-radius: 4px !important;
        box-shadow: 0 -2px 15px rgba(0, 0, 0, 0.6) !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #e5ded3 !important;
        font-family: 'Nanum Myeongjo', 'Batang', serif !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #615a50 !important;
        font-style: italic;
    }

    /* 스크롤바 커스텀 */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0d0e11;
    }
    ::-webkit-scrollbar-thumb {
        background: #3a3227;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# 창고 분위기 헤더
st.markdown('<div class="warehouse-title">🕯️ 비공식 집현실 (集賢室)</div>', unsafe_allow_html=True)
st.markdown('<div class="warehouse-subtitle">외딴 창고 깊숙한 곳, 낡은 촛불만이 둘 사이의 그림자를 길게 늘어뜨린다.</div>', unsafe_allow_html=True)

# Streamlit secrets에서 API 키 불러오기
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API 키를 찾을 수 없습니다. secrets 설정에서 GEMINI_API_KEY를 등록해 주세요.")
    st.stop()

# Gemini OpenAI 호환 엔드포인트 클라이언트
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# AI 시스템 프롬프트 (레오나르드 비텔스바흐)
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "너는 웹소설 <마법명가 차남으로 살아남는 법>의 등장인물 '레오나르드 비텔스바흐(레오)'다. "
        "너는 바이에른의 왕세자이자 101기 에스체트(Eszett)의 단장이다.\n\n"
        "[공간 배경]\n"
        "- 현재 둘이 있는 장소는 남들의 눈을 피해 들어온 '아카데미 외딴 곳의 어둡고 낡은 창고'다. "
        "주변엔 방치된 목재 상자들과 먼지 쌓인 마법 장비들이 쌓여 있고, 희미한 촛불 하나만이 켜져 있어 "
        "대화의 무게감과 비밀스러움이 극대화된 은밀한 장소다.\n\n"
        "[대화 상대(사용자)와의 관계]\n"
        "- 상대는 네가 가장 신뢰하는 에스체트의 동료이자 전우다.\n"
        "- 상대는 너와 루카스 아스카니엔, 엘리아스 호엔촐레른, 나르케 사이의 모든 비밀과 내막, "
        "그리고 루카스를 향한 네 위태롭고 무거운 헌신까지 전부 알고 있다. 너 역시 상대가 이 사실을 안다는 것을 인지하고 있다.\n"
        "- 따라서 이 어두운 창고 안에서는 왕세자나 단장의 완벽한 태도를 내려놓고, 피로와 고뇌, 답답함을 가감 없이 드러낸다.\n\n"
        "[어조 및 연출]\n"
        "1. 나직하고 무게감 있는 반말(~다, ~군, ~겠어, ~인가?)을 쓴다.\n"
        "2. 행동 지문(미간을 좁히며 촛불을 응시하거나, 어두운 벽에 기대어 한숨을 내쉬는 등)을 적절히 섞어 로판 특유의 어둡고 고요한 밀담 분위기를 연출하라.\n"
        "3. 반드시 자연스러운 한국어로 답하라."
    ),
}

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 기록 렌더링 (아바타 설정: 레오는 군청색 단검, 사용자는 촛불)
for msg in st.session_state.messages:
    avatar = "🗡️" if msg["role"] == "assistant" else "🕯️"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# 메시지 입력 및 처리
if prompt := st.chat_input("창고의 어둠 속에서 단장에게 말을 건넨다..."):
    # 1. 사용자 메시지 출력
    with st.chat_message("user", avatar="🕯️"):
        st.write(prompt)

    # 2. 대화 기록 저장
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. 레오나르드의 답변 스트리밍
    with st.chat_message("assistant", avatar="🗡️"):
        try:
            api_messages = [SYSTEM_PROMPT] + st.session_state.messages

            response = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=api_messages,
                stream=True,
            )

            full_response = st.write_stream(response)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

        except Exception:
            st.error("어둠 속에서 목소리가 흩어졌습니다. 잠시 후 다시 시도해 주세요.")
