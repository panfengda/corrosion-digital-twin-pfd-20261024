
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="深海管道腐蚀数字孪生",
    layout="wide"
)

st.title("深海管道腐蚀监测数字孪生平台")
st.caption("演示原型 · 所有数据均为模拟数据，不用于实际工程安全判断")

rng = np.random.default_rng(42)
n = 40
position = np.arange(1, n + 1)

wall = 20 - 0.025 * position + rng.normal(0, 0.12, n)
wall[27:31] -= 0.7

df = pd.DataFrame({
    "管段编号": [f"P-{i:02d}" for i in position],
    "位置": position,
    "当前壁厚_mm": np.round(wall, 2)
})

threshold = st.sidebar.slider(
    "演示预警阈值（mm）",
    min_value=15.0,
    max_value=20.0,
    value=18.5,
    step=0.1
)

alerts = df[df["当前壁厚_mm"] < threshold]

c1, c2, c3 = st.columns(3)
c1.metric("监测管段", f"{n}")
c2.metric("模拟平均壁厚", f"{wall.mean():.2f} mm")
c3.metric("待复核管段", f"{len(alerts)}")

left, right = st.columns([1.3, 1])

with left:
    st.subheader("管道三维示意")

    theta = np.linspace(0, 2 * np.pi, 32)
    x = np.linspace(0, 12, n)

    X, T = np.meshgrid(x, theta)
    Y = 0.6 * np.cos(T)
    Z = 0.6 * np.sin(T)

    fig3d = go.Figure(
        go.Surface(
            x=X,
            y=Y,
            z=Z,
            surfacecolor=np.tile(wall, (len(theta), 1)),
            colorscale="RdYlGn",
            colorbar=dict(title="壁厚 mm")
        )
    )
    fig3d.update_layout(
        height=430,
        scene=dict(
            xaxis_title="管道长度",
            yaxis_title="Y",
            zaxis_title="Z",
            aspectmode="manual",
            aspectratio=dict(x=2.5, y=1, z=1)
        ),
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig3d, use_container_width=True)

with right:
    st.subheader("壁厚变化分布")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=position,
        y=wall,
        mode="lines+markers",
        name="模拟壁厚"
    ))
    fig.add_hline(
        y=threshold,
        line_dash="dash",
        annotation_text="演示阈值"
    )
    fig.update_layout(
        height=300,
        xaxis_title="管段位置",
        yaxis_title="壁厚（mm）"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("待复核管段")
    if alerts.empty:
        st.success("当前没有触发演示阈值的管段")
    else:
        st.dataframe(alerts, hide_index=True)

st.subheader("模拟监测数据")
st.dataframe(df, use_container_width=True, hide_index=True)
st.download_button(
    "下载模拟数据 CSV",
    df.to_csv(index=False).encode("utf-8-sig"),
    file_name="simulated_wall_thickness.csv",
    mime="text/csv"
)
