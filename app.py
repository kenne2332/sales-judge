from hmac import compare_digest
from pathlib import Path

import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="ยอดขายร้านสหกรณ์", layout="wide")

if not st.session_state.get("judge_logged_in"):
    st.title("เข้าสู่ระบบสำหรับกรรมการ")

    with st.form("judge_login"):
        username = st.text_input("ชื่อผู้ใช้")
        password = st.text_input("รหัสผ่าน", type="password")
        submitted = st.form_submit_button("เข้าสู่ระบบ")

    if submitted:
        account = st.secrets["judge"]
        username_ok = compare_digest(username.encode(), account["username"].encode())
        password_ok = compare_digest(password.encode(), account["password"].encode())

        if username_ok and password_ok:
            st.session_state["judge_logged_in"] = True
            st.rerun()

        st.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

    st.stop()

if st.button("ออกจากระบบ"):
    st.session_state["judge_logged_in"] = False
    st.rerun()

pages = {
    "แดชบอร์ดยอดขาย": "index.html",
    "ตารางผลวิเคราะห์": "sales-results-thai.html",
}
selected = st.radio("เลือกหน้าที่ต้องการดู", list(pages), horizontal=True)
content = Path(__file__).with_name(pages[selected]).read_text(encoding="utf-8")

if selected == "แดชบอร์ดยอดขาย":
    # ใช้เมนู Streamlit ด้านบนเปิดหน้าตาราง
    content = content.replace(
        '<a class="report-button" href="sales-results-thai.html">เปิดตารางผลวิเคราะห์</a>',
        "",
        1,
    )

html(content, height=850, scrolling=True)