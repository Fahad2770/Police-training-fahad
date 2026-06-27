import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ایپ کی سیٹنگز
st.set_page_config(page_title="🏗️ ہوم کنسٹرکشن کھاتہ", layout="wide")

# پاس ورڈ لاگ ان سسٹم
st.sidebar.title("🔐 سیکیورٹی لاگ ان")
password = st.sidebar.text_input("خفیہ پاس ورڈ لکھیں:", type="password")

# اپنا مرضی کا پاس ورڈ یہاں سیٹ کریں (جیسے 1234 یا کچھ بھی)
if password != "786":
    st.warning("براہ کرم ایپ استعمال کرنے کے لیے بائیں طرف (Sidebar) صحیح پاس ورڈ درج کریں۔")
    st.stop()

# ڈیٹا فائل کا نام
DB_FILE = "construction_ledger_v3.csv"

# ڈیٹا لوڈ کرنے کا فنکشن
def load_data():
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE)
            # کالمز کی اسپیلنگ اور ترتیب پکی کرنا
            required_cols = ["تاریخ", "تفصیل", "کیٹیگری", "اخراجات", "ڈسکاؤنٹ", "جمع رقم"]
            for col in required_cols:
                if col not in df.columns:
                    df[col] = 0 if col in ["اخراجات", "ڈسکاؤنٹ", "جمع رقم"] else ""
            return df[required_cols]
        except:
            return pd.DataFrame(columns=["تاریخ", "تفصیل", "کیٹیگری", "اخراجات", "ڈسکاؤنٹ", "جمع رقم"])
    else:
        return pd.DataFrame(columns=["تاریخ", "تفصیل", "کیٹیگری", "اخراجات", "ڈسکاؤنٹ", "جمع رقم"])

df = load_data()

# ڈیٹا کو نمبرز میں تبدیل کرنا تاکہ حساب صحیح ہو
df["اخراجات"] = pd.to_numeric(df["اخراجات"], errors='coerce').fillna(0)
df["ڈسکاؤنٹ"] = pd.to_numeric(df["ڈسکاؤنٹ"], errors='coerce').fillna(0)
df["جمع رقم"] = pd.to_numeric(df["جمع رقم"], errors='coerce').fillna(0)

# مین ٹائٹل
st.title("🏗️ ہوم کنسٹرکشن کھاتہ دیش بورڈ")

# کارڈز (حساب کتاب کے ڈبے)
total_paid = df["جمع رقم"].sum()
total_spent = df["اخراجات"].sum()
total_discount = df["ڈسکاؤنٹ"].sum()
balance = total_paid - total_spent + total_discount

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 کل جمع (Paid)", f"{total_paid:,.1f} Rs")
col2.metric("📉 کل خرچ (Spent)", f"{total_spent:,.1f} Rs")
col3.metric("🎁 کل رعایت (Discount)", f"{total_discount:,.1f} Rs")
col4.metric("⚖️ الباقی رقم (Balance)", f"{balance:,.1f} Rs", delta_color="inverse")

st.markdown("---")

# گراف کا سیکشن
if not df.empty and total_spent > 0:
    st.subheader("📊 اخراجات کا گراف اور تجزیہ")
    
    # کیٹیگری کے حساب سے خرچہ جمع کرنا
    chart_data = df[df["اخراجات"] > 0].groupby("کیٹیگری")["اخراجات"].sum().reset_index()
    
    g1, g2 = st.columns(2)
    with g1:
        fig_pie = px.pie(chart_data, values="اخراجات", names="کیٹیگری", title="خرچے کی تقسیم (فیصد میں)", hole=0.3)
        st.plotly_chart(fig_pie, use_container_width=True)
    with g2:
        fig_bar = px.bar(chart_data, x="کیٹیگری", y="اخراجات", title="کس چیز پر کتنا خرچ ہوا؟", color="کیٹیگری")
        st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# نئی انٹری کا فارم
with st.expander("➕ نئی انٹری شامل کریں", expanded=False):
    with st.form("entry_form", clear_on_submit=True):
        date = st.text_input("تاریخ (مثال: 25-Dec)")
        name = st.text_input("تفصیل / نام")
        category = st.selectbox("کیٹیگری", [
            "thykidar", "cement", "ent", "rait", "linter", "mazdori", 
            "M.F Rana", "living items", "helping items", "elec", "gate", "water", "rent", "ڈیگر"
        ])
        expenses = st.number_input("اخراجات", min_value=0.0, step=100.0)
        discount = st.number_input("رعایت / ڈسکاؤنٹ", min_value=0.0, step=5.0)
        paid = st.number_input("جمع رقم", min_value=0.0, step=1000.0)
        
        submit = st.form_submit_button("کھاتے میں لکھیں")
        
        if submit:
            new_row = {"تاریخ": date, "تفصیل": name, "کیٹیگری": category, "اخراجات": expenses, "ڈسکاؤنٹ": discount, "جمع رقم": paid}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success(" انٹری کامیابی سے محفوظ ہو گئی!")
            st.rerun()

# موجودہ ریکارڈ کا ٹیبل
st.subheader("📋 موجودہ ریکارڈ")
if not df.empty:
    st.dataframe(df.iloc[::-1], use_container_width=True) # تازہ ترین انٹری سب سے اوپر دکھانے کے لیے
    
    # ڈیٹا ڈاؤن لوڈ کرنے کا بٹن
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 پورا کھاتہ موبائل میں ڈاؤن لوڈ کریں (CSV)",
        data=csv_data,
        file_name="home_construction_backup.csv",
        mime="text/csv"
    )
else:
    st.info("کھاتہ فی الحال خالی ہے۔")