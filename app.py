import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="میرا گھر کھاتہ", page_icon="🏗️", layout="centered")
st.title("🏗️ ہوم کنسٹرکشن کھاتہ")

DB_FILE = "construction_ledger.csv"

if not os.path.exists(DB_FILE):
    initial_df = pd.DataFrame(columns=["تاریخ", "تفصیل", "کیٹیگری", "اخراجات", "ڈسکاؤنٹ", "جمع رقم"])
    initial_df.to_csv(DB_FILE, index=False)

df = pd.read_csv(DB_FILE)

with st.expander("➕ نئی انٹری شامل کریں", expanded=False):
    with st.form("entry_form", clear_on_submit=True):
        date = st.text_input("تاریخ (مثال: 25-Dec)")
        name = st.text_input("تفصیل / نام")
        category = st.selectbox("کیٹیگری", ["thykidar", "cement", "ent", "rait", "linter", "mazdori", "M.F Rana", "living items", "helping items", "دیگر"])
        expenses = st.number_input("اخراجات", min_value=0.0, step=100.0)
        discount = st.number_input("رعایت", min_value=0.0, step=5.0)
        paid = st.number_input("جمع رقم", min_value=0.0, step=1000.0)
        submit = st.form_submit_with_button("کھاتے میں لکھیں")
        if submit:
            new_row = {"تاریخ": date, "تفصیل": name, "کیٹیگری": category, "اخراجات": expenses, "ڈسکاؤنٹ": discount, "جمع رقم": paid}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("انٹری کامیابی سے محفوظ ہو گئی!")
            st.rerun()

df["جمع رقم"] = pd.to_numeric(df["جمع رقم"], errors='coerce').fillna(0)
df["اخراجات"] = pd.to_numeric(df["اخراجات"], errors='coerce').fillna(0)
df["ڈسکاؤنٹ"] = pd.to_numeric(df["ڈسکاؤنٹ"], errors='coerce').fillna(0)

total_paid = df["جمع رقم"].sum()
total_expenses = df["اخراجات"].sum()

balance = 0
balances = []
for idx, row in df.iterrows():
    balance = balance + row["جمع رقم"] - row["اخراجات"] + row["ڈسکاؤنٹ"]
    balances.append(balance)
df["الباقی (Balance)"] = balances

col1, col2, col3 = st.columns(3)
col1.metric("کل جمع (Paid)", f"{total_paid:,.1f} Rs")
col2.metric("کل خرچ (Spent)", f"{total_expenses:,.1f} Rs")
col3.metric("الباقی (Balance)", f"{balance:,.1f} Rs")

st.markdown("---")
st.subheader("📋 موجودہ ریکارڈ")
st.dataframe(df, use_container_width=True)
