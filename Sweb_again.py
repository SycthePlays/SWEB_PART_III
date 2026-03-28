import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

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

    n = len(df_sorted)
    # containers for numeric scores
    data_Uni = [0]*n
    data_GPA = [0]*n
    data_LT = [0]*n

    data_in = [0]*n
    data_ach = [0]*n
    data_ach_busi = [0]*n
    data_ana = [0]*n

    data_Exp = [0]*n
    data_Role = [0]*n
    data_LS = [0]*n

    for x in range(n):
        # University & Degree
        s = df_sorted["Degree|radio-4"].iloc[x]
        if s == "S2 - Master Degree":
            data_Uni[x] = 100
        else:
            s1 = df_sorted["Name of University|radio-2"].iloc[x]
            if df_sorted["Country in which the university is located|radio-3"].iloc[x] == "Other":
                data_Uni[x] = 100
            elif s1 in ["Universitas Indonesia (UI)", "Institut Teknologi Bandung (ITB)", "Universitas Gadjah Mada (UGM)"]:
                data_Uni[x] = 100
            elif any(k in s1 for k in ["Brawijaya", "ITS", "UNAIR", "UNDIP", "IPB", "UNPAD", "PRASMUL"]):
                data_Uni[x] = 70
            elif s1 == "Other":
                s2 = str(df_sorted["University Name|text-6"].iloc[x]).lower()
                if any(k in s2 for k in ["binus", "prasetiya", "prasetya", "prasmul"]):
                    data_Uni[x] = 70
                else:
                    data_Uni[x] = 40

        # GPA
        try:
            s_gpa = float(df_sorted["GPA|number-3"].iloc[x])
        except Exception:
            s_gpa = 0.0
        if s_gpa >= 3.75:
            data_GPA[x] = 100
        elif s_gpa >= 3.5:
            data_GPA[x] = 70
        elif s_gpa >= 3.2:
            data_GPA[x] = 40
        else:
            data_GPA[x] = 0

        # Logical Thinking combined score
        denom_lt = (w_uni + w_gpa) if (w_uni + w_gpa) != 0 else 1
        data_LT[x] = (data_Uni[x]*w_uni + data_GPA[x]*w_gpa) / denom_lt

        # Leadership
        s_org = df_sorted["Have you ever had organizational experience?|radio-18"].iloc[x]
        if s_org == "No":
            data_Exp[x] = 0
            data_Role[x] = 0
        else:
            s_type = df_sorted["Organization Type|radio-21"].iloc[x]
            data_Exp[x] = {"International": 100, "National": 70}.get(s_type, 40)

            s_role = df_sorted["Organization Role|radio-19"].iloc[x]
            data_Role[x] = {"Chief or Core Management": 100, "Team Leader (Division or Department Head)": 70}.get(s_role, 40)

        denom_ls = (w_type + w_role) if (w_type + w_role) != 0 else 1
        data_LS[x] = (data_Exp[x]*w_type + data_Role[x]*w_role) / denom_ls

        # Analytical Skills
        s_intern = df_sorted["Have you completed any internship?|radio-7"].iloc[x]
        s6 = df_sorted["Have you had any full-time work experience?|radio-5"].iloc[x]
        if s_intern == "No" and s6 == "No":
            data_in[x] = 0
        else:
            if s_intern == "Consulting Firm" or s6 == "Yes":
                data_in[x] = 100
            elif s_intern in ["Private Companies", "Startup / Tech Companies"]:
                data_in[x] = 70
            else:
                data_in[x] = 40

        s_ach = df_sorted["Have you received any academic related achievements?|radio-10"].iloc[x]
        if s_ach == "No":
            data_ach[x] = 0
            data_ach_busi[x] = 0
        else:
            data_ach[x] = {"International Level": 100, "National Level": 85}.get(s_ach, 70)
            s_case = df_sorted["Have you ever participated in a business case competition?|radio-15"].iloc[x]
            data_ach_busi[x] = {"Yes, as a winner/finalist": 100, "Yes, as a participant": 50}.get(s_case, 0)

        denom_ana = (w_intern + w_ach + w_case) if (w_intern + w_ach + w_case) != 0 else 1
        data_ana[x] = (data_in[x]*w_intern + data_ach[x]*w_ach + data_ach_busi[x]*w_case) / denom_ana

    # Build DataFrame with numeric scores (for calculations) and display strings (for table)
    df_out = pd.DataFrame({
        "Email": df_sorted.get("Email Address|email-1", pd.Series([""]*n)),
        "Name": df_sorted["Full Name|name-1"],
        "Submission Date": df_sorted.get("Submission Date|hidden-3", pd.Series([""]*n)),
        # numeric columns
        "LT_score": data_LT,
        "AS_score": data_ana,
        "LS_score": data_LS,
        # sub-attributes numeric (kept for reference if needed)
        "Uni_score": data_Uni,
        "GPA_score": data_GPA,
        "Internship_score": data_in,
        "Achievement_score": data_ach,
        "BusinessCase_score": data_ach_busi,
        "OrgType_score": data_Exp,
        "OrgRole_score": data_Role
    })

    # Overall final score
    denom_overall = (w_LT + w_ANA + w_LS) if (w_LT + w_ANA + w_LS) != 0 else 1
    df_out["Overall"] = (df_out["LT_score"] * w_LT + df_out["AS_score"] * w_ANA + df_out["LS_score"] * w_LS) / denom_overall
    df_out["Overall"] = df_out["Overall"].round(2)

    # Create display dicts for HTML rendering
    df_out["Logical Thinking_display"] = df_out.apply(
        lambda r: {
            "title": "Logical Thinking",
            "rows": [
                ("University", int(r['Uni_score'])),
                ("GPA", int(r['GPA_score'])),
                ("OVR", round(r['LT_score'], 2))
            ]
        },
        axis=1
    )
    df_out["Analytical Skills_display"] = df_out.apply(
        lambda r: {
            "title": "Analytical Skills",
            "rows": [
                ("Internship", int(r['Internship_score'])),
                ("Achievement", int(r['Achievement_score'])),
                ("Business Case", int(r['BusinessCase_score'])),
                ("OVR", round(r['AS_score'], 2))
            ]
        },
        axis=1
    )
    df_out["Leadership_display"] = df_out.apply(
        lambda r: {
            "title": "Leadership",
            "rows": [
                ("Org Type", int(r['OrgType_score'])),
                ("Org Role", int(r['OrgRole_score'])),
                ("OVR", round(r['LS_score'], 2))
            ]
        },
        axis=1
    )

    return df_out

# -------------------------------
# Helper: render HTML table with subheadings (updated to use iterrows)
# -------------------------------
def render_summary_html(df_display):
    css = """
    <style>
    .summary-table { border-collapse: collapse; width: 100%; font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 14px; color: #000; }
    .summary-table th, .summary-table td { border: 1px solid #ddd; padding: 10px; vertical-align: top; color: #000; }
    .summary-table th { background-color: #f4f6fb; text-align: left; padding-top: 12px; padding-bottom: 12px; font-weight: 800; color: #000; }
    .cat-title { font-weight: 800; color: #000; margin-bottom: 6px; display:block; font-size: 13px; }
    .sub-row { margin: 2px 0; line-height: 1.2; }
    .sub-label { font-weight: 700; color: #000; display:inline-block; width: 100px; }
    .sub-value { margin-left: 125px; color: #000; font-weight: 1000; }
    .overall-cell { font-weight: 800; text-align: center; background-color: #f8fafc; color: #000; }
    .meta { color: #333; font-size: 13px; font-weight: 600; }
    .name-cell { font-weight: 700; color: #000; }
    .index-cell { font-weight: 700; color: #000; text-align: center; width: 50px; }
    @media (max-width: 800px) {
      .sub-label { display:block; width: auto; }
    }
    </style>
    """

    header = """
    <table class="summary-table">
      <thead>
        <tr>
          <th>No</th>
          <th>Email</th>
          <th>Name</th>
          <th>Submission Date</th>
          <th>Logical Thinking</th>
          <th>Analytical Skills</th>
          <th>Leadership</th>
          <th>Overall</th>
        </tr>
      </thead>
      <tbody>
    """

    rows_html = ""
    for idx, (_, r) in enumerate(df_display.iterrows(), start=1):
        lt = r["Logical Thinking_display"]
        an = r["Analytical Skills_display"]
        ls = r["Leadership_display"]

        def render_cat(cat):
            inner = f'<span class="cat-title">{cat["title"]}</span>'
            for label, val in cat["rows"]:
                inner += f'<div class="sub-row"><span class="sub-label">{label}</span><span class="sub-value">{val}</span></div>'
            return inner

        lt_html = render_cat(lt)
        an_html = render_cat(an)
        ls_html = render_cat(ls)

        rows_html += f"""
        <tr>
          <td class="index-cell">{idx}</td>
          <td class="meta">{r.get('Email','')}</td>
          <td class="name-cell">{r['Name']}</td>
          <td class="meta">{r.get('Submission Date','')}</td>
          <td>{lt_html}</td>
          <td>{an_html}</td>
          <td>{ls_html}</td>
          <td class="overall-cell">{r['Overall']}</td>
        </tr>
        """

    footer = """
      </tbody>
    </table>
    """

    html = css + header + rows_html + footer
    return html

# -------------------------------
# 📊 Main App Logic
# -------------------------------
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df_sorted = df.sort_values(by="Full Name|name-1").reset_index(drop=True)
    weights = (w_uni, w_gpa, w_intern, w_ach, w_case, w_type, w_role, w_LT, w_ANA, w_LS)
    temp1 = evaluate_candidates(df_sorted, weights)

    # --- Search and Sort controls (added alphabetical sort) ---
    st.subheader("Tabel Ringkasan Penilaian")
    search_query = st.text_input("Cari nama (ketik sebagian nama untuk mencari)", value="")

    sort_by = st.selectbox(
        "Urutkan",
        options=[
            "Nama A → Z",
            "Nama Z → A",
            "Overall Tertinggi",
            "Overall Terendah"
        ],
        index=0
    )

    # Filter by search (case-insensitive, partial)
    if search_query.strip() != "":
        mask = temp1["Name"].str.contains(search_query.strip(), case=False, na=False)
        filtered = temp1[mask].copy()
    else:
        filtered = temp1.copy()

    # Apply sorting berdasarkan pilihan user
    if sort_by == "Nama A → Z":
        filtered = filtered.sort_values(by="Name", ascending=True).reset_index(drop=True)
    elif sort_by == "Nama Z → A":
        filtered = filtered.sort_values(by="Name", ascending=False).reset_index(drop=True)
    elif sort_by == "Overall Tertinggi":
        filtered = filtered.sort_values(by="Overall", ascending=False).reset_index(drop=True)
    else:  # Overall Terendah
        filtered = filtered.sort_values(by="Overall", ascending=True).reset_index(drop=True)

    # Render HTML summary table using components.html
    html_table = render_summary_html(filtered)

    # compute height dynamically (approx 120px per row + header)
    approx_height = 160 + len(filtered) * 120
    height = min(max(approx_height, 300), 2200)

    components.html(html_table, height=height, scrolling=True)

    # Radar chart still uses numeric scores
    st.title("Visualisasi Penilaian Kandidat")
    names_list = filtered["Name"].tolist()
    if names_list:
        selected_name = st.selectbox("Pilih Nama:", names_list)
        row = filtered[filtered["Name"] == selected_name].iloc[0]

        categories = ["Logical Thinking", "Analytical Skills", "Leadership"]
        values = [row["LT_score"], row["AS_score"], row["LS_score"]]
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
        st.info("Tidak ada kandidat yang cocok dengan pencarian.")

else:
    st.warning("Silakan unggah file CSV kandidat terlebih dahulu di sidebar.")
