import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# H-R 다이어그램 데이터 설정 (태양 질량 1 기준 생애 주기)
def get_stellar_evolution():
    time = np.linspace(0, 1, 100)  # 정규화된 시간 (0~1)
    # 단계별 데이터 (단순화된 모델)
    temp = np.zeros(100)
    lum = np.zeros(100)
    size = np.zeros(100)
    
    # 원시별 (Protostar)
    temp[:20] = 3000 + 1000 * np.exp(-2 * time[:20])
    lum[:20] = 0.1 + 0.4 * np.exp(-1 * time[:20])
    size[:20] = 5 + 5 * np.exp(-1 * time[:20])
    
    # 주계열성 (Main Sequence)
    temp[20:40] = 5800 - 200 * (time[20:40] - 0.2)
    lum[20:40] = 1.0 - 0.2 * (time[20:40] - 0.2)
    size[20:40] = 1.0 + 0.5 * (time[20:40] - 0.2)
    
    # 적색거성 (Red Giant)
    temp[40:70] = 3500 + 500 * np.exp(-2 * (time[40:70] - 0.4))
    lum[40:70] = 100 - 90 * (time[40:70] - 0.4)
    size[40:70] = 10 + 20 * np.exp(-1 * (time[40:70] - 0.4))
    
    # 백색왜성 (White Dwarf)
    temp[70:] = 8000 - 2000 * (time[70:] - 0.7)
    lum[70:] = 0.01 + 0.04 * np.exp(-2 * (time[70:] - 0.7))
    size[70:] = 0.1 + 0.5 * np.exp(-1 * (time[70:] - 0.7))
    
    return time, temp, lum, size

# Streamlit 앱
st.title("Stellar Evolution on H-R Diagram")

# 데이터 생성 (태양 질량 1로 고정)
time, temp, lum, size = get_stellar_evolution()

# Matplotlib Figure 설정
fig, ax = plt.subplots()
ax.set_xlabel("Temperature (K)")
ax.set_ylabel("Luminosity (Solar Units)")
ax.set_title("H-R Diagram - Stellar Evolution (1 Solar Mass)")
ax.set_xlim(3000, 9000)  # 고정된 온도 범위
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
