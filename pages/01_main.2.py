import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 함수 정의: 변광성 밝기 계산
def calculate_brightness(period, max_brightness, min_brightness, t):
    # 사인 파형을 이용한 밝기 계산
    return (max_brightness - min_brightness) * np.sin(2 * np.pi * t / period) + (max_brightness + min_brightness) / 2

# 앱 설정
st.title("변광성 주기 시뮬레이터")

# 변광성 유형 선택
star_type = st.selectbox("변광성 유형을 선택하세요:", ["세페이드", "RR Lyrae", "맥동변광성"])

# 주기 및 밝기 범위 설정
period = st.slider("주기 (일수)", 1, 500, 72)  # 주기 설정 (기본값 72)
max_brightness = st.slider("최대 밝기", 0.0, 10.0, 8.0)
min_brightness = st.slider("최소 밝기", 0.0, 10.0, 4.0)

# 시간 관련 변수 설정
time_step = 0.1  # 시간 간격 (단위: 일)
total_time = period * 2  # 두 주기 동안 애니메이션

# 밝기 변화 애니메이션 함수
def animate_brightness(i):
    # 시간 값 계산
    t = i * time_step
    brightness = calculate_brightness(period, max_brightness, min_brightness, t)
    
    # 그래프 업데이트
    ax.clear()
    ax.plot(t_values[:i+1], brightness_values[:i+1], color="blue")
    ax.set_xlim(0, total_time)
    ax.set_ylim(min_brightness - 1, max_brightness + 1)
    ax.set_title(f"{star_type} 변광성 밝기 변화 (주기: {period}일)")
    ax.set_xlabel("시간 (일)")
    ax.set_ylabel("밝기")

# 애니메이션 설정
fig, ax = plt.subplots()
t_values = np.arange(0, total_time, time_step)
brightness_values = [calculate_brightness(period, max_brightness, min_brightness, t) for t in t_values]

ani = FuncAnimation(fig, animate_brightness, frames=len(t_values), interval=50)

# 애니메이션 표시
st.pyplot(fig)

# 텍스트로 주기-광도 관계 설명
st.write(f"선택된 변광성 유형: {star_type}")
st.write(f"주기: {period}일")
st.write(f"최대 밝기: {max_brightness}")
st.write(f"최소 밝기: {min_brightness}")

