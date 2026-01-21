import streamlit as st

st.set_page_config(
    page_title="BAR À CROISSANT – ROI Simulator",
    layout="wide"
)

st.title("🥐 BAR À CROISSANT – ROI Simulator")
st.markdown("Results of **BAR À CROISSANT ROI**")

# ==================================================
# 🟧 CAPEX
# ==================================================
st.sidebar.header("🟧 CAPEX (Initial investment)")

def capex_line(label, default_price, default_qty):
    col1, col2 = st.sidebar.columns(2)
    unit_price = col1.number_input(
        f"{label} – unit price (€)",
        min_value=0.0,
        max_value=10000.0,
        value=default_price,
        step=1.0
    )
    qty = col2.number_input(
        f"{label} – qty",
        min_value=0,
        max_value=10,
        value=default_qty,
        step=1
    )
    return unit_price * qty

injector = capex_line("Injector", 798.0, 3)
base = capex_line("Base", 284.0, 1)
waffle = capex_line("Waffle iron (croiffle + Eiffel Tower)", 1000.0, 1)
transport = capex_line("Transport", 600.0, 1)

total_equipment = injector + base + waffle + transport

st.sidebar.markdown("### 🧾 CAPEX breakdown (calculated)")
st.sidebar.write(f"Injector total: €{injector:,.0f}")
st.sidebar.write(f"Base total: €{base:,.0f}")
st.sidebar.write(f"Waffle iron total: €{waffle:,.0f}")
st.sidebar.write(f"Transport total: €{transport:,.0f}")

# ==================================================
# 🟩 SALES
# ==================================================
st.sidebar.header("🟩 Sales")

price_with_vat = st.sidebar.number_input(
    "Selling price WITH VAT (€)", 0.0, 20.0, 3.90, 0.05
)
vat_rate = st.sidebar.number_input(
    "VAT (%)", 0.0, 30.0, 5.5, 0.1
)

price_ex_vat = price_with_vat / (1 + vat_rate / 100)
st.sidebar.markdown(f"**Selling price EX VAT:** €{price_ex_vat:.2f}")

# ==================================================
# 🟩 OPERATIONS
# ==================================================
st.sidebar.header("🟩 Operations")

days_per_year = st.sidebar.number_input(
    "Number of days in operation / year",
    min_value=320,
    max_value=320,
    value=320,
    step=1
)

product_margin_pct = st.sidebar.number_input(
    "Product margin (%)", 0.0, 100.0, 65.0, 1.0
)

extra_turnover_day = st.sidebar.number_input(
    "Extra turnover generated / day (€)",
    0.0, 1000.0, 64.0, 1.0
)

# ==================================================
# 🔒 CALCULATIONS
# ==================================================
extra_turnover_year = extra_turnover_day * days_per_year
extra_margin_year = extra_turnover_year * (product_margin_pct / 100)

roi_month = total_equipment / (extra_margin_year / 12)

# ==================================================
# 📊 RESULTS
# ==================================================
st.header("📊 Results of BAR À CROISSANT ROI")

col1, col2, col3 = st.columns(3)
col1.metric("Total equipment (€)", f"{total_equipment:,.0f}")
col2.metric("Extra turnover / year (€)", f"{extra_turnover_year:,.0f}")
col3.metric("ROI (months)", f"{roi_month:.2f}")
