import streamlit as st

st.set_page_config(
    page_title="BAR À CROISSANT – ROI Simulator",
    layout="wide"
)

st.title("🥐 BAR À CROISSANT – ROI Simulator")
st.markdown("Model rebuilt strictly from Excel (FEUIL 2)")

# ==================================================
# 🟧 CAPEX — INPUTS
# ==================================================
st.sidebar.header("🟧 CAPEX")

def capex_input(label, unit_default, qty_default):
    c1, c2 = st.sidebar.columns(2)
    unit = c1.number_input(
        f"{label} – unit price (€)", 0.0, 10000.0, unit_default, 1.0
    )
    qty = c2.number_input(
        f"{label} – qty", 0, 20, qty_default, 1
    )
    return unit * qty

injector = capex_input("Injector", 798.0, 3)
base = capex_input("Base", 284.0, 1)
waffle = capex_input("Waffle iron (croiffle + Eiffel Tower)", 1000.0, 1)
transport = capex_input("Transport", 600.0, 1)

total_equipment = injector + base + waffle + transport

# ==================================================
# 🟩 SALES — INPUTS
# ==================================================
st.sidebar.header("🟩 Sales")

price_with_vat = st.sidebar.number_input(
    "Selling price WITH VAT (€)", 0.0, 20.0, 3.90, 0.05
)

vat_pct = st.sidebar.number_input(
    "VAT (%)", 0.0, 30.0, 5.5, 0.1
)

price_ex_vat = price_with_vat / (1 + vat_pct / 100)

# ==================================================
# 🟩 OPERATIONS — INPUTS
# ==================================================
st.sidebar.header("🟩 Operations")

days_year = st.sidebar.number_input(
    "Number of days in operations / year", 1, 365, 320, 1
)

croissants_day = st.sidebar.number_input(
    "Actual croissant sales quantity / day", 0, 5000, 50, 1
)

additional_pct = st.sidebar.number_input(
    "Additional filled croissant sold (%)", 0.0, 100.0, 35.0, 1.0
)

extra_sku_day = st.sidebar.number_input(
    "Number of extra SKU sales / day", 0, 5000, 18, 1
)

extra_turnover_day = st.sidebar.number_input(
    "Extra turnover generated / day (€)", 0.0, 5000.0, 64.0, 1.0
)

margin_pct = st.sidebar.number_input(
    "Product margin (%)", 0.0, 100.0, 65.0, 1.0
)

# ==================================================
# 🔒 CALCULATIONS — STRICT
# ==================================================

converted_filled_day = croissants_day * (additional_pct / 100)

extra_turnover_year = extra_turnover_day * days_year

extra_margin_year = extra_turnover_year * (margin_pct / 100)

roi_month = (
    total_equipment / (extra_margin_year / 12)
    if extra_margin_year > 0
    else 0
)

# ==================================================
# 📊 RESULTS
# ==================================================
st.header("📊 Results of BAR À CROISSANT ROI")

c1, c2, c3 = st.columns(3)
c1.metric("Total equipment (€)", f"{total_equipment:,.0f}")
c2.metric("Extra turnover / year (€)", f"{extra_turnover_year:,.0f}")
c3.metric("ROI (months)", f"{roi_month:.2f}")

st.divider()

st.subheader("Calculated values (locked)")

st.write(f"• Selling price EX VAT: **€{price_ex_vat:.2f}**")
st.write(f"• Converted filled croissant / day: **{converted_filled_day:.1f}**")
st.write(f"• Extra margin / year: **€{extra_margin_year:,.0f}**")
