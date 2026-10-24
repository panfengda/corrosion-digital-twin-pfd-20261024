
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# =========================
# 1. 页面配置
# =========================
st.set_page_config(
    page_title="OCEAN TWIN | 海底管道数字孪生",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# 2. 工业深色界面
# =========================
st.markdown("""
<style>
.stApp {
    background: #08121f;
    color: #e6f0fa;
}
[data-testid="stHeader"] {
    background: rgba(8,18,31,0.95);
}
[data-testid="stSidebar"] {
    background: #101e30;
    border-right: 1px solid #263b52;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1800px;
}
h1, h2, h3 {
    color: #f0f7ff !important;
}
p, label, span {
    color: inherit;
}
div[data-testid="stMetric"] {
    background: #112238;
    border: 1px solid #28435d;
    padding: 16px;
    border-radius: 12px;
}
div[data-testid="stMetricLabel"] {
    color: #9db6ce !important;
}
div[data-testid="stMetricValue"] {
    color: #55d9ee !important;
}
.panel {
    background: #101e30;
    border: 1px solid #28435d;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 12px;
}
.eyebrow {
    color: #55d9ee;
    font-size: 12px;
    letter-spacing: 2px;
    font-weight: 700;
}
.muted {
    color: #91a9c2;
    font-size: 13px;
}
.status {
    color: #ffc46b;
    border: 1px solid #73572e;
    background: #302719;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
}
div[data-testid="stDataFrame"] {
    border: 1px solid #28435d;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 3. 模拟监测数据
# =========================
rng = np.random.default_rng(42)
n = 40
position = np.arange(1, n + 1)

wall = 20 - 0.025 * position + rng.normal(0, 0.12, n)
wall[27:31] -= 0.7

df = pd.DataFrame({
    "管段编号": [f"P-{i:02d}" for i in position],
    "位置": position,
    "当前壁厚_mm": np.round(wall, 2),
    "数据类型": ["模拟数据"] * n
})

# =========================
# 4. 左侧控制面板
# =========================
st.sidebar.markdown(
    '<div class="eyebrow">OCEAN TWIN</div>',
    unsafe_allow_html=True
)
st.sidebar.title("监测控制中心")
st.sidebar.caption("SUBSEA INTEGRITY SYSTEM")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "系统导航",
    ["综合监测", "管段数据", "系统说明"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 监测参数")

threshold = st.sidebar.slider(
    "演示预警阈值 (mm)",
    min_value=15.0,
    max_value=20.0,
    value=18.5,
    step=0.1
)

selected = st.sidebar.selectbox(
    "选择重点管段",
    df["管段编号"].tolist(),
    index=28
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    '<span class="muted">● 演示系统运行中</span>',
    unsafe_allow_html=True
)
st.sidebar.caption("所有数据均为模拟数据")

# =========================
# 5. 顶部标题
# =========================
title_col, status_col = st.columns([4, 1])

with title_col:
    st.markdown(
        '<div class="eyebrow">OFFSHORE ENGINEERING / DIGITAL TWIN</div>',
        unsafe_allow_html=True
    )
    st.title("深海管道腐蚀监测平台")
    st.caption("SUBSEA PIPELINE INTEGRITY · 数字孪生演示原型")

with status_col:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="status">● SIMULATION MODE</div>',
        unsafe_allow_html=True
    )
    st.caption("数据更新时间：" + datetime.now().strftime("%H:%M:%S"))

st.markdown("---")

# =========================
# 6. 指标计算
# =========================
alerts = df[df["当前壁厚_mm"] < threshold]
avg_wall = float(df["当前壁厚_mm"].mean())
min_wall = float(df["当前壁厚_mm"].min())

if page == "综合监测":

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("监测管段", f"{n:02d}", "模拟测点")
    m2.metric("平均壁厚", f"{avg_wall:.2f} mm")
    m3.metric("最小壁厚", f"{min_wall:.2f} mm")
    m4.metric("待复核位置", f"{len(alerts):02d}", "演示阈值筛选")

    st.markdown("### 三维资产与状态监测")
    left, right = st.columns([1.65, 1])

    # =========================
    # 7. 三维海底场景
    # =========================
    with left:
        st.markdown(
            '<div class="eyebrow">01 / 3D ASSET VIEW</div>',
            unsafe_allow_html=True
        )
        st.subheader("海底输送管道")

        # 管道表面
        x = np.linspace(0, 12, n)
        theta = np.linspace(0, 2 * np.pi, 40)
        X, T = np.meshgrid(x, theta)

        radius = 0.38
        Y = radius * np.cos(T)
        Z = -0.58 + radius * np.sin(T)

        color_values = np.tile(wall, (len(theta), 1))

        fig3d = go.Figure()

        # 海床表面
        sx = np.linspace(-1, 13, 36)
        sy = np.linspace(-2.5, 2.5, 24)
        SX, SY = np.meshgrid(sx, sy)

        SZ = (
            -1.03
            + 0.06 * np.sin(SX * 1.4)
            + 0.04 * np.cos(SY * 2.2)
        )

        fig3d.add_trace(go.Surface(
            x=SX,
            y=SY,
            z=SZ,
            colorscale=[
                [0, "#172c3b"],
                [0.5, "#254357"],
                [1, "#3c5968"]
            ],
            showscale=False,
            opacity=0.95,
            hoverinfo="skip",
            name="海床"
        ))

        # 管道表面按壁厚着色
        fig3d.add_trace(go.Surface(
            x=X,
            y=Y,
            z=Z,
            surfacecolor=color_values,
            colorscale=[
                [0.0, "#ed5353"],
                [0.25, "#ffb15c"],
                [0.5, "#f5e995"],
                [0.75, "#55c995"],
                [1.0, "#159eaa"]
            ],
            cmin=float(wall.min()),
            cmax=float(wall.max()),
            colorbar=dict(
                title=dict(text="壁厚 mm", font=dict(color="#dce9f7")),
                tickfont=dict(color="#dce9f7"),
                bgcolor="#101e30",
                outlinecolor="#38516b",
                x=1.02
            ),
            opacity=1,
            name="管道壁厚",
            hovertemplate="壁厚：%{surfacecolor:.2f} mm<extra></extra>"
        ))

        # 管道检测点
        fig3d.add_trace(go.Scatter3d(
            x=x,
            y=np.zeros(n),
            z=np.full(n, -0.18),
            mode="markers",
            marker=dict(
                size=3.5,
                color=wall,
                colorscale="RdYlGn",
                cmin=float(wall.min()),
                cmax=float(wall.max()),
                showscale=False,
                line=dict(color="#e6f7ff", width=1)
            ),
            customdata=np.column_stack([position, wall]),
            hovertemplate=(
                "管段位置：%{customdata[0]}<br>"
                "壁厚：%{customdata[1]:.2f} mm"
                "<extra></extra>"
            ),
            name="检测位置"
        ))

        fig3d.update_layout(
            height=510,
            paper_bgcolor="#101e30",
            plot_bgcolor="#101e30",
            margin=dict(l=0, r=30, t=10, b=0),
            scene=dict(
                bgcolor="#101e30",
                xaxis=dict(
                    title="管道长度",
                    color="#9bb4cc",
                    gridcolor="#294158",
                    zerolinecolor="#294158"
                ),
                yaxis=dict(
                    title="横向",
                    color="#9bb4cc",
                    gridcolor="#294158",
                    zerolinecolor="#294158"
                ),
                zaxis=dict(
                    title="高程",
                    color="#9bb4cc",
                    gridcolor="#294158",
                    zerolinecolor="#294158"
                ),
                aspectmode="manual",
                aspectratio=dict(x=2.4, y=1, z=0.8),
                camera=dict(eye=dict(x=1.6, y=1.6, z=1.1))
            ),
            showlegend=False
        )

        st.plotly_chart(
            fig3d,
            use_container_width=True,
            config={"displaylogo": False}
        )

        st.caption(
            "三维管道与海床为程序生成的示意几何；"
            "壁厚颜色映射模拟数据，并非真实海底地形或设备扫描。"
        )

    # =========================
    # 8. 右侧数据面板
    # =========================
    with right:
        st.markdown(
            '<div class="eyebrow">02 / WALL THICKNESS</div>',
            unsafe_allow_html=True
        )
        st.subheader("壁厚演化分布")

        line = go.Figure()

        line.add_trace(go.Scatter(
            x=position,
            y=wall,
            mode="lines+markers",
            line=dict(color="#46c8f0", width=2.5),
            marker=dict(size=6, color="#71e4f4"),
            name="模拟壁厚"
        ))

        line.add_hline(
            y=threshold,
            line_dash="dash",
            line_color="#ffad55",
            annotation_text="演示阈值",
            annotation_font_color="#ffad55"
        )

        line.update_layout(
            height=280,
            paper_bgcolor="#101e30",
            plot_bgcolor="#101e30",
            font=dict(color="#dce9f7"),
            margin=dict(l=10, r=10, t=25, b=10),
            xaxis=dict(
                title="管段位置",
                gridcolor="#263b52",
                zeroline=False
            ),
            yaxis=dict(
                title="壁厚 (mm)",
                gridcolor="#263b52",
                zeroline=False
            ),
            showlegend=False
        )

        st.plotly_chart(
            line,
            use_container_width=True,
            config={"displaylogo": False}
        )

        st.markdown(
            '<div class="eyebrow">03 / INSPECTION LIST</div>',
            unsafe_allow_html=True
        )
        st.subheader("待复核管段")

        if alerts.empty:
            st.success("当前没有触发演示阈值的管段")
        else:
            st.dataframe(
                alerts[["管段编号", "位置", "当前壁厚_mm"]],
                use_container_width=True,
                hide_index=True,
                height=220
            )

    # =========================
    # 9. 底部监测数据
    # =========================
    st.markdown("---")
    st.markdown("### 监测数据明细")

    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "下载模拟监测数据 CSV",
        data=csv,
        file_name="simulated_corrosion_data.csv",
        mime="text/csv"
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

elif page == "管段数据":

    st.subheader("管段数据查询")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    row = df[df["管段编号"] == selected].iloc[0]

    a, b, c = st.columns(3)
    a.metric("选中管段", row["管段编号"])
    b.metric("当前位置", f'{row["位置"]}')
    c.metric("当前壁厚", f'{row["当前壁厚_mm"]:.2f} mm')

    st.info(
        "当前数据由程序模拟生成。实际工程应用需接入经过核验的检测记录。"
    )

else:

    st.subheader("系统说明")

    st.markdown("""
    本系统为深海管道腐蚀监测数字孪生演示原型。

    **当前已实现**
    - 模拟管段壁厚数据生成
    - 三维管道及海床示意
    - 壁厚颜色映射与交互查看
    - 壁厚趋势图
    - 可调节演示阈值及待复核列表
    - 模拟数据导出

    **当前尚未实现**
    - 真实传感器和在线数据采集
    - 历史数据库及连续监测存储
    - 真实海底地形和精细设备模型
    - 经验证的腐蚀速率与剩余寿命预测
    - 经过工程标准验证的安全预警

    当前所有数据均为模拟数据。页面中的阈值只用于演示，
    不代表真实设备的安全限值。
    """)
