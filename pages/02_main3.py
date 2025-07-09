import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# H-R 다이어그램 데이터 설정 (질량에 따른 생애 주기)
def get_stellar_evolution(mass):
    time = np.linspace(0, 1, 100)  # 정규화된 시간 (0~1)
    if mass <= 2:  # 저질량 별 (예: M형)
        temp = 3500 + 500 * np.exp(-5 * time)
        lum = 0.01 + 0.09 * np.exp(-2 * time)
        size = 1 + 4 * np.exp(-2 * time)
    elif 2 < mass <= 8:  # 중간질량 별 (예: G형, K형)
        temp = 6000 - 2000 * time
        lum = 1 - 0.8 * time
        size = 1 + 9 * np.exp(-2 * time)
    else:  # 고질량 별 (예: O형, B형)
        temp = 30000 - 29000 * time
        lum = 100 - 95 * time
        size = 10 + 40 * np.exp(-2 * time)
    return time, temp, lum, size

# Streamlit 앱
st.title("Stellar Evolution on H-R Diagram")

# 사용자 입력: 별의 질량
mass = st.slider("Star Mass (Solar Masses)", 0.5, 15.0, 1.0)

# 데이터 생성
time, temp, lum, size = get_stellar_evolution(mass)

# Matplotlib Figure 설정
fig, ax = plt.subplots()
ax.set_xlabel("Temperature (K)")
ax.set_ylabel("Luminosity (Solar Units)")
ax.set_title("H-R Diagram - Stellar Evolution")
ax.set_xlim(3000, 35000)  # 고정된 온도 범위
ax.set_ylim(0, 120)  # 고정된 광도 범위
ax.invert_xaxis()
scatter = ax.scatter([temp[0]], [lum[0]], s=[size[0]], c='red', label="Star")
ax.legend()

# 애니메이션 업데이트 함수
def update(frame):
    x = [temp[frame]]
    y = [lum[frame]]
    s = [size[frame]]  # 크기 변화 반영
    scatter.set_offsets(np.c_[x, y])
    scatter.set_sizes(s)
    return scatter,

# 애니메이션 생성
ani = FuncAnimation(fig, update, frames=range(len(time)), interval=50, blit=True)

# Streamlit에 그래프 표시
st.pyplot(fig)

# GitHub에 배포 지침
st.write("To deploy on GitHub, save this script as `stellar_evolution_app.py`, create a `requirements.txt` with `streamlit matplotlib numpy`, and use Streamlit Community Cloud.")
