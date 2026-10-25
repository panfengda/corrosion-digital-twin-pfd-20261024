import hmac
import os
from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

# PFD historical-weather digital-twin prototype
# Install: pip install -r requirements.txt
# Weather source: Open-Meteo Historical Weather API (ERA5/ERA5-Land reanalysis).
# IMPORTANT: Open-Meteo's free API is for non-commercial use. For commercial customer
# demonstrations/promotional use, use a data source/licence that permits that use.

st.set_page_config(
    page_title="PFD | Wind Turbine Digital Twin",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.stApp { background: #071321; color: #edf6fb; }
[data-testid="stHeader"] { background: rgba(7,19,33,.92); }
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1500px; }
[data-testid="stSidebar"] { background: #0a1b2b; border-right: 1px solid #1c3a4c; }
h1,h2,h3 { color: #e9f6fc; }
div[data-testid="stMetric"] { background: #0d2437; border: 1px solid #234559; padding: 14px; border-radius: 12px; }
div[data-testid="stAlert"] { border-radius: 10px; }
.pfd-card { background: linear-gradient(145deg,#102a3e,#0b1c2b); border:1px solid #24475a; padding:16px; border-radius:13px; }
.small-note { color:#9bb4c5; font-size: .88rem; }
</style>
""", unsafe_allow_html=True)


def login_gate():
    """Optional shared-password gate. Configure APP_PASSWORD in Streamlit Secrets."""
    try:
        expected = st.secrets.get("APP_PASSWORD", "")
    except Exception:
        expected = os.environ.get("APP_PASSWORD", "")

    if not expected:
        st.sidebar.warning(
            "尚未配置访问密码。测试时可继续浏览；正式公开前请在 Streamlit Secrets "
            "中设置 APP_PASSWORD。"
        )
        return

    if "pfd_logged_in" not in st.session_state:
        st.session_state.pfd_logged_in = False

    if st.session_state.pfd_logged_in:
        st.sidebar.success("已通过团队共享密码验证")
        if st.sidebar.button("退出登录", use_container_width=True):
            st.session_state.pfd_logged_in = False
            st.rerun()
        return

    st.title("PFD | 风电数字孪生研究平台")
    st.caption("团队成员请使用管理员提供的共享访问密码")
    password = st.text_input("访问密码", type="password")
    if st.button("登录", type="primary"):
        if hmac.compare_digest(password, str(expected)):
            st.session_state.pfd_logged_in = True
            st.rerun()
        else:
            st.error("密码不正确，请重试。")
    st.stop()


login_gate()

st.markdown("""
<div class="pfd-card">
  <div style="color:#59dce5;font-size:12px;font-weight:800;letter-spacing:2px">PFD · WIND ENERGY DIGITAL TWIN</div>
  <h1 style="margin:6px 0 4px">多场址历史气象与机组状态研究平台</h1>
  <div class="small-note">2 MW 级双馈感应发电机组（DFIG）｜历史天气回放｜环境风险指标｜可解释演示原型</div>
</div>
""", unsafe_allow_html=True)

st.info(
    "数据边界：天气数据是历史再分析估计，不是风机现场传感器实测；机组功率、温度、振动和损伤指标在本版本中为演示性估算，"
    "不能作为真实故障诊断、剩余寿命或安全决策依据。"
)

# Candidate coordinates are examples, not claims about a specific customer's turbine.
SITES = {
    "海上候选点｜北海示例": {"lat": 54.5, "lon": 2.0, "kind": "offshore", "height": "海上网格点"},
    "平原候选点｜美国中部示例": {"lat": 35.2, "lon": -101.8, "kind": "plain", "height": "平原参考点"},
    "山地候选点｜美国西部示例": {"lat": 39.5, "lon": -120.2, "kind": "mountain", "height": "山地参考点"},
}

WEATHER_URL = "https://archive-api.open-meteo.com/v1/archive"


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_historical_weather(lat, lon, start, end, site_kind):
    hourly_vars = [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "wind_speed_10m",
        "wind_gusts_10m",
        "wind_direction_10m",
        "wind_speed_100m",
    ]
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start,
        "end_date": end,
        "hourly": ",".join(hourly_vars),
        "timezone": "UTC",
        "wind_speed_unit": "ms",
        "precipitation_unit": "mm",
    }
    # Prefer ERA5-Land for land points, ERA5 for offshore points.
    params["models"] = "era5" if site_kind == "offshore" else "era5_land"
    response = requests.get(WEATHER_URL, params=params, timeout=35)
    response.raise_for_status()
    payload = response.json()
    hourly = payload.get("hourly", {})
    if not hourly or "time" not in hourly:
        raise ValueError("天气接口未返回逐小时数据。")
    df = pd.DataFrame(hourly)
    df["time"] = pd.to_datetime(df["time"], utc=True, errors="coerce")
    df = df.dropna(subset=["time"]).sort_values("time").drop_duplicates("time")
    df["site"] = ""
    df["source_type"] = "历史再分析估计"
    return df, payload


def demo_weather(start, end, site_name, site):
    """Clearly labelled fallback data when the public API is unreachable."""
    idx = pd.date_range(pd.Timestamp(start, tz="UTC"), pd.Timestamp(end, tz="UTC") + pd.Timedelta(hours=23), freq="h")
    seed = int(abs(site["lat"] * 100 + site["lon"] * 10)) % 997
    # Deterministic illustrative signal, not measured weather.
    import numpy as np
    rng = np.random.default_rng(seed)
    t = np.arange(len(idx))
    base = {"offshore": 9.2, "plain": 7.1, "mountain": 6.4}[site["kind"]]
    wind = np.clip(base + 2.4*np.sin(t/19) + rng.normal(0, 1.1, len(t)), 0.2, 25)
    gust = wind + np.clip(rng.normal(2.4, 1.0, len(t)), 0.2, 7)
    temp = 13 + 7*np.sin(t/(24*8)) + rng.normal(0, 1.2, len(t))
    rain = np.where(rng.random(len(t)) < .12, rng.gamma(1.5, 1.1, len(t)), 0)
    humidity = np.clip(68 + 18*np.sin(t/31) + rng.normal(0, 7, len(t)), 25, 100)
    return pd.DataFrame({
        "time": idx, "temperature_2m": temp, "relative_humidity_2m": humidity,
        "precipitation": rain, "wind_speed_10m": wind, "wind_gusts_10m": gust,
        "wind_direction_10m": (210 + 45*np.sin(t/35)) % 360,
        "wind_speed_100m": wind*1.12, "site": site_name, "source_type": "演示模拟数据（非真实天气）"
    })


def clean_weather(df):
    """Range checks: retain raw values and flag invalid observations."""
    out = df.copy()
    numeric_ranges = {
        "temperature_2m": (-70, 65),
        "relative_humidity_2m": (0, 100),
        "precipitation": (0, 500),
        "wind_speed_10m": (0, 80),
        "wind_gusts_10m": (0, 100),
        "wind_direction_10m": (0, 360),
        "wind_speed_100m": (0, 100),
    }
    flags = []
    for _, row in out.iterrows():
        row_flags = []
        for col, (lo, hi) in numeric_ranges.items():
            if col not in out.columns:
                continue
            val = row[col]
            if pd.isna(val):
                row_flags.append(f"{col}:缺失")
            elif not lo <= float(val) <= hi:
                row_flags.append(f"{col}:超范围")
        flags.append("; ".join(row_flags))
    out["quality_flag"] = flags
    out["quality_status"] = out["quality_flag"].apply(lambda x: "需检查" if x else "范围检查通过")
    return out


def add_proxy_indicators(df, site_kind):
    """Transparent indicators for demonstration only; not a validated damage model."""
    out = df.copy()
    wind = out["wind_speed_100m"].fillna(out["wind_speed_10m"])
    gust = out["wind_gusts_10m"].fillna(out["wind_speed_10m"])
    rain = out["precipitation"].fillna(0).clip(lower=0)
    humidity = out["relative_humidity_2m"].fillna(60).clip(0, 100)
    temp = out["temperature_2m"].fillna(15)

    # Simple dimensionless weather-exposure index, deliberately not a material loss estimate.
    gust_factor = (gust / 25.0).clip(0, 1.5)
    wind_factor = (wind / 25.0).clip(0, 1.5)
    rain_factor = (rain / 5.0).clip(0, 2.0)
    exposure = (0.45*wind_factor + 0.25*gust_factor + 0.20*rain_factor + 0.10*(humidity/100)).clip(0, 1)
    if site_kind == "offshore":
        exposure = (exposure + 0.12*(humidity/100)).clip(0, 1)
    elif site_kind == "mountain":
        # Terrain effects cannot be resolved from this grid-weather-only proxy.
        exposure = (exposure + 0.08*gust_factor).clip(0, 1)
    out["environment_exposure_index"] = exposure * 100

    # Synthetic operating estimates, not real SCADA. Marked as proxies in UI.
    out["estimated_power_mw"] = (2.0 * (wind.clip(0, 12) / 12.0) ** 3).clip(0, 2)
    out.loc[wind < 3, "estimated_power_mw"] = 0
    out.loc[wind >= 25, "estimated_power_mw"] = 0
    out["estimated_bearing_temp_c"] = (45 + 10*out["estimated_power_mw"] + 0.15*(temp-15)).clip(25, 100)
    out["estimated_vibration_mm_s"] = (1.0 + 2.5*gust_factor + 0.5*rain_factor).clip(0.2, 12)
    return out


with st.sidebar:
    st.markdown("## 研究设置")
    site_names = list(SITES.keys())
    selected_sites = st.multiselect(
        "选择对比场址",
        site_names,
        default=site_names,
        help="默认三个候选点仅用于演示方法。正式研究请换成目标风场坐标。",
    )
    default_end = date.today() - timedelta(days=7)  # ERA5 commonly has several days' latency
    default_start = default_end - timedelta(days=13)
    start_date = st.date_input("历史开始日期", value=default_start, max_value=default_end - timedelta(days=1))
    end_date = st.date_input("历史结束日期", value=default_end, max_value=default_end)
    use_demo_fallback = st.checkbox("API 失败时使用演示模拟数据", value=True)
    fetch_button = st.button("查询历史天气并分析", type="primary", use_container_width=True)
    st.caption("默认查询结束日比今天早 7 天，避免把尚未完整的再分析数据误认为完整历史。")

if not selected_sites:
    st.warning("请至少选择一个场址。")
    st.stop()
if start_date >= end_date:
    st.error("开始日期必须早于结束日期。")
    st.stop()
if (end_date - start_date).days > 31:
    st.warning("为控制请求量和页面负载，单次查询建议不超过 31 天。")

if "weather_results" not in st.session_state:
    st.session_state.weather_results = None

if fetch_button or st.session_state.weather_results is None:
    results = {}
    start_s, end_s = start_date.isoformat(), end_date.isoformat()
    with st.spinner("正在获取历史天气数据……"):
        for name in selected_sites:
            site = SITES[name]
            try:
                df, meta = fetch_historical_weather(site["lat"], site["lon"], start_s, end_s, site["kind"])
                df["site"] = name
                df = clean_weather(df)
                df = add_proxy_indicators(df, site["kind"])
                results[name] = {"df": df, "source": "Open-Meteo Historical API / ERA5 再分析", "meta": meta, "error": None}
            except Exception as exc:
                if use_demo_fallback:
                    df = demo_weather(start_s, end_s, name, site)
                    df = clean_weather(df)
                    df = add_proxy_indicators(df, site["kind"])
                    results[name] = {"df": df, "source": "演示模拟数据（API 请求失败）", "meta": None, "error": str(exc)}
                else:
                    results[name] = {"df": None, "source": "不可用", "meta": None, "error": str(exc)}
    st.session_state.weather_results = {
        "results": results, "start": start_s, "end": end_s, "selected": selected_sites
    }

bundle = st.session_state.weather_results
# If selection or dates changed since last fetch, prompt explicit refresh rather than silently showing stale results.
if bundle["start"] != start_date.isoformat() or bundle["end"] != end_date.isoformat() or bundle["selected"] != selected_sites:
    st.warning("查询条件已改变。点击左侧“查询历史天气并分析”以刷新结果。")

results = bundle["results"]
frames = []
for name in selected_sites:
    item = results.get(name)
    if item and item["df"] is not None:
        frames.append(item["df"])
if not frames:
    st.error("当前没有可展示的数据。请检查网络，或启用演示模拟数据。")
    st.stop()
all_df = pd.concat(frames, ignore_index=True)

sources = sorted(all_df["source_type"].dropna().unique().tolist())
if any("模拟" in str(s) for s in sources):
    st.warning("当前结果中包含模拟数据。请查看各场址的数据来源标记，不要将模拟曲线引用为真实天气记录。")

# Top summary
col1, col2, col3, col4 = st.columns(4)
col1.metric("对比场址数", len(frames))
col2.metric("时间范围", f"{start_date:%m-%d} 至 {end_date:%m-%d}")
col3.metric("有效记录", f"{len(all_df):,}")
quality_pct = 100 * (all_df["quality_status"] == "范围检查通过").mean()
col4.metric("范围检查通过率", f"{quality_pct:.1f}%")

tab_overview, tab_weather, tab_twin, tab_quality = st.tabs([
    "场址对比", "历史气象", "机组状态与风险指标", "数据质量与导出"
])

with tab_overview:
    st.subheader("不同场址的历史环境差异")
    summary = all_df.groupby("site", as_index=False).agg(
        平均风速=("wind_speed_10m", "mean"),
        最大阵风=("wind_gusts_10m", "max"),
        累计降水=("precipitation", "sum"),
        平均温度=("temperature_2m", "mean"),
        平均湿度=("relative_humidity_2m", "mean"),
        平均环境暴露指数=("environment_exposure_index", "mean"),
        数据来源=("source_type", lambda x: ", ".join(sorted(set(map(str, x)))))
    )
    summary["平均风速"] = summary["平均风速"].round(2)
    summary["最大阵风"] = summary["最大阵风"].round(2)
    summary["累计降水"] = summary["累计降水"].round(2)
    summary["平均温度"] = summary["平均温度"].round(2)
    summary["平均湿度"] = summary["平均湿度"].round(1)
    summary["平均环境暴露指数"] = summary["平均环境暴露指数"].round(1)
    st.dataframe(summary, use_container_width=True, hide_index=True)
    fig = px.line(
        all_df, x="time", y="wind_speed_10m", color="site",
        title="10 m 风速历史变化（再分析/模拟数据，按来源标记）",
        labels={"time": "时间（UTC）", "wind_speed_10m": "风速（m/s）", "site": "场址"}
    )
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("场址候选坐标是示例点，不代表已选定的真实风电场；比较结果仅适用于所选时间窗和数据源。")

with tab_weather:
    st.subheader("历史天气曲线")
    variable_map = {
        "风速（10 m）": ("wind_speed_10m", "m/s"),
        "风速（100 m）": ("wind_speed_100m", "m/s"),
        "阵风（10 m）": ("wind_gusts_10m", "m/s"),
        "气温（2 m）": ("temperature_2m", "°C"),
        "相对湿度": ("relative_humidity_2m", "%"),
        "降水": ("precipitation", "mm/h"),
    }
    chosen_var = st.selectbox("选择变量", list(variable_map.keys()))
    colname, unit = variable_map[chosen_var]
    fig = px.line(all_df, x="time", y=colname, color="site", title=f"{chosen_var}历史时序", labels={"time":"时间（UTC）",colname:f"{chosen_var}（{unit}）","site":"场址"})
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)
    if colname == "precipitation":
        fig2 = px.bar(all_df, x="time", y=colname, color="site", barmode="group", title="逐小时降水")
        fig2.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend_title_text="")
        st.plotly_chart(fig2, use_container_width=True)
    st.caption("历史再分析是融合观测与数值模式的格点估计，不能等同于风机现场测风塔数据。")

with tab_twin:
    st.subheader("2 MW DFIG 状态与环境风险演示")
    st.warning("本页机组功率、轴承温度和振动为天气驱动的简化代理指标，并非真实 SCADA 数据，也不是经过验证的故障诊断模型。")
    proxy_cols = st.columns(3)
    proxy_cols[0].metric("平均估算功率", f"{all_df['estimated_power_mw'].mean():.2f} MW")
    proxy_cols[1].metric("平均估算轴承温度", f"{all_df['estimated_bearing_temp_c'].mean():.1f} °C")
    proxy_cols[2].metric("平均环境暴露指数", f"{all_df['environment_exposure_index'].mean():.1f}/100")
    fig = go.Figure()
    for name, grp in all_df.groupby("site"):
        fig.add_trace(go.Scatter(x=grp["time"], y=grp["environment_exposure_index"], mode="lines", name=f"{name}｜环境暴露指数"))
    fig.update_layout(title="环境暴露指数（无量纲演示指标，不代表损伤百分比）", xaxis_title="时间（UTC）", yaxis_title="指数（0–100）", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    fig = px.line(all_df, x="time", y="estimated_power_mw", color="site", title="天气驱动的估算功率曲线（代理模型）", labels={"time":"时间（UTC）","estimated_power_mw":"估算功率（MW）","site":"场址"})
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    **下一阶段如何升级为真实模型**
    1. 导入真实 SCADA：风速、功率、转速、桨距角、状态码。
    2. 导入 CMS/检修数据：轴承温度、振动特征、故障标签与检修时间。
    3. 叶片损伤需要材料/涂层参数、检查图像或损伤评级，以及载荷或试验数据。
    4. 先用时间外推和跨场址测试评估基准模型，再显示误差与预测区间。
    """)

with tab_quality:
    st.subheader("数据质量、来源与下载")
    quality = all_df.groupby(["site", "source_type", "quality_status"], dropna=False).size().reset_index(name="记录数")
    st.dataframe(quality, use_container_width=True, hide_index=True)
    issue_df = all_df[all_df["quality_status"] != "范围检查通过"]
    if issue_df.empty:
        st.success("范围检查未发现超出配置范围的数值；这不等于数据已被现场验证。")
    else:
        st.warning(f"发现 {len(issue_df)} 条需要检查的记录。")
        st.dataframe(issue_df[["site","time","quality_flag"]].head(200), use_container_width=True, hide_index=True)
    st.download_button(
        "下载当前对比数据 CSV",
        data=all_df.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"pfd_historical_weather_{start_date}_{end_date}.csv",
        mime="text/csv",
        use_container_width=True,
    )
    st.markdown("""
    **来源与许可说明**
    - Open-Meteo Historical Weather API：历史数据通常来自 ERA5 / ERA5-Land 再分析；请在使用和展示时注明数据来源并核对当前许可。
    - Open-Meteo 免费 API 条款面向非商业用途。如果该网页用于商业客户演示、推广或商业产品，请不要直接依赖其免费 API；应改用允许相应用途的数据源或取得适当许可。
    - 该页面不连接真实风机，不提供安全联锁、停机或维护决策。
    """)
    st.markdown("[Open-Meteo Historical Weather API 文档](https://open-meteo.com/en/docs/historical-weather-api) · [使用条款](https://open-meteo.com/en/terms)")

st.divider()
st.caption("PFD · Wind Energy Digital Twin Research Prototype | 历史天气回放，不是实时监控。数据来源、质量与模型边界应与图表一同展示。")
