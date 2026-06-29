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
raw_data = "construction_ledger_v3.csv"
# DataFrame banana (Taake calculations asan hon)
df = pd.DataFrame(raw_data)

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
with tab1: # Python rules ke mutabiq hum tab2 ka content idhar likhein ge
    pass 

with tab2:
    st.subheader("👷 ٹھیکیدار کی مخصوص تفصیل (Contractor Math)")
    
    # Thykidar ki alag calculations dikhana
    thykidar_paid = df[df["Type"] == "thykidar"]["Expenses"].sum()
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
        # 2. Pie Chart: Expenses Breakdown by Type
        expense_df = df[df["Expenses"] > 0].groupby("Type")["Expenses"].sum().reset_index()
        fig_pie = px.pie(expense_df, values='Expenses', names='Type', title="اخراجات کہاں کتنے فیصد ہوئے؟", hole=0.3)
        st.plotly_chart(fig_pie, use_container_width=True)
