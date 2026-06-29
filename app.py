import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. ایپ کی بنیادی سیٹنگز اور تھیم ٹچ
st.set_page_config(
    page_title="🏗️ اسمارٹ ہوم کنسٹرکشن ڈیش بورڈ", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# خوبصورت کسٹم سٹائلنگ (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #2e7d32;
    }
    div[data-testid="stExpander"] {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    </style>
""", unsafe_allow_html=True)

# 2. سیکیورٹی لاگ ان لاک سسٹم
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

# ڈیٹا کو نمبرز میں درست تبدیل کرنا
for col in ginti_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# 3. سائیڈ بار مینو اور نیویگیشن (جدید لک کیلئے)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #2e7d32;'>🏗️ مینو کنٹرول</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # سرچ اور فلٹر کی سہولت
    st.markdown("### 🔍 ریکارڈ فلٹر کریں")
    search_name = st.text_input("نام یا تفصیل سے سرچ کریں:")
    
    unique_types = ["سب کیٹیگریز"] + sorted(list(df["type"].dropna().unique()))
    filter_type = st.selectbox("مخصوص کیٹیگری منتخب کریں:", unique_types)

# فلٹر لاگو کرنا
filtered_df = df.copy()
if search_name:
    filtered_df = filtered_df[filtered_df["Name"].str.contains(search_name, case=False, na=False)]
if filter_type != "سب کیٹیگریز":
    filtered_df = filtered_df[filtered_df["type"] == filter_type]

# 4. مین ڈیش بورڈ ہیڈر
st.markdown("<h1 style='text-align: center; color: #1b5e20;'>🏛️ ہوم کنسٹرکشن اسمارٹ کھاتہ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>تعمیراتی اخراجات اور حساب کتاب کا جدید نظام</p>", unsafe_allow_html=True)
st.markdown("---")

# 5. خوبصورت فائنینشل کارڈز (Metrics)
total_paid = df["Paid"].sum()
total_spent = df["Expenses"].sum()
balance_Now = df["باقی"].iloc[-1] if not df.empty else 0.0

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("💰 کل جمع فنڈ (Total Paid)", f"{total_paid:,.0f} Rs")
with c2:
    st.metric("📉 کل تعمیری خرچ (Total Expenses)", f"{total_spent:,.0f} Rs")
with c3:
    # اگر باقی رقم منفی میں ہو تو لال رنگ کا الرٹ تاثر دینے کیلئے کسٹمائزڈ بھی کر سکتے ہیں
    st.metric("⚖️ نیٹ بیلنس پوزیشن (باقی)", f"{balance_Now:,.0f} Rs")

st.markdown("---")

# 6. گراف اور اینالیٹکس (خوبصورت رنگوں کے ساتھ)
if not df.empty and total_spent > 0:
    st.markdown("### 📊 اخراجات کا گراف اور گہرائی سے تجزیہ")
    chart_data = df[df["Expenses"] > 0].groupby("type")["Expenses"].sum().reset_index()
    
    g1, g2 = st.columns(2)
    with g1:
        fig_pie = px.pie(
            chart_data, values="Expenses", names="type", 
            title="🎯 اخراجات کی فیصد تقسیم", hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Dark24
        )
        fig_pie.update_layout(margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig_pie, use_container_width=True)
    with g2:
        fig_bar = px.bar(
            chart_data.sort_values(by="Expenses", ascending=False), 
            x="type", y="Expenses", title="📊 کس چیز پر کتنا بجٹ لگا؟",
            color="type", color_discrete_sequence=px.colors.qualitative.Dark24
        )
        fig_bar.update_layout(showlegend=False, margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# 7. نئی انٹری شامل کرنے کا جدید فارم
with st.expander("➕ نئی تعمیری انٹری یا فنڈز شامل کریں", expanded=False):
    with st.form("entry_form", clear_on_submit=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            date = st.text_input("تاریخ (مثال: 25-Dec)")
        with f2:
            name = st.text_input("تفصیل / نام / دکان کا نام")
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
            expenses = st.number_input("کل خرچ (Expenses) - [اگر تعداد 1 ہے تو یہاں لکھیں]", min_value=0.0, step=100.0)
            
        f7, f8 = st.columns(2)
        with f7:
            discount = st.number_input("ڈسکاؤنٹ (Discount)", min_value=0.0, step=5.0)
        with f8:
            paid = st.number_input("جمع کروائی گئی رقم (Paid) - [اگر فنڈ آیا ہے]", min_value=0.0, step=1000.0)

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
            st.success("✅ انٹری کامیابی سے نئے ڈیزائن کھاتے میں درج ہو گئی!")
            st.rerun()

# 8. موجودہ ریکارڈ اور ڈاؤن لوڈ سسٹم
st.markdown("### 📋 تعمیری ریکارڈ اور لیجر شیٹ")
if not filtered_df.empty:
    # انٹریز کو الٹا کر کے دکھانا تاکہ نئی اوپر آئے
    st.dataframe(filtered_df.iloc[::-1], use_container_width=True) 

    # خوبصورت ڈاؤن لوڈ بٹن سائیڈ پر
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 پورا اصل کھاتہ بیک اپ ڈاؤن لوڈ کریں (CSV)",
        data=csv_data,
        file_name="home_construction_master.csv",
        mime="text/csv"
    )
else:
    st.info("آپ کے فلٹر کے مطابق کوئی ریکارڈ نہیں ملا یا کھاتہ خالی ہے۔")
