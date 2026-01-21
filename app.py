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
    price = col1.number_input(
        f"{label} – unit price (€)",
        min_value=0.0,
        max_value=10000.0,
        value=default_price,
        step=10.0
    )
    qty = col2.number_input(
        f"{label} – qty",
        min_value=0,
        max_value=10,
        value=default_qty,
        step=1
    )
    return price * qty

injector = capex_line("Injector", 798.0, 3)
base = capex_line("Base", 284.0, 1)
waffle = capex_line("Waffle iron (croiffle + Eiffel Tower)", 1000.0, 1)
transport = capex_line("Transport", 600.0, 1)

total_equipment = injector + base + waffle + transport

# CAPEX breakdown (CALCULATED)
st.sidebar.markdown("### 🧾 CAPEX breakdown (calculated)")
st.sidebar.write(f"Injector total: €{injector:,.0f}")
st.sidebar.write(f"Base total: €{base:,.0f}")
st.sidebar.write(f"Waffle iron total: €{waffle:,.0f}")
st.sidebar.write(f"Transport total: €{transport:,.0f}")

# ==================================================
# 🟩 SALES (VARIABLES)
#
