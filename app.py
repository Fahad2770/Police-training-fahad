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
raw_data = [
    {"Date": "3-Oct", "Name": "cement coy", "Type": "Bhai Aamir", "Quantity": 0, "Price": 0, "Expenses": 0, "Discount": 0, "Paid": 100000},
    {"Date": "2-Oct", "Name": "advance satilement", "Type": "thykidar", "Quantity": 1, "Price": 25000, "Expenses": 25000, "Discount": 0, "Paid": 0},
    {"Date": "", "Name": "روڑے ایروں کیلئے", "Type": "ent", "Quantity": 1, "Price": 11000, "Expenses": 11000, "Discount": 0, "Paid": 0},
    {"Date": "", "Name": "روڑے کٹائی", "Type": "mazdori", "Quantity": 1, "Price": 1900, "Expenses": 1900, "Discount": 0, "Paid": 0},
    {"Date": "", "Name": "ریت ٹرالی", "Type": "rait", "Quantity": 1, "Price": 7300, "Expenses": 7300, "Discount": 0, "Paid": 0},
    {"Date": "", "Name": "سیمنٹ 20 عدد", "Type": "cement", "Quantity": 20, "Price": 1380, "Expenses": 27600, "Discount": 0, "Paid": 0},
    {"Date": "", "Name": "پانی کا پائپ", "Type": "helping items", "Quantity": 1, "Price": 1500, "Expenses": 1500, "Discount": 0, "Paid": 0},
    {"Date": "", "Name": "اینٹ کی ٹرالی", "Type": "ent", "Quantity": 1, "Price": 44200, "Expenses": 44200, "Discount": 0, "Paid": 0},
    {"Date": "15-Oct", "Name": "سیمنٹ کمپنی", "Type": "Bhai Aamir", "Quantity": 0, "Price": 0, "Expenses": 0, "Discount": 0, "Paid": 100000},
    {"Date": "16-Oct", "Name": "تھکیدر کو دیئے", "Type": "thykidar", "Quantity": 1, "Price": 14000, "Expenses": 14000, "Discount": 0, "Paid": 0},
    {"Date": "20-Oct", "Name": "ٹھیکیدار کو دیئے", "Type": "thykidar", "Quantity": 1, "Price": 10000, "Expenses": 10000, "Discount": 0, "Paid": 0},
    {"Date": "", "Name": "اینٹ کی ٹرالي", "Type": "ent", "Quantity": 1, "Price": 45000, "Expenses": 45000, "Discount": 0, "Paid": 0},
    {"Date": "23-Oct", "Name": "سیمنٹ کمپنی", "Type": "Bhai Aamir", "Quantity": 0, "Price": 0, "Expenses": 0, "Discount": 0, "Paid": 100000},
    {"Date": "", "Name": "ریت ٹرالی", "Type": "rait", "Quantity": 1, "Price": 7500, "Expenses": 7500, "Discount": 0, "Paid": 0},
    {"Date": "", "Name": "اینٹ کی ٹرالی", "Type": "ent", "Quantity": 1, "Price": 44500, "Expenses": 44500, "Discount": 0, "Paid": 0},
    {"Date": "", "Name": "موٹر سیکنڈ ہینڈ", "Type": "living items", "Quantity": 1, "Price": 8500, "Expenses": 8500, "Discount": 0, "Paid": 0},
    {"Date": "", "Name": "بجری، سریہ، سیمنٹ", "Type": "DPC", "Quantity": 1, "Price": 31300, "Expenses": 31300, "Discount": 0, "Paid": 0},
    {"Date": "", "Name": "فوٹو کاپی گیس، بجلی میٹر", "Type": "living items", "Quantity": 1, "Price": 2000, "Expenses": 2000, "Discount": 0, "Paid": 0},
    {"Date": "23-Oct", "Name": "ٹھیکیدار کو دیئے", "Type": "thykidar", "Quantity": 1, "Price": 26000, "Expenses": 26000, "Discount": 0, "Paid": 0},
    {"Date": "27-Oct", "Name": "ٹھیکیدار کو دیئے", "Type": "thykidar", "Quantity": 1, "Price": 15000, "Expenses": 15000, "Discount": 0, "Paid": 0},
    {"Date": "5-Nov", "Name": "misbah account", "Type": "M.F Rana", "Quantity": 0, "Price": 0, "Expenses": 0, "Discount": 0, "Paid": 100000},
    {"Date": "19-Nov", "Name": "misbah account", "Type": "M.F Rana", "Quantity": 0, "Price": 0, "Expenses": 0, "Discount": 0, "Paid": 100000},
    {"Date": "29-Nov-26", "Name": "ٹھیکیدار کو دیئے", "Type": "thykidar", "Quantity": 1, "Price": 4000, "Expenses": 4000, "Discount": 0, "Paid": 0},
    {"Date": "10-Dec", "Name": "misbah account", "Type": "M.F Rana", "Quantity": 0, "Price": 0, "Expenses": 0, "Discount": 0, "Paid": 193000},
    {"Date": "", "Name": "bhart waly ko diye", "Type": "bhart", "Quantity": 1, "Price": 70000, "Expenses": 70000, "Discount": 0, "Paid": 0},
    {"Date": "", "Name": "ento ki trali", "Type": "ent", "Quantity": 1, "Price": 45000, "Expenses": 45000, "Discount": 0, "Paid": 0},
    {"Date": "", "Name": "kam walo ko diye", "Type": "mazdori", "Quantity": 1, "Price": 1000, "Expenses": 1000, "Discount": 0, "Paid": 0},
    {"Date": "", "Name": "ryyt trali", "Type": "rait", "Quantity": 1, "Price": 7500, "Expenses": 7500, "Discount": 0, "Paid": 0},
    {"Date": "10-Dec", "Name": "سیمنٹ میپل لیف", "Type": "cement", "Quantity": 20, "Price": 1450, "Expenses": 29000, "Discount": 0, "Paid": 0},
    {"Date": "11-Dec", "Name": "x3 اینٹ کی ٹرالی", "Type": "ent", "Quantity": 3, "Price": 45000, "Expenses": 135000, "Discount": 0, "Paid": 0},
    {"Date": "11-Dec", "Name": "کرایہ 3 ٹرالیوں کا", "Type": "rent", "Quantity": 1, "Price": 600, "Expenses": 600, "Discount": 0, "Paid": 0},
    {"Date": "", "Name": "ریت چھنوائی", "Type": "mazdori", "Quantity": 1, "Price": 100, "Expenses": 100, "Discount": 0, "Paid": 0},
    {"Date": "13-Dec", "Name": "ٹھیکیدار کو دیئے", "Type": "thykidar", "Quantity": 1, "Price": 12000, "Expenses": 12000, "Discount": 0, "Paid": 0},
    {"Date": "13-Dec", "Name": "ٹھیکیدار کو دیئے", "Type": "thykidar", "Quantity": 1, "Price": 15000, "Expenses": 15000, "Discount": 0, "Paid": 0},
    {"Date": "13-Dec", "Name": "ٹھیکیدار کو سینٹ کیئے", "Type": "M.F Rana", "Quantity": 0, "Price": 0, "Expenses": 0, "Discount": 0, "Paid": 15000},
    {"Date": "15-Dec", "Name": "ٹھیکیدار کو دیئے", "Type": "thykidar", "Quantity": 1, "Price": 5000, "Expenses": 5000, "Discount": 0, "Paid": 0},
    {"Date": "16-Dec", "Name": "misbah account", "Type": "M.F Rana", "Quantity": 0, "Price": 0, "Expenses": 0, "Discount": 0, "Paid": 100000},
    {"Date": "17-Dec", "Name": "چوکھٹ", "Type": "gate doors", "Quantity": 1, "Price": 25000, "Expenses": 25000, "Discount": 0, "Paid": 0}
]

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
