import streamlit as st
from Home import face_rec
from streamlit_webrtc import webrtc_streamer
import av
import time

st.set_page_config(
    page_title="Real Time Prediction",
    page_icon="📹",
    layout="wide"
)

st.markdown("""
<style>
    .prediction-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="prediction-container">
    <h1>📹 Real Time Face Recognition</h1>
    <p>Live attendance tracking with AI-powered face detection</p>
</div>
""", unsafe_allow_html=True)

# Retrieve the data from Database
with st.spinner("Retrieving data from Redis database ..."):
    redis_face_db = face_rec.retrieve_data('academy:register')
    st.dataframe(redis_face_db)
st.success("Data successfully retrieved from Redis")

# time
waitTime = 30
setTime = time.time()
realtimepred = face_rec.RealTimePred()

# Real Time Prediction
def video_frame_callback(frame):
    global setTime

    img = frame.to_ndarray(format='bgr24')  # 3 dimension numpy array
    pred_frame = realtimepred.face_prediction(img, redis_face_db, 0.5)

    timenow = time.time()
    difftime = timenow - setTime
    if difftime >= waitTime:
        realtimepred.savelogs_redis()
        setTime = time.time()
        print("Save data to redis")
        
    return av.VideoFrame.from_ndarray(pred_frame, format='bgr24')

webrtc_streamer(
    key='realtimePrediction', 
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

# Instructions
with st.expander("📋 Instructions & Tips"):
    st.markdown("""
    ### How to Use:
    1. Click **Start** to begin
    2. Position your face clearly in the camera view
    3. Wait for recognition (green box indicates success)
    4. Attendance will be automatically marked after least 30s
    
    ### Tips for Better Recognition:
    - Ensure good lighting conditions
    - Keep face centered and at normal distance
    - Avoid excessive movement
    - Remove masks or sunglasses
    - Clean camera lens if blurry
    """)