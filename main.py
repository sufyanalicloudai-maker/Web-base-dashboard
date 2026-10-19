import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Northstar Labs Analytics", page_icon="📊", layout="wide")

st.markdown(
    """
    <style>
        .stApp {
            background: radial-gradient(circle at top left, rgba(245, 199, 90, 0.20), transparent 16%),
                        radial-gradient(circle at right, rgba(255, 191, 0, 0.10), transparent 18%),
                        linear-gradient(135deg, #030303 0%, #0b0b0b 33%, #121212 55%, #080808 100%);
            color: #f7f1d0;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #fff3bf;
            text-shadow: 0 0 10px rgba(245, 199, 90, 0.25);
        }

        .main-header {
            background: linear-gradient(90deg, rgba(245, 199, 90, 0.12), rgba(255, 191, 0, 0.04));
            border: 1px solid rgba(245, 199, 90, 0.9);
            border-radius: 18px;
            padding: 1.2rem 1.4rem;
            box-shadow: 0 0 14px rgba(245, 199, 90, 0.35), inset 0 0 18px rgba(245, 199, 90, 0.08);
            margin-bottom: 1rem;
        }

        .main-header h1 {
            margin-bottom: 0.35rem;
            font-size: 2.3rem;
            letter-spacing: 0.03em;
        }

        .main-header p {
            margin: 0;
            color: #f3d98d;
            font-size: 1rem;
        }

        .kpi-ribbon {
            display: flex;
            gap: 0.8rem;
            flex-wrap: wrap;
            margin: 1rem 0 1.3rem 0;
        }

        .kpi-pill {
            flex: 1 1 180px;
            background: rgba(16, 16, 16, 0.9);
            border: 1px solid rgba(245, 199, 90, 0.75);
            border-radius: 12px;
            padding: 0.9rem 1rem;
            box-shadow: 0 0 14px rgba(245, 199, 90, 0.12), inset 0 0 18px rgba(245, 199, 90, 0.05);
        }

        .kpi-label {
            color: #f3d98d;
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }

        .kpi-value {
            margin-top: 0.35rem;
            font-size: 1.5rem;
            font-weight: 700;
            color: #fff6d0;
        }

        .kpi-delta {
            display: inline-block;
            margin-top: 0.35rem;
            font-size: 0.75rem;
            padding: 0.18rem 0.48rem;
            border-radius: 999px;
            background: rgba(245, 199, 90, 0.12);
            color: #ffd76a;
            border: 1px solid rgba(245, 199, 90, 0.6);
        }

        .filter-strip {
            display: flex;
            gap: 0.55rem;
            flex-wrap: wrap;
            margin: 0 0 1rem 0;
        }

        .chip {
            padding: 0.42rem 0.8rem;
            border-radius: 999px;
            background: rgba(18, 18, 18, 0.9);
            border: 1px solid rgba(245, 199, 90, 0.45);
            color: #f8e7b2;
            font-size: 0.8rem;
            box-shadow: inset 0 0 12px rgba(245, 199, 90, 0.06);
        }

        .chip.active {
            background: linear-gradient(135deg, rgba(245, 199, 90, 0.18), rgba(255, 191, 0, 0.04));
            border-color: rgba(255, 191, 0, 0.95);
            box-shadow: 0 0 12px rgba(255, 191, 0, 0.25);
        }

        .status-badge {
            display: inline-block;
            margin: 0.1rem 0.3rem 0 0;
            padding: 0.25rem 0.6rem;
            border-radius: 999px;
            font-size: 0.68rem;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            background: rgba(255, 191, 0, 0.10);
            border: 1px solid rgba(255, 191, 0, 0.55);
            color: #ffd76a;
        }

        .status-badge.warn {
            background: rgba(255, 191, 0, 0.12);
            border-color: rgba(255, 191, 0, 0.5);
            color: #f5d66d;
        }

        .status-badge.alert {
            background: rgba(255, 118, 78, 0.10);
            border-color: rgba(255, 118, 78, 0.4);
            color: #ffb197;
        }

        .activity-box,
        .forecast-box,
        .panel-box {
            background: rgba(14, 14, 14, 0.9);
            border: 1px solid rgba(245, 199, 90, 0.8);
            border-radius: 16px;
            padding: 1rem;
            box-shadow: 0 0 18px rgba(245, 199, 90, 0.08), inset 0 0 16px rgba(245, 199, 90, 0.04);
        }

        .activity-list {
            list-style: none;
            padding: 0;
            margin: 0.8rem 0 0 0;
        }

        .activity-item {
            display: flex;
            gap: 0.7rem;
            align-items: flex-start;
            padding: 0.62rem 0;
            border-bottom: 1px solid rgba(245, 199, 90, 0.15);
        }

        .activity-item:last-child {
            border-bottom: none;
        }

        .dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-top: 0.45rem;
            background: linear-gradient(135deg, #ffd76a, #f5b700);
            box-shadow: 0 0 12px rgba(255, 191, 0, 0.7);
        }

        .activity-time {
            color: #f3d98d;
            font-size: 0.72rem;
        }

        .activity-text {
            color: #f8f3d7;
            font-size: 0.85rem;
            line-height: 1.5;
        }

        .budget-tag {
            display: inline-block;
            padding: 0.2rem 0.52rem;
            border-radius: 999px;
            background: rgba(245, 199, 90, 0.10);
            color: #ffd76a;
            border: 1px solid rgba(245, 199, 90, 0.4);
            font-size: 0.72rem;
        }

        .mini-badge {
            display: inline-block;
            padding: 0.2rem 0.5rem;
            border-radius: 999px;
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }

        .mini-badge.positive {
            background: rgba(255, 191, 0, 0.12);
            color: #ffd76a;
            border: 1px solid rgba(255, 191, 0, 0.4);
        }

        .mini-badge.warn {
            background: rgba(255, 191, 0, 0.08);
            color: #f7d36d;
            border: 1px solid rgba(255, 191, 0, 0.35);
        }

        .mini-badge.alert {
            background: rgba(255, 118, 78, 0.1);
            color: #ffb197;
            border: 1px solid rgba(255, 118, 78, 0.4);
        }

        .custom-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 0.8rem;
            border: 1px solid rgba(245, 199, 90, 0.65);
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 0 12px rgba(245, 199, 90, 0.1);
        }

        .custom-table th,
        .custom-table td {
            padding: 0.75rem 0.7rem;
            border-bottom: 1px solid rgba(245, 199, 90, 0.2);
            text-align: left;
            color: #f7f1d0;
        }

        .custom-table th {
            color: #f3d98d;
            background: rgba(245, 199, 90, 0.06);
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .custom-table tr:hover {
            background: rgba(245, 199, 90, 0.05);
        }

        .custom-table tr:nth-child(even) {
            background: rgba(255, 255, 255, 0.012);
        }

        div[data-baseweb="select"] > div,
        .stSlider > div {
            background: rgba(16, 16, 16, 0.96);
            border: 1px solid rgba(245, 199, 90, 0.6);
            color: #fff6d0;
            box-shadow: 0 0 10px rgba(245, 199, 90, 0.08);
        }

        .stDataFrame, .stTable {
            background: rgba(16, 16, 16, 0.9);
            border: 1px solid rgba(245, 199, 90, 0.7);
            border-radius: 14px;
            box-shadow: 0 0 15px rgba(245, 199, 90, 0.08), inset 0 0 18px rgba(245, 199, 90, 0.03);
        }

        .stAlert {
            border-radius: 12px;
            border: 1px solid rgba(245, 199, 90, 0.55);
        }

        .stCaption {
            color: #f3d98d;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(12, 12, 12, 0.98), rgba(14, 14, 14, 0.96));
            border-right: 1px solid rgba(245, 199, 90, 0.5);
            box-shadow: inset 0 0 18px rgba(245, 199, 90, 0.05);
        }

        .brand-box {
            background: linear-gradient(135deg, rgba(245, 199, 90, 0.10), rgba(255, 191, 0, 0.04));
            border: 1px solid rgba(245, 199, 90, 0.75);
            border-radius: 14px;
            padding: 14px 12px;
            margin-top: 0.2rem;
            margin-bottom: 1rem;
            box-shadow: 0 0 18px rgba(245, 199, 90, 0.12);
        }

        .brand-box .brand-icon {
            display: inline-flex;
            width: 34px;
            height: 34px;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            background: linear-gradient(135deg, #ffd76a, #d48e00);
            color: #111111;
            font-weight: 800;
            box-shadow: 0 0 18px rgba(255, 191, 0, 0.55);
        }

        .brand-box .brand-text {
            font-size: 1.02rem;
            font-weight: 700;
            color: #fff7d6;
            margin-left: 10px;
        }

        .brand-box .brand-sub {
            font-size: 0.72rem;
            color: #f3d98d;
            margin-top: 4px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .stTabs [role="tablist"] {
            background: rgba(18, 18, 18, 0.8);
            border-radius: 12px;
            border: 1px solid rgba(245, 199, 90, 0.3);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
    <div class="brand-box">
        <div style="display: flex; align-items: center;">
            <div class="brand-icon">S</div>
            <div>
                <div class="brand-text">Sufyan Ali</div>
                <div class="brand-sub">Revenue OS</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
    <div>
        <span class="status-badge">Live</span>
        <span class="status-badge warn">Q3 Focus</span>
        <span class="status-badge alert">At Risk</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.header("Controls")
selected_metric = st.sidebar.selectbox("Choose a metric to explore:", ["Revenue", "Profit", "Visitors"])
show_trend = st.sidebar.checkbox("Show trend lines", value=True)
region = st.sidebar.radio("Region", ["Global", "North America", "Europe", "APAC"])

st.markdown(
    """
    <div class="main-header">
        <h1>Northstar Labs Analytics</h1>
        <p>Executive overview of growth, efficiency, and customer engagement.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="filter-strip">
        <span class="chip active">All Products</span>
        <span class="chip">Enterprise</span>
        <span class="chip">North America</span>
        <span class="chip">This Quarter</span>
    </div>
    """,
    unsafe_allow_html=True,
)

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"]
revenue = [120, 180, 165, 220, 250, 240, 300, 330]
cost = [80, 110, 95, 130, 145, 140, 170, 190]
profit = np.array(revenue) - np.array(cost)
visitors = [420, 510, 500, 640, 700, 680, 760, 820]

sales_df = pd.DataFrame(
    {
        "Month": months,
        "Revenue": revenue,
        "Cost": cost,
        "Profit": profit,
        "Visitors": visitors,
    }
)

forecast_months = ["Sep", "Oct", "Nov", "Dec", "Jan"]
forecast_values = [360, 390, 430, 470, 520]
forecast_df = pd.DataFrame({"Month": forecast_months, "Forecast": forecast_values})

team_rows = [
    {"Account": "Acme Corp", "Owner": "Ayesha", "Status": "Healthy", "MRR": "$18.2K", "Renewal": "87%"},
    {"Account": "NovaWorks", "Owner": "Javed", "Status": "Watch", "MRR": "$11.4K", "Renewal": "72%"},
    {"Account": "BridgeOps", "Owner": "Sara", "Status": "Critical", "MRR": "$20.5K", "Renewal": "61%"},
    {"Account": "Cobalt AI", "Owner": "Hamza", "Status": "Healthy", "MRR": "$15.1K", "Renewal": "90%"},
]

team_df = pd.DataFrame(team_rows)
team_df["Status"] = team_df["Status"].map(
    {
        "Healthy": '<span class="mini-badge positive">Healthy</span>',
        "Watch": '<span class="mini-badge warn">Watch</span>',
        "Critical": '<span class="mini-badge alert">Critical</span>',
    }
)

st.markdown('<div class="kpi-ribbon">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        '<div class="kpi-pill"><div class="kpi-label">Total Revenue</div><div class="kpi-value">$' + f"{sum(revenue):,}" + '</div><div class="kpi-delta">+12.4%</div></div>',
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        '<div class="kpi-pill"><div class="kpi-label">Net Profit</div><div class="kpi-value">$' + f"{sum(profit):,}" + '</div><div class="kpi-delta">+8.1%</div></div>',
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        '<div class="kpi-pill"><div class="kpi-label">Visitors</div><div class="kpi-value">' + f"{int(np.mean(visitors))}" + '</div><div class="kpi-delta">+15.0%</div></div>',
        unsafe_allow_html=True,
    )
with col4:
    st.markdown(
        '<div class="kpi-pill"><div class="kpi-label">Best Month</div><div class="kpi-value">' + months[np.argmax(revenue)] + '</div><div class="kpi-delta">Peak</div></div>',
        unsafe_allow_html=True,
    )
st.markdown('</div>', unsafe_allow_html=True)

main_col, aside_col = st.columns([3.2, 1.5])

with main_col:
    st.subheader("Performance Overview")
    line_fig = px.line(
        sales_df,
        x="Month",
        y=selected_metric,
        title=f"{selected_metric} Trend",
        markers=True,
        color_discrete_sequence=["#ffd76a"],
        template="plotly_dark",
    )
    if show_trend:
        line_fig.add_scatter(
            x=sales_df["Month"],
            y=sales_df[selected_metric].rolling(2).mean(),
            mode="lines",
            line=dict(dash="dot", color="#f2c14e"),
            name="Trend",
        )
    line_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#fff3bf"},
        margin={"l": 20, "r": 20, "t": 40, "b": 20},
        title_font={"color": "#fff3bf"},
        legend={"bordercolor": "#f5c75a", "borderwidth": 1},
        xaxis={"gridcolor": "rgba(245,199,90,0.12)", "showline": True, "linecolor": "#f5c75a"},
        yaxis={"gridcolor": "rgba(245,199,90,0.12)", "showline": True, "linecolor": "#f5c75a"},
        transition={"duration": 700},
    )
    st.plotly_chart(line_fig, use_container_width=True, config={"displayModeBar": False})

    st.subheader("Revenue Mix")
    bar_fig = px.bar(
        sales_df,
        x="Month",
        y=["Revenue", "Cost", "Profit"],
        barmode="group",
        title="Revenue, Cost, and Profit by Month",
        color_discrete_sequence=["#ffd76a", "#f4a261", "#e9c46a"],
        template="plotly_dark",
    )
    bar_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#fff3bf"},
        margin={"l": 20, "r": 20, "t": 40, "b": 20},
        title_font={"color": "#fff3bf"},
        legend={"bordercolor": "#f5c75a", "borderwidth": 1},
        xaxis={"gridcolor": "rgba(245,199,90,0.12)", "showline": True, "linecolor": "#f5c75a"},
        yaxis={"gridcolor": "rgba(245,199,90,0.12)", "showline": True, "linecolor": "#f5c75a"},
        transition={"duration": 700},
    )
    st.plotly_chart(bar_fig, use_container_width=True, config={"displayModeBar": False})

    st.subheader("Growth Mix")
    donut_col1, donut_col2 = st.columns(2)
    with donut_col1:
        segment_df = pd.DataFrame(
            {"Segment": ["Enterprise", "SMB", "Startup", "Mid-Market"], "Value": [42, 30, 18, 10]}
        )
        segment_fig = px.pie(
            segment_df,
            values="Value",
            names="Segment",
            title="Revenue Segments",
            color_discrete_sequence=["#ffd76a", "#f6c453", "#d9a441", "#f4e29b"],
            template="plotly_dark",
        )
        segment_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#fff3bf"},
            margin={"l": 10, "r": 10, "t": 40, "b": 10},
            title_font={"color": "#fff3bf"},
            legend={"bordercolor": "#f5c75a", "borderwidth": 1},
            transition={"duration": 700},
        )
        st.plotly_chart(segment_fig, use_container_width=True, config={"displayModeBar": False})

    with donut_col2:
        channel_df = pd.DataFrame(
            {"Channel": ["Inbound", "Outbound", "Partners", "Self-Serve"], "Value": [38, 26, 22, 14]}
        )
        channel_fig = px.pie(
            channel_df,
            values="Value",
            names="Channel",
            title="Acquisition Mix",
            color_discrete_sequence=["#ffd76a", "#f2c14e", "#d69e2e", "#f9e4a0"],
            template="plotly_dark",
        )
        channel_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#fff3bf"},
            margin={"l": 10, "r": 10, "t": 40, "b": 10},
            title_font={"color": "#fff3bf"},
            legend={"bordercolor": "#f5c75a", "borderwidth": 1},
            transition={"duration": 700},
        )
        st.plotly_chart(channel_fig, use_container_width=True, config={"displayModeBar": False})

    heatmap_df = pd.DataFrame(
        np.array([
            [88, 82, 90, 96],
            [76, 79, 83, 90],
            [68, 72, 79, 84],
            [54, 63, 70, 80],
        ]),
        index=["Enterprise", "SMB", "Startup", "Mid-Market"],
        columns=["Q1", "Q2", "Q3", "Q4"],
    )
    heatmap_fig = px.imshow(
        heatmap_df,
        color_continuous_scale="YlOrBr",
        aspect="auto",
        title="Customer Health Heatmap",
        template="plotly_dark",
    )
    heatmap_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#fff3bf"},
        margin={"l": 20, "r": 20, "t": 40, "b": 20},
        title_font={"color": "#fff3bf"},
        transition={"duration": 700},
    )
    st.plotly_chart(heatmap_fig, use_container_width=True, config={"displayModeBar": False})

    st.subheader("Pipeline Overview")
    st.markdown(team_df.to_html(index=False, escape=False, classes="custom-table"), unsafe_allow_html=True)

with aside_col:
    st.markdown(
        """
        <div class="activity-box">
            <h3>Activity Feed</h3>
            <ul class="activity-list">
                <li class="activity-item">
                    <div class="dot"></div>
                    <div>
                        <div class="activity-text">New enterprise deal closed</div>
                        <div class="activity-time">2h ago</div>
                    </div>
                </li>
                <li class="activity-item">
                    <div class="dot"></div>
                    <div>
                        <div class="activity-text">Marketing campaign exceeded target by 18%</div>
                        <div class="activity-time">5h ago</div>
                    </div>
                </li>
                <li class="activity-item">
                    <div class="dot"></div>
                    <div>
                        <div class="activity-text">Support SLA improved to 98.7%</div>
                        <div class="activity-time">Today</div>
                    </div>
                </li>
                <li class="activity-item">
                    <div class="dot"></div>
                    <div>
                        <div class="activity-text">Ops team flagged 3 renewals at risk</div>
                        <div class="activity-time">Today</div>
                    </div>
                </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="forecast-box" style="margin-top: 1rem;">
            <h3>Revenue Forecast</h3>
            <div style="font-size: 1.8rem; font-weight: 700; color: #fff7d6; margin-top: 0.5rem;">$2.1M</div>
            <div class="budget-tag" style="margin-top: 0.5rem;">+14.2% vs target</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    forecast_fig = px.line(
        forecast_df,
        x="Month",
        y="Forecast",
        title="Forecast Trend",
        markers=True,
        color_discrete_sequence=["#ffd76a"],
        template="plotly_dark",
    )
    forecast_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#fff3bf"},
        margin={"l": 10, "r": 10, "t": 30, "b": 10},
        title_font={"color": "#fff3bf"},
        xaxis={"gridcolor": "rgba(245,199,90,0.12)", "showline": True, "linecolor": "#f5c75a"},
        yaxis={"gridcolor": "rgba(245,199,90,0.12)", "showline": True, "linecolor": "#f5c75a"},
        transition={"duration": 700},
    )
    st.plotly_chart(forecast_fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        """
        <div class="panel-box" style="margin-top: 1rem;">
            <h3>Team Pulse</h3>
            <div style="margin-top: 0.8rem; color: #fff3bf;">CSAT: 94%</div>
            <div style="margin-top: 0.4rem; color: #f3d98d;">On-time delivery: 96%</div>
            <div style="margin-top: 0.4rem; color: #f3d98d;">NPS: 62</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption("Created by Sufyan Ali")
