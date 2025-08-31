import streamlit as st
from Home import face_rec
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer
import av

st.set_page_config(
    page_title="Registration Form",
    page_icon="📝",
    layout="wide"
)

st.markdown("""
<style>
    .registration-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="registration-header">
    <h1>📝 User Registration</h1>
    <p>Register new users for face recognition attendance system</p>
</div>
""", unsafe_allow_html=True)

registration_form = face_rec.RegistrationForm()

# Collect person name and person role
person_name = st.text_input(label='Name', placeholder='First & Last Name')
role = st.selectbox(label='Select your Role', options=('Student','Teacher'))

# Collect facial embedding of person
def video_callback_func(frame):
    img = frame.to_ndarray(format='bgr24')
    reg_img, embedding = registration_form.get_embedding(img)

    # Save embed into local computer
    if embedding is not None:
        with open('face_embedding.txt', 'ab') as f:
            np.savetxt(f, embedding)

    return av.VideoFrame.from_ndarray(reg_img, format='bgr24')

webrtc_streamer(key='registration', video_frame_callback=video_callback_func,
                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

# Save the data in Redis
if st.button('Submit'):
    check = registration_form.save_data_redis(person_name,role)
    if check == True:
        st.success(f"{person_name} registered successfully")
    elif check == 'name_false':
        st.error('Please enter the name : Name cannot be empty or spaces')
    elif check == 'file_false':
        st.error('face_embedding.txt is not found. Please refresh the page and execute again!!!')

# Registration guidelines
with st.expander("📋 Registration Guidelines"):
    st.markdown("""
    ### Photo Requirements:
    - **Face clearly visible** - No hats, sunglasses, or masks
    - **Good lighting** - Avoid shadows on face
    - **Front-facing** - Look directly at camera
    - **Single person** - Only one face in the image
    - **High quality** - Clear, not blurry
    
    ### Registration Process:
    1. Fill out all required user details
    2. Capture or upload a clear face photo
    3. Preview the image to ensure quality
    4. Complete registration
    
    ### Tips:
    - Use good lighting for better recognition accuracy
    - Ensure face takes up 30-50% of the image
    - Keep a neutral expression
    - Remove any face coverings
    """)