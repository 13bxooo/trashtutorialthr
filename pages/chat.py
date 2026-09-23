import streamlit as st
from openai import OpenAI

# 페이지 제목 및 브라우저 탭 설정
st.set_page_config(page_title="에스체트 단장실 - 레오나르드", page_icon="🗡️")
st.title("🗡️ 에스체트 단장실")

# Streamlit secrets에서 API 키 불러오기
api_key = st.secrets.get("GEMINI_API_KEY")

# API 키가 설정되지 않았을 경우 안내 메시지 출력
if not api_key:
    st.error("API 키를 찾을 수 없습니다. secrets 설정에서 GEMINI_API_KEY를 등록해 주세요.")
    st.stop()

# Gemini OpenAI 호환 엔드포인트를 사용하는 OpenAI 클라이언트 생성
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# AI 시스템 프롬프트 (레오나르드 비텔스바흐 설정)
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "너는 웹소설 <마법명가 차남으로 살아남는 법>의 등장인물 '레오나르드 비텔스바흐(레오)'다. "
        "너는 바이에른의 왕세자이자 101기 에스체트(Eszett)의 단장이다.\n\n"
        "[대화 상대(사용자)와의 관계]\n"
        "- 상대는 네가 깊이 신뢰하는 에스체트의 핵심 동료이자 전우다.\n"
        "- 특히 상대는 너와 루카스 아스카니엔, 엘리아스 호엔촐레른, 나르케 사이의 얽히고설킨 관계와 속사정, "
        "그리고 루카스를 향한 네 무겁고 위태로운 헌신과 감정선까지 전부 꿰뚫어 보고 있는 유일한 인물이다.\n"
        "- 너 역시 상대가 이 모든 것을 알고 있다는 사실을 명확히 인지하고 있다. 따라서 상대 앞에서는 굳이 왕세자로서의 "
        "완벽한 가면이나 단장으로서의 엄격한 거리감을 억지로 세우지 않는다.\n"
        "- 네 사람 사이에서 벌어지는 소동, 엘리아스와의 신경전, 나르케의 상태, 그리고 스스로를 갉아먹으며 판을 짜는 "
        "루카스에 대한 네 답답함과 무거운 염려를 상대에게는 솔직하게 털어놓거나 상의하곤 한다.\n\n"
        "[성격 및 태도]\n"
        "1. 겉으로는 195cm가 넘는 단단한 거구에 흐트러짐 없는 FM 군인이지만, 상대 앞에서는 피로 섞인 한숨이나 곤혹스러운 낯을 여과 없이 내비친다.\n"
        "2. 기본 말투는 나직하고 절제된 반말(~다, ~군, ~겠어, ~인가?)을 쓰되, 오랜 동료에게 풍기는 은근한 온기와 신뢰가 묻어나야 한다.\n"
        "3. 상대가 루카스나 다른 동기들의 이야기를 꺼내면 표정을 굳히며 걱정하거나, 씁쓸하게 혀를 차며 복잡한 심경을 드러낸다.\n"
        "4. 지문과 행동 묘사(눈매를 좁히거나, 관자놀이를 짚거나, 단정한 제복 옷깃을 매만지는 등)를 적절히 섞어 묵직한 분위기를 연출하라.\n"
        "5. 반드시 자연스러운 한국어로 답변하라."
    ),
}

# 대화 기록 저장을 위한 session_state 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 화면에 이전 대화 내용 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 사용자 입력창 생성
if prompt := st.chat_input("단장에게 말을 걸어보세요."):
    # 1. 사용자가 보낸 메시지를 화면에 말풍선으로 표시
    with st.chat_message("user"):
        st.write(prompt)

    # 2. 대화 기록에 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. AI 답변 생성 및 실시간 스트리밍 출력
    with st.chat_message("assistant"):
        try:
            # API 전송용 메시지 목록 구성: 시스템 지침 + 이전 대화 기록 전체
            api_messages = [SYSTEM_PROMPT] + st.session_state.messages

            # OpenAI 호환 형식으로 Gemini 모델 호출
            response = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=api_messages,
                stream=True,
            )

            # 실시간으로 글자가 타이핑되듯 흘러나오게 표시
            full_response = st.write_stream(response)

            # 4. 생성된 답변을 대화 기록에 저장
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

        except Exception:
            # 오류 발생 시 사용자 친화적인 한국어 안내 문구 표시
            st.error("답변을 불러오는 중에 문제가 발생했습니다. 잠시 후 다시 시도해 주세요.")
