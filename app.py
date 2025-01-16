import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="Timesheets Dashboard", layout="wide")

# Add custom CSS for Poppins font and styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
        
        * {font-family: 'Poppins', sans-serif !important;}
        
        /* Heading styles */
        h1, h3, .viz-header {
            font-weight: 700 !important;
        }
        
        h1 {
            font-size: 24px !important;
            margin-bottom: 20px !important;
        }
        
        h3 {
            font-size: 16px !important;
            margin-bottom: 0 !important;
        }
        
        /* Date input styling */
        .stDateInput > label {
            font-size: 14px !important;
        }
        
        .stDateInput input {
            font-size: 14px !important;
            min-width: 300px !important;
        }
        
        /* Metric styling */
        .metric-container {
            background-color: white;
            padding: 20px;
            border-radius: 0;
            border: 1px solid #eee;
            box-shadow: none;
            text-align: left;
        }
        
        .metric-value {
            font-size: 24px;
            font-weight: 700;
            color: #333;
            margin-bottom: 4px;
        }
        
        .metric-label {
            font-size: 12px;
            font-weight: 600;
            color: #666;
        }
        
        /* Sidebar styling */
        .filter-container {
            border: 1px solid #eee;
            margin: 10px 0;
            border-radius: 4px;
            padding: 10px;
        }
        
        /* Style the checkboxes within filter container */
        .filter-container div[data-testid="element-container"] {
            margin: 0;
            padding: 2px 0;
        }
        
        /* Remove extra padding from stVerticalBlock */
        .filter-container div[data-testid="stVerticalBlock"] {
            padding: 0;
            gap: 0;
        }
        
        /* Specific sidebar targeting to prevent affecting main content */
        [data-testid="stSidebar"] .stMarkdown {
            margin-bottom: 0 !important;
        }
        
        [data-testid="stSidebar"] h3 {
            margin-bottom: 0 !important;
        }
        
        /* Target all filter sections in sidebar */
        [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div:has(div.stCheckbox) {
            max-height: calc(8 * 32px) !important;  /* Height of 8 checkboxes */
            overflow-y: auto !important;
            border: 1.5px solid #ddd;  /* More visible border */
            border-radius: 4px;
            padding: 10px;
            margin: 10px 0;
            background-color: white;  /* Ensure white background */
            box-shadow: inset 0 0 4px rgba(0,0,0,0.05);  /* Subtle inset shadow */
        }

        /* Style the checkboxes for consistent height */
        [data-testid="stSidebar"] .stCheckbox {
            height: 32px;
            padding: 4px 0;
            margin: 0;
        }
        
        /* Filter container styling */
        .filter-box {
            border: 2px solid #ddd;
            border-radius: 4px;
            padding: 8px;
            margin: 10px 0;
            height: 240px;
            overflow-y: auto;
        }
        
        /* Style the checkboxes to be smaller and contained */
        .filter-box .stCheckbox {
            padding: 0;
            margin: 0;
            line-height: 1;
            font-size: 13px;
        }
        
        .filter-box .stCheckbox label {
            padding: 2px 0;
        }
        
        /* Remove default streamlit vertical spacing */
        .filter-box [data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }
        
        /* Filter container styling */
        .filter-wrapper {
            border: 2px solid #ddd;
            border-radius: 4px;
            margin: 10px 0;
        }
        
        .filter-scroll {
            height: 240px;
            overflow-y: auto;
            padding: 8px;
        }
        
        .filter-scroll .stCheckbox {
            font-size: 13px;
            padding: 1px 0;
        }
        
        /* Specific filter styling */
        [data-testid="stSidebar"] .stCheckbox {
            font-size: 13px;
            padding: 1px 0;
        }
        
        /* Filter container styling */
        .filter-container {
            border: 2px solid #ddd;
            border-radius: 4px;
            margin: 10px 0;
            height: 240px;
            overflow-y: auto;
            padding: 4px;  /* Reduced padding */
        }
        
        /* Style the checkboxes to be smaller and contained */
        [data-testid="stSidebar"] .stCheckbox {
            font-size: 13px;
            padding: 1px 0;
            margin: 0;
            line-height: 1;
        }
        
        [data-testid="stSidebar"] .stCheckbox label {
            padding: 2px 0;
        }
        
        /* Remove default streamlit spacing */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }
        
        /* Filter container base styling */
        .filter-container {
            border: 2px solid #ddd;
            border-radius: 4px;
            margin: 10px 0;
            height: 240px;
            padding: 4px;
        }
        
        /* Checkbox styling */
        [data-testid="stSidebar"] .stCheckbox {
            font-size: 13px;
            padding: 1px 0;
            margin: 0;
            line-height: 1;
        }
        
        /* Remove default spacing */
        [data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }
        
        /* Form container styling */
        [data-testid="stForm"] {
            border: 2px solid #ddd;
            border-radius: 0;  /* Square corners */
            padding: 4px;
            height: 240px;
            overflow-y: auto;
            margin-bottom: 20px;  /* Space below filter blocks */
        }
        
        [data-testid="stForm"] > div {
            overflow: visible;
        }
        
        /* Filter headings */
        [data-testid="stSidebar"] h3 {
            margin-bottom: 10px !important;  /* Space below headings */
        }
        
        /* Checkbox styling */
        [data-testid="stSidebar"] .stCheckbox {
            font-size: 12px !important;  /* Smaller font size */
            padding: 1px 0;
            margin: 0;
            line-height: 1;
        }
        
        /* Form button styling */
        [data-testid="stForm"] [data-testid="baseButton-secondary"],
        [data-testid="stForm"] [data-testid="baseButton-secondary"]:hover,
        [data-testid="stForm"] [data-testid="baseButton-secondary"]:active,
        [data-testid="stForm"] [data-testid="baseButton-secondary"]:focus {
            padding: 0 !important;
            height: 18px !important;
            min-height: 18px !important;
            font-size: 9px !important;
            border-radius: 0 !important;
            width: 100% !important;
            margin-top: 4px !important;
            line-height: 1 !important;
            border: 1px solid #ccc !important;
            box-shadow: none !important;
        }
        
        /* Date range styling */
        [data-testid="stDateInput"] {
            margin-bottom: 30px;
        }
        
        /* Add spacing between visualizations */
        .viz-header {
            margin-top: 40px !important;
            margin-bottom: 15px !important;
        }
        
        /* Add space after table */
        [data-testid="stDataFrame"] {
            margin-bottom: 40px;
        }
        
        /* Checkbox text truncation */
        .stCheckbox label p {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 180px;  /* Adjust based on your sidebar width */
            display: inline-block;
        }
    </style>
""", unsafe_allow_html=True)

# Load data
FILE_PATH = 'Feb - December 2024.xlsx'
@st.cache_data
def load_data(file_path):
    df = pd.read_excel(file_path, sheet_name="Sheet1")
    df['Date'] = pd.to_datetime(df['Date'])
    # Convert columns to strings to avoid type comparison issues
    df['Company'] = df['Company'].astype(str)
    df['Employee'] = df['Employee'].astype(str)
    df['Project'] = df['Project'].astype(str)
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    return df

data = load_data(FILE_PATH)

# Initialize the options dictionaries before using them
company_options = {}
employee_options = {}
project_options = {}

# Sidebar
with st.sidebar:
    st.image("zakheni-logo.png", width=150)
    st.markdown("---")
    
    # Company Filter
    st.subheader("Company")
    with st.form("company_filter", clear_on_submit=False):
        companies = sorted(data["Company"].astype(str).unique().tolist())
        for company in companies:
            truncated_text = company[:20] + ('...' if len(company) > 20 else '')
            company_options[company] = st.checkbox(
                truncated_text,
                value=True,
                key=f"company_{company}",
                help=company if len(company) > 20 else None
            )
        st.form_submit_button("Apply", type="secondary", use_container_width=True)

    # Employee Filter
    st.subheader("Employee")
    with st.form("employee_filter", clear_on_submit=False):
        employees = sorted(data["Employee"].astype(str).unique().tolist())
        for employee in employees:
            truncated_text = employee[:20] + ('...' if len(employee) > 20 else '')
            employee_options[employee] = st.checkbox(
                truncated_text,
                value=True,
                key=f"employee_{employee}",
                help=employee if len(employee) > 20 else None
            )
        st.form_submit_button("Apply", type="secondary", use_container_width=True)

    # Project Filter
    st.subheader("Project")
    with st.form("project_filter", clear_on_submit=False):
        projects = sorted(data["Project"].astype(str).unique().tolist())
        for project in projects:
            truncated_text = project[:20] + ('...' if len(project) > 20 else '')
            project_options[project] = st.checkbox(
                truncated_text,
                value=True,
                key=f"project_{project}",
                help=project if len(project) > 20 else None
            )
        st.form_submit_button("Apply", type="secondary", use_container_width=True)

# Main content
st.title("Timesheets")

# Date range selector
col1, col2 = st.columns([3, 2])
with col2:
    date_range = st.date_input(
        "Date Range",
        value=(data['Date'].min(), data['Date'].max()),
        min_value=data['Date'].min(),
        max_value=data['Date'].max(),
    )

# Apply filters
selected_companies = [comp for comp, selected in company_options.items() if selected]
selected_employees = [emp for emp, selected in employee_options.items() if selected]
selected_projects = [proj for proj, selected in project_options.items() if selected]

filtered_data = data[
    (data['Company'].isin(selected_companies)) &
    (data['Employee'].isin(selected_employees)) &
    (data['Project'].isin(selected_projects))
]

# Metrics
metrics_col1, metrics_col2, metrics_col3, metrics_col4, metrics_col5 = st.columns(5)

with metrics_col1:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{len(filtered_data['Company'].unique())}</div>
            <div class="metric-label">COMPANIES</div>
        </div>
    """, unsafe_allow_html=True)

with metrics_col2:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{len(filtered_data['Employee'].unique())}</div>
            <div class="metric-label">EMPLOYEES</div>
        </div>
    """, unsafe_allow_html=True)

with metrics_col3:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{len(filtered_data['Project'].unique())}</div>
            <div class="metric-label">PROJECTS</div>
        </div>
    """, unsafe_allow_html=True)

with metrics_col4:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{len(filtered_data)}</div>
            <div class="metric-label">TASKS</div>
        </div>
    """, unsafe_allow_html=True)

with metrics_col5:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{filtered_data['Quantity'].sum():,.0f}</div>
            <div class="metric-label">EFFORT</div>
        </div>
    """, unsafe_allow_html=True)

# Visualizations
st.markdown("---")

# Table Visualization
st.markdown('<p class="viz-header">Table Visualization</p>', unsafe_allow_html=True)
st.dataframe(filtered_data, use_container_width=True)

# First row of visualizations (60/40 split)
viz_row1_col1, viz_row1_col2 = st.columns([6, 4])

# Task Count by Employee (60%)
with viz_row1_col1:
    st.markdown('<p class="viz-header">Task Count by Employee</p>', unsafe_allow_html=True)
    task_counts = filtered_data.groupby("Employee")["Task"].count()
    fig = px.bar(
        x=task_counts.index,
        y=task_counts.values,
        labels={"x": "Employee", "y": "Number of Tasks"},
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Effort by Company (40%)
with viz_row1_col2:
    st.markdown('<p class="viz-header">Effort by Company</p>', unsafe_allow_html=True)
    effort_by_company = filtered_data.groupby("Company")["Quantity"].sum()
    fig = px.bar(
        x=effort_by_company.index,
        y=effort_by_company.values,
        labels={"x": "Company", "y": "Total Effort"},
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Second row of visualizations (60/40 split)
viz_row2_col1, viz_row2_col2 = st.columns([6, 4])

# Effort by Employee (60%)
with viz_row2_col1:
    st.markdown('<p class="viz-header">Effort by Employee</p>', unsafe_allow_html=True)
    effort_by_employee = filtered_data.groupby("Employee")["Quantity"].sum()
    fig = px.bar(
        x=effort_by_employee.index,
        y=effort_by_employee.values,
        labels={"x": "Employee", "y": "Total Effort"},
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Expenditure Type Breakdown (40%)
with viz_row2_col2:
    st.markdown('<p class="viz-header">Expenditure Type Breakdown</p>', unsafe_allow_html=True)
    expenditure_counts = filtered_data.groupby("Expenditure Type")["Quantity"].sum()
    expenditure_percentages = (expenditure_counts / expenditure_counts.sum() * 100).round(1)
    
    fig = px.pie(
        values=expenditure_percentages.values,
        names=expenditure_percentages.index,
        hole=0.4
    )
    fig.update_traces(textposition='inside', textinfo='percent')
    fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, b=0, l=0, r=0),
        height=250
    )
    st.plotly_chart(fig, use_container_width=True)
