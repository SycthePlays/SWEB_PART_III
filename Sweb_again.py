import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
import io
import json
 
# -------------------------------
# 🎨 Page Config & Global Styling
# -------------------------------
st.set_page_config(
    page_title="Candidate Assessment",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');
 
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
 
.stApp { background: linear-gradient(135deg, #0A1628 0%, #0D1F3C 50%, #0A1628 100%); }
 
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1F3C 0%, #091729 100%);
    border-right: 1px solid rgba(74, 144, 217, 0.15);
}
[data-testid="stSidebar"] > div:first-child { padding-top: 2rem; }
[data-testid="stSidebar"] h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem !important;
    color: #E8EDF5 !important;
    letter-spacing: 0.02em;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(74, 144, 217, 0.4);
    margin-bottom: 1.5rem !important;
}
[data-testid="stSidebar"] h3 {
    color: #4A90D9 !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 1.5rem !important;
    margin-bottom: 0.5rem !important;
}
[data-testid="stSidebar"] label { color: #A8B8D0 !important; font-size: 0.82rem !important; }
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background-color: #4A90D9 !important;
    border-color: #4A90D9 !important;
    box-shadow: 0 0 8px rgba(74, 144, 217, 0.5) !important;
}
[data-testid="stFileUploader"] {
    background: rgba(74, 144, 217, 0.06) !important;
    border: 1px dashed rgba(74, 144, 217, 0.3) !important;
    border-radius: 8px !important;
}
[data-testid="stFileUploader"] label { color: #A8B8D0 !important; }
 
.main-header {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem; color: #E8EDF5;
    letter-spacing: 0.01em; margin-bottom: 0.25rem; line-height: 1.2;
}
.main-subheader {
    color: #4A90D9; font-size: 0.85rem; font-weight: 500;
    letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 2rem;
}
.section-heading {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem; color: #E8EDF5;
    margin-top: 2rem; margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(74, 144, 217, 0.2);
}
 
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] input {
    background: rgba(13, 31, 60, 0.8) !important;
    border: 1px solid rgba(74, 144, 217, 0.2) !important;
    border-radius: 6px !important;
    color: #E8EDF5 !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: rgba(74, 144, 217, 0.6) !important;
    box-shadow: 0 0 0 2px rgba(74, 144, 217, 0.12) !important;
}
 
/* Metric cards */
[data-testid="stMetric"] {
    background: rgba(13,31,60,0.7) !important;
    border: 1px solid rgba(74,144,217,0.15) !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
}
[data-testid="stMetricLabel"] { color: #6B8BAF !important; font-size: 0.8rem !important; }
[data-testid="stMetricValue"] { color: #E8EDF5 !important; font-size: 1.4rem !important; }
 
.stAlert {
    background: rgba(74, 144, 217, 0.08) !important;
    border: 1px solid rgba(74, 144, 217, 0.25) !important;
    border-radius: 8px !important; color: #A8B8D0 !important;
}
.js-plotly-plot .plotly .bg { fill: transparent !important; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0A1628; }
::-webkit-scrollbar-thumb { background: rgba(74, 144, 217, 0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(74, 144, 217, 0.55); }
 
/* Download button per row */
.stDownloadButton > button {
    background: rgba(74,144,217,0.12) !important;
    border: 1px solid rgba(74,144,217,0.3) !important;
    color: #4A90D9 !important;
    border-radius: 6px !important;
    font-size: 0.8rem !important;
    padding: 4px 12px !important;
}
.stDownloadButton > button:hover {
    background: rgba(74,144,217,0.25) !important;
    border-color: #4A90D9 !important;
}
 
/* Sort toolbar buttons (mimic clickable table header cells) */
div[data-testid="stHorizontalBlock"].sort-toolbar-row .stButton > button {
    background: linear-gradient(90deg,#0D1F3C 0%,#112340 100%) !important;
    border: 1px solid rgba(74,144,217,0.25) !important;
    color: #4A90D9 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border-radius: 6px 6px 0 0 !important;
    padding: 10px 6px !important;
    width: 100%;
}
div[data-testid="stHorizontalBlock"].sort-toolbar-row .stButton > button:hover {
    background: rgba(74,144,217,0.18) !important;
    border-color: #4A90D9 !important;
    color: #7FB3E8 !important;
}
</style>
""", unsafe_allow_html=True)
 
# -------------------------------
# 🎯 Sidebar: Upload & Parameters
# -------------------------------
st.sidebar.title("Parameter Penilaian")
uploaded_file = st.sidebar.file_uploader("Pilih file CSV kandidat", type=["csv"])
 
st.sidebar.subheader("Logical Thinking")
w_uni  = st.sidebar.slider("Bobot University", 0.0, 1.0, 0.7, 0.01)
w_gpa  = st.sidebar.slider("Bobot GPA", 0.0, 1.0, 0.3, 0.01)
 
st.sidebar.subheader("Analytical Skills")
w_intern = st.sidebar.slider("Bobot Internship", 0.0, 1.0, 0.6, 0.01)
w_ach    = st.sidebar.slider("Bobot Academic Achievement", 0.0, 1.0, 0.2, 0.01)
w_case   = st.sidebar.slider("Bobot Business Case", 0.0, 1.0, 0.2, 0.01)
 
st.sidebar.subheader("Leadership")
w_type = st.sidebar.slider("Bobot Org Type", 0.0, 1.0, 0.3, 0.01)
w_role = st.sidebar.slider("Bobot Org Role", 0.0, 1.0, 0.7, 0.01)
 
st.sidebar.subheader("Overall Score")
w_LT  = st.sidebar.slider("Bobot Logical Thinking", 0.0, 1.0, 0.3, 0.01)
w_ANA = st.sidebar.slider("Bobot Analytical Skills", 0.0, 1.0, 0.4, 0.01)
w_LS  = st.sidebar.slider("Bobot Leadership", 0.0, 1.0, 0.4, 0.01)
 
# -------------------------------
# 🧠 Evaluation Function
# -------------------------------
def evaluate_candidates(df_raw, weights):
    w_uni, w_gpa, w_intern, w_ach, w_case, w_type, w_role, w_LT, w_ANA, w_LS = weights
    df_sorted = df_raw.copy()
    n = len(df_sorted)
 
    data_Uni=[0]*n; data_GPA=[0]*n; data_LT=[0]*n
    data_in=[0]*n; data_ach=[0]*n; data_ach_busi=[0]*n; data_ana=[0]*n
    data_Exp=[0]*n; data_Role=[0]*n; data_LS=[0]*n
 
    for x in range(n):
        # --- Degree path: Master's degree completed? ---
        s_master = str(df_sorted["Have you completed a Master's degree?|radio-4"].iloc[x]).strip()
        if s_master.startswith("Yes"):
            data_Uni[x] = 100
            gpa_col = "GPA|number-10"
        else:
            s1 = str(df_sorted["Name of University (Bachelor Degree)|radio-2"].iloc[x]).upper().strip()
            s_country = str(df_sorted["Country in which the university is located|radio-3"].iloc[x]).strip()
            if s_country == "Abroad":
                data_Uni[x] = 100
            elif s1 in ["UNIVERSITAS INDONESIA (UI)", "INSTITUT TEKNOLOGI BANDUNG (ITB)", "UNIVERSITAS GADJAH MADA (UGM)"]:
                data_Uni[x] = 100
            elif any(k in s1 for k in ["BRAWIJAYA","ITS","UNAIR","UNDIP","IPB","UNPAD","PRASMUL"]):
                data_Uni[x] = 70
            elif s1 == "OTHER":
                s2 = str(df_sorted["University Name|text-6"].iloc[x]).upper().strip()
                data_Uni[x] = 70 if any(k in s2 for k in ["BINUS","PRASETIYA","PRASETYA","PRASMUL","BINA NUSANTARA"]) else 40
            gpa_col = "GPA|number-3"
 
        try: s_gpa = float(df_sorted[gpa_col].iloc[x])
        except: s_gpa = 0.0
        if s_gpa >= 3.75: data_GPA[x] = 100
        elif s_gpa >= 3.5: data_GPA[x] = 70
        elif s_gpa >= 3.2: data_GPA[x] = 40
 
        denom_lt = (w_uni+w_gpa) or 1
        data_LT[x] = (data_Uni[x]*w_uni + data_GPA[x]*w_gpa) / denom_lt
 
        # --- Leadership: campus / student organization experience ---
        s_org = str(df_sorted["Have you ever had any campus or student organization experience?|radio-18"].iloc[x]).strip()
        if s_org == "No":
            data_Exp[x] = 0; data_Role[x] = 0
        else:
            s_scale = str(df_sorted["Organization Scale|radio-21"].iloc[x]).strip()
            s_role  = str(df_sorted["Organization Role|radio-19"].iloc[x]).strip()
            data_Exp[x]  = {"International (e.g., Model United Nations)":100,
                             "National (e.g., Perhimpunan Pelajar Indonesia)":70}.get(s_scale, 40)
            data_Role[x] = {"Chief or Core Management":100,
                             "Team Leader (Division or Department Head)":70}.get(s_role, 40)
 
        denom_ls = (w_type+w_role) or 1
        data_LS[x] = (data_Exp[x]*w_type + data_Role[x]*w_role) / denom_ls
 
        # --- Analytical: internship / full-time work ---
        s_intern_yn   = str(df_sorted["Have you completed any internship?|radio-7"].iloc[x]).strip()
        s_work_yn     = str(df_sorted["Have you had any full-time work experience?|radio-5"].iloc[x]).strip()
        s_intern_type = str(df_sorted["Type of Organization|radio-8"].iloc[x]).strip()
        if s_intern_yn == "No" and s_work_yn == "No":
            data_in[x] = 0
        elif s_intern_type == "Consulting Firm" or s_work_yn == "Yes":
            data_in[x] = 100
        elif s_intern_type in ["Private Companies","Startup / Tech Industries"]:
            data_in[x] = 70
        else:
            data_in[x] = 40
 
        # --- Analytical: academic achievement ---
        s_ach = str(df_sorted["Have you received any academic related achievements?|radio-10"].iloc[x]).strip()
        if s_ach == "No":
            data_ach[x] = 0
        else:
            s_ach_level = str(df_sorted["Level of Competition or Recognition|radio-12"].iloc[x]).strip()
            data_ach[x] = {"International Level":100,"National Level":85}.get(s_ach_level, 70)
 
        # --- Analytical: business case competition (independent of academic achievement) ---
        s_case_v = str(df_sorted["Have you ever participated in a business case competition?|radio-15"].iloc[x]).strip()
        data_ach_busi[x] = {"Yes, as a winner/finalist":100,"Yes, as a participant":50}.get(s_case_v, 0)
 
        denom_ana = (w_intern+w_ach+w_case) or 1
        data_ana[x] = (data_in[x]*w_intern + data_ach[x]*w_ach + data_ach_busi[x]*w_case) / denom_ana
 
    # Helper: safe get column
    def gcol(col, default=""):
        return df_sorted[col] if col in df_sorted.columns else pd.Series([default]*n)
 
    df_out = pd.DataFrame({
        "Name":            df_sorted["Full Name|name-1"],
        "Email":           gcol("Email Address|email-1"),
        "Phone":           gcol("Mobile Phone|phone-1"),
        "Submission Date": gcol("Submission Date|hidden-3"),
        "CV_Link":         gcol("CV / Resume|upload-1"),
        "Transcript_Link": gcol("Academic Transricpt|upload-2"),   # note: typo in CSV kept as-is
        "LT_score":   data_LT,   "AS_score":  data_ana,  "LS_score":  data_LS,
        "Uni_score":  data_Uni,  "GPA_score": data_GPA,
        "Internship_score":   data_in,   "Achievement_score": data_ach,
        "BusinessCase_score": data_ach_busi,
        "OrgType_score": data_Exp, "OrgRole_score": data_Role,
    })
 
    denom_overall = (w_LT+w_ANA+w_LS) or 1
    df_out["Overall"] = ((df_out["LT_score"]*w_LT + df_out["AS_score"]*w_ANA + df_out["LS_score"]*w_LS) / denom_overall).round(2)
 
    df_out["Logical Thinking_display"]  = df_out.apply(lambda r: {"title":"Logical Thinking",  "rows":[("University",int(r.Uni_score)),("GPA",int(r.GPA_score)),("OVR",round(r.LT_score,2))]}, axis=1)
    df_out["Analytical Skills_display"] = df_out.apply(lambda r: {"title":"Analytical Skills", "rows":[("Internship",int(r.Internship_score)),("Achievement",int(r.Achievement_score)),("Business Case",int(r.BusinessCase_score)),("OVR",round(r.AS_score,2))]}, axis=1)
    df_out["Leadership_display"]        = df_out.apply(lambda r: {"title":"Leadership",        "rows":[("Org Type",int(r.OrgType_score)),("Org Role",int(r.OrgRole_score)),("OVR",round(r.LS_score,2))]}, axis=1)
 
    return df_out
 
# -------------------------------
# Helpers
# -------------------------------
def score_color(val):
    try: v = float(val)
    except: return "#A8B8D0"
    if v >= 80: return "#4A90D9"
    elif v >= 60: return "#5BB8A0"
    elif v >= 40: return "#E0A030"
    else: return "#C85A5A"
 
def overall_badge_color(val):
    try: v = float(val)
    except: return "#A8B8D0"
    if v >= 80:   return "linear-gradient(135deg,#4A90D9,#2E6EBF)"
    elif v >= 60: return "linear-gradient(135deg,#5BB8A0,#3A9880)"
    elif v >= 40: return "linear-gradient(135deg,#E0A030,#C08020)"
    else:         return "linear-gradient(135deg,#C85A5A,#A03A3A)"
 
def convert_df_to_excel(df):
    output = io.BytesIO()
    clean_df = df.drop(columns=[c for c in df.columns if "_display" in c])
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        clean_df.to_excel(writer, index=False, sheet_name='Ranking Kandidat')
    return output.getvalue()
 
def make_candidate_excel(row):
    """Generate a single-candidate detailed Excel."""
    output = io.BytesIO()
    data = {
        "Field": [
            "Name", "Email", "Phone", "Submission Date",
            "CV Link", "Academic Transcript Link",
            "Overall Score",
            "Logical Thinking Score", "  University Score", "  GPA Score",
            "Analytical Skills Score", "  Internship Score", "  Achievement Score", "  Business Case Score",
            "Leadership Score", "  Org Type Score", "  Org Role Score",
        ],
        "Value": [
            row.get("Name",""), row.get("Email",""), row.get("Phone",""), row.get("Submission Date",""),
            row.get("CV_Link",""), row.get("Transcript_Link",""),
            row.get("Overall",""),
            round(row.get("LT_score",0),2), int(row.get("Uni_score",0)), int(row.get("GPA_score",0)),
            round(row.get("AS_score",0),2), int(row.get("Internship_score",0)), int(row.get("Achievement_score",0)), int(row.get("BusinessCase_score",0)),
            round(row.get("LS_score",0),2), int(row.get("OrgType_score",0)), int(row.get("OrgRole_score",0)),
        ]
    }
    df_single = pd.DataFrame(data)
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_single.to_excel(writer, index=False, sheet_name='Detail Kandidat')
        wb = writer.book
        ws = writer.sheets['Detail Kandidat']
        # Styling
        hdr_fmt = wb.add_format({'bold':True,'bg_color':'#0D1F3C','font_color':'#4A90D9','border':1})
        field_fmt = wb.add_format({'bold':True,'font_color':'#1A3A5C','bg_color':'#EEF4FB','border':1})
        val_fmt   = wb.add_format({'border':1})
        link_fmt  = wb.add_format({'font_color':'#0563C1','underline':True,'border':1})
        ws.write(0,0,"Field",hdr_fmt); ws.write(0,1,"Value",hdr_fmt)
        ws.set_column(0,0,32); ws.set_column(1,1,80)
        for i, (f,v) in enumerate(zip(data["Field"],data["Value"]), start=1):
            ws.write(i,0,f,field_fmt)
            if isinstance(v,str) and v.startswith("http"):
                ws.write_url(i,1,v,link_fmt,v)
            else:
                ws.write(i,1,v,val_fmt)
    return output.getvalue()
 
# -------------------------------
# HTML Table renderer
# -------------------------------
def render_summary_html(df_display, start_index=1):
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');
    *{box-sizing:border-box;margin:0;padding:0;}
    body{background:transparent;font-family:'DM Sans',sans-serif;color:#E8EDF5;}
    .tbl-wrap{width:100%;overflow-x:auto;overflow-y:hidden;display:block;}
    .summary-table{border-collapse:separate;border-spacing:0;width:100%;font-size:13px;color:#E8EDF5;background:transparent;}
    .summary-table thead tr{background:linear-gradient(90deg,#0D1F3C 0%,#112340 100%);}
    .summary-table th{padding:14px 16px;text-align:left;font-weight:600;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#4A90D9;border-bottom:1px solid rgba(74,144,217,.25);white-space:nowrap;position:sticky;top:0;z-index:2;background:#0D1F3C;}
    .summary-table th:first-child{border-radius:8px 0 0 0;}.summary-table th:last-child{border-radius:0 8px 0 0;}
    .summary-table tbody tr{background:rgba(13,31,60,.6);transition:background .2s;border-bottom:1px solid rgba(74,144,217,.08);}
    .summary-table tbody tr:hover{background:rgba(74,144,217,.08);}
    .summary-table tbody tr:nth-child(even){background:rgba(10,22,40,.7);}
    .summary-table tbody tr:nth-child(even):hover{background:rgba(74,144,217,.08);}
    .summary-table td{padding:12px 16px;vertical-align:top;border-bottom:1px solid rgba(74,144,217,.07);}
    .index-cell{text-align:center;color:rgba(74,144,217,.6);font-weight:600;font-size:12px;width:44px;min-width:44px;vertical-align:middle!important;}
    .name-cell{font-weight:600;color:#E8EDF5;white-space:nowrap;min-width:150px;vertical-align:middle!important;}
    .meta{color:#6B8BAF;font-size:12px;font-weight:400;vertical-align:middle!important;}
    .phone-cell{color:#8AA8CC;font-size:12px;white-space:nowrap;vertical-align:middle!important;}
 
    /* link pill */
    .link-pill{
        display:inline-flex;align-items:center;gap:5px;
        padding:4px 10px;border-radius:20px;font-size:11px;font-weight:600;
        text-decoration:none;white-space:nowrap;
        background:rgba(74,144,217,.12);
        border:1px solid rgba(74,144,217,.3);
        color:#4A90D9;
        transition:background .2s,border-color .2s;
        margin:2px 0;
    }
    .link-pill:hover{background:rgba(74,144,217,.25);border-color:#4A90D9;color:#7FB3E8;}
    .link-pill.transcript{background:rgba(91,184,160,.1);border-color:rgba(91,184,160,.3);color:#5BB8A0;}
    .link-pill.transcript:hover{background:rgba(91,184,160,.25);border-color:#5BB8A0;}
    .links-cell{vertical-align:middle!important;min-width:120px;}
 
    .cat-card{background:rgba(74,144,217,.05);border:1px solid rgba(74,144,217,.12);border-radius:8px;padding:10px 12px;min-width:150px;display:inline-block;}
    .cat-title{font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#4A90D9;margin-bottom:8px;display:block;}
    .sub-row{display:flex;justify-content:space-between;align-items:center;margin:4px 0;gap:12px;}
    .sub-label{font-size:12px;color:#8AA8CC;font-weight:400;flex:1;}
    .sub-value{font-size:12px;font-weight:700;text-align:right;min-width:32px;}
    .ovr-row{margin-top:6px;padding-top:6px;border-top:1px solid rgba(74,144,217,.15);}
    .ovr-label{font-size:11px;font-weight:700;color:#4A90D9;letter-spacing:.05em;}
    .ovr-value{font-size:13px;font-weight:700;color:#E8EDF5;}
    .overall-badge{display:inline-block;padding:6px 14px;border-radius:20px;font-weight:700;font-size:14px;color:#fff;text-align:center;white-space:nowrap;box-shadow:0 2px 8px rgba(0,0,0,.3);}
    .overall-cell{text-align:center;vertical-align:middle!important;min-width:80px;}
 
    .tbl-wrap::-webkit-scrollbar{height:8px;width:8px;}
    .tbl-wrap::-webkit-scrollbar-track{background:rgba(10,22,40,.5);border-radius:4px;}
    .tbl-wrap::-webkit-scrollbar-thumb{background:rgba(74,144,217,.5);border-radius:4px;}
    .tbl-wrap::-webkit-scrollbar-thumb:hover{background:#4A90D9;}
    </style>
    """
 
    header = """
    <div class="tbl-wrap">
    <table class="summary-table">
      <thead><tr>
        <th>#</th>
        <th>Name</th>
        <th>Email</th>
        <th>Phone</th>
        <th>Submission Date</th>
        <th>Documents</th>
        <th>Logical Thinking</th>
        <th>Analytical Skills</th>
        <th>Leadership</th>
        <th>Overall</th>
      </tr></thead>
      <tbody>
    """
 
    rows_html = ""
    for idx, (_, r) in enumerate(df_display.iterrows(), start=start_index):
 
        def render_cat(cat):
            inner = f'<div class="cat-card"><span class="cat-title">{cat["title"]}</span>'
            for label, val in cat["rows"]:
                is_ovr = (label == "OVR")
                color = score_color(val) if not is_ovr else "#E8EDF5"
                if is_ovr:
                    inner += f'<div class="sub-row ovr-row"><span class="sub-label ovr-label">OVR</span><span class="sub-value ovr-value" style="color:{color}">{val}</span></div>'
                else:
                    inner += f'<div class="sub-row"><span class="sub-label">{label}</span><span class="sub-value" style="color:{color}">{val}</span></div>'
            return inner + '</div>'
 
        cv_url  = str(r.get("CV_Link","")).strip()
        tr_url  = str(r.get("Transcript_Link","")).strip()
        cv_html = f'<a class="link-pill" href="{cv_url}" target="_blank">📄 CV</a>' if cv_url and cv_url != "nan" else '<span style="color:#3A5070;font-size:11px;">—</span>'
        tr_html = f'<a class="link-pill transcript" href="{tr_url}" target="_blank">📋 Transcript</a>' if tr_url and tr_url != "nan" else '<span style="color:#3A5070;font-size:11px;">—</span>'
 
        badge_bg = overall_badge_color(r['Overall'])
 
        rows_html += f"""
        <tr>
          <td class="index-cell">{idx}</td>
          <td class="name-cell">{r.get('Name','')}</td>
          <td class="meta">{r.get('Email','')}</td>
          <td class="phone-cell">{r.get('Phone','')}</td>
          <td class="meta">{r.get('Submission Date','')}</td>
          <td class="links-cell">{cv_html}<br>{tr_html}</td>
          <td>{render_cat(r["Logical Thinking_display"])}</td>
          <td>{render_cat(r["Analytical Skills_display"])}</td>
          <td>{render_cat(r["Leadership_display"])}</td>
          <td class="overall-cell"><span class="overall-badge" style="background:{badge_bg}">{r['Overall']}</span></td>
        </tr>
        """
 
    return css + header + rows_html + "</tbody></table></div>"
 
# -------------------------------
# Popup Detail
# -------------------------------
@st.dialog("📋 Detail Lengkap Kandidat", width="large")
def show_popup_detail(row):
    st.markdown(f"## 🧑‍💼 {row['Name']}")
    st.caption(f"📧 {row.get('Email','-')}  |  📱 {row.get('Phone','-')}  |  📅 {row.get('Submission Date','-')}")
 
    cv_url = str(row.get("CV_Link","")).strip()
    tr_url = str(row.get("Transcript_Link","")).strip()
    link_cols = st.columns(2)
    if cv_url and cv_url != "nan":
        link_cols[0].link_button("📄 Buka CV", cv_url, use_container_width=True)
    if tr_url and tr_url != "nan":
        link_cols[1].link_button("📋 Buka Transcript", tr_url, use_container_width=True)
 
    st.divider()
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("🌟 Overall",   f"{row['Overall']}")
    m2.metric("🧠 Log. Think", f"{row['LT_score']:.2f}")
    m3.metric("📊 Analytical", f"{row['AS_score']:.2f}")
    m4.metric("🗣️ Leadership", f"{row['LS_score']:.2f}")
 
    categories = ["Logical Thinking","Analytical Skills","Leadership"]
    vals = [row["LT_score"], row["AS_score"], row["LS_score"]]
    fig = go.Figure(data=[go.Scatterpolar(
        r=vals+[vals[0]], theta=categories+[categories[0]], fill='toself',
        line=dict(color='#4A90D9',width=3), fillcolor='rgba(74,144,217,.18)',
        marker=dict(color='#4A90D9',size=8)
    )])
    fig.update_layout(
        height=500,
        polar=dict(bgcolor='rgba(13,31,60,.6)',
            radialaxis=dict(visible=True,range=[0,100],tickfont=dict(color='#6B8BAF',size=12),gridcolor='rgba(74,144,217,.15)',linecolor='rgba(74,144,217,.2)'),
            angularaxis=dict(tickfont=dict(color='#A8B8D0',size=14,family='DM Sans'),gridcolor='rgba(74,144,217,.12)',linecolor='rgba(74,144,217,.2)')
        ),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False,
        margin=dict(t=30,b=30,l=30,r=30)
    )
    st.plotly_chart(fig, use_container_width=True, config={'scrollZoom':True,'displayModeBar':True})
 
# -------------------------------
# 📊 Main App
# -------------------------------
st.markdown('<p class="main-subheader">Candidate Evaluation Dashboard</p>', unsafe_allow_html=True)
st.markdown('<h1 class="main-header">Penilaian Kandidat</h1>', unsafe_allow_html=True)
 
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df_raw = df.sort_values(by="Full Name|name-1").reset_index(drop=True)
    weights = (w_uni,w_gpa,w_intern,w_ach,w_case,w_type,w_role,w_LT,w_ANA,w_LS)
    temp1 = evaluate_candidates(df_raw, weights)
 
    st.markdown('<div class="section-heading">Tabel Ringkasan Penilaian</div>', unsafe_allow_html=True)
 
    ITEMS_PER_PAGE = 10
 
    # Sort state (replaces the "Urutkan berdasarkan" dropdown with clickable headers)
    if "sort_col" not in st.session_state:
        st.session_state.sort_col = "Name"
        st.session_state.sort_asc = True
 
    col1, col3, col_dl = st.columns([3, 1, 1.5])
    with col1:
        search_query = st.text_input("🔍 Cari nama", value="", placeholder="Ketik nama...")
 
    if search_query.strip():
        filtered = temp1[temp1["Name"].str.contains(search_query.strip(), case=False, na=False)].copy()
    else:
        filtered = temp1.copy()
 
    filtered = filtered.sort_values(by=st.session_state.sort_col, ascending=st.session_state.sort_asc).reset_index(drop=True)
 
    total_pages = max(1, (len(filtered)-1)//ITEMS_PER_PAGE + 1)
    with col3:
        page = st.number_input(f"Hal (1-{total_pages})", min_value=1, max_value=total_pages, value=1, step=1)
    with col_dl:
        st.write("")
        excel_all = convert_df_to_excel(filtered)
        st.download_button("📥 Download Semua (Excel)", data=excel_all,
            file_name="Ranking_Kandidat.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True)
 
    # Clickable sort toolbar - mimics sortable table header titles
    sort_fields = [
        ("Nama", "Name"),
        ("Tanggal Submit", "Submission Date"),
        ("Logical Thinking", "LT_score"),
        ("Analytical Skills", "AS_score"),
        ("Leadership", "LS_score"),
        ("Overall", "Overall"),
    ]
    st.markdown('<div class="sort-toolbar-row">', unsafe_allow_html=True)
    sort_container = st.container()
    with sort_container:
        st.markdown('<span style="font-size:11px;color:#6B8BAF;letter-spacing:.08em;text-transform:uppercase;">Urutkan:</span>', unsafe_allow_html=True)
        toolbar_cols = st.columns(len(sort_fields))
        for i, (label, colname) in enumerate(sort_fields):
            arrow = ""
            if st.session_state.sort_col == colname:
                arrow = " ▲" if st.session_state.sort_asc else " ▼"
            if toolbar_cols[i].button(label+arrow, use_container_width=True, key=f"sortbtn_{colname}"):
                if st.session_state.sort_col == colname:
                    st.session_state.sort_asc = not st.session_state.sort_asc
                else:
                    st.session_state.sort_col = colname
                    st.session_state.sort_asc = True
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
 
    start_idx = (page-1)*ITEMS_PER_PAGE
    paginated  = filtered.iloc[start_idx:start_idx+ITEMS_PER_PAGE]
 
    html_table = render_summary_html(paginated, start_index=start_idx+1)
    approx_height = 160 + len(paginated)*130
    components.html(html_table, height=approx_height, scrolling=True)
 
    # ── Per-row download ──
    st.markdown('<div class="section-heading">📥 Download Detail per Kandidat</div>', unsafe_allow_html=True)
    st.caption("Klik tombol di bawah untuk mendownload data lengkap tiap kandidat dalam format Excel.")
 
    cols_per_row = 3
    names_paginated = paginated["Name"].tolist()
    for i in range(0, len(names_paginated), cols_per_row):
        chunk = names_paginated[i:i+cols_per_row]
        cols = st.columns(cols_per_row)
        for j, name in enumerate(chunk):
            row_data = filtered[filtered["Name"]==name].iloc[0]
            excel_single = make_candidate_excel(row_data)
            safe_name = name.replace(" ","_").replace("/","_")
            cols[j].download_button(
                label=f"⬇ {name}",
                data=excel_single,
                file_name=f"Detail_{safe_name}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key=f"dl_{start_idx}_{i}_{j}"
            )
 
    # ── Detail & Visualisasi ──
    st.markdown('<div class="section-heading">🔎 Detail & Visualisasi Kandidat</div>', unsafe_allow_html=True)
 
    names_list = filtered["Name"].tolist()
    if names_list:
        selected_name = st.selectbox("Pilih nama kandidat:", names_list)
        row_sel = filtered[filtered["Name"]==selected_name].iloc[0]
 
        # Info bar
        cv_u = str(row_sel.get("CV_Link","")).strip()
        tr_u = str(row_sel.get("Transcript_Link","")).strip()
        info_cols = st.columns([3,1,1])
        info_cols[0].markdown(f"**📧** {row_sel.get('Email','-')}  &nbsp;|&nbsp;  **📱** {row_sel.get('Phone','-')}  &nbsp;|&nbsp;  **📅** {row_sel.get('Submission Date','-')}")
        if cv_u and cv_u != "nan":
            info_cols[1].link_button("📄 CV", cv_u, use_container_width=True)
        if tr_u and tr_u != "nan":
            info_cols[2].link_button("📋 Transcript", tr_u, use_container_width=True)
 
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("🌟 Overall Score",   f"{row_sel['Overall']}")
        m2.metric("🧠 Logical Thinking", f"{row_sel['LT_score']:.2f}")
        m3.metric("📊 Analytical Skills",f"{row_sel['AS_score']:.2f}")
        m4.metric("🗣️ Leadership",       f"{row_sel['LS_score']:.2f}")
 
        cats = ["Logical Thinking","Analytical Skills","Leadership"]
        vals = [row_sel["LT_score"],row_sel["AS_score"],row_sel["LS_score"]]
        fig = go.Figure(data=[go.Scatterpolar(
            r=vals+[vals[0]], theta=cats+[cats[0]], fill='toself',
            line=dict(color='#4A90D9',width=3), fillcolor='rgba(74,144,217,.18)',
            marker=dict(color='#4A90D9',size=8)
        )])
        fig.update_layout(
            height=450,
            polar=dict(bgcolor='rgba(13,31,60,.6)',
                radialaxis=dict(visible=True,range=[0,100],tickfont=dict(color='#6B8BAF',size=12),gridcolor='rgba(74,144,217,.15)',linecolor='rgba(74,144,217,.2)'),
                angularaxis=dict(tickfont=dict(color='#A8B8D0',size=14,family='DM Sans'),gridcolor='rgba(74,144,217,.12)',linecolor='rgba(74,144,217,.2)')
            ),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False,
            margin=dict(t=40,b=40,l=40,r=40)
        )
        st.plotly_chart(fig, use_container_width=True, config={'scrollZoom':True,'displayModeBar':True})
 
        if st.button("📈 Buka di Pop-up Layar Penuh", type="secondary"):
            show_popup_detail(row_sel)
    else:
        st.info("Tidak ada kandidat yang cocok dengan pencarian.")
 
else:
    st.markdown("""
    <div style="margin-top:4rem;text-align:center;padding:4rem 2rem;
        background:rgba(13,31,60,.5);border:1px solid rgba(74,144,217,.15);
        border-radius:16px;max-width:540px;margin-left:auto;margin-right:auto;">
        <div style="font-size:2.5rem;margin-bottom:1rem;">📂</div>
        <div style="font-family:'DM Sans',sans-serif;font-size:1.1rem;font-weight:600;color:#E8EDF5;margin-bottom:.5rem;">Unggah File CSV</div>
        <div style="font-size:.875rem;color:#6B8BAF;line-height:1.6;">Silakan unggah file CSV kandidat<br>melalui sidebar untuk memulai penilaian.</div>
    </div>""", unsafe_allow_html=True)
 
