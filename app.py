import streamlit as st

st.set_page_config(page_title="BAR À CROISSANT – ROI Simulator", layout="wide")

st.title("🥐 BAR À CROISSANT – ROI Simulator")
st.markdown("Results of **BAR À CROISSANT ROI**")

# ======================
# 🟧 CAPEX (VARIABLES)
# ======================
st.sidebar.header("🟧 CAPEX (Initial investment)")

def capex_line(label, default_price, default_qty):
    col1, col2 = st.sidebar.columns(2)
    price = col1.number_input(f"{label} – unit price (€)", 0.0, 10000.0, default_price, 10.0)
    qty = col2.number_input(f"{label} – qty", 0, 10, default_qty)
    return price * qty

injector = capex_line("Injector", 798.0, 3)
base = capex_line("Base", 284.0, 1)
waffle = capex_line("Waffle iron (croiffle + Eiffel)", 1000.0, 1)
transport = capex_line("Transport", 600.0, 1)

total_equipment = injector + base + waffle + transport

# ======================
# 🟩 SALES (VARIABLES)
# ======================
st.sidebar.header("🟩 Sales")

price_with_vat = st.sidebar.number_input("Selling price WITH VAT (€)", 0.0, 20.0, 3.90, 0.05)
vat_rate = st.sidebar.number_input("VAT (%)", 0.0, 30.0, 5.5, 0.1)

price_ex_vat = price_with_vat / (1 + vat_rate / 100)

# ======================
# 🟩 OPERATIONS (VARIABLES)
# ======================
st.sidebar.header("🟩 Operations")

product_margin_pct = st.sidebar.number_input("Product margin (%)", 0.0, 100.0, 65.0, 1.0)
days_per_year = st.sidebar.number_input("Number of days in operation / year", 1, 365, 320)
croissants_per_day = st.sidebar.number_input("Actual croissant sales quantity / day", 0, 5000, 50)

additional_pct = st.sidebar.number_input(
    "Additional to filled croissant / croiffle (%)", 0.0, 100.0, 35.0, 1.0
)

extra_sku_per_day = st.sidebar.number_input(
    "Number of extra SKU sales / day", 0, 5000, 18
)

# ======================
# 🔒 CALCULATIONS (LOCKED)
# ======================
cost_per_unit = price_ex_vat * (1 - product_margin_pct / 100)

daily_turnover_core = croissants_per_day * price_ex_vat
daily_extra_turnover = extra_sku_per_day * price_ex_vat * (additional_pct / 100)

annual_turnover_core = daily_turnover_core * days_per_year
annual_extra_turnover = daily_extra_turnover * days_per_year

total_annual_turnover = annual_turnover_core + annual_extra_turnover

# ROI month (as in Excel)
roi_month = total_equipment / (total_annual_turnover / 12) if total_annual_turnover > 0 else 0

# ======================
# 📊 RESULTS (DISPLAY ONLY)
# ======================
st.header("📊 Results of BAR À CROISSANT ROI")

col1, col2, col3 = st.columns(3)

col1.metric("Total Equipment (€)", f"{total_equipment:,.0f}")
col2.metric("Annual Turnover (€)", f"{total_annual_turnover:,.0f}")
col3.metric("ROI (months)", f"{roi_month:.2f}")

st.divider()

st.subheader("Turnover breakdown (calculated)")

col_a, col_b = st.columns(2)

col_a.metric(
    "Extra turnover generated / day (€)",
    f"{daily_extra_turnover:,.0f}"
)

col_b.metric(
    "Extra turnover generated / year (€)",
    f"{annual_extra_turnover:,.0f}"
)

st.divider()

st.write(f"• Core croissant turnover / year: **€{annual_turnover_core:,.0f}**")



