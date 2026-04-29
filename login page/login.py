import streamlit as st
import re

# --- CUSTOM CSS & ANIMATIONS ---
# Using Streamlit's markdown to inject styles for advanced look and round animation
custom_css = """
<style>
/* Simple background gradient and font styling */
body {
    /* popular login background: dark-to-light blue gradient with centered panel */
    background: linear-gradient(135deg, #0d47a1 0%, #1976d2 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #fff;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
}

/* center the app container so other elements mimic standard login page layout */
#root > div[role="main"] {
    width: 100%;
    max-width: 400px;
}

/* Brighter accent for headings and links */
h1, h2, h3, h4, h5, h6 {
    color: #fff;
}

.stMarkdown p, label {
    color: #fff;
}

/* Animated rounded container for the forms */
.rounded-form {
    border-radius: 20px;
    padding: 30px;
    background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(242,242,242,0.95) 100%);
    animation: pulse 3s ease-in-out infinite;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    border: 2px solid rgba(255,255,255,0.3);
}

/* Button hover animation */
.stButton>button {
    background: linear-gradient(45deg, #6a11cb, #2575fc);
    color: white;
    font-weight: bold;
    transition: transform 0.2s, box-shadow 0.2s, background 0.4s;
    border-radius: 10px;
    padding: 10px 24px;
}
.stButton>button:hover {
    transform: scale(1.08);
    box-shadow: 0 6px 16px rgba(0,0,0,0.3);
    background: linear-gradient(45deg, #2575fc, #6a11cb);
}

/* Keyframes for the pulsing round effect */
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.02); }
    100% { transform: scale(1); }
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)


# --- SETTINGS ---
st.set_page_config(page_title="Admin Login", page_icon="🔒")

# Initialize a dictionary in session state to act as a database
if 'db' not in st.session_state:
    st.session_state.db = {} # Format: {username: password}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Password Format Checker (Regex)
def check_password_format(password):
    # Rules: 1 Uppercase, 1 Number, 1 Special Char, 8+ chars
    pattern = r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return re.match(pattern, password)

# --- APP LOGIC ---
if not st.session_state.logged_in:
    st.title("Admin Portal")
    
    choice = st.radio("Select Action", ["Login", "Signup"])

    if choice == "Signup":
        # styled container start
        st.markdown("<div class='rounded-form'>", unsafe_allow_html=True)
        st.subheader("Create New Admin Account")
        new_user = st.text_input("Username", placeholder="e.g., admin")
        new_pass = st.text_input("Password", type="password", help="Must have 1 Uppercase, 1 Number, and 1 Special Character")
        
        if st.button("Register"):
            if new_user in st.session_state.db:
                st.error("User already exists!")
            elif not check_password_format(new_pass):
                st.error("Invalid Format! Use 1 Uppercase, 1 Number, and 1 Special Char (@$!%*?&).")
            elif new_user and new_pass:
                st.session_state.db[new_user] = new_pass
                st.success("Account created! Now switch to Login.")
            else:
                st.warning("Please fill all fields.")
        # styled container end
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        # styled container start
        st.markdown("<div class='rounded-form'>", unsafe_allow_html=True)
        st.subheader("Login to Dashboard")
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if user in st.session_state.db and st.session_state.db[user] == pw:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Incorrect username or password.")
                if pw and not check_password_format(pw):
                    st.info("Reminder: Password must include Uppercase, Number, and Special Char.")
        # styled container end
        st.markdown("</div>", unsafe_allow_html=True)

# --- DASHBOARD AREA ---
else:
    st.title(f"Welcome, {st.session_state.user}! 👋")
    st.success("You are now logged into the secure admin area.")
    
    # Dashboard visual
    st.divider()
    col1, col2 = st.columns(2)
    col1.metric("Server Status", "Online 🟢")
    col2.metric("Database", "Secure 🔒")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()