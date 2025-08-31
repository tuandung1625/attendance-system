import streamlit as st
from Home import face_rec

st.set_page_config(
    page_title="Delete Records",
    page_icon="🗑️",
    layout="wide"
)

st.markdown("""
<style>
    .delete-header {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .warning-box {
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
        border: 2px solid #ffc107;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="delete-header">
    <h1>🗑️ Delete User Records</h1>
    <p>Manage and remove user records from the attendance system</p>
</div>
""", unsafe_allow_html=True)


with st.spinner("Retrieving data from Redis database ..."):
    redis_face_db = face_rec.retrieve_data('academy:register')
    st.dataframe(redis_face_db)
st.success("Data successfully retrieved from Redis")

# Initialize session state
if 'confirm_delete' not in st.session_state:
    st.session_state.confirm_delete = {}
if 'refresh_data' not in st.session_state:
    st.session_state.refresh_data = True

# Warning message
st.markdown("""
<div class="warning-box">
    <h3>⚠️ Important Warning</h3>
    <p>Deleting user records is <strong>permanent</strong> and cannot be undone. 
    This will remove all face encodings and attendance history for the selected user.</p>
</div>
""", unsafe_allow_html=True)

# Nếu redis_face_db là DataFrame
if not redis_face_db.empty:
    members = redis_face_db[['Name', 'Role']].to_dict(orient='records')
    
    # Tạo list hiển thị: "Tên (Role)"
    display_list = [f"{m['Name']} ({m['Role']})" for m in members]
    selected = st.selectbox("Choose member for deleting:", display_list)
    
    if st.button("Delete member"):
        # Find index
        idx = display_list.index(selected)
        member_to_delete = members[idx]
        # Delete
        face_rec.delete_member('academy:register', member_to_delete['Name'], member_to_delete['Role'])
        st.success(f"Delete {member_to_delete['Name']} successfully!")
else:
    st.info("Không có member nào trong database.")

if st.button("🔄 Refresh User List", use_container_width=True):
    st.session_state.confirm_delete = {}
    st.rerun()