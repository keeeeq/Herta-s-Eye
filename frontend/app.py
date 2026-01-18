"""
黑塔之眼 - 前端界面 (v5.0 Gaming Edition)
==========================================
- 条件显示: 如果数据为 None/0, 则隐藏对应卡片
- 新增: GPU VRAM / 功耗 / 频率 卡片
"""

import streamlit as st
import requests
import time
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="黑塔系统 // 监控终端",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS ---
HERTA_PURPLE = "#a56de2"
HERTA_GOLD = "#ffd700" 
HOLOGRAM_BLUE = "#00f3ff"
WARNING_RED = "#ff2a6d"
BG_COLOR = "#050510"
BORDER_COLOR = "rgba(0, 243, 255, 0.2)"

st.markdown(f"""
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="theme-color" content="#050510">
</head>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap');

    /* 隐藏 Streamlit 默认 UI */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display: none;}}

    .stApp {{
        background-color: {BG_COLOR};
        background-image: 
            linear-gradient(rgba(0, 243, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 243, 255, 0.03) 1px, transparent 1px);
        background-size: 30px 30px;
        color: #e0e0e0;
        font-family: 'Rajdhani', 'Noto Sans SC', sans-serif;
    }}
    
    .stApp::before {{
        content: " ";
        display: block; position: absolute;
        top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
        z-index: 999;
        background-size: 100% 2px;
        pointer-events: none;
    }}

    h1 {{
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700; font-size: 2.5rem; color: {HOLOGRAM_BLUE};
        text-transform: uppercase; letter-spacing: 3px;
        text-shadow: 2px 2px 0px {HERTA_PURPLE};
        border-bottom: 2px solid {HERTA_PURPLE};
        display: inline-block; padding-right: 20px;
    }}

    .metric-card {{
        background: rgba(10, 14, 23, 0.85);
        border: 1px solid {BORDER_COLOR}; border-top: 2px solid {HOLOGRAM_BLUE};
        border-radius: 4px; padding: 12px 15px; margin-bottom: 10px;
        clip-path: polygon(0 0, 100% 0, 100% 85%, 95% 100%, 0% 100%);
    }}
    .metric-card.warning {{ border-top-color: {WARNING_RED}; }}
    
    .metric-label {{ font-size: 0.75rem; color: {HERTA_GOLD}; text-transform: uppercase; }}
    .metric-value {{ font-size: 1.8rem; font-weight: 700; color: #fff; font-family: 'Rajdhani', sans-serif; }}
    .metric-unit {{ font-size: 0.9rem; color: {HOLOGRAM_BLUE}; margin-left: 3px; }}
    .metric-sub {{ font-size: 0.7rem; color: #888; }}

    .prog-bg {{ width: 100%; height: 5px; background: rgba(255,255,255,0.1); margin-top: 8px; }}
    .prog-fill {{ height: 100%; background: {HOLOGRAM_BLUE}; transition: width 0.5s ease; }}
    .warning .prog-fill {{ background: {WARNING_RED}; }}

    .herta-bubble {{
        display: flex; align-items: center; margin-top: 15px;
        background: rgba(165, 109, 226, 0.1); border: 1px solid {HERTA_PURPLE};
        padding: 15px; border-radius: 0 15px 0 15px;
    }}
    .herta-avatar {{ font-size: 1.8rem; margin-right: 15px; }}
    .herta-text {{ font-size: 1rem; font-style: italic; color: #ddd; font-family: 'Noto Sans SC', sans-serif; }}
</style>
""", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000"

def get_data():
    try:
        r1 = requests.get(f"{API_URL}/stats", timeout=0.3)
        r2 = requests.get(f"{API_URL}/roast", timeout=0.3)
        if r1.ok and r2.ok:
            return r1.json(), r2.json()
    except:
        pass
    return None, None

if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Time', 'CPU', 'GPU', 'RAM'])

# --- Header ---
col_head, col_status = st.columns([3, 1])
with col_head:
    st.markdown("<h1>黑塔系统 <span style='font-size:0.9rem;color:#888'>// 游戏监控</span></h1>", unsafe_allow_html=True)

status_ph = col_status.empty()
main_ph = st.empty()

# --- Helper: 渲染卡片 (条件显示) ---
def render_card(label, value, unit, sub="", warn_thresh=85, show_bar=True):
    """如果 value 为 None 或 0, 返回空字符串 (不显示)"""
    if value is None or value == 0:
        return ""
    
    is_warn = value > warn_thresh if warn_thresh else False
    warn_class = "warning" if is_warn else ""
    bar_html = f'<div class="prog-bg"><div class="prog-fill" style="width:{min(value, 100)}%"></div></div>' if show_bar else ''
    
    return f"""
    <div class="metric-card {warn_class}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}<span class="metric-unit">{unit}</span></div>
        <div class="metric-sub">{sub}</div>
        {bar_html}
    </div>
    """

while True:
    stats, roast = get_data()
    
    if stats:
        # Status Indicator
        with status_ph.container():
            if stats.get('is_mock', False):
                st.markdown(f"<div style='text-align:right; color:{WARNING_RED}; font-weight:bold;'>⚠️ 模拟信号</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align:right; color:{HOLOGRAM_BLUE}; font-weight:bold;'>✅ 硬件直连</div>", unsafe_allow_html=True)

        with main_ph.container():
            # Update History
            curr_time = time.strftime("%H:%M:%S")
            new_row = pd.DataFrame({
                'Time': [curr_time],
                'CPU': [stats.get('cpu') or 0],
                'GPU': [stats.get('gpu_usage') or 0],
                'RAM': [stats.get('ram') or 0]
            })
            st.session_state.history = pd.concat([st.session_state.history, new_row]).tail(60)

            # === 动态卡片布局 ===
            cards_html = []
            
            # CPU
            cpu_sub = f"{stats.get('cpu_temp') or '--'}°C" if stats.get('cpu_temp') else ""
            cards_html.append(render_card("CPU 占用", stats.get('cpu'), "%", cpu_sub, warn_thresh=85))
            
            # GPU
            gpu_sub = f"{stats.get('gpu_temp') or '--'}°C" if stats.get('gpu_temp') else ""
            cards_html.append(render_card("GPU 占用", stats.get('gpu_usage'), "%", gpu_sub, warn_thresh=90))
            
            # RAM
            cards_html.append(render_card("内存占用", stats.get('ram'), "%", "", warn_thresh=90))
            
            # VRAM
            vram_used = stats.get('gpu_vram_used')
            vram_total = stats.get('gpu_vram_total')
            if vram_used and vram_total:
                vram_pct = round((vram_used / vram_total) * 100, 1)
                cards_html.append(render_card("显存占用", vram_pct, "%", f"{int(vram_used)}/{int(vram_total)} MB", warn_thresh=90))
            
            # GPU Power
            cards_html.append(render_card("GPU 功耗", stats.get('gpu_power'), "W", "", warn_thresh=None, show_bar=False))
            
            # GPU Clock
            cards_html.append(render_card("GPU 频率", stats.get('gpu_clock'), "MHz", "", warn_thresh=None, show_bar=False))
            
            # Fan
            fan = stats.get('fan_speed')
            if fan:
                cards_html.append(f"""
                <div class="metric-card">
                    <div class="metric-label">风扇转速</div>
                    <div class="metric-value" style="font-size:1.4rem">{fan}</div>
                </div>
                """)
            
            # 过滤空卡片并渲染
            valid_cards = [c for c in cards_html if c.strip()]
            
            # 动态列数 (最多4列)
            num_cols = min(len(valid_cards), 4)
            if num_cols > 0:
                cols = st.columns(num_cols)
                for i, card in enumerate(valid_cards[:num_cols]):
                    with cols[i]:
                        st.markdown(card, unsafe_allow_html=True)
                
                # 如果超过4个卡片，换行显示
                if len(valid_cards) > 4:
                    cols2 = st.columns(len(valid_cards) - 4)
                    for i, card in enumerate(valid_cards[4:]):
                        with cols2[i]:
                            st.markdown(card, unsafe_allow_html=True)

            # === Row 2: Chart + Herta ===
            c1, c2 = st.columns([1, 2])
            
            with c1:
                st.markdown(f"""
                <div class="herta-bubble">
                    <div class="herta-avatar">👾</div>
                    <div class="herta-text">"{roast['message']}"</div>
                </div>
                """, unsafe_allow_html=True)
            
            with c2:
                source = st.session_state.history.melt('Time', var_name='Metric', value_name='Usage')
                chart = alt.Chart(source).mark_line(strokeWidth=2).encode(
                    x=alt.X('Time', axis=None),
                    y=alt.Y('Usage', scale=alt.Scale(domain=[0, 100]), axis=None),
                    color=alt.Color('Metric', legend=alt.Legend(orient='top', title=None),
                        scale=alt.Scale(domain=['CPU','GPU','RAM'], range=[HOLOGRAM_BLUE, WARNING_RED, HERTA_GOLD])),
                    tooltip=['Time', 'Metric', 'Usage']
                ).properties(height=120, background='transparent').configure_view(stroke=None)
                st.altair_chart(chart, use_container_width=True)
    else:
        with main_ph.container():
             st.error("等待连接...")
             
    time.sleep(1)
