from hmac import compare_digest
from pathlib import Path

import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="ยอดขายร้านสหกรณ์", layout="wide")

if not st.session_state.get("judge_logged_in"):
    st.markdown("""
    <style>
      .st-key-judge_card {
        max-width: 460px;
        margin: 36px auto 0;
        padding: 24px;
        background: #f1f8f5;
        border-radius: 18px;
      }
     .st-key-judge_card :is(h1, h2, h3, h4) {
  color: #075c56 !important;
}

.st-key-judge_card [data-testid="stCaptionContainer"] p,
.st-key-judge_card label,
.st-key-judge_card label p {
  color: #243e38 !important;
}

.st-key-judge_card input {
  color: #ffffff;
  caret-color: #ffffff;
}
      }
    </style>
    """, unsafe_allow_html=True)

    with st.container(key="judge_card", border=True):
        st.subheader("แดชบอร์ดยอดขายร้านสหกรณ์")
        st.caption("เข้าสู่ระบบสำหรับกรรมการ")

        with st.form("judge_login", border=False):
            username = st.text_input("ชื่อผู้ใช้")
            password = st.text_input("รหัสผ่าน", type="password")
            submitted = st.form_submit_button(
                "เข้าสู่ระบบ", type="primary", use_container_width=True
            )

        if submitted:
            account = st.secrets["judge"]
            username_ok = compare_digest(
                username.encode(), account["username"].encode()
            )
            password_ok = compare_digest(
                password.encode(), account["password"].encode()
            )

            if username_ok and password_ok:
                st.session_state["judge_logged_in"] = True
                st.rerun()

            st.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

    st.stop()
