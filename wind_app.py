
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="PFD | Offshore Wind Digital Twin",
    page_icon="🌊",
    layout="wide"
)

# -------------------- Theme --------------------
st.markdown("""
<style>
.stApp {
    background: #071321;
    color: #edf5ff;
}
[data-testid="stHeader"] {
    background: #071321;
}
[data-testid="stSidebar"] {
    background: #0c1d30;
    border-right: 1px solid #29435b;
}
.block-container {
    max-width: 1800px;
    padding-top: 1.1rem;
    padding-bottom: 2rem;
}
h1, h2, h3 {
    color: #f2f7ff !important;
}
h1 {font-size: 2rem !important; font-weight: 800 !important;}
h2 {font-size: 1.35rem !important;}
h3 {font-size: 1.05rem !important;}
[data-testid="stMetric"] {
    background: linear-gradient(140deg, #142a40, #0f2033);
    border: 1px solid #2a465f;
    border-radius: 12px;
    padding: 15px 18px;
}
[data-testid="stMetricLabel"] {
    color: #a9bfd4 !important;
}
[data-testid="stMetricValue"] {
    color: #58d9ec !important;
    font-weight: 750 !important;
}
[data-testid="stPlotlyChart"] {
    background: #0c1b2b;
    border: 1px solid #263f57;
    border-radius: 12px;
    padding: 5px;
}
.eyebrow {
    color: #53d7e8;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 2px;
}
.small-note {
    color: #9eb4c9;
    font-size: 0.82rem;
}
</style>
""", unsafe_allow_html=True)

# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown(
        '<div style="font-size:25px;font-weight:850;letter-spacing:2px;'
        'color:#f3f8ff">PFD <span style="color:#53d7e8">/</span></div>',
        unsafe_allow_html=True
    )
    st.caption("OFFSHORE WIND DIGITAL TWIN")
    st.markdown("---")
    st.subheader("运行控制")

    rotor_angle = st.slider(
        "叶轮旋转角度",
        min_value=0,
        max_value=360,
        value=25,
        step=5,
        help="演示叶轮旋转状态；拖动滑块查看不同角度。"
    )

    wind_speed = st.slider(
        "风速 (m/s)", 0.0, 35.0, 12.0, 0.5
    )
    wave_height = st.slider(
        "浪高 (m)", 0.0, 15.0, 2.5, 0.1
    )
    salinity = st.slider(
        "海水盐度 (PSU)", 20.0, 40.0, 35.0, 0.5
    )
    damage_level = st.slider(
        "叶片表面损伤演示程度 (%)",
        0, 100, 28, 1
    )

    st.markdown("---")
    st.caption("当前为模拟数据演示，不连接真实风机。")

# -------------------- Header --------------------
left, right = st.columns([4, 1])
with left:
    st.markdown(
        '<div class="eyebrow">PFD / OFFSHORE ENGINEERING</div>',
        unsafe_allow_html=True
    )
    st.title("海上风电叶片数字孪生")
    st.caption("OFFSHORE WIND TURBINE · CONDITION MONITORING")
with right:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align:center;border:1px solid #28644f;'
        'background:#103328;color:#6de5b7;border-radius:8px;'
        'padding:8px;font-size:12px;font-weight:750">● DEMO MODE</div>',
        unsafe_allow_html=True
    )
    st.caption(datetime.now().strftime("%Y-%m-%d %H:%M"))

st.markdown("---")

# -------------------- KPIs --------------------
power_estimate = max(0, min(100, ((wind_speed - 3) / 12) ** 3 * 100))
power_estimate = min(power_estimate, 100)

a, b, c, d = st.columns(4)
a.metric("风速", f"{wind_speed:.1f} m/s")
b.metric("浪高", f"{wave_height:.1f} m")
c.metric("海水盐度", f"{salinity:.1f} PSU")
d.metric("损伤演示值", f"{damage_level}%")

# -------------------- 3D Scene --------------------
st.markdown("## 三维风机与海洋环境")
scene_col, info_col = st.columns([1.7, 1], gap="large")

with scene_col:
    st.markdown(
        '<div class="eyebrow">01 / OFFSHORE ASSET VIEW</div>',
        unsafe_allow_html=True
    )

    fig = go.Figure()

    # Ocean surface
    ox = np.linspace(-7, 7, 35)
    oy = np.linspace(-7, 7, 35)
    OX, OY = np.meshgrid(ox, oy)
    OZ = -0.3 + 0.035 * np.sin(OX * 1.8) * np.cos(OY * 1.4)

    fig.add_trace(go.Surface(
        x=OX, y=OY, z=OZ,
        colorscale=[
            [0, "#082d49"],
            [0.5, "#0b4968"],
            [1, "#16738a"]
        ],
        showscale=False,
        opacity=0.95,
        hoverinfo="skip",
        name="海面"
    ))

    # Tower: tapered cylindrical surface
    theta = np.linspace(0, 2 * np.pi, 32)
    tz = np.linspace(0, 5.5, 25)
    TH, TZ = np.meshgrid(theta, tz)
    tower_r = 0.13 - 0.045 * (TZ / 5.5)
    TX = tower_r * np.cos(TH)
    TY = tower_r * np.sin(TH)

    fig.add_trace(go.Surface(
        x=TX, y=TY, z=TZ,
        colorscale=[[0, "#b8c9d8"], [0.5, "#eef5fa"], [1, "#718ca3"]],
        showscale=False,
        hoverinfo="skip",
        name="塔筒",
        lighting=dict(ambient=0.65, diffuse=0.8, specular=0.5)
    ))

    # Hub position
    hub_x, hub_y, hub_z = 0.0, 0.0, 5.55
    fig.add_trace(go.Scatter3d(
        x=[hub_x], y=[hub_y], z=[hub_z],
        mode="markers",
        marker=dict(size=9, color="#e8f5ff",
                    line=dict(color="#53d7e8", width=2)),
        name="轮毂",
        hovertemplate="风机轮毂<extra></extra>"
    ))

    # Three rotor blades, with synthetic damage color sections
    angle0 = np.deg2rad(rotor_angle)
    blade_length = 2.55
    radii = np.linspace(0.15, blade_length, 36)

    for blade_index in range(3):
        angle = angle0 + blade_index * 2 * np.pi / 3
        bx = hub_x + radii * np.cos(angle)
        by = hub_y + radii * np.sin(angle)
        bz = hub_z + 0.22 * radii * np.sin(angle + 0.6)

        # Divide each blade into sections so damage can be highlighted.
        for j in range(len(radii) - 1):
            fraction = (j + 1) / len(radii)
            damaged = fraction > (1 - damage_level / 125)

            if damaged and damage_level >= 1:
                color = "#ff735e" if fraction > 0.78 else "#ffbc69"
            else:
                color = "#e5edf5"

            fig.add_trace(go.Scatter3d(
                x=bx[j:j+2],
                y=by[j:j+2],
                z=bz[j:j+2],
                mode="lines",
                line=dict(color=color, width=7),
                showlegend=False,
                hovertemplate=(
                    f"叶片 {blade_index + 1}<br>"
                    f"径向分区 {fraction:.0%}<extra></extra>"
                )
            ))

    # Floating foundation / simplified support
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[-0.25, 0.05],
        mode="lines",
        line=dict(color="#9cb7c8", width=10),
        showlegend=False,
        hoverinfo="skip"
    ))

    fig.update_layout(
        height=610,
        paper_bgcolor="#0c1b2b",
        plot_bgcolor="#0c1b2b",
        margin=dict(l=0, r=0, t=5, b=0),
        font=dict(color="#dce8f4"),
        showlegend=False,
        scene=dict(
            bgcolor="#0c1b2b",
            xaxis=dict(visible=False, range=[-4, 4]),
            yaxis=dict(visible=False, range=[-4, 4]),
            zaxis=dict(visible=False, range=[-1, 9]),
            aspectmode="manual",
            aspectratio=dict(x=1, y=1, z=1.15),
            camera=dict(eye=dict(x=1.55, y=1.7, z=1.1))
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displaylogo": False}
    )
    st.caption(
        "三维风机为程序生成的简化示意模型；"
        "叶片颜色为损伤演示效果，不代表真实检测结果。"
    )

# -------------------- Right panels --------------------
with info_col:
    st.markdown(
        '<div class="eyebrow">02 / BLADE CONDITION</div>',
        unsafe_allow_html=True
    )
    st.subheader("叶片状态评估")

    if damage_level < 25:
        status_text = "常规观察"
        status_color = "#5de0ad"
    elif damage_level < 60:
        status_text = "建议检查"
        status_color = "#ffbd66"
    else:
        status_text = "重点复核"
        status_color = "#ff6673"

    st.markdown(
        f'<div style="background:#102338;border:1px solid #2b465e;'
        f'border-radius:12px;padding:18px">'
        f'<div style="font-size:13px;color:#a9bfd4">演示状态</div>'
        f'<div style="font-size:25px;font-weight:800;color:{status_color};'
        f'margin-top:8px">{status_text}</div>'
        f'<div style="font-size:13px;color:#9eb4c9;margin-top:10px">'
        f'依据可调节的模拟损伤程度显示，不代表工程诊断。</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 环境参数")
    env_df = pd.DataFrame({
        "参数": ["风速", "浪高", "海水盐度"],
        "当前值": [
            f"{wind_speed:.1f} m/s",
            f"{wave_height:.1f} m",
            f"{salinity:.1f} PSU"
        ],
        "数据来源": ["模拟", "模拟", "模拟"]
    })

    st.dataframe(
        env_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### 损伤分区示意")
    damage_df = pd.DataFrame({
        "叶片分区": ["根部", "中段", "外段"],
        "演示损伤程度 (%)": [
            int(damage_level * 0.25),
            int(damage_level * 0.65),
            int(damage_level)
        ]
    })

    st.dataframe(
        damage_df,
        use_container_width=True,
        hide_index=True
    )

# -------------------- Bottom panel --------------------
st.markdown("---")
st.markdown("## 监测与维护建议")

if damage_level < 25:
    advice = "继续按计划开展巡检，并持续记录叶片表面状态。"
elif damage_level < 60:
    advice = "建议安排进一步目视检查或无损检测，确认损伤范围与深度。"
else:
    advice = "建议优先复核相关区域，并依据真实检测数据和适用标准评估维修需求。"

st.info(advice)

st.markdown(
    '<div class="small-note">PFD · OCEAN TWIN · '
    '模拟数据演示原型。当前版本不接入真实风机传感器，'
    '不用于实际设备安全判断或剩余寿命预测。</div>',
    unsafe_allow_html=True
)

