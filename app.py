import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration (App ki buniyaad)
st.set_page_config(
    page_title="🏗️ Home Construction Dashboard",
    layout="wide"
)

# App ka Title
st.title("🏛️ اسمارٹ ہوم کنسٹرکشن ڈیش بورڈ")
st.markdown("---")

# 2. DATA INPUT (Aap ka sara data hum yahan direct code mein shamil kar rahe hain)
# Thykidar ki summary ka data
thykidar_stats = {
    "total_area": 1280,
    "total_contract": 345600,
    "paid_percentage": 91.87,
    "savings_at_75": -58300
}

# Date-wise construction list ka data
# FIXED: Load CSV file properly using pd.read_csv instead of passing string to pd.DataFrame
try:
    df = pd.read_csv("construction_ledger_v3.csv")
except FileNotFoundError:
    st.error("❌ Error: construction_ledger_v3.csv file not found!")
    st.stop()

# Automatic Running Balance ('باقی') calculate karna
running_balance = []
current_bal = 0
for index, row in df.iterrows():
    current_bal = current_bal + row['Paid'] - row['Expenses']
    running_balance.append(current_bal)
df['باقی'] = running_balance

# Totals nikalna
total_paid = df["Paid"].sum()
total_expenses = df["Expenses"].sum()
remaining_balance = current_bal


# 3. TWO DASHBOARDS (TABS) CREATION
tab1, tab2 = st.tabs(["📋 کھاتہ لسٹ اور سمری (Dashboard 1)", "📊 گراف اور ٹھیکیدار تفصیل (Dashboard 2)"])

# ==========================================
# DASHBOARD 1: List aur Total Paise
# ==========================================
with tab1:
    st.subheader("💰 مالیاتی سمری (Financial Summary)")
    
    # Khas headings (Metrics)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="جتنے پیسے دیے (Total Paid)", value=f"{total_paid:,} Rs")
    with col2:
        st.metric(label="جو خرچہ ہو گئے (Total Expenses)", value=f"{total_expenses:,} Rs")
    with col3:
        st.metric(label="جو باقی ہیں (Net Balance)", value=f"{remaining_balance:,} Rs")
        
    st.markdown("---")
    st.subheader("📋 تمام تعمیری ریکارڈ کی لسٹ (Ledger List)")
    
    # Poori list Table ki surat mein dikhana
    st.dataframe(df, use_container_width=True)


# ==========================================
# DASHBOARD 2: Graphs aur Thykidar Detail
# ==========================================
with tab2:
    st.subheader("👷 ٹھیکیدار کی مخصوص تفصیل (Contractor Math)")
    
    # FIXED: Changed "Type" to "type" (lowercase - sahi column name)
    thykidar_paid = df[df["type"] == "thykidar"]["Expenses"].sum()
    thykidar_remaining = thykidar_stats["total_contract"] - thykidar_paid
    
    t_col1, t_col2, t_col3 = st.columns(3)
    with t_col1:
        st.write(f"📐 **کل رقبہ:** {thykidar_stats['total_area']} مربع فٹ")
        st.write(f"📜 **کل ٹھیکہ رقم:** {thykidar_stats['total_contract']:,} Rs")
    with t_col2:
        st.write(f"✅ **ٹھیکیدار کو ادا کیے:** {thykidar_paid:,} Rs")
        st.write(f"📊 **فیصد ادائیگی:** {thykidar_stats['paid_percentage']}%")
    with t_col3:
        st.write(f"⚖️ **75% میں بچت/پوزیشن:** {thykidar_stats['savings_at_75']:,} Rs")
        st.write(f"🔴 **ٹھیکیدار کے باقی پیسے:** {thykidar_remaining:,} Rs")

    st.markdown("---")
    st.subheader("📊 تعمیری گراف (Visual Analytics)")
    
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        # 1. Bar Chart: Expenses vs Paid vs Remaining
        chart_data = pd.DataFrame({
            'Category': ['Total Paid', 'Total Expenses', 'Remaining'],
            'Amount (Rs)': [total_paid, total_expenses, remaining_balance]
        })
        fig_bar = px.bar(chart_data, x='Category', y='Amount (Rs)', title="کل فنڈز بمقابلہ اخراجات", color='Category')
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with g_col2:
        # 2. Pie Chart: Expenses Breakdown by Type (FIXED: Thykidar ko exclude kiya)
        # FIXED: صرف M.F Rana اور Bhai Aamir کی expenses دکھانا
        expense_df = df[(df["Expenses"] > 0) & (df["type"] != "thykidar")].groupby("type")["Expenses"].sum().reset_index()
        
        if len(expense_df) > 0:
            fig_pie = px.pie(expense_df, values='Expenses', names='type', title="اخراجات کہاں کتنے فیصد ہوئے؟ (Thykidar شامل نہیں)", hole=0.3)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("⚠️ اخراجات کی معلومات دستیاب نہیں")
