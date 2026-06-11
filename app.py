import streamlit as st
import google.generativeai as genai
import json

# 1. API 키 설정 (Streamlit 시스템 설정에서 가져옴)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. 웹 페이지 기본 레이아웃 설정
st.set_page_config(page_title="KHU:VOICE AI 라우팅 데모", layout="wide")
st.title("🦁 KHU:VOICE AI 1차 필터링 및 자동 분류 데모")
st.markdown("사용자의 제안을 AI가 분석하여 **진성 제안 여부**와 **담당 부서**를 자동으로 JSON 형태로 분류하는 백엔드 시뮬레이터입니다.")

# 3. 사용자 입력창 만들기
user_input = st.text_area("제안 내용을 입력하세요:", height=150, placeholder="예: 수강신청 서버가 너무 느려요. 클라우드로 바꿔주세요.")

# 4. 분석 버튼 클릭 시 실행될 로직
if st.button("AI 분석 실행"):
    if user_input:
        with st.spinner("AI가 처무규정을 바탕으로 분석 중입니다..."):
            try:
                # 제미나이 모델 설정 (가장 중요: JSON 출력 강제)
                model = genai.GenerativeModel(
                    "gemini-2.5-flash",
                    generation_config={
                        "response_mime_type": "application/json"
                    },
                    system_instruction="""너는 경희대학교 KHU:VOICE 시스템의 AI 분류기야.
                    사용자의 입력을 분석해서 다음 JSON 스키마로만 대답해:
                    {
                        "is_valid_proposal": boolean (단순 불만이나 시설 수리 요청이면 false, 제도/시스템 개선 제안이면 true),
                        "category": string (분류 카테고리),
                        "department": string (예상 담당 부서: 정보처, 총무처, 관재처, 교무처 등),
                        "reasoning": string (분류 이유),
                        "user_feedback_message": string (사용자에게 보여줄 친절한 안내 멘트)
                    }"""
                )
                
                # AI에게 질문 던지기
                response = model.generate_content(user_input)
                result_json = json.loads(response.text)
                
                st.success("분석 완료!")
                
                # 5. 결과 화면을 좌우 두 칸으로 나누어 보여주기
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("💬 사용자 화면 (프론트엔드)")
                    st.write("AI가 사용자에게 띄워줄 팝업 메시지입니다.")
                    if result_json["is_valid_proposal"]:
                        st.info(result_json["user_feedback_message"])
                    else:
                        st.warning(result_json["user_feedback_message"])
                
                with col2:
                    st.subheader("⚙️ 서버 전송 데이터 (백엔드 JSON)")
                    st.write("이 데이터가 DB에 저장되고, 담당 부서로 자동 메일이 발송됩니다.")
                    st.json(result_json) # JSON 형태로 예쁘게 출력
                    
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("제안 내용을 입력해 주세요.")
