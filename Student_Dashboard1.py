import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Student Performance Database",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to bottom right, #1e293b, #334155, #1e293b);
    }
    h1 {
        color: white;
        font-size: 3rem;
    }
    h2 {
        color: #60a5fa;
    }
    h3 {
        color: #34d399;
    }
    </style>
    """, unsafe_allow_html=True)

# Load the actual CSV data
@st.cache_data
def load_student_data():
    # You need to upload the CSV file to the same directory as your script
    # Or use the file uploader below
    try:
        df = pd.read_csv('StudentsPerformance_Updated.csv')
        return df
    except:
        return None

# File uploader option
uploaded_file = st.file_uploader("Upload StudentsPerformance_Updated.csv", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = load_student_data()

if df is not None:
    # Header
    st.markdown("<h1>📊 Student Performance Database</h1>", unsafe_allow_html=True)
    st.markdown(f"**Analyzing {len(df)} student records - INPUT FILTERS & GET OUTPUT RESULTS**")
    st.markdown("---")

    # INPUT SECTION
    st.markdown("<h2>🔍 INPUT: Filters</h2>", unsafe_allow_html=True)

    # Create filter columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        gender_filter = st.selectbox(
            "Gender",
            options=['All'] + sorted(list(df['gender'].unique()))
        )
        
        race_filter = st.selectbox(
            "Race/Ethnicity",
            options=['All'] + sorted(list(df['race/ethnicity'].unique()))
        )

    with col2:
        education_filter = st.selectbox(
            "Parental Education",
            options=['All'] + sorted(list(df['parental level of education'].unique()))
        )
        
        lunch_filter = st.selectbox(
            "Lunch Program",
            options=['All'] + sorted(list(df['lunch'].unique()))
        )

    with col3:
        prep_filter = st.selectbox(
            "Test Prep",
            options=['All'] + sorted(list(df['test preparation course'].unique()))
        )
        
        attendance_min = st.number_input("Attendance Min", min_value=0, max_value=10, value=0, step=1)

    with col4:
        attendance_max = st.number_input("Attendance Max", min_value=0, max_value=10, value=10, step=1)
        
        study_hours_min = st.number_input("Study Hours Min", min_value=0.0, max_value=12.0, value=0.0, step=0.1)

    # Score filters in expandable section
    with st.expander("📝 Score Range Filters", expanded=False):
        col5, col6, col7 = st.columns(3)
        
        with col5:
            st.write("**Math Score**")
            math_min = st.number_input("Math Min", min_value=0, max_value=100, value=0, step=1)
            math_max = st.number_input("Math Max", min_value=0, max_value=100, value=100, step=1)
        
        with col6:
            st.write("**Reading Score**")
            reading_min = st.number_input("Reading Min", min_value=0, max_value=100, value=0, step=1)
            reading_max = st.number_input("Reading Max", min_value=0, max_value=100, value=100, step=1)
        
        with col7:
            st.write("**Writing Score**")
            writing_min = st.number_input("Writing Min", min_value=0, max_value=100, value=0, step=1)
            writing_max = st.number_input("Writing Max", min_value=0, max_value=100, value=100, step=1)

    col8, col9 = st.columns([1, 1])
    with col8:
        study_hours_max = st.number_input("Study Hours Max", min_value=0.0, max_value=12.0, value=12.0, step=0.1)
    
    with col9:
        avg_score_min = st.number_input("Avg Score Min", min_value=0.0, max_value=100.0, value=0.0, step=1.0)

    # Reset button
    if st.button("🔄 Reset All Filters", type="secondary"):
        st.rerun()

    st.markdown("---")

    # Apply filters
    filtered_df = df.copy()

    if gender_filter != 'All':
        filtered_df = filtered_df[filtered_df['gender'] == gender_filter]

    if race_filter != 'All':
        filtered_df = filtered_df[filtered_df['race/ethnicity'] == race_filter]

    if education_filter != 'All':
        filtered_df = filtered_df[filtered_df['parental level of education'] == education_filter]

    if lunch_filter != 'All':
        filtered_df = filtered_df[filtered_df['lunch'] == lunch_filter]

    if prep_filter != 'All':
        filtered_df = filtered_df[filtered_df['test preparation course'] == prep_filter]

    filtered_df = filtered_df[
        (filtered_df['math score'] >= math_min) & 
        (filtered_df['math score'] <= math_max) &
        (filtered_df['reading score'] >= reading_min) & 
        (filtered_df['reading score'] <= reading_max) &
        (filtered_df['writing score'] >= writing_min) & 
        (filtered_df['writing score'] <= writing_max) &
        (filtered_df['Attendance'] >= attendance_min) &
        (filtered_df['Attendance'] <= attendance_max) &
        (filtered_df['StudyHours'] >= study_hours_min) &
        (filtered_df['StudyHours'] <= study_hours_max) &
        (filtered_df['avg_Score'] >= avg_score_min)
    ]

    # OUTPUT SECTION
    if len(filtered_df) > 0:
        st.markdown("<h2>📈 OUTPUT: Results</h2>", unsafe_allow_html=True)
        
        # Statistics Cards
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                label="Records Found",
                value=len(filtered_df)
            )
        
        with col2:
            st.metric(
                label="Avg Math",
                value=f"{filtered_df['math score'].mean():.2f}"
            )
        
        with col3:
            st.metric(
                label="Avg Reading",
                value=f"{filtered_df['reading score'].mean():.2f}"
            )
        
        with col4:
            st.metric(
                label="Avg Study Hours",
                value=f"{filtered_df['StudyHours'].mean():.2f}"
            )
        
        with col5:
            st.metric(
                label="Avg Attendance",
                value=f"{filtered_df['Attendance'].mean():.2f}"
            )
        
        st.markdown("---")
        
        # Charts Section
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Score Analysis", "📈 Correlations", "🎯 Performance", "📚 Study Patterns"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Subject Score Distribution")
                chart_data = pd.DataFrame({
                    'Subject': ['Math', 'Reading', 'Writing'],
                    'Average': [
                        filtered_df['math score'].mean(),
                        filtered_df['reading score'].mean(),
                        filtered_df['writing score'].mean()
                    ]
                })
                
                fig = px.bar(
                    chart_data,
                    x='Subject',
                    y='Average',
                    color='Subject',
                    color_discrete_map={
                        'Math': '#3b82f6',
                        'Reading': '#10b981',
                        'Writing': '#f59e0b'
                    },
                    title="Average Scores by Subject"
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### Average Score Distribution")
                fig = px.histogram(
                    filtered_df,
                    x='avg_Score',
                    nbins=20,
                    title="Distribution of Average Scores",
                    color_discrete_sequence=['#8b5cf6']
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Study Hours vs Average Score")
                fig = px.scatter(
                    filtered_df,
                    x='StudyHours',
                    y='avg_Score',
                    color='test preparation course',
                    title="Study Hours Impact on Performance",
                    hover_data=['gender', 'race/ethnicity'],
                    color_discrete_map={'none': '#ef4444', 'completed': '#10b981'}
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### Attendance vs Average Score")
                fig = px.scatter(
                    filtered_df,
                    x='Attendance',
                    y='avg_Score',
                    color='lunch',
                    title="Attendance Impact on Performance",
                    hover_data=['gender', 'race/ethnicity'],
                    color_discrete_map={'standard': '#3b82f6', 'free/reduced': '#f59e0b'}
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Performance by Test Prep")
                prep_data = filtered_df.groupby('test preparation course')['avg_Score'].mean().reset_index()
                fig = px.bar(
                    prep_data,
                    x='test preparation course',
                    y='avg_Score',
                    color='test preparation course',
                    title="Test Prep Impact",
                    color_discrete_map={'none': '#ef4444', 'completed': '#10b981'}
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### Performance by Lunch Program")
                lunch_data = filtered_df.groupby('lunch')['avg_Score'].mean().reset_index()
                fig = px.bar(
                    lunch_data,
                    x='lunch',
                    y='avg_Score',
                    color='lunch',
                    title="Lunch Program Impact",
                    color_discrete_map={'standard': '#3b82f6', 'free/reduced': '#f59e0b'}
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Study Hours Distribution")
                fig = px.histogram(
                    filtered_df,
                    x='StudyHours',
                    nbins=20,
                    title="Study Hours Frequency",
                    color_discrete_sequence=['#8b5cf6']
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### Attendance Distribution")
                fig = px.histogram(
                    filtered_df,
                    x='Attendance',
                    nbins=11,
                    title="Attendance Frequency",
                    color_discrete_sequence=['#3b82f6']
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Results Table
        st.markdown(f"### 📋 All Student Records ({len(filtered_df)} total)")
        
        # Display dataframe with better formatting
        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=400,
            column_config={
                "math score": st.column_config.NumberColumn("Math", format="%.0f"),
                "reading score": st.column_config.NumberColumn("Reading", format="%.0f"),
                "writing score": st.column_config.NumberColumn("Writing", format="%.0f"),
                "avg_Score": st.column_config.NumberColumn("Avg Score", format="%.2f"),
                "Attendance": st.column_config.NumberColumn("Attendance", format="%.0f"),
                "StudyHours": st.column_config.NumberColumn("Study Hours", format="%.1f"),
            }
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name="student_performance_results.csv",
            mime="text/csv",
        )
        
        # Correlation Analysis
        st.markdown("---")
        st.markdown("### 🔗 Correlation Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            corr_study_avg = filtered_df['StudyHours'].corr(filtered_df['avg_Score'])
            st.metric("Study Hours ↔ Avg Score", f"{corr_study_avg:.3f}")
        
        with col2:
            corr_attend_avg = filtered_df['Attendance'].corr(filtered_df['avg_Score'])
            st.metric("Attendance ↔ Avg Score", f"{corr_attend_avg:.3f}")
        
        with col3:
            corr_math_read = filtered_df['math score'].corr(filtered_df['reading score'])
            st.metric("Math ↔ Reading", f"{corr_math_read:.3f}")

    else:
        st.error("❌ No students match your filter criteria. Please adjust your filters.")

    # Footer
    st.markdown("---")
    st.markdown("**💡 Key Features:**")
    st.markdown("""
    - Filter by demographics, test prep, lunch program
    - Analyze study hours and attendance impact
    - View correlations between factors
    - Download filtered results
    - Interactive visualizations
    """)

else:
    st.error("⚠️ Please upload the StudentsPerformance_Updated.csv file to begin analysis.")
    st.info("Use the file uploader above to upload your CSV file.")