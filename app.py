import streamlit as st

st.set_page_config(page_title="Bar à Croissant – ROI Simulator", layout="wide")

st.title("🥐 Bar à Croissant – ROI Simulator (Realistic Model)")

st.markdown("This simulator is designed for **real operational decision-making**, not investor hype.")

# ------------------------
# SIDEBAR – INPUTS
# ------------------------
st.sidebar.header("📊 Business Inputs")

price = st.sidebar.number_input("Selling price per croissant (€)", 1.0, 10.0, 3.0, 0.1)
daily_volume = st.sidebar.number_input("Average croissants sold per day", 10, 2000, 300, 10)
days_open = st.sidebar.number_input("Days open per month", 1, 31, 26)

variable_cost = st.sidebar.number_input("Variable cost per croissant (€)", 0.1, 5.0, 0.8, 0.05)

st.sidebar.subheader("👩‍🍳 Staff costs")
staff_count = st.sidebar.number_input("Number of staff", 0, 10, 2)
hourly_rate = st.sidebar.number_input("Hourly rate per staff (€)", 8.0, 30.0, 14.0, 0.5)
hours_per_month = st.sidebar.number_input("Hours per staff per month", 20, 300, 160, 10)

st.sidebar.subheader("🏢 Fixed costs")
rent = st.sidebar.number_input("Monthly rent (€)", 0, 20000, 3500, 100)
other_costs = st.sidebar.number_input("Other fixed monthly costs (€)", 0, 10000, 1200, 100)

st.sidebar.subheader("⚠️ Stress test")
stress = st.sidebar.selectbox(
    "Scenario",
    ["None", "-10% volume", "+10% costs", "Combined shock"]
)

# ------------------------
# CALCULATIONS
# ------------------------
monthly_volume = daily_volume * days_open
revenue = monthly_volume * price
variable_costs = monthly_volume * variable_cost

staff_costs = staff_count * hourly_rate * hours_per_month

fixed_costs = rent + other_costs + staff_costs
total_costs = fixed_costs + variable_costs

if stress == "-10% volume":
    revenue *= 0.9
    variable_costs *= 0.9
elif stress == "+10% costs":
    fixed_costs *= 1.1
    variable_costs *= 1.1
elif stress == "Combined shock":
    revenue *= 0.9
    fixed_costs *= 1.1
    variable_costs *= 1.1

total_costs = fixed_costs + variable_costs
profit = revenue - total_costs
annual_profit = profit * 12

initial_investment = 60000
roi = (annual_profit / initial_investment) * 100 if initial_investment > 0 else 0

if profit > 0:
    breakeven_months = initial_investment / profit
else:
    breakeven_months = None

# ------------------------
# OUTPUT
# ------------------------
st.header("📈 Results")

col1, col2, col3 = st.columns(3)

col1.metric("Monthly Revenue (€)", f"{revenue:,.0f}")
col2.metric("Monthly Profit (€)", f"{profit:,.0f}")
col3.metric("Annual Profit (€)", f"{annual_profit:,.0f}")

st.divider()

if profit > 3000:
    st.success("🟢 VIABLE — solid operational margin")
elif profit > 0:
    st.warning("🟠 FRAGILE — viable but sensitive to shocks")
else:
    st.error("🔴 NOT VIABLE — structural loss")

if breakeven_months:
    st.info(f"⏳ Break-even in approximately **{breakeven_months:.1f} months**")
else:
    st.info("❌ No break-even achievable with current assumptions")
