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
    price = col1.number_input(
        f"{label} – unit price (€)", 0.0, 10000.0, default_price, 10.0
    )
    qty = col2.number_input(
        f"{label} – qty", 0, 10, default_qty
    )
    return price * qty

injector = capex_line("Injector", 798.0, 3)
base = capex_line("Base", 284.0, 1)
waffle = capex_line("Waffle iron (croiffle + Eiffel Tower)", 1000.0, 1)
transport = capex_line("Transport", 600.0, 1)

total_equipment = injector + base + waffle + transport

# ======================
# 🟩 SALES (VARIABLES)
# ======================
st.sidebar.header("🟩 Sales")

price_with_vat = st.sidebar.number_input(
    "Selling price WITH VAT (€)", 0.0, 20.0, 3.90, 0.05
)
vat_rate = st.sidebar.number_input(
    "VAT (%)", 0.0, 30.0, 5.5, 0.1
)

price_ex_vat = price_with_vat / (1 + vat_rate / 100)

# ======================
# 🟩 OPERATIONS (VARIABLES)
# ======================
st.sidebar.header("🟩 Operations")

days_per_year = st.sidebar.number_input(
    "Number of days in operation / year", 1, 365, 322
)

croissants_per_day = st.sidebar.number_input(
    "Actual croissant sales quantity / day", 0, 5000, 50
)

conversion_pct = st.sidebar.number_input(
    "Conversion to filled croissant / croiffle (%)", 0.0, 100.0, 35.0, 1.0
)

sku_sales_per_day = st.sidebar.number_input(
    "Number SKU sales / day (assumption)", 0, 5000, 18
)

product_margin_pct = st.sidebar.number_input(
    "Product margin (%)", 0.0, 100.0, 65.0, 1.0
)

# ======================
# 🔒 CALCULATIONS (STRICT FEUIL 2)
# ======================

# Converted SKU/day (informational only)
converted_sku_per_day = croissants_per_day * (conversion_pct / 100)

# Extra turnover
extra_turnover_day = sku_sales_per_day * price_ex_vat
extra_turnover_year = extra_turnover_day * days_per_year

# Extra margin (used for ROI)
extra_margin_year = extra_turnover_year * (product_margin_pct / 100)

# ROI (month)
roi_month = (
    total_equipment
    / (extra_margin_year / 12)
    if extra_margin_year > 0
    else 0
)

# ======================
# 📊 RESULTS
# ======================
st.header("📊 Results of BAR À CROISSANT ROI")

col1, col2, col3 = st.columns(3)

col1.metric("Total Equipment (€)", f"{total_equipment:,.0f}")
col2.metric("Extra turnover / year (€)", f"{extra_turnover_year:,.0f}")
col3.metric("ROI (months)", f"{roi_month:.2f}")

st.divider()

st.subheader("Calculated values (locked)")

st.write(f"• Converted SKU product / day: **{converted_sku_per_day:.1f}**")
st.write(f"• Extra turnover generated / day: **€{extra_turnover_day:,.0f}**")
st.write(f"• Extra margin / year (used for ROI): **€{extra_margin_year:,.0f}**")
