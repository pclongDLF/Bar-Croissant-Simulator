import streamlit as st

st.set_page_config(page_title="Bar à Croissant – ROI Simulator", layout="wide")

st.title("🥐 Bar à Croissant – ROI Simulator")
st.markdown("Model faithfully reproduced from **FEUIL 2**")

# ======================
# SECTION 1 — CAPEX
# ======================
st.sidebar.header("1️⃣ Initial Investment (CAPEX)")

injector = st.sidebar.number_input("Injector (€)", 0, 100000, 8000, 500)
base = st.sidebar.number_input("Base (€)", 0, 100000, 5000, 500)
waffle_iron = st.sidebar.number_input("Waffle iron (croiffle + Eiffel Tower) (€)", 0, 100000, 12000, 500)
transport = st.sidebar.number_input("Transport (€)", 0, 50000, 3000, 500)

total_capex = injector + base + waffle_iron + transport

# ======================
# SECTION 2 — PRICE
# ======================
st.sidebar.header("2️⃣ Price Structure")

price_with_vat = st.sidebar.number_input("Selling price (with VAT) (€)", 1.0, 20.0, 5.0, 0.1)
vat_rate = st.sidebar.number_input("VAT (%)", 0.0, 30.0, 20.0, 0.5)

price_ex_vat = price_with_vat / (1 + vat_rate / 100)

# ======================
# SECTION 3 — OPERATIONS
# ======================
st.sidebar.header("3️⃣ Operations")

days_per_year = st.sidebar.number_input("Operating days / year", 1, 365, 300)
sales_per_day = st.sidebar.number_input("Croissants sold / day", 0, 5000, 300)
cost_per_unit = st.sidebar.number_input("Cost per croissant (€)", 0.0, 10.0, 1.2, 0.05)

# Core turnover
daily_turnover_core = sales_per_day * price_ex_vat
annual_turnover_core = daily_turnover_core * days_per_year

# ======================
# SECTION 3B — ADDITIONAL SKUs
# ======================
st.sidebar.subheader("➕ Additional SKUs")

extra_sku_per_day = st.sidebar.number_input("Number of extra SKU sales / day", 0, 5000, 50)
extra_price = st.sidebar.number_input("Extra SKU price (ex VAT) (€)", 0.0, 20.0, 1.5, 0.1)

extra_turnover_day = extra_sku_per_day * extra_price
extra_turnover_year = extra_turnover_day * days_per_year

# ======================
# TOTAL TURNOVER
# ======================
total_daily_turnover = daily_turnover_core + extra_turnover_day
total_annual_turnover = annual_turnover_core + extra_turnover_year

# ======================
# RESULTS DISPLAY
# ======================
st.header("📊 Results (Results of BAR À CROISSANT ROI)")

col1, col2, col3 = st.columns(3)

col1.metric("Total CAPEX (€)", f"{total_capex:,.0f}")
col2.metric("Daily Turnover (€)", f"{total_daily_turnover:,.0f}")
col3.metric("Annual Turnover (€)", f"{total_annual_turnover:,.0f}")

st.divider()

st.subheader("🔍 Breakdown")

st.write(f"• Core annual turnover: **€{annual_turnover_core:,.0f}**")
st.write(f"• Extra SKU annual turnover: **€{extra_turnover_year:,.0f}**")

if total_capex > 0:
    roi = (total_annual_turnover / total_capex) * 100
    st.metric("ROI (%)", f"{roi:.1f}%")
else:
    st.info("ROI not available (CAPEX = 0)")


