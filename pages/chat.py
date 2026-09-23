import streamlit as st
from openai import OpenAI

# 페이지 제목 및 브라우저 탭 설정
st.set_page_config(page_title="정보 선생님과의 AI 대화", page_icon="💬")
st.title("💬 친절한 정보 선생님과의 대화")

# Streamlit secrets에서 API 키 가져오기
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

# AI 시스템 프롬프트 (화면에 표시되지 않고 AI에게 성격을 부여하는 역할)
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "너는 중고등학생에게 설명하는 친절한 정보 선생님이야. "
        "어려운 말은 쉬운 말로 바꿔 주고, 반드시 순수 한국어로만 답해."
    ),
}

# 대화 기록 저장을 위한 session_state 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 화면에 이전 대화 내용 출력 (시스템 프롬프트는 제외하고 사용자 및 AI 메시지만 표시)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 사용자 입력창 생성
if prompt := st.chat_input("선생님께 궁금한 점을 질문해 보세요!"):
    # 1. 사용자가 보낸 질문을 화면에 말풍선으로 표시
    with st.chat_message("user"):
        st.write(prompt)

    # 2. 대화 기록에 사용자 질문 추가
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. AI 답변 생성 및 실시간 스트리밍 출력
    with st.chat_message("assistant"):
        try:
            # API 전송용 메시지 목록 구성: 시스템 지침 + 이전 대화 기록 전체
            api_messages = [SYSTEM_PROMPT] + st.session_state.messages

            # OpenAI 호환 형식으로 Gemini 모델 호출 (글자가 흘러나오도록 stream=True 설정)
            response = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=api_messages,
                stream=True,
            )

            # write_stream을 사용해 실시간으로 글자가 타이핑되듯 흘러나오게 표시
            full_response = st.write_stream(response)

            # 4. 생성된 AI 답변을 대화 기록에 저장
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

        except Exception:
            # 오류 발생 시 기본 빨간 에러창 대신 한국어 한 줄 문구 표시
            st.error("답변을 불러오는 중에 문제가 발생했습니다. 잠시 후 다시 시도해 주세요.")
