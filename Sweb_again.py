import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interact, widgets
from flask import Flask, render_template
import os
import plotly.graph_objects as go
import streamlit as st

# -------------------------------
# 🎯 Sidebar: Upload & Parameters
# -------------------------------

st.sidebar.title("Parameter Penilaian")

uploaded_file = st.sidebar.file_uploader("Pilih file CSV kandidat", type=["csv"])

# Logical Thinking
st.sidebar.subheader("Logical Thinking")
w_uni = st.sidebar.slider("Bobot University", 0.0, 1.0, 0.7, 0.01)
w_gpa = st.sidebar.slider("Bobot GPA", 0.0, 1.0, 0.3, 0.01)

# Analytical Skills
st.sidebar.subheader("Analytical Skills")
w_intern = st.sidebar.slider("Bobot Internship", 0.0, 1.0, 0.6, 0.01)
w_ach = st.sidebar.slider("Bobot Academic Achievement", 0.0, 1.0, 0.2, 0.01)
w_case = st.sidebar.slider("Bobot Business Case", 0.0, 1.0, 0.2, 0.01)

# Leadership
st.sidebar.subheader("Leadership")
w_type = st.sidebar.slider("Bobot Org Type", 0.0, 1.0, 0.3, 0.01)
w_role = st.sidebar.slider("Bobot Org Role", 0.0, 1.0, 0.7, 0.01)

# Overall Score
st.sidebar.subheader("Overall Score")
w_LT = st.sidebar.slider("Bobot Logical Thinking", 0.0, 1.0, 0.3, 0.01)
w_ANA = st.sidebar.slider("Bobot Analytical Skills", 0.0, 1.0, 0.4, 0.01)
w_LS = st.sidebar.slider("Bobot Leadership", 0.0, 1.0, 0.4, 0.01)

# -------------------------------
# 🧠 Evaluation Function
# -------------------------------
def evaluate_candidates(df_sorted, weights):
    w_uni, w_gpa, w_intern, w_ach, w_case, w_type, w_role, w_LT, w_ANA, w_LS = weights
    data_Uni, data_GTA, data_LT = [], [], []
    data_Exp, data_Role, data_LS = [], [], []
    data_in, data_ach, data_ach_busi, data_ana = [], [], [], []

    for x in range(len(df_sorted)):
        # University & Degree
        s = df_sorted["Degree|radio-4"].iloc[x]
        if s == "S2 - Master Degree":
            data_Uni.append(100)
        else:
            s1 = df_sorted["Name of University|radio-2"].iloc[x]
            if df_sorted["Country in which the university is located|radio-3"].iloc[x] == "Other":
                data_Uni.append(100)
            elif s1 in ["Universitas Indonesia (UI)", "Institut Teknologi Bandung (ITB)", "Universitas Gadjah Mada (UGM)"]:
                data_Uni.append(100)
            elif "Brawijaya" in s1 or "ITS" in s1 or "UNAIR" in s1 or "UNDIP" in s1 or "IPB" in s1 or "UNPAD" in s1 or "PRASMUL" in s1:
                data_Uni.append(70)
            elif s1 == "Other":
                s2 = df_sorted["University Name|text-6"].iloc[x].lower()
                if "binus" in s2 or "prasetiya" in s2 or "prasetya" in s2 or "prasmul" in s2:
                    data_Uni.append(70)
                else:
                    data_Uni.append(40)

        # GPA
        s = df_sorted["GPA|number-3"].iloc[x]
        if s >= 3.75:
            data_GTA.append(100)
        elif s >= 3.5:
            data_GTA.append(70)
        elif s >= 3.2:
            data_GTA.append(40)
        else:
            data_GTA.append(0)

        data_LT.append((data_Uni[x]*w_uni + data_GTA[x]*w_gpa) / (w_uni + w_gpa))

        # Leadership
        s = df_sorted["Have you ever had organizational experience?|radio-18"].iloc[x]
        if s == "No":
            data_Exp.append(0)
            data_Role.append(0)
        else:
            s1 = df_sorted["Organization Type|radio-21"].iloc[x]
            data_Exp.append({"International": 100, "National": 70}.get(s1, 40))

            s1 = df_sorted["Organization Role|radio-19"].iloc[x]
            data_Role.append({"Chief or Core Management": 100, "Team Leader (Division or Department Head)": 70}.get(s1, 40))

        data_LS.append((data_Exp[x]*w_type + data_Role[x]*w_role) / (w_type + w_role))

        # Analytical Skills
        s = df_sorted["Have you completed any internship?|radio-7"].iloc[x]
        if s == "No":
            data_in.append(0)
        else:
            if s == "Consulting Firm" or df_sorted["Have you had any full-time work experience?|radio-5"].iloc[x] == "Yes":
                data_in.append(100)
            elif s in ["Private Companies", "Startup / Tech Companies"]:
                data_in.append(70)
            else:
                data_in.append(40)

        s = df_sorted["Have you received any academic related achievements?|radio-10"].iloc[x]
        if s == "No":
            data_ach.append(0)
            data_ach_busi.append(0)
        else:
            data_ach.append({"International Level": 100, "National Level": 85}.get(s, 70))

            s = df_sorted["Have you ever participated in a business case competition?|radio-15"].iloc[x]
            data_ach_busi.append({"Yes, as a winner/finalist": 100, "Yes, as a participant": 50}.get(s, 0))

        data_ana.append((data_in[x]*w_intern + data_ach[x]*w_ach + data_ach_busi[x]*w_case) / (w_intern + w_ach + w_case))

    temp1 = pd.DataFrame({
        "Name": df_sorted["Full Name|name-1"],
        "Logical Thinking": data_LT,
        "Analytical Skills": data_ana,
        "Leadership": data_LS
    })

    temp1["Overall"] = (
        (temp1["Logical Thinking"] * w_LT +
         temp1["Analytical Skills"] * w_ANA +
         temp1["Leadership"] * w_LS) / (w_LT + w_ANA + w_LS)
    )

    temp1_1 = pd.DataFrame({
        "Name": df_sorted["Full Name|name-1"],
        "Experience": data_Uni,
        "GPA": data_GTA,
        "Logical Thinking": data_LT
    })

    return temp1, temp1_1

# -------------------------------
# 📊 Main App Logic
# -------------------------------
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df_sorted = df.sort_values(by="Full Name|name-1")
    weights = (w_uni, w_gpa, w_intern, w_ach, w_case, w_type, w_role, w_LT, w_ANA, w_LS)
    temp1, temp1_1 = evaluate_candidates(df_sorted, weights)

    st.subheader("Tabel Ringkasan Penilaian")
    st.dataframe(
        temp1[["Name", "Logical Thinking", "Analytical Skills", "Leadership", "Overall"]]
        .sort_values(by="Name", ascending=True)
        .reset_index(drop=True),
        use_container_width=True
    )

    st.subheader("Tabel Logical Thinking")
    st.dataframe(
        temp1_1[["Name", "Experience", "GPA", "Logical Thinking"]]
        .sort_values(by="Name", ascending=True)
        .reset_index(drop=True),
        use_container_width=True
    )
    
    st.title("Visualisasi Penilaian Kandidat")
    selected_name = st.selectbox("Pilih Nama:", temp1["Name"])
    row = temp1[temp1["Name"] == selected_name].iloc[0]

    categories = ["Logical Thinking", "Analytical Skills", "Leadership", "Overall"]
    values = [row[cat] for cat in categories]
    values += [values[0]]
    categories += [categories[0]]

    fig = go.Figure(
        data=[go.Scatterpolar(r=values, theta=categories, fill='toself', name=row["Name"])]
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        title=f"Radar Chart: {row['Name']}"
    )
    st.plotly_chart(fig)

else:
    st.warning("Silakan unggah file CSV kandidat terlebih dahulu di sidebar.")
