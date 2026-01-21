import streamlit as st

st.set_page_config(
    page_title="BAR À CROISSANT – ROI Simulator",
    layout="wide"
)

st.title("🥐 BAR À CROISSANT – ROI Simulator")
st.markdown("Results of **BAR À CROISSANT ROI**")

# ==================================================
# 🟧 CAPEX (VARIABLES)
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

# CAPEX breakdown (calculated)
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
    "Selling price WITH VAT (€)",
    min_value=0.0,
    max_value=20.0,
    value=3.90,
    step=0.05
)

vat_rate = st.sidebar.number_input(
    "VAT (%)",
    min_value=0.0,
    max_value=30.0,
    value=5.5,
    step=0.1
)

price_ex_vat = price_with_vat / (1 + vat_rate / 100)

# ==================================================
# 🟩 OPERATIONS
# ==================================================
st.sidebar.header("🟩 Operations")

days_per_year = st.sidebar.number_input(
    "Number of days in operation / year",
    min_value=1,
    max_value=365,
    value=322,
    step=1
)

croissants_per_day = st.sidebar.number_input(
    "Actual croissant sales quantity / day",
    min_value=0,
    max_value=5000,
    value=50,
    step=1
)

conversion_pct = st.sidebar.number_input(
    "Conversion to filled croissant / croiffle (%)",
    min_value=0.0,
    max_value=100.0,
    value=35.0,
    step=1.0
)

sku_sales_per_day = st.sidebar.number_input(
    "Number SKU sales / day (assumption)",
    min_value=0,
    max_value=5000,
    value=18,
    step=1
)

product_margin_pct = st.sidebar.number_input(
    "Product margin (%)",
    min_value=0.0,
    max_value=100.0,
    value=65.0,
    step=1.0
)

# ==================================================
# 🔒 CALCULATIONS (FEUIL 2 STRICT)
# ==================================================

converted_sku_per_day = croissants_per_day * (conversion_pct / 100)

extra_turnover_day = sku_sales_per_day * price_ex_vat
extra_turnover_year = extra_turnover_day * days_per_year

extra_margin_year = extra_turnover_year * (product_margin_pct / 100)

roi_month = (
    total_equipment / (extra_margin_year / 12)
    if extra_margin_year > 0
    else 0
)

# ==================================================
# 📊 RESULTS
# ==================================================
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
