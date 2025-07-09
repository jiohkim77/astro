import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import io
import matplotlib
import subprocess
matplotlib.use('Agg')  # 비대화형 백엔드 사용

# FFmpeg 설치 확인 함수
def check_ffmpeg():
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

# 함수 정의: 변광성 밝기 계산
def calculate_brightness(period, max_brightness, min_brightness, t, star_type):
    if star_type == "RR Lyrae":
        # RR Lyrae: 비대칭 톱니파 형태
        return (max_brightness - min_brightness) * (np.sin(2 * np.pi * t / period) ** 2) + min_brightness
    elif star_type == "맥동변광성":
        # 맥동변광성: 부드러운 사인파
        return (max_brightness - min_brightness) * np.sin(2 * np.pi * t / period) * 0.8 + (max_brightness + min_brightness) / 2
    else:
        # 세페이드: 기본 사인파
        return (max_brightness - min_brightness) * np.sin(2 * np.pi * t / period) + (max_brightness + min_brightness) / 2

# 앱 설정
st.title("변광성 주기 시뮬레이터")
st.write("""
이 앱은 변광성의 주기적 밝기 변화를 시뮬레이션합니다. 변광성은 주기적으로 밝기가 변하는 별로, 천문학에서 거리 측정에 사용됩니다.
아래에서 변광성 유형, 주기, 밝기 범위, 애니메이션 속도를 설정하여 실시간으로 밝기 변화를 확인해 보세요!
""")

# 변광성 유형 선택
star_type = st.selectbox("변광성 유형을 선택하세요:", ["세페이드", "RR Lyrae", "맥동변광성"])
st.write({
    "세페이드": "세페이드 변광성은 긴 주기(1~100일)와 안정적인 밝기 변화로, 은하 거리 측정에 중요합니다.",
    "RR Lyrae": "RR Lyrae 변광성은 짧은 주기(0.2~1일)와 비대칭 밝기 변화로, 구상성단 연구에 유용합니다.",
    "맥동변광성": "맥동변광성은 다양한 주기와 밝기 변화를 가지며, 별의 진화 연구에 기여합니다."
}[star_type])

# 주기 및 밝기 범위 설정
period = st.slider("주기 (일수)", 1, 500, 72)
max_brightness = st.slider("최대 밝기", 0.0, 10.0, 8.0)
min_brightness = st.slider("최소 밝기", 0.0, max_brightness, 4.0)
fps = st.slider("애니메이션 속도 (FPS)", 5, 30, 20)

# 시간 관련 변수 설정
time_step = 0.1
total_time = period * 2
t_values = np.arange(0, total_time, time_step)

# 애니메이션 설정
fig, ax = plt.subplots()

def animate_brightness(i):
    t = i * time_step
    brightness = calculate_brightness(period, max_brightness, min_brightness, t, star_type)
    ax.clear()
    ax.plot(t_values[:i+1], [calculate_brightness(period, max_brightness, min_brightness, t, star_type) for t in t_values[:i+1]], color="blue")
    ax.set_xlim(0, total_time)
    ax.set_ylim(min_brightness - 1, max_brightness + 1)
    ax.set_title(f"{star_type} 변광성 밝기 변화 (주기: {period}일)")
    ax.set_xlabel("시간 (일)")
    ax.set_ylabel("밝기")

# 애니메이션 생성
ani = FuncAnimation(fig, animate_brightness, frames=len(t_values), interval=1000/fps)

# FFmpeg 설치 확인
if check_ffmpeg():
    try:
        # MP4로 저장 시도
        buffer = io.BytesIO()
        ani.save(buffer, format='mp4', fps=fps, writer='ffmpeg')
        buffer.seek(0)
        st.video(buffer)
    except Exception as e:
        st.error(f"MP4 생성 중 오류 발생: {str(e)}")
        st.warning("MP4 생성에 실패했습니다. GIF로 전환하여 표시합니다.")
        # GIF로 폴백
        buffer = io.BytesIO()
        ani.save(buffer, format='gif', fps=fps, writer='pillow')
        buffer.seek(0)
        st.image(buffer)
else:
    st.warning("FFmpeg가 설치되지 않았습니다. GIF로 표시합니다.")
    # GIF로 저장
    buffer = io.BytesIO()
    ani.save(buffer, format='gif', fps=fps, writer='pillow')
    buffer.seek(0)
    st.image(buffer)

# 주기-광도 관계 설명
st.write("### 주기-광도 관계")
st.write(f"""
선택된 변광성: **{star_type}**  
주기: **{period}일**  
최대 밝기: **{max_brightness}**  
최소 밝기: **{min_brightness}**  
변광성의 주기는 밝기(절대 등급)와 밀접한 관계가 있습니다. 예를 들어, 세페이드 변광성은 주기가 길수록 더 밝습니다.
이 시뮬레이터를 통해 주기와 밝기 변화를 조정하며 천문학적 현상을 탐구해 보세요!
""")

# 리소스 정리
plt.close(fig)
