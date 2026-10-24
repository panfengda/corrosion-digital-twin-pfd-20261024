import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ============================================================
# OCEAN TWIN | Subsea Pipeline Corrosion Monitoring Demo
# All default measurements are synthetic demonstration data.
# ============================================================

st.set_page_config(
    page_title="OCEAN TWIN | 深海管道数字孪生",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------- Theme -----------------------------
st.markdown(
    """
    <style>
    :root {
        --bg: #07111f;
        --panel: #101f31;
        --panel-2: #14283d;
        --border: #29435c;
        --text: #edf4fc;
        --muted: #a7bbcf;
        --cyan: #52d7e8;
        --green: #5de0ad;
        --amber: #ffbd66;
        --red: #ff6673;
    }
    .stApp {
        background: var(--bg);
        color: var(--text);
        font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
    }
    [data-testid="stHeader"] {
        background: rgba(7, 17, 31, 0.96);
    }
    [data-testid="stSidebar"] {
        background: #0c1929;
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] * {
        color: #dce7f4;
    }
    .main .block-container {
        max-width: 1800px;
        padding: 1.25rem 2rem 2.5rem;
    }
    h1, h2, h3 {
        color: var(--text) !important;
        letter-spacing: -0.3px;
    }
    h1 {
        font-size: 2rem !important;
        font-weight: 780 !important;
    }
    h2 {
        font-size: 1.35rem !important;
        font-weight: 720 !important;
    }
    h3 {
        font-size: 1.05rem !important;
        font-weight: 680 !important;
    }
    p, label, .stMarkdown {
        color: #d0dceb;
    }
    [data-testid="stCaptionContainer"] {
        color: var(--muted) !important;
    }
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #14283d 0%, #102033 100%);
        border: 1px solid var(--border);
        border-radius: 13px;
        padding: 16px 18px;
        min-height: 112px;
    }
    [data-testid="stMetricLabel"] {
        color: #b5c8dc !important;
        font-size: 0.88rem !important;
    }
    [data-testid="stMetricValue"] {
        color: #f2f7fd !important;
        font-size: 1.85rem !important;
        font-weight: 760 !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.8rem !important;
    }
    [data-testid="stPlotlyChart"] {
        background: #0d1b2b;
        border: 1px solid #243a51;
        border-radius: 13px;
        padding: 6px;
    }
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 10px;
    }
    .eyebrow {
        color: var(--cyan);
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 6px;
    }
    .subtitle {
        color: var(--muted);
        font-size: 0.92rem;
        margin-top: -7px;
    }
    .status-pill {
        display: inline-block;
        color: #72e5ba;
        background: #103328;
        border: 1px solid #24674f;
        padding: 7px 12px;
        border-radius: 8px;
        font-size: 0.76rem;
        font-weight: 750;
        letter-spacing: 0.4px;
    }
    .info-panel {
        background: #101f31;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 15px 17px;
    }
    .small-muted {
        color: #9eb2c7;
        font-size: 0.82rem;
    }
    div[data-baseweb="select"] > div {
        background: #14283d;
        border-color: #35516d;
    }
    .stButton button, .stDownloadButton button {
        border-radius: 8px;
        border: 1px solid #35516d;
        background: #14283d;
        color: #f2f7fd;
        font-weight: 650;
    }
    .stButton button:hover, .stDownloadButton button:hover {
        border-color: var(--cyan);
        color: var(--cyan);
    }
    hr {
        border-color: #263b52;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------- Data ------------------------------
def make_demo_data(seed: int = 42, count: int = 40) -> pd.DataFrame:
    """Generate synthetic wall-thickness values for interface demonstration."""
    rng = np.random.default_rng(seed)
    position = np.arange(1, count + 1)
    wall = 20.0 - 0.025 * position + rng.normal(0, 0.12, count)
    # A deliberately lower-thickness region for visual demonstration.
    wall[27:31] -= 0.7
    return pd.DataFrame(
        {
            "管段编号": [f"P-{i:02d}" for i in position],
            "位置": position,
            "当前壁厚_mm": np.round(wall, 2),
        }
    )


def normalize_uploaded_data(uploaded_file) -> pd.DataFrame:
    """Read a CSV/XLSX file and map common column names to the app schema."""
    if uploaded_file.name.lower().endswith(".xlsx"):
        raw = pd.read_excel(uploaded_file)
    else:
        try:
            raw = pd.read_csv(uploaded_file, encoding="utf-8-sig")
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            raw = pd.read_csv(uploaded_file, encoding="gb18030")

    raw.columns = [str(c).strip() for c in raw.columns]
    position_candidates = ["位置", "position", "point", "index", "测点", "管段位置"]
    wall_candidates = [
        "当前壁厚_mm", "壁厚_mm", "壁厚", "wall_thickness",
        "thickness", "wall thickness", "当前壁厚", "测量壁厚"
    ]
    id_candidates = ["管段编号", "管段", "id", "segment", "管段ID", "测点编号"]

    def find_column(candidates):
        lower_map = {c.lower(): c for c in raw.columns}
        for candidate in candidates:
            if candidate.lower() in lower_map:
                return lower_map[candidate.lower()]
        return None

    pos_col = find_column(position_candidates)
    wall_col = find_column(wall_candidates)
    id_col = find_column(id_candidates)

    if wall_col is None:
        raise ValueError(
            "未找到壁厚列。请使用“当前壁厚_mm”“壁厚”“wall_thickness”或“thickness”作为列名。"
        )

    wall = pd.to_numeric(raw[wall_col], errors="coerce")
    if pos_col is not None:
        pos = pd.to_numeric(raw[pos_col], errors="coerce")
    else:
        pos = pd.Series(np.arange(1, len(raw) + 1), index=raw.index)

    valid = wall.notna() & pos.notna()
    raw = raw.loc[valid].copy()
    wall = wall.loc[valid].astype(float)
    pos = pos.loc[valid].astype(float)

    if raw.empty:
        raise ValueError("文件中没有可用的数值壁厚记录。")

    if id_col is not None:
        ids = raw[id_col].astype(str).tolist()
    else:
        ids = [f"P-{int(p):02d}" if float(p).is_integer() else f"P-{p:g}" for p in pos]

    result = pd.DataFrame(
        {
            "管段编号": ids,
            "位置": pos.to_numpy(),
            "当前壁厚_mm": wall.to_numpy(),
        }
    )
    return result.sort_values("位置").reset_index(drop=True)


def make_dark_layout(fig, height=350, margin=None):
    """Apply a consistent dark industrial theme to Plotly charts."""
    fig.update_layout(
        paper_bgcolor="#0d1b2b",
        plot_bgcolor="#0d1b2b",
        font=dict(color="#dce7f4", family="Arial, Microsoft YaHei, sans-serif"),
        margin=margin or dict(l=12, r=12, t=28, b=12),
        height=height,
        hoverlabel=dict(
            bgcolor="#172a40",
            bordercolor="#42627e",
            font=dict(color="#f2f7fd"),
        ),
    )
    return fig


# ------------------------- Sidebar ---------------------------
with st.sidebar:
    st.markdown('<div class="eyebrow">OCEAN TWIN</div>', unsafe_allow_html=True)
    st.markdown("## 监测控制中心")
    st.markdown('<div class="small-muted">SUBSEA INTEGRITY MONITORING</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 数据来源")
    uploaded_file = st.file_uploader(
        "上传测厚数据（CSV / XLSX）",
        type=["csv", "xlsx"],
        help="可使用“位置”和“当前壁厚_mm”等列名。未上传时使用模拟数据。",
    )

    if uploaded_file is not None:
        try:
            df = normalize_uploaded_data(uploaded_file)
            data_source = "用户上传数据"
            st.success(f"已读取 {len(df)} 条有效记录")
        except Exception as exc:
            st.error(f"文件读取失败：{exc}")
            df = make_demo_data()
            data_source = "模拟数据（上传文件读取失败）"
    else:
        df = make_demo_data()
        data_source = "模拟数据"

    st.markdown("---")
    st.markdown("### 监测参数")
    default_threshold = 18.5
    min_wall_setting = float(min(15.0, df["当前壁厚_mm"].min() - 0.5))
    max_wall_setting = float(max(20.0, df["当前壁厚_mm"].max() + 0.5))
    threshold = st.slider(
        "演示预警阈值（mm）",
        min_value=min_wall_setting,
        max_value=max_wall_setting,
        value=float(np.clip(default_threshold, min_wall_setting, max_wall_setting)),
        step=0.1,
    )

    selected_segment = st.selectbox(
        "选择重点管段",
        df["管段编号"].astype(str).tolist(),
        index=min(28, len(df) - 1),
    )

    st.markdown("---")
    st.markdown(
        '<span class="small-muted">● 界面运行中</span>',
        unsafe_allow_html=True,
    )
    st.caption("如未上传文件，当前全部为模拟数据。")

# ------------------------- Navigation ------------------------
header_left, header_right = st.columns([4, 1])
with header_left:
    st.markdown('<div class="eyebrow">OFFSHORE ENGINEERING / DIGITAL TWIN</div>', unsafe_allow_html=True)
    st.title("深海管道腐蚀监测平台")
    st.markdown(
        '<div class="subtitle">SUBSEA PIPELINE INTEGRITY · 数字孪生演示原型</div>',
        unsafe_allow_html=True,
    )
with header_right:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="status-pill">● DEMO MODE</div>', unsafe_allow_html=True)
    st.caption(datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))

page = st.radio(
    "主导航",
    ["综合监测", "管段数据", "系统说明"],
    horizontal=True,
    label_visibility="collapsed",
)
st.markdown("---")

# ------------------------- KPIs ------------------------------
alerts = df[df["当前壁厚_mm"] < threshold].copy()
avg_wall = float(df["当前壁厚_mm"].mean())
min_wall = float(df["当前壁厚_mm"].min())
selected_row = df[df["管段编号"].astype(str) == str(selected_segment)].iloc[0]

if page == "综合监测":
    st.markdown('<div class="eyebrow">LIVE OVERVIEW</div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("监测记录", f"{len(df):,}", "条记录")
    k2.metric("平均壁厚", f"{avg_wall:.2f} mm")
    k3.metric("最小壁厚", f"{min_wall:.2f} mm")
    k4.metric("待复核位置", f"{len(alerts):02d}", "按演示阈值筛选")

    st.markdown("## 三维资产与状态监测")
    scene_col, trend_col = st.columns([1.55, 1.0], gap="large")

    # --------------------- 3D Scene --------------------------
    with scene_col:
        st.markdown('<div class="eyebrow">01 / 3D ASSET VIEW</div>', unsafe_allow_html=True)
        st.markdown("### 海底输送管道")

        wall_values = df["当前壁厚_mm"].to_numpy(dtype=float)
        n = len(df)
        x = np.linspace(0.0, 12.0, n)
        theta = np.linspace(0, 2 * np.pi, 48)
        radius = 0.36
        center_z = 0.12

        # Surface coordinates: pipe axis is horizontal (X).
        X = np.tile(x, (len(theta), 1))
        T = np.tile(theta[:, None], (1, n))
        Y = radius * np.cos(T)
        Z = center_z + radius * np.sin(T)
        surface_color = np.tile(wall_values, (len(theta), 1))

        fig3d = go.Figure()

        # Synthetic seabed, shown as a subdued background surface.
        seabed_x = np.linspace(-0.7, 12.7, 42)
        seabed_y = np.linspace(-2.3, 2.3, 30)
        SX, SY = np.meshgrid(seabed_x, seabed_y)
        SZ = -0.52 + 0.055 * np.sin(SX * 1.15) + 0.035 * np.cos(SY * 2.0)

        fig3d.add_trace(
            go.Surface(
                x=SX, y=SY, z=SZ,
                colorscale=[[0, "#152b3c"], [0.55, "#203d50"], [1, "#2c4b5b"]],
                showscale=False,
                opacity=0.94,
                hoverinfo="skip",
                name="示意海床",
                lighting=dict(ambient=0.72, diffuse=0.55, specular=0.12, roughness=0.9),
            )
        )

        fig3d.add_trace(
            go.Surface(
                x=X, y=Y, z=Z,
                surfacecolor=surface_color,
                colorscale=[
                    [0.00, "#d94b55"],
                    [0.20, "#f17a58"],
                    [0.40, "#f7bd67"],
                    [0.60, "#e9e98c"],
                    [0.80, "#66c99a"],
                    [1.00, "#28b9b6"],
                ],
                cmin=float(wall_values.min()),
                cmax=float(wall_values.max()),
                colorbar=dict(
                    title=dict(text="壁厚 (mm)", font=dict(color="#e1edf8", size=12)),
                    tickfont=dict(color="#c5d7e8", size=10),
                    bgcolor="#102033",
                    outlinecolor="#38516b",
                    thickness=13,
                    len=0.76,
                    x=1.01,
                ),
                name="壁厚分布",
                hovertemplate="壁厚：%{surfacecolor:.2f} mm<extra></extra>",
                lighting=dict(ambient=0.72, diffuse=0.75, specular=0.25, roughness=0.55),
            )
        )

        # Measurement locations are placed along the visible upper side of the pipe.
        marker_z = np.full(n, center_z + radius + 0.015)
        marker_colors = np.where(wall_values < threshold, "#ff6574", "#58d9e8")
        fig3d.add_trace(
            go.Scatter3d(
                x=x,
                y=np.zeros(n),
                z=marker_z,
                mode="markers",
                marker=dict(
                    size=3.8,
                    color=marker_colors,
                    line=dict(color="#e8f7ff", width=0.6),
                ),
                customdata=np.column_stack(
                    [df["管段编号"].astype(str).to_numpy(), wall_values, df["位置"].to_numpy()]
                ),
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "位置：%{customdata[2]}<br>"
                    "壁厚：%{customdata[1]:.2f} mm"
                    "<extra></extra>"
                ),
                name="测厚位置",
            )
        )

        # Selected segment indicator.
        selected_index = int(df.index[df["管段编号"].astype(str) == str(selected_segment)][0])
        fig3d.add_trace(
            go.Scatter3d(
                x=[x[selected_index]],
                y=[0],
                z=[marker_z[selected_index] + 0.07],
                mode="markers+text",
                marker=dict(size=7, color="#ffffff", line=dict(color="#52d7e8", width=2)),
                text=[str(selected_segment)],
                textposition="top center",
                textfont=dict(color="#ffffff", size=10),
                name="当前选中",
                hoverinfo="skip",
            )
        )

        fig3d.update_layout(
            paper_bgcolor="#0d1b2b",
            plot_bgcolor="#0d1b2b",
            font=dict(color="#dce7f4", family="Arial, Microsoft YaHei, sans-serif"),
            height=570,
            margin=dict(l=0, r=30, t=8, b=0),
            showlegend=False,
            scene=dict(
                bgcolor="#0d1b2b",
                xaxis=dict(
                    title="管道长度",
                    color="#9fb5ca",
                    gridcolor="#20384e",
                    zerolinecolor="#20384e",
                    showbackground=False,
                ),
                yaxis=dict(
                    title="横向",
                    color="#9fb5ca",
                    gridcolor="#20384e",
                    zerolinecolor="#20384e",
                    showbackground=False,
                ),
                zaxis=dict(
                    title="高程",
                    color="#9fb5ca",
                    gridcolor="#20384e",
                    zerolinecolor="#20384e",
                    showbackground=False,
                ),
                aspectmode="manual",
                aspectratio=dict(x=3.1, y=1.0, z=0.72),
                camera=dict(
                    eye=dict(x=1.55, y=-2.1, z=1.05),
                    up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0),
                ),
            ),
        )
        st.plotly_chart(fig3d, use_container_width=True, config={"displaylogo": False})
        st.caption(
            "三维管道与海床为程序生成的示意几何。壁厚颜色对应当前数据；"
            "并非真实海底地形、设备扫描或工程安全评价。"
        )

    # --------------------- Trend & alerts --------------------
    with trend_col:
        st.markdown('<div class="eyebrow">02 / WALL THICKNESS</div>', unsafe_allow_html=True)
        st.markdown("### 壁厚变化趋势")

        trend = go.Figure()
        trend.add_trace(
            go.Scatter(
                x=df["位置"],
                y=df["当前壁厚_mm"],
                mode="lines+markers",
                line=dict(color="#52d7e8", width=2.5),
                marker=dict(size=6, color="#80e8f2", line=dict(width=0)),
                name="壁厚",
                customdata=df["管段编号"],
                hovertemplate="%{customdata}<br>位置：%{x}<br>壁厚：%{y:.2f} mm<extra></extra>",
            )
        )
        trend.add_hline(
            y=threshold,
            line_dash="dash",
            line_color="#ffbd66",
            line_width=2,
            annotation_text="演示阈值",
            annotation_position="top right",
            annotation_font_color="#ffbd66",
        )
        make_dark_layout(trend, height=310, margin=dict(l=8, r=12, t=35, b=8))
        trend.update_layout(
            showlegend=False,
            xaxis=dict(title="管段位置", gridcolor="#263c52", zeroline=False),
            yaxis=dict(title="壁厚 (mm)", gridcolor="#263c52", zeroline=False),
        )
        st.plotly_chart(trend, use_container_width=True, config={"displaylogo": False})

        st.markdown('<div class="eyebrow">03 / INSPECTION LIST</div>', unsafe_allow_html=True)
        st.markdown("### 待复核管段")
        if alerts.empty:
            st.success("当前没有低于演示阈值的记录。")
        else:
            display_alerts = alerts[["管段编号", "位置", "当前壁厚_mm"]].copy()
            display_alerts.columns = ["管段编号", "位置", "壁厚 (mm)"]
            st.dataframe(display_alerts, use_container_width=True, hide_index=True, height=225)

        st.markdown(
            f"""
            <div class="info-panel">
              <div class="eyebrow">SELECTED SEGMENT</div>
              <div style="font-size:1.35rem;font-weight:750;color:#f1f7ff;">
                {selected_row["管段编号"]}
              </div>
              <div style="margin-top:8px;color:#b5c8dc;">
                位置：{selected_row["位置"]}　
                壁厚：{selected_row["当前壁厚_mm"]:.2f} mm
              </div>
              <div class="small-muted" style="margin-top:8px;">
                状态依据当前演示阈值自动标记，不代表设备真实风险等级。
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------- Data export -----------------------
    st.markdown("---")
    bottom_left, bottom_right = st.columns([3, 1])
    with bottom_left:
        st.markdown("### 监测数据明细")
        st.caption(f"数据来源：{data_source} · 共 {len(df)} 条有效记录")
    with bottom_right:
        csv_bytes = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "下载 CSV 数据",
            data=csv_bytes,
            file_name="corrosion_monitoring_data.csv",
            mime="text/csv",
            use_container_width=True,
        )
    st.dataframe(df, use_container_width=True, hide_index=True)

elif page == "管段数据":
    st.markdown('<div class="eyebrow">ASSET DATA / MEASUREMENT RECORDS</div>', unsafe_allow_html=True)
    st.markdown("## 管段数据管理")
    st.caption(f"数据来源：{data_source}。上传的文件仅在当前应用会话中使用，不会自动保存到数据库。")

    search_text = st.text_input("搜索管段编号", placeholder="例如 P-12")
    filtered = df[df["管段编号"].astype(str).str.contains(search_text, case=False, na=False)]
    st.dataframe(filtered, use_container_width=True, hide_index=True)

    csv_bytes = filtered.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "下载当前筛选数据",
        data=csv_bytes,
        file_name="filtered_pipeline_data.csv",
        mime="text/csv",
    )

    st.markdown("### 选中管段详情")
    detail_id = st.selectbox("选择管段", df["管段编号"].astype(str).tolist(), key="detail_segment")
    detail = df[df["管段编号"].astype(str) == detail_id].iloc[0]
    a, b, c = st.columns(3)
    a.metric("管段编号", str(detail["管段编号"]))
    b.metric("位置", f'{detail["位置"]:g}')
    c.metric("当前壁厚", f'{detail["当前壁厚_mm"]:.2f} mm')

elif page == "系统说明":
    st.markdown('<div class="eyebrow">SYSTEM OVERVIEW / LIMITATIONS</div>', unsafe_allow_html=True)
    st.markdown("## 系统说明")
    st.markdown(
        """
        本系统是用于界面展示与功能验证的工业腐蚀监测数字孪生原型。

        **当前版本具备**
        - 模拟管段壁厚数据生成与 CSV / XLSX 文件导入
        - 三维管道与示意海床场景
        - 基于壁厚值的颜色映射和检测点交互
        - 壁厚趋势曲线、阈值筛选与待复核列表
        - 数据查看、筛选与导出

        **当前版本尚不具备**
        - 真实传感器接入和连续在线采集
        - 持久化数据库、用户权限与审计日志
        - 真实海底地形和精细化设备模型
        - 经验证的腐蚀速率、剩余寿命或失效概率预测
        - 经过工程标准验证的安全预警功能

        **工程使用注意事项**

        当前阈值仅用于界面演示。实际工程应用需要结合设备设计参数、材料、检测方法、
        测量不确定度、服役环境和适用规范进行评估，不能仅凭本页面判断设备安全性。
        """
    )
    st.info("建议先用模拟数据完成演示与测试；接入真实设备前，应完成数据质量、权限、安全和模型验证。")

st.markdown("---")
st.markdown(
    '<div class="small-muted">OCEAN TWIN · Corrosion Monitoring Prototype · 演示数据不用于实际工程安全决策</div>',
    unsafe_allow_html=True,
)
