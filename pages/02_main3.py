import streamlit as st
import numpy as np
import plotly.graph_objects as go

# H-R 다이어그램 데이터 설정 (질량에 따른 생애 주기)
def get_stellar_evolution(mass):
    time = np.linspace(0, 1, 100)  # 정규화된 시간 (0~1)
    temp = np.zeros(100)
    lum = np.zeros(100)
    size = np.zeros(100)
    
    # 원시별 (Protostar)
    temp[:20] = 3000 + 1000 * np.exp(-2 * time[:20])
    lum[:20] = 0.1 * mass + 0.4 * mass * np.exp(-1 * time[:20])
    size[:20] = 5 + 5 * np.exp(-1 * time[:20])
    
    # 주계열성 (Main Sequence)
    temp[20:40] = 5800 * (mass / 1.0) - 200 * (time[20:40] - 0.2)
    lum[20:40] = 1.0 * mass - 0.2 * mass * (time[20:40] - 0.2)
    size[20:40] = 1.0 + 0.5 * (time[20:40] - 0.2)
    
    # 적색거성 (Red Giant)
    temp[40:70] = 3500 + 500 * np.exp(-2 * (time[40:70] - 0.4))
    lum[40:70] = 100 * mass - 90 * mass * (time[40:70] - 0.4)
    size[40:70] = 10 + 20 * np.exp(-1 * (time[40:70] - 0.4))
    
    # 백색왜성 (White Dwarf)
    temp[70:] = 8000 - 2000 * (time[70:] - 0.7)
    lum[70:] = 0.01 * mass + 0.04 * mass * np.exp(-2 * (time[70:] - 0.7))
    size[70:] = 0.1 + 0.5 * np.exp(-1 * (time[70:] - 0.7))
    
    return time, temp, lum, size

# Streamlit 앱
st.title("Stellar Evolution on H-R Diagram")

# 사용자 입력: 별의 질량
mass = st.slider("Star Mass (Solar Masses)", 0.5, 15.0, 1.0)

# 데이터 생성
time, temp, lum, size = get_stellar_evolution(mass)

# Plotly Figure 설정
fig = go.Figure(
    data=[go.Scatter(x=[temp[0]], y=[lum[0]], mode='markers', marker=dict(size=[size[0]], color='red'), name="Star")],
    layout=go.Layout(
        xaxis=dict(title="Temperature (K)", range=[40000, 3000], autorange=False),
        yaxis=dict(title="Luminosity (Solar Units)", range=[0.0001, 100000], type="log", autorange=False),
        title=f"H-R Diagram - Stellar Evolution ({mass} Solar Masses)",
        showlegend=True
    )
)

# 프레임 데이터
frames = [go.Frame(data=[go.Scatter(x=[temp[i]], y=[lum[i]], mode='markers', marker=dict(size=[size[i]], color='red'))]) for i in range(len(time))]
fig.frames = frames

# 자동 애니메이션 설정
fig.update_layout(
    updatemenus=[dict(
        type="buttons",
        buttons=[dict(label="Play",
                      method="animate",
                      args=[None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}}])],
    )]
)

# Streamlit에 그래프 표시
st.plotly_chart(fig)

# GitHub에 배포 지침
st.write("To deploy on GitHub, save this script as `02_main3.py`, create a `requirements.txt` with `streamlit plotly numpy`, and use Streamlit Community Cloud.")
