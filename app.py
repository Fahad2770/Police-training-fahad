import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. ایپ کی بنیادی ترتیبات
st.set_page_config(
    page_title="🏗️ اسمارٹ ہوم کنسٹرکشن ڈیش بورڈ", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# خوبصورت اور پکا ڈیزائن (CSS)
st.markdown("""
    <style>
    .header-box {
        background: linear-gradient(135deg, #111827, #1f2937);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .thykidar-card {
        background-color: #fffaf0;
        padding: 20px;
        border-radius: 12px;
        border-top: 5px solid #d97706;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    </style>
""", unsafe_allow_html=True)

# 2. سیکیورٹی لاگ ان سسٹم
if "pass" in st.query_params and st.query_params["pass"] == "786":
    st.session_state.logged_in = True
else:
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

if not st.session_state.logged_in:
    placeholder = st.empty()
    with placeholder.container():
        st.title("🔐 سیکیورٹی لاگ ان")
        password = st.text_input("خفیہ پاس ورڈ لکھیں:", type="password")
        if password == "786":
            st.session_state.logged_in = True
            st.query_params["pass"] = "786"
            placeholder.empty()
            st.rerun()
        elif password != "":
            st.error("❌ درست پاسورڈ لکھیں")
            st.stop()
        else:
            st.stop()

# ڈیٹا فائل کنکشن
DB_FILE = "construction_ledger_v3.csv"
required_cols = ["Date", "Name", "type", "Quantity", "Price per unit", "Expenses", "Discount", "Paid", "باقی"]
ginti_cols = ["Quantity", "Price per unit", "Expenses", "Discount", "Paid", "باقی"]

def load_data():
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE)
            for col in required_cols:
                if col not in df.columns:
                    df[col] = 0 if col in ginti_cols else ""
            return df[required_cols]
        except:
            return pd.DataFrame(columns=required_cols)
    else:
        return pd.DataFrame(columns=required_cols)

df = load_data()

# 3. سائیڈ بار کنٹرول (سرچ، فلٹر اور فائل اپلوڈ بٹن)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #d97706;'>📥 فائل کنٹرول</h2>", unsafe_allow_html=True)
    
    # ڈائریکٹ فائل اپلوڈ کرنے کا بٹن (WPS سے تبدیل شدہ فائل کے لیے)
    uploaded_file = st.file_uploader("WPS / Excel سے بدلی ہوئی فائل اپلوڈ کریں:", type=["csv"])
    if uploaded_file is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_file)
            # کالمز چیک کرنا
            if any(col in uploaded_df.columns for col in ["Name", "Expenses", "Paid"]):
                uploaded_df.to_csv(DB_FILE, index=False)
                st.success("✅ فائل کامیابی سے اپلوڈ ہو گئی! کھاتہ اپڈیٹ کر دیا گیا ہے۔")
                st.rerun()
            else:
                st.error("فائل کے کالمز میچ نہیں ہو رہے، براہ کرم اصل فارمیٹ والی فائل اپلوڈ کریں۔")
        except Exception as e:
            st.error(f"فائل پڑھنے میں مسئلہ ہوا: {e}")
            
    st.markdown("---")
    st.markdown("### 🔍 فلٹر اور تلاش")
    search_name = st.text_input("تفصیل یا نام لکھیں:")
    
    unique_types = ["سب کیٹیگریز"] + sorted(list(df["type"].dropna().unique()))
    filter_type = st.selectbox("مخصوص کیٹیگری چنیں:", unique_types)

# ڈیٹا فلٹر کرنا
for col in ginti_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

filtered_df = df.copy()
if search_name:
    filtered_df = filtered_df[filtered_df["Name"].str.contains(search_name, case=False, na=False)]
if filter_type != "سب کیٹیگریز":
    filtered_df = filtered_df[filtered_df["type"] == filter_type]

# 4. مین ڈیش بورڈ ہیڈر
st.markdown("""
    <div class="header-box">
        <h1 style="margin:0; padding:0; font-size:32px;">🏛️ ہوم کنسٹرکشن ماسٹر ڈیش بورڈ</h1>
        <p style="margin:5px 0 0 0; opacity:0.8; font-size:16px;">آف لائن اور آن لائن سنک (Sync) کے ساتھ خودکار حساب کتاب</p>
    </div>
""", unsafe_allow_html=True)

# 5. ٹھیکیدار کے فارمولا کا مینو (Contractor Ledger Account)
st.markdown("### 👷 ٹھیکیدار کھاتہ سمری (Contractor Math)")
total_to_thykidar = df[df["type"] == "thykidar"]["Expenses"].sum()

# آپ کے دیے گئے فارمولا پیرامیٹرز
total_area_sqft = 1280
total_contract_value = 345600
actual_paid_to_thykidar = 317500 # جو آپ نے شیئر کیا
percent_paid = (actual_paid_to_thykidar / total_contract_value) * 100
budget_75_percent = total_contract_value * 0.75
savings_at_75 = budget_75_percent - actual_paid_to_thykidar

t1, t2, t3, t4 = st.columns(4)
with t1:
    st.metric("📐 کل رقبہ", f"{total_area_sqft:,} مربع فٹ")
with t2:
    st.metric("📜 کل ٹھیکہ رقم", f"{total_contract_value:,} Rs")
with t3:
    st.metric("✅ ادا شدہ (Paid)", f"{actual_paid_to_thykidar:,} Rs", f"{percent_paid:.2f}%")
with t4:
    st.metric("⚖️ 75% بجٹ پوزیشن", f"{savings_at_75:,.0f} Rs", delta_color="inverse")

st.markdown("---")

# 6. جنرل فائنینشل کارڈز
total_paid = df["Paid"].sum()
total_spent = df["Expenses"].sum()
balance_Now = df["باقی"].iloc[-1] if not df.empty else 0.0

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("💰 کل جمع فنڈ (Total Paid)", f"{total_paid:,.1f} Rs")
with c2:
    st.metric("📉 کل تعمیری خرچ (Total Expenses)", f"{total_spent:,.1f} Rs")
with c3:
    st.metric("⚖️ نیٹ بیلنس پوزیشن (باقی رقم)", f"{balance_Now:,.1f} Rs")

st.markdown("---")

# 7. گراف کا سیکشن
if not df.empty and total_spent > 0:
    st.markdown("### 📊 اخراجات کا گرافکل تجزیہ")
    chart_data = df[df["Expenses"] > 0].groupby("type")["Expenses"].sum().reset_index()
    
    g1, g2 = st.columns(2)
    with g1:
        fig_pie = px.pie(
            chart_data, values="Expenses", names="type", 
            title="🎯 کس کیٹیگری پر کتنے فیصد خرچ ہوا؟", hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    with g2:
        fig_bar = px.bar(
            chart_data.sort_values(by="Expenses", ascending=False), 
            x="type", y="Expenses", title="📊 تعمیری مٹیریل کا کل بجٹ گراف",
            color="type", color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# 8. نئی انٹری کا فارم
with st.expander("➕ نئی تعمیری انٹری یا فنڈز شامل کریں", expanded=False):
    with st.form("entry_form", clear_on_submit=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            date = st.text_input("تاریخ (مثال: 25-Dec)")
        with f2:
            name = st.text_input("تفصیل / نام")
        with f3:
            category = st.selectbox("کیٹیگری (type)", [
                "thykidar", "cement", "ent", "rait", "linter", "mazdori", 
                "M.F Rana", "living items", "helping items", "elec", "gate doors", 
                "water", "rent", "Bhai Aamir", "DPC", "slap", "parrchhati", "khirat", "bhart", "personal", "ڈیگر"
            ])
            
        f4, f5, f6 = st.columns(3)
        with f4:
            quantity = st.number_input("تعداد (Quantity)", min_value=0.0, step=1.0, value=1.0)
        with f5:
            price_per_unit = st.number_input("فی عدد ریٹ (Price per unit)", min_value=0.0, step=10.0)
        with f6:
            expenses = st.number_input("کل خرچ (Expenses)", min_value=0.0, step=100.0)
            
        f7, f8 = st.columns(2)
        with f7:
            discount = st.number_input("ڈسکاؤنٹ (Discount)", min_value=0.0, step=5.0)
        with f8:
            paid = st.number_input("جمع کروائی گئی رقم (Paid)", min_value=0.0, step=1000.0)

        submit = st.form_submit_button("⚡ کھاتے میں محفوظ کریں")

        if submit:
            if expenses == 0.0 and quantity > 0 and price_per_unit > 0:
                expenses = quantity * price_per_unit
                
            new_balance = balance_Now + paid - expenses

            new_row = {
                "Date": date, "Name": name, "type": category, 
                "Quantity": quantity, "Price per unit": price_per_unit, 
                "Expenses": expenses, "Discount": discount, "Paid": paid, "باقی": new_balance
            }
            
            df_new = pd.DataFrame([new_row])
            df = pd.concat([df, df_new], ignore_index=True)[required_cols]
            df.to_csv(DB_FILE, index=False)
            st.success("✅ انٹری کامیابی سے محفوظ ہو گئی!")
            st.rerun()

# 9. ریکارڈز کا ڈیٹا ٹیبل
st.markdown("### 📋 تعمیری ریکارڈ اور لیجر شیٹ")
if not filtered_df.empty:
    st.dataframe(filtered_df.iloc[::-1], use_container_width=True) 

    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 پورا اصل کھاتہ بیک اپ ڈاؤن لوڈ کریں (CSV)",
        data=csv_data,
        file_name="home_construction_master.csv",
        mime="text/csv"
    )
else:
    st.info("کوئی ریکارڈ نہیں ملا۔")