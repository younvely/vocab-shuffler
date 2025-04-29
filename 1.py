import re
import random
import streamlit as st

st.set_page_config(page_title="어휘 보기 변형기", layout="wide")
st.title("🧠 어휘 보기 랜덤 섞기 웹툴")

st.markdown("""
지문을 아래에 붙여넣고 **[보기 섞기]** 버튼을 누르세요.  
`❶ [정답 / 오답]` 형식을 그대로 유지하며, 보기 순서를 무작위로 바꿉니다.  
**정답/오답 모두 굵은 글씨로 강조됩니다.**
""")

# ✅ 세션 상태 초기화
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "original_text" not in st.session_state:
    st.session_state.original_text = ""
if "result" not in st.session_state:
    st.session_state.result = ""

# ✅ 입력창
st.session_state.input_text = st.text_area("✍️ 여기에 지문을 붙여넣으세요", value=st.session_state.input_text, height=300)

# ✅ 보기 섞기 함수
def shuffle_and_bold_choices(text):
    pattern = r'(❶|❷|❸|❹|❺|❻|❼|❽|❾|❿) \[(.*?) / (.*?)\]'
    def replacer(match):
        number = match.group(1)
        choices = [match.group(2).strip(), match.group(3).strip()]
        random.shuffle(choices)
        return f"{number} [**{choices[0]} / {choices[1]}**]"
    return re.sub(pattern, replacer, text)

# ✅ 버튼 영역
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎲 보기 섞기"):
        if st.session_state.input_text.strip() == "":
            st.warning("⛔ 지문을 먼저 입력해주세요.")
        else:
            st.session_state.original_text = st.session_state.input_text  # 원본 저장
            st.session_state.result = shuffle_and_bold_choices(st.session_state.input_text)

with col2:
    if st.button("🔄 다시 섞기"):
        if st.session_state.original_text.strip() == "":
            st.warning("⛔ 먼저 지문을 입력하고 섞어주세요.")
        else:
            st.session_state.result = shuffle_and_bold_choices(st.session_state.original_text)

with col3:
    if st.button("🧹 지문 초기화"):
        st.session_state.input_text = ""
        st.session_state.original_text = ""
        st.session_state.result = ""

# ✅ 결과 출력
if st.session_state.result:
    st.markdown("---")
    st.markdown("### ✅ 보기 섞인 결과 (서식 포함)")
    st.markdown(st.session_state.result)
