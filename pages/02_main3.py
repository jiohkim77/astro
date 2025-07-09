import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# H-R 다이어그램 데이터 설정 (예시 데이터)
def get_stellar_data(mass):
    time = np.linspace(0, 10, 100)  # 시간 (임의 단위)
    temp = 10000 * np.exp(-0.1 * time) if mass > 5 else 6000 * np.exp(-0.05 * time)  # 온도 변화
    lum = 100 * np.exp(-0.2 * time) if mass > 5 else 1 * np.exp(-0.1 * time)  # 광도 변화
    size = 10 * np.exp(-0.15 * time) if mass > 5 else 5 * np.exp(-0.05 * time)  # 크기 변화
    return time, temp, lum, size

# Streamlit 앱
st.title("Stellar Evolution on H-R Diagram")

# 사용자 입력: 별의 질량
mass = st.slider("Star Mass (Solar Masses)", 1.0, 10.0, 4.71)

# 데이터 생성
time, temp, lum, size = get_stellar_data(mass)

# Matplotlib Figure 설정
fig, ax = plt.subplots()
ax.set_xlabel("Temperature (K)")
ax.set_ylabel("Luminosity (Solar Units)")
ax.set_title("H-R Diagram - Stellar Evolution")
ax.set_xlim(2000, 12000)  # 고정된 온도 범위
ax.set_ylim(0, 120)  # 고정된 광도 범위
ax.invert_xaxis()
scatter = ax.scatter([temp[0]], [lum[0]], s=[size[0]], c='red', label="Star")

# 애니메이션 업데이트 함수
def update(frame):
    x = [temp[frame]]
    y = [lum[frame]]
    s = [size[frame]]  # 단일 크기 값으로 리스트로 전달
    scatter.set_offsets(np.c_[x, y])
    scatter.set_sizes(s)
    return scatter,

# 애니메이션 생성
ani = FuncAnimation(fig, update, frames=range(len(time)), interval=50, blit=True)

# Streamlit에 그래프 표시
st.pyplot(fig)

# GitHub에 배포 지침
st.write("To deploy on GitHub, save this script as `stellar_evolution_app.py`, create a `requirements.txt` with `streamlit matplotlib numpy`, and use Streamlit Community Cloud.")
