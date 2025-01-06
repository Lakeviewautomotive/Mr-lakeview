import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize data (replace with a database or file system later)
if "logs" not in st.session_state:
    st.session_state["logs"] = []

# App title
st.title("Lakeview Automotive: Technician and Payroll Tracker")

# Sidebar for navigation
st.sidebar.title("Navigation")
options = ["Technician Logging", "Payroll Summary", "Service Advisor Dashboard"]
choice = st.sidebar.radio("Go to:", options)

# Technician Logging Interface
if choice == "Technician Logging":
    st.header("Technician Logging")
    with st.form("log_form"):
        technician = st.selectbox("Technician Name", ["Adam C", "Sam G", "Lei V", "Will H", "Johnathan D"])
        ro_number = st.text_input("Repair Order (RO) Number")
        task_type = st.selectbox("Task Type", ["Regular Work", "Butter-Up Work", "In-House Build", "Personal Vehicle", "Non-Billable"])
        time_billed_customer = st.number_input("Time Billed to Customer (hrs)", min_value=0.0, step=0.5)
        time_billed_lakeview = st.number_input("Time Billed to Lakeview (hrs)", min_value=0.0, step=0.5)
        notes = st.text_area("Notes (optional)")
        date = st.date_input("Date", value=datetime.now().date())

        submitted = st.form_submit_button("Log Task")
        if submitted:
            st.session_state["logs"].append({
                "Technician": technician,
                "RO Number": ro_number,
                "Task Type": task_type,
                "Time Billed to Customer (hrs)": time_billed_customer,
                "Time Billed to Lakeview (hrs)": time_billed_lakeview,
                "Notes": notes,
                "Date": str(date)
            })
            st.success("Task logged successfully!")

    # Display current logs
    st.subheader("Logged Tasks")
    if st.session_state["logs"]:
        logs_df = pd.DataFrame(st.session_state["logs"])
        st.dataframe(logs_df)
    else:
        st.write("No tasks logged yet.")

# Payroll Summary
elif choice == "Payroll Summary":
    st.header("Payroll Summary")
    st.write("Summarize technician hours by payroll period.")
    
    if st.session_state["logs"]:
        logs_df = pd.DataFrame(st.session_state["logs"])
        start_date = st.date_input("Start Date", value=datetime.now().date())
        end_date = st.date_input("End Date", value=datetime.now().date())
        
        if start_date > end_date:
            st.warning("Start date cannot be after the end date.")
        else:
            filtered_logs = logs_df[
                (pd.to_datetime(logs_df["Date"]) >= pd.to_datetime(start_date)) &
                (pd.to_datetime(logs_df["Date"]) <= pd.to_datetime(end_date))
            ]
            summary = filtered_logs.groupby("Technician")[
                ["Time Billed to Customer (hrs)", "Time Billed to Lakeview (hrs)"]
            ].sum().reset_index()
            st.dataframe(summary)
    else:
        st.write("No data available for payroll summaries.")

# Service Advisor Dashboard
elif choice == "Service Advisor Dashboard":
    st.header("Service Advisor Dashboard")
    if st.session_state["logs"]:
        logs_df = pd.DataFrame(st.session_state["logs"])
        ro_summary = logs_df.groupby("RO Number")[
            ["Time Billed to Customer (hrs)", "Time Billed to Lakeview (hrs)"]
        ].sum().reset_index()
        st.dataframe(ro_summary)
    else:
        st.write("No tasks logged yet.")
