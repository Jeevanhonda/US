import streamlit as st
import admin,person  # This is your page manager

# Page config
st.set_page_config(page_title="Jeevan Honda", layout="wide")

# Dummy login data
valid_users = {
    "admin": "admin123",
    "ho" : "hovusp_2025",
    "kmr" : "kmrah_2025",
    "tnr":"tnrk_2025",
    "nmp":"nmpm_2025",
    "ckm":"ckmn_2025",
    "tmg":"tmgspv_2025",
    "klk":"klkk_2025"
}

# Session state init
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# If already logged in
if st.session_state.logged_in:
    st.sidebar.success(f"✅ Logged in as: {st.session_state.username}")
    st.sidebar.button("🚪 Logout", on_click=logout)
    if st.session_state.username=="admin":
        admin.app()  # Show the page manager
    if st.session_state.username=="ho":
        person.app(name=["Santhana Revathi","Usha","Pavithra J","Muthukumar M"])
    if st.session_state.username=="kmr":
        person.app(name=["Harini"])
    if st.session_state.username=="tnr":
        person.app(name=["Karthikeyan G"])
    if st.session_state.username=="nmp":
        person.app(name=["Manoj"])
    if st.session_state.username=="ckm":
        person.app(name=["Nivageetha"])
    if st.session_state.username=="tmg":
        person.app(name=["Sundari","Pavithra S","Vinothini"])
    if st.session_state.username=="klk":
        person.app(name=["Kannan Prabhu"])
    

        
else:
    # Login UI
    st.markdown(
        """
        <style>
            .login-box {
                max-width: 400px;
                margin: 5rem auto;
                padding: 2rem;
                border-radius: 15px;
                background-color: #f9f9f9;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                text-align: center;
            }
        </style>
        """, unsafe_allow_html=True
    )
    st.markdown('<div class="login-box"><h2>🔐 Jeevan Honda Admin Login</h2>', unsafe_allow_html=True)
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")
    if st.button("Login"):
        if username in valid_users and valid_users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid credentials.")
    st.markdown('</div>', unsafe_allow_html=True)
