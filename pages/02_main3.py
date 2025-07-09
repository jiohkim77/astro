import streamlit as st
import numpy as np
import plotly.graph_objects as go

# H-R 다이어그램 데이터 설정 (태양 질량 1 기준 생애 주기)
def get_stellar_evolution():
    time = np.linspace(0, 1, 100)  # 정규화된 시간 (0~1)
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

# Plotly Figure 설정
fig = go.Figure(
    data=[go.Scatter(x=[temp[0]], y=[lum[0]], mode='markers', marker=dict(size=[size[0]], color='red'), name="Star")],
    layout=go.Layout(
        xaxis=dict(title="Temperature (K)", range=[9000, 3000], autorange=False),
        yaxis=dict(title="Luminosity (Solar Units)", range=[0.001, 120], type="log", autorange=False),
        title="H-R Diagram - Stellar Evolution (1 Solar Mass)",
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
                      args=[None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True}])],
    )]
)

# Streamlit에 그래프 표시
st.plotly_chart(fig)

# GitHub에 배포 지침
st.write("To deploy on GitHub, save this script as `02_main3.py`, create a `requirements.txt` with `streamlit plotly numpy`, and use Streamlit Community Cloud.")
