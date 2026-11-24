from hmac import compare_digest
from pathlib import Path

import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="ยอดขายร้านสหกรณ์", layout="wide")

if not st.session_state.get("judge_logged_in", False):
    st.markdown("""
    <style>
      [data-testid="stAppViewContainer"]:has(.st-key-judge_card) {
        background: #f3f7f6;
      }
      .stApp:has(.st-key-judge_card) [data-testid="stHeader"] {
        background: transparent;
      }
      .st-key-judge_card {
        width: 100%;
        max-width: 460px;
        box-sizing: border-box;
        margin: clamp(16px, 6vh, 64px) auto 0;
        padding: clamp(18px, 4vw, 32px);
        background: #fff;
        border: 1px solid #dce8e4;
        border-radius: 18px;
        box-shadow: 0 12px 32px rgba(16, 48, 40, 0.08);
      }
      .st-key-judge_card :is(h1, h2, h3, h4) {
        color: #123c34 !important;
      }
      .st-key-judge_card [data-testid="stCaptionContainer"] p,
      .st-key-judge_card label,
      .st-key-judge_card label p {
        color: #243e38 !important;
      }
      .st-key-judge_card [data-baseweb="input"],
      .st-key-judge_card [data-baseweb="input"] > div,
      .st-key-judge_card [data-baseweb="input"] button,
      .st-key-judge_card input {
        background: #f7faf9 !important;
        color: #173e3a !important;
        border-color: #c8dad4 !important;
      }
      .st-key-judge_card [data-baseweb="input"]:focus-within {
        outline: 2px solid #13786b;
        outline-offset: 2px;
      }
      .st-key-judge_card input {
        -webkit-text-fill-color: #173e3a !important;
        caret-color: #173e3a;
      }
      .st-key-judge_card [data-testid="stFormSubmitButton"] button {
        min-height: 44px;
        color: #fff !important;
        background: #08665b !important;
        border: 0;
        border-radius: 10px;
      }
      .st-key-judge_card [data-testid="stFormSubmitButton"] button:hover {
        background: #064d45 !important;
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
            try:
                account = st.secrets["judge"]
                username_ok = compare_digest(
                    username.encode("utf-8"), account["username"].encode("utf-8")
                )
                password_ok = compare_digest(
                    password.encode("utf-8"), account["password"].encode("utf-8")
                )
            except (FileNotFoundError, KeyError):
                st.error("ยังตั้งค่าบัญชีไม่ครบใน Streamlit Secrets")
            else:
                if username_ok and password_ok:
                    st.session_state["judge_logged_in"] = True
                    st.rerun()
                st.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

    st.stop()

# จัดหน้าเต็มหน้าต่างหลังล็อกอิน
st.markdown("""
<style>
  .stApp:has(.st-key-sales_view) {
    --sales-nav-height: 72px;
  }
  [data-testid="stAppViewContainer"]:has(.st-key-sales_view),
  [data-testid="stMain"]:has(.st-key-sales_view) {
    overflow: hidden !important;
  }
  .stApp:has(.st-key-sales_view) [data-testid="stHeader"] {
    display: none;
  }
  .st-key-sales_nav {
    position: fixed;
    inset: 0 0 auto;
    z-index: 100;
    height: var(--sales-nav-height, 72px);
    box-sizing: border-box;
    padding: 12px clamp(12px, 3vw, 32px);
    background: var(--background-color, #fff);
    border-bottom: 1px solid #dce8e4;
  }
  .st-key-sales_nav [data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important;
    gap: 8px;
  }
  .st-key-sales_nav [data-testid="stColumn"] {
    flex: 1 1 0% !important;
    min-width: 0 !important;
    width: auto !important;
  }
  .st-key-sales_nav [data-testid="stColumn"]:last-child {
    flex: 0 0 auto !important;
  }
  .st-key-sales_view iframe {
    position: fixed;
    inset: var(--sales-nav-height, 72px) 0 auto;
    width: 100% !important;
    height: calc(100vh - var(--sales-nav-height, 72px)) !important;
    height: calc(100dvh - var(--sales-nav-height, 72px)) !important;
    border: 0;
  }
</style>
""", unsafe_allow_html=True)

pages = {
    "แดชบอร์ดยอดขาย": "index.html",
    "ตารางผลวิเคราะห์": "sales-results-thai (2).html",
}

with st.container(key="sales_nav"):
    menu, actions = st.columns([4, 1], vertical_alignment="center")
    with menu:
        selected = st.selectbox(
            "เลือกหน้า", list(pages), label_visibility="collapsed"
        )
    with actions:
        if st.button("ออกจากระบบ"):
            st.session_state["judge_logged_in"] = False
            st.rerun()

page_path = Path(__file__).with_name(pages[selected])
if not page_path.is_file():
    st.error(f"หาไฟล์ {page_path.name} ไม่เจอ ให้เช็กว่าอยู่ข้าง app.py ใน GitHub")
    st.stop()

content = page_path.read_text(encoding="utf-8")
if selected == "แดชบอร์ดยอดขาย":
    content = content.replace(
        '<a class="report-button" href="sales-results-thai.html">เปิดตารางผลวิเคราะห์</a>',
        "",
        1,
    )
if selected == "ตารางผลวิเคราะห์":
    jump_script = """
<script>
document.addEventListener("click", function (event) {
    const link = event.target.closest('nav a[href^="#"]');
    if (!link) return;

    event.preventDefault();
    const id = link.getAttribute("href").slice(1);
    const heading = document.getElementById(id);

    if (heading) {
        heading.scrollIntoView({ block: "start" });
    }
});
</script>
"""
    content = content.replace("</body>", jump_script + "</body>", 1)
with st.container(key="sales_view"):
    html(content, height=850, scrolling=True)
