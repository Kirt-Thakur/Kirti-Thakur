# ============================================================
# STOCK PORTFOLIO DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Stock Portfolio Dashboard",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("📈 Stock Portfolio Dashboard")

st.caption(
    "Analysis of selected Indian stocks, portfolio performance, "
    "SENSEX comparison and CAPM analysis."
)


# ============================================================
# STOCK DEFINITIONS
# ============================================================

stocks = {
    "Axis Bank": "AXISBANK.NS",
    "Hindustan Unilever": "HINDUNILVR.NS",
    "Eternal": "ETERNAL.NS",
    "Tech Mahindra": "TECHM.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS"
}

sensex_ticker = "^BSESN"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

@st.cache_data(ttl=3600)
def download_data(ticker, period):

    data = yf.download(
        ticker,
        period=period,
        auto_adjust=False,
        progress=False
    )

    return data


def clean_data(data):

    if data.empty:
        return data

    data = data.copy()

    # Handle yfinance MultiIndex columns
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.dropna()

    return data


# ============================================================
# SIDEBAR - DASHBOARD CONTROLS
# ============================================================

st.sidebar.header("⚙️ Dashboard Controls")


# ------------------------------------------------------------
# TIME PERIOD
# ------------------------------------------------------------

st.sidebar.subheader("📅 Time Period")

tenure = st.sidebar.selectbox(
    "Select Period",
    [
        "1 Week",
        "1 Month",
        "3 Months",
        "6 Months",
        "1 Year",
        "2 Years",
        "5 Years"
    ],
    index=3
)

period_map = {
    "1 Week": "1mo",
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "2 Years": "2y",
    "5 Years": "5y"
}

yf_period = period_map[tenure]

# ------------------------------------------------------------
# STOCK NAVIGATION
# ------------------------------------------------------------

st.sidebar.divider()

st.sidebar.subheader("📌 Stocks")

selected_stock = st.sidebar.radio(
    "Select Asset",
    [
        "Axis Bank",
        "Hindustan Unilever",
        "Eternal",
        "Tech Mahindra",
        "Kotak Mahindra Bank",
        "SENSEX"
    ]
)


# ------------------------------------------------------------
# PORTFOLIO WEIGHTS
# ------------------------------------------------------------

st.sidebar.divider()

st.sidebar.subheader("💼 Portfolio Weights")

axis_weight = st.sidebar.number_input(
    "Axis Bank (%)",
    min_value=0.0,
    max_value=100.0,
    value=20.0,
    step=1.0
)

hul_weight = st.sidebar.number_input(
    "Hindustan Unilever (%)",
    min_value=0.0,
    max_value=100.0,
    value=20.0,
    step=1.0
)

eternal_weight = st.sidebar.number_input(
    "Eternal (%)",
    min_value=0.0,
    max_value=100.0,
    value=20.0,
    step=1.0
)

techm_weight = st.sidebar.number_input(
    "Tech Mahindra (%)",
    min_value=0.0,
    max_value=100.0,
    value=20.0,
    step=1.0
)

kotak_weight = st.sidebar.number_input(
    "Kotak Mahindra Bank (%)",
    min_value=0.0,
    max_value=100.0,
    value=20.0,
    step=1.0
)


weights = {
    "Axis Bank": axis_weight,
    "Hindustan Unilever": hul_weight,
    "Eternal": eternal_weight,
    "Tech Mahindra": techm_weight,
    "Kotak Mahindra Bank": kotak_weight
}


total_weight = sum(weights.values())


st.sidebar.metric(
    "Total Weight",
    f"{total_weight:.0f}%"
)


if total_weight == 100:
    st.sidebar.success("✅ Portfolio = 100%")
else:
    st.sidebar.warning(
        "⚠️ Total weight must equal 100%"
    )



# ------------------------------------------------------------
# ANALYSIS NAVIGATION
# ------------------------------------------------------------

st.sidebar.divider()

st.sidebar.subheader("📊 Analysis")

selected_analysis = st.sidebar.radio(
    "Select Analysis",
    [
        "Portfolio Analysis",
        "CAPM Analysis"
    ]
)


# ------------------------------------------------------------
# NEWS NAVIGATION
# ------------------------------------------------------------

st.sidebar.divider()

st.sidebar.subheader("📰 Latest News")

selected_news_company = st.sidebar.radio(
    "Select Company",
    [
        "Axis Bank",
        "Hindustan Unilever",
        "Eternal",
        "Tech Mahindra",
        "Kotak Mahindra Bank"
    ]
)


# ============================================================
# SELECT TICKER
# ============================================================

if selected_stock == "SENSEX":

    selected_ticker = sensex_ticker

else:

    selected_ticker = stocks[selected_stock]


# ============================================================
# MAIN STOCK ANALYSIS
# ============================================================

st.divider()

st.header(f"📊 {selected_stock} Stock Analysis")


data = download_data(
    selected_ticker,
    yf_period
)

data = clean_data(data)


if data.empty:

    st.error(
        f"Unable to download data for {selected_stock}."
    )

else:

    # --------------------------------------------------------
    # RETURNS
    # --------------------------------------------------------

    data["Return (%)"] = (
        (
            data["Close"]
            - data["Close"].shift(1)
        )
        / data["Close"].shift(1)
    ) * 100


    # --------------------------------------------------------
    # TABLE TIME FILTER
    # --------------------------------------------------------

    table_period = st.selectbox(
        "📅 Select Price Table Period",
        [
            "1 Week",
            "1 Month",
            "3 Months",
            "6 Months",
            "1 Year"
        ]
    )


    table_days = {
        "1 Week": 7,
        "1 Month": 30,
        "3 Months": 90,
        "6 Months": 180,
        "1 Year": 365
    }


    selected_days = table_days[table_period]


    table_data = data.tail(selected_days).copy()


    # --------------------------------------------------------
    # PRICE TABLE
    # --------------------------------------------------------

    st.subheader(
        f"📋 {selected_stock} — {table_period} Price Data"
    )


    display_table = pd.DataFrame({

        "Date":
            table_data.index.strftime("%d-%b-%Y"),

        "Open":
            table_data["Open"].values,

        "High":
            table_data["High"].values,

        "Low":
            table_data["Low"].values,

        "Close":
            table_data["Close"].values,

        "Return (%)":
            table_data["Return (%)"].values

    })


    st.dataframe(
        display_table.round(2),
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # CANDLESTICK CHART
    # --------------------------------------------------------

    st.subheader(
        f"🕯️ {selected_stock} Candlestick Chart"
    )


    fig = go.Figure(
        data=[
            go.Candlestick(
                x=data.index,
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                name=selected_stock
            )
        ]
    )


    fig.update_layout(
        title=f"{selected_stock} Price Movement",
        xaxis_title="Date",
        yaxis_title="Price (₹)",
        height=550,
        xaxis_rangeslider_visible=False
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# DOWNLOAD ALL STOCK DATA FOR PORTFOLIO ANALYSIS
# ============================================================

portfolio_prices = pd.DataFrame()


for company_name, ticker in stocks.items():

    company_data = download_data(
        ticker,
        yf_period
    )

    company_data = clean_data(company_data)


    if not company_data.empty:

        portfolio_prices[
            company_name
        ] = company_data["Close"]


portfolio_prices = portfolio_prices.dropna()


# ============================================================
# PORTFOLIO ANALYSIS
# ============================================================

st.divider()

st.header("💼 Portfolio Analysis")


if total_weight != 100:

    st.warning(
        "Please make the total portfolio weight equal to 100% "
        "to calculate portfolio returns."
    )

elif portfolio_prices.empty:

    st.error(
        "Portfolio data could not be downloaded."
    )

else:

    # --------------------------------------------------------
    # DAILY RETURNS
    # --------------------------------------------------------

    stock_returns = portfolio_prices.pct_change() * 100

    stock_returns = stock_returns.dropna()


    # --------------------------------------------------------
    # WEIGHTS AS DECIMALS
    # --------------------------------------------------------

    weight_series = pd.Series(weights) / 100


    # --------------------------------------------------------
    # PORTFOLIO DAILY RETURN
    # --------------------------------------------------------

    portfolio_return_series = (
        stock_returns * weight_series
    ).sum(axis=1)


    # --------------------------------------------------------
    # LATEST ASSET RETURNS TABLE
    # --------------------------------------------------------

    latest_returns = stock_returns.iloc[-1]


    portfolio_table = pd.DataFrame({

        "Company":
            list(latest_returns.index),

        "Daily Return (%)":
            latest_returns.values,

        "Weight (%)":
            [
                weights[company]
                for company in latest_returns.index
            ]

    })


    overall_return = portfolio_return_series.iloc[-1]


    portfolio_table.loc[
        len(portfolio_table)
    ] = [
        "OVERALL PORTFOLIO",
        overall_return,
        100
    ]


    st.subheader("📋 Latest Portfolio Returns")


    st.dataframe(
        portfolio_table.round(2),
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # METRIC
    # --------------------------------------------------------

    st.metric(
        "Overall Portfolio Daily Return",
        f"{overall_return:.2f}%"
    )


    # --------------------------------------------------------
    # PORTFOLIO RETURN LINE GRAPH
    # --------------------------------------------------------

    st.subheader(
        "📈 Portfolio Daily Return Over Time"
    )


    portfolio_chart = go.Figure()


    portfolio_chart.add_trace(
        go.Scatter(
            x=portfolio_return_series.index,
            y=portfolio_return_series.values,
            mode="lines",
            name="Portfolio Return"
        )
    )


    portfolio_chart.update_layout(
        xaxis_title="Date",
        yaxis_title="Daily Return (%)",
        height=450
    )


    st.plotly_chart(
        portfolio_chart,
        use_container_width=True
    )


    # ========================================================
    # PORTFOLIO VS SENSEX
    # ========================================================

    st.divider()

    st.header("📊 Portfolio vs SENSEX")


    sensex_data = download_data(
        sensex_ticker,
        yf_period
    )

    sensex_data = clean_data(sensex_data)


    if not sensex_data.empty:

        sensex_close = sensex_data["Close"]


        # Normalise portfolio value

        portfolio_growth = (
            (1 + portfolio_return_series / 100)
            .cumprod()
            * 1
        )


        sensex_growth = (
            sensex_close
            / sensex_close.iloc[0]
        ) * 1


        comparison = pd.concat(
            [
                portfolio_growth.rename("Portfolio"),
                sensex_growth.rename("SENSEX")
            ],
            axis=1
        ).dropna()


        comparison_chart = go.Figure()


        comparison_chart.add_trace(
            go.Scatter(
                x=comparison.index,
                y=comparison["Portfolio"],
                mode="lines",
                name="Portfolio"
            )
        )


        comparison_chart.add_trace(
            go.Scatter(
                x=comparison.index,
                y=comparison["SENSEX"],
                mode="lines",
                name="SENSEX"
            )
        )


        comparison_chart.update_layout(
            title="Portfolio Performance vs SENSEX",
            xaxis_title="Date",
            yaxis_title="Returns",
            height=500
        )


        st.plotly_chart(
            comparison_chart,
            use_container_width=True
        )


# ============================================================
# CAPM ANALYSIS
# ============================================================

st.divider()

st.header("📊 CAPM Analysis")


risk_free_rate = st.number_input(
    "Risk-Free Rate (%)",
    min_value=0.0,
    max_value=20.0,
    value=6.50,
    step=0.25
)


if not portfolio_prices.empty:

    sensex_capm = download_data(
        sensex_ticker,
        yf_period
    )

    sensex_capm = clean_data(sensex_capm)


    if not sensex_capm.empty:

        market_returns = (
            sensex_capm["Close"]
            .pct_change()
            .dropna()
        )


        capm_results = []


        for company in stocks.keys():

            asset_returns = (
                portfolio_prices[company]
                .pct_change()
                .dropna()
            )


            combined_returns = pd.concat(
                [
                    asset_returns.rename("Asset"),
                    market_returns.rename("Market")
                ],
                axis=1
            ).dropna()


            if len(combined_returns) > 2:

                beta = (
                    combined_returns["Asset"]
                    .cov(combined_returns["Market"])
                    /
                    combined_returns["Market"].var()
                )


                actual_return = (
                    (
                        portfolio_prices[company].iloc[-1]
                        /
                        portfolio_prices[company].iloc[0]
                    )
                    - 1
                ) * 100


                market_return = (
                    (
                        sensex_capm["Close"].iloc[-1]
                        /
                        sensex_capm["Close"].iloc[0]
                    )
                    - 1
                ) * 100


                expected_return = (
                    risk_free_rate
                    + beta
                    * (
                        market_return
                        - risk_free_rate
                    )
                )


                alpha = (
                    actual_return
                    - expected_return
                )


                capm_results.append({

                    "Company": company,
                    "Beta": beta,
                    "Actual Return (%)": actual_return,
                    "CAPM Expected Return (%)":
                        expected_return,
                    "Alpha (%)": alpha

                })


        capm_df = pd.DataFrame(
            capm_results
        )


        st.dataframe(
            capm_df.round(2),
            use_container_width=True,
            hide_index=True
        )


        # ----------------------------------------------------
        # CAPM BAR CHART
        # ----------------------------------------------------

        if not capm_df.empty:

            capm_chart = go.Figure()


            capm_chart.add_trace(
                go.Bar(
                    x=capm_df["Company"],
                    y=capm_df["Actual Return (%)"],
                    name="Actual Return"
                )
            )


            capm_chart.add_trace(
                go.Bar(
                    x=capm_df["Company"],
                    y=capm_df[
                        "CAPM Expected Return (%)"
                    ],
                    name="CAPM Expected Return"
                )
            )


            capm_chart.update_layout(
                title="Actual Return vs CAPM Expected Return",
                xaxis_title="Company",
                yaxis_title="Return (%)",
                barmode="group",
                height=500
            )


            st.plotly_chart(
                capm_chart,
                use_container_width=True
            )


# ============================================================
# LATEST NEWS - ECONOMIC TIMES
# ============================================================

st.divider()

st.header(
    f"📰 Latest News — {selected_news_company}"
)

st.caption(
    "Company-specific news from The Economic Times."
)


et_news_pages = {

    "Axis Bank":
        "https://economictimes.indiatimes.com/axis-bank-ltd/stocksupdate/companyid-9175.cms",

    "Hindustan Unilever":
        "https://economictimes.indiatimes.com/hindustan-unilever-ltd/stocks/companyid-13616.cms",

    "Eternal":
        "https://economictimes.indiatimes.com/eternal-ltd/stocks/companyid-57948.cms",

    "Tech Mahindra":
        "https://economictimes.indiatimes.com/tech-mahindra-ltd/stocksupdate/companyid-11221.cms",

    "Kotak Mahindra Bank":
        "https://economictimes.indiatimes.com/kotak-mahindra-bank-ltd/stocksupdate/companyid-12161.cms"
}


selected_news_url = et_news_pages[
    selected_news_company
]


st.markdown(
    f"""
    ### 📰 {selected_news_company}

    **Source: The Economic Times**

    [View Latest {selected_news_company} News on
    The Economic Times →]({selected_news_url})
    """
)

# ============================================================
# MY NOTES - SIDEBAR
# ============================================================

st.sidebar.divider()

st.sidebar.subheader("📝 My Notes")

note_company = st.sidebar.selectbox(
    "Select Asset for Notes",
    [
        "Axis Bank",
        "Hindustan Unilever",
        "Eternal",
        "Tech Mahindra",
        "Kotak Mahindra Bank",
        "SENSEX"
    ],
    key="note_company_select"
)

# ============================================================
# NOTES / OBSERVATIONS
# ============================================================

st.divider()

st.header("📝 My Notes & Observations")

st.caption(
    f"Personal notes for {note_company}"
)

if "notes" not in st.session_state:
    st.session_state.notes = {}

if note_company not in st.session_state.notes:
    st.session_state.notes[note_company] = ""


note_text = st.text_area(
    "Write your observation:",
    value=st.session_state.notes[note_company],
    height=180,
    placeholder=(
        "Example: Stock showed high volatility after the "
        "quarterly results. Consider monitoring beta..."
    ),
    key=f"note_{note_company}"
)


if st.button(
    "💾 Save Note",
    key=f"save_note_{note_company}"
):

    st.session_state.notes[note_company] = note_text

    st.success(
        f"Note saved for {note_company}."
    )
# ============================================================
# END OF DASHBOARD
# ============================================================
