import streamlit as st
import google.generativeai as genai
import json

# 1. API 키 설정 (Streamlit 시스템 설정에서 가져옴)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. 웹 페이지 기본 레이아웃 설정
st.set_page_config(page_title="KHU:VOICE AI 라우팅 데모", layout="wide")
st.title("🦁 KHU:VOICE AI 1차 필터링 및 자동 분류 데모")
st.markdown("경희대학교 처무규정(2025.12.06. 시행)과 **V.O.I.C.E 신청 분야**를 기반으로 사용자의 제안을 자동 분류하는 백엔드 엔진입니다.")

# 3. 사용자 입력창 만들기
user_input = st.text_area("제안 내용을 입력하세요:", height=150, placeholder="예: 대학 행정업무 자동화를 위해 생성형 AI를 도입하고, 관련 서버 인프라를 구축해 주세요.")

# 4. 분석 버튼 클릭 시 실행될 로직
if st.button("AI 분석 실행"):
    if user_input:
        with st.spinner("AI가 처무규정과 V.O.I.C.E 기준을 바탕으로 분석 중입니다..."):
            try:
                # 제미나이 모델 설정
                model = genai.GenerativeModel(
                    "gemini-2.5-flash-lite",
                    generation_config={
                        "response_mime_type": "application/json"
                    },
                    system_instruction="""너는 경희대학교 행정 제안 시스템 'KHU:VOICE'의 핵심 인공지능 라우터 에이전트야.
                    아래 제시된 [경희대학교 부서별 실제 업무분장(처무규정)]과 [KHU:VOICE 신청 분야(V.O.I.C.E)]를 완벽하게 숙지하고, 사용자의 제안을 가장 적합한 부서와 분야로 분류해라.

                    [KHU:VOICE 신청 분야 (V.O.I.C.E) 분류 기준]
                    제안의 성격을 분석하여 아래 5가지 중 가장 핵심적인 1개의 가치를 'voice_category'로 도출한다.
                    1. V - Value-up: 대학의 유/무형 자원 자산화, 새로운 가치/수입 창출 (지출 합리화, 발전기금 모금, 지식사업화 등 재정 수입 증대 방안)
                    2. O - Open: 데이터/정보 개방 및 의사결정 과정 공유 (데이터기반 열린행정 시스템 도입, 발전적인 제도 도입 및 개선)
                    3. I - Insight: 미래 환경 변화에 선제 대응하는 본질적 혁신 (행정업무 자동화 등 AI/AX/DX 혁신, 학사제도/미래형 커리큘럼 전환, 교육/연구/복지 시설 및 공간 개선)
                    4. C - Co-creation: 구성원/캠퍼스/기관 간 협업으로 시너지 창출 (하나의 대학 구현, 이원화 캠퍼스 시너지, 평판도/구성원 Pride 제고, 학생 지원 프로그램 체질 개선)
                    5. E - Execution: 기존 제도를 실제 운영/개선 제도로 구현하는 실행력 (위 4개에 속하지 않는 모든 영역의 일반적인 개선 필요 제도)

                    [경희대학교 부서별 세부 업무분장(처무규정 핵심 요약)]
                    1. 기획조정처: 대학 중장기 발전계획 및 예산의 편성, 제규정의 제정, 개·폐 심의, 기관 및 부서 간 업무 조정, 교내 민원 처리 관련 각종 업무 지도 및 감독.
                    2. 교무처: 교육과정 편성, 교원인사, 학적 변동 업무(등록, 제적, 복학, 휴학, 재입학, 전과 및 퇴학 관련 업무총괄), 수강신청 관련 업무, 종합강의 시간표 편성, 졸업 및 성적 관리.
                    3. 미래혁신원: 교내외 장학 및 학자금 대출 업무, 총학생회 등 학생자치단체 지도ㆍ지원, 학생 진로, 학교 생활, 심리 등 관련 상담, 취업/진학 박람회, 채용 설명회, 창업휴학 및 창업대체학점 인정.
                    4. 정보처: 학부 학사행정 관리시스템 운영, 일반행정 관리시스템 운영, 정보통신기기, 정보통신망 등 정보시스템 기반시설 구축, 포털 및 웹메일 운영, 교내 소프트웨어 라이선스 관리.
                    5. 총무관리처: 물품구매 및 예정가격 작성(총무팀), 건물의 유지관리 및 건축물 관리비를 이용한 소규모 개보수(관리팀), 비품 수급계획 수립 및 폐기(관재팀), 안전관리 총괄(안전팀), 대관시설 연간 활용계획 수립 및 대관업무 총괄(시설운영팀).
                    6. 입학처: 학부 신‧편입학, 일반대학원 내국인 학생선발 및 입학 사정, 관리, 입학전산시스템 계획 수립, 운용 및 관리.
                    7. 인사처: 직원 정원조정 및 임용계획 수립, 직원의 급여 및 각종 수당 지급, 노동조합과의 협의체 운영.
                    8. 국제처: 외국인 학부/일반대학원 입시, 외국인 교원 및 학생(학부/일반대학원) 출입국 업무, 체류 관리, 해외대학, 기관과의 학생 관련 교류 프로그램 기획 및 운영.
                    9. 대외협력처: 발전기금 기부자 발굴 및 예우, 동문 데이터베이스 및 네트워크 구축·관리.
                    10. 커뮤니케이션센터: 본교 메인 홈페이지(국·영문) 개발·운영, 공보 간행물 기획 및 제작, 본교 디자인 업무 총괄.
                    11. 생활관: 사생 선발, 기숙사 시설 관리, 유지, 기숙사의 식당운영.
                    12. 도서관(중앙도서관): 인쇄 및 전자자료의 선정, 구입, 기증 및 수증, 등록, 전자도서관 및 학술정보시스템 개발 및 운영, 자료 대출, 반납, 예약 등 열람 서비스.

                    [분류 및 라우팅 엄격한 규칙]
                    - 입력된 텍스트가 위 규정과 연관된 '제도적, 인프라적, 행정적 개선안'인지 먼저 판단한다. 
                    - [단순 민원 반려 기준] 즉각 조치가 필요한 단순 불만(예: '강의실 에어컨 고장', '변기 막힘')이나, 개인의 단순 편의 도모 및 일회성 예외 적용 요구(예: '축제 기간 기숙사 통금 연장', '오늘 하루 주차비 면제')는 구조적 제안이 아니므로 반드시 'is_valid_proposal'을 false로 반환한다.
                    - [정보시스템 규칙] '전산 시스템의 단순 에러나 인프라 문제'는 정보처를 주관 부서로 매핑한다. 단, '인포21에 새로운 기능/버튼 추가, 기존 행정 규칙(장학, 성적 등) 전산 반영' 등 현업 부서의 정책과 전산 개발이 동시에 필요한 경우, 반드시 정책 주관 부서(예: 교무처, 미래혁신원 등)를 'department'에 넣고, 실제 개발을 수행할 '정보처'를 'collaborative_departments'에 필수로 포함시킨다.
                    [출력 JSON 스키마 (반드시 이 형태만 유지)]
                    {
                        "is_valid_proposal": boolean,
                        "voice_category": "string (예: 'I - Insight', 'V - Value-up' 등 5개 중 택 1)",
                        "department": "string (가장 적합한 주관 부서명)",
                        "collaborative_departments": ["string", "string"],
                        "confidence_score": integer (0~100 사이의 신뢰도 점수),
                        "reasoning": "string (선택한 분야 및 부서들의 상세 매핑 사유)",
                        "user_feedback_message": "string (사용자 안내 메시지)"
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
                    st.write("시스템이 실시간으로 판단하여 사용자에게 띄워주는 메시지입니다.")
                    
                    if result_json.get("is_valid_proposal"):
                        # V.O.I.C.E 카테고리를 예쁘게 뱃지처럼 표시
                        st.markdown(f"🏷️ **신청 분야:** `{result_json.get('voice_category', '분류 미정')}`")
                        st.info(f"✅ **[접수 완료]** 주관 부서: {result_json.get('department', '미정')}")
                        
                        collab_depts = result_json.get("collaborative_departments", [])
                        if collab_depts:
                            st.caption(f"🤝 시스템 도출 협조 부서: {', '.join(collab_depts)}")
                            
                        st.write(result_json.get("user_feedback_message", ""))
                    else:
                        st.warning(f"❌ **[접수 보류]** 사유: 단순 민원 또는 부적절한 제안")
                        st.write(result_json.get("user_feedback_message", ""))
                    
                    st.markdown("---")
                    score = result_json.get('confidence_score', 0)
                    st.markdown(f"**🤖 AI 신뢰도 점수:** `{score}점`")
                    if score < 80:
                        st.caption("⚠️ *점수가 80점 미만이므로, 실제 시스템에서는 기획조정처 미분류함으로 1차 이관되어 수동 검토를 거칩니다.*")
                
                with col2:
                    st.subheader("⚙️ 서버 전송 데이터 (백엔드 JSON)")
                    st.write("MariaDB에 저장되고, 담당 부서 자동 이메일 발송 파라미터로 사용되는 원본 데이터입니다.")
                    st.json(result_json)
                    
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("제안 내용을 입력해 주세요.")
