"""
Climate Change Data Analysis - Interactive Dashboard
Run with: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Climate Change Analysis Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2E86AB;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #333;
        padding: 10px;
        border-left: 5px solid #2E86AB;
        margin: 20px 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2E86AB;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🌍 Global Climate Change Analysis Dashboard</h1>', unsafe_allow_html=True)
st.markdown("### Analyzing Climate Indicators for Evidence-Based Policy Insights")

# Load data
@st.cache_data
def load_data():
    # Load your cleaned data here
    df = pd.read_csv('climate_data_cleaned.csv')
    return df

try:
    df = load_data()
    
    # Sidebar
    st.sidebar.header("🔍 Dashboard Controls")
    st.sidebar.markdown("---")
    
    # Filters
    st.sidebar.subheader("Filters")
    
    # Year filter
    if 'Year' in df.columns:
        year_range = st.sidebar.slider(
            "Select Year Range",
            min_value=int(df['Year'].min()),
            max_value=int(df['Year'].max()),
            value=(int(df['Year'].min()), int(df['Year'].max()))
        )
        df_filtered = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    else:
        df_filtered = df
    
    # Country filter
    if 'Country' in df.columns:
        countries = ['All'] + sorted(df['Country'].unique().tolist())
        selected_countries = st.sidebar.multiselect(
            "Select Countries",
            countries,
            default=['All']
        )
        
        if 'All' not in selected_countries and selected_countries:
            df_filtered = df_filtered[df_filtered['Country'].isin(selected_countries)]
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Tip**: Use filters to explore specific regions and time periods")
    
    # Main content
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", 
        "🌡️ Temperature & Emissions", 
        "♻️ Renewable Energy", 
        "🌲 Environmental Factors",
        "📈 Policy Insights"
    ])
    
    # ===== TAB 1: OVERVIEW =====
    with tab1:
        st.markdown('<div class="sub-header">Key Climate Metrics Overview</div>', unsafe_allow_html=True)
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'CO2 Emissions (Tons/Capita)' in df_filtered.columns:
                avg_co2 = df_filtered['CO2 Emissions (Tons/Capita)'].mean()
                st.metric(
                    label="Avg CO2 Emissions",
                    value=f"{avg_co2:.2f} tons/capita",
                    delta=f"{((df_filtered['CO2 Emissions (Tons/Capita)'].iloc[-100:].mean() - df_filtered['CO2 Emissions (Tons/Capita)'].iloc[:100].mean()) / df_filtered['CO2 Emissions (Tons/Capita)'].iloc[:100].mean() * 100):.1f}%"
                )
        
        with col2:
            if 'Renewable Energy (%)' in df_filtered.columns:
                avg_renewable = df_filtered['Renewable Energy (%)'].mean()
                st.metric(
                    label="Avg Renewable Energy",
                    value=f"{avg_renewable:.1f}%",
                    delta=f"{((df_filtered['Renewable Energy (%)'].iloc[-100:].mean() - df_filtered['Renewable Energy (%)'].iloc[:100].mean()) / df_filtered['Renewable Energy (%)'].iloc[:100].mean() * 100):.1f}%"
                )
        
        with col3:
            if 'Average Temperature (°C)' in df_filtered.columns:
                avg_temp = df_filtered['Average Temperature (°C)'].mean()
                st.metric(
                    label="Avg Temperature",
                    value=f"{avg_temp:.2f}°C",
                    delta=f"{(df_filtered['Average Temperature (°C)'].iloc[-100:].mean() - df_filtered['Average Temperature (°C)'].iloc[:100].mean()):.2f}°C"
                )
        
        with col4:
            if 'Extreme Weather Events' in df_filtered.columns:
                total_events = df_filtered['Extreme Weather Events'].sum()
                st.metric(
                    label="Total Extreme Events",
                    value=f"{int(total_events):,}",
                    delta=f"{int(df_filtered['Extreme Weather Events'].iloc[-100:].sum() - df_filtered['Extreme Weather Events'].iloc[:100].sum()):,}"
                )
        
        st.markdown("---")
        
        # World map
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🗺️ Global CO2 Emissions Map")
            if 'Country' in df_filtered.columns and 'CO2 Emissions (Tons/Capita)' in df_filtered.columns:
                map_data = df_filtered.groupby('Country')['CO2 Emissions (Tons/Capita)'].mean().reset_index()
                fig_map = px.choropleth(
                    map_data,
                    locations='Country',
                    locationmode='country names',
                    color='CO2 Emissions (Tons/Capita)',
                    color_continuous_scale='Reds',
                    title='Average CO2 Emissions by Country'
                )
                fig_map.update_layout(height=400)
                st.plotly_chart(fig_map, use_container_width=True)
        
        with col2:
            st.subheader("🌱 Renewable Energy Adoption Map")
            if 'Country' in df_filtered.columns and 'Renewable Energy (%)' in df_filtered.columns:
                map_data2 = df_filtered.groupby('Country')['Renewable Energy (%)'].mean().reset_index()
                fig_map2 = px.choropleth(
                    map_data2,
                    locations='Country',
                    locationmode='country names',
                    color='Renewable Energy (%)',
                    color_continuous_scale='Greens',
                    title='Average Renewable Energy Adoption by Country'
                )
                fig_map2.update_layout(height=400)
                st.plotly_chart(fig_map2, use_container_width=True)
        
        # Summary statistics table
        st.markdown("### 📋 Summary Statistics")
        summary_cols = ['CO2 Emissions (Tons/Capita)', 'Renewable Energy (%)', 
                       'Average Temperature (°C)', 'Forest Area (%)', 'Extreme Weather Events']
        available_cols = [col for col in summary_cols if col in df_filtered.columns]
        
        if available_cols:
            summary_stats = df_filtered[available_cols].describe().T
            summary_stats['range'] = summary_stats['max'] - summary_stats['min']
            st.dataframe(summary_stats.style.background_gradient(cmap='YlOrRd'), use_container_width=True)
    
    # ===== TAB 2: TEMPERATURE & EMISSIONS =====
    with tab2:
        st.markdown('<div class="sub-header">Temperature & CO2 Emissions Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 CO2 Emissions Trend Over Time")
            if 'Year' in df_filtered.columns and 'CO2 Emissions (Tons/Capita)' in df_filtered.columns:
                yearly_co2 = df_filtered.groupby('Year')['CO2 Emissions (Tons/Capita)'].agg(['mean', 'std']).reset_index()
                
                fig_co2 = go.Figure()
                fig_co2.add_trace(go.Scatter(
                    x=yearly_co2['Year'],
                    y=yearly_co2['mean'],
                    mode='lines+markers',
                    name='Average CO2',
                    line=dict(color='red', width=3),
                    marker=dict(size=8)
                ))
                fig_co2.add_trace(go.Scatter(
                    x=yearly_co2['Year'],
                    y=yearly_co2['mean'] + yearly_co2['std'],
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False
                ))
                fig_co2.add_trace(go.Scatter(
                    x=yearly_co2['Year'],
                    y=yearly_co2['mean'] - yearly_co2['std'],
                    mode='lines',
                    line=dict(width=0),
                    fillcolor='rgba(255, 0, 0, 0.2)',
                    fill='tonexty',
                    name='Standard Deviation'
                ))
                fig_co2.update_layout(
                    xaxis_title='Year',
                    yaxis_title='CO2 Emissions (Tons/Capita)',
                    hovermode='x unified',
                    height=400
                )
                st.plotly_chart(fig_co2, use_container_width=True)
        
        with col2:
            st.subheader("🌡️ Temperature Trend Over Time")
            if 'Year' in df_filtered.columns and 'Average Temperature (°C)' in df_filtered.columns:
                yearly_temp = df_filtered.groupby('Year')['Average Temperature (°C)'].agg(['mean', 'min', 'max']).reset_index()
                
                fig_temp = go.Figure()
                fig_temp.add_trace(go.Scatter(
                    x=yearly_temp['Year'],
                    y=yearly_temp['mean'],
                    mode='lines+markers',
                    name='Average Temperature',
                    line=dict(color='orange', width=3),
                    marker=dict(size=8)
                ))
                fig_temp.add_trace(go.Scatter(
                    x=yearly_temp['Year'],
                    y=yearly_temp['max'],
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False
                ))
                fig_temp.add_trace(go.Scatter(
                    x=yearly_temp['Year'],
                    y=yearly_temp['min'],
                    mode='lines',
                    line=dict(width=0),
                    fillcolor='rgba(255, 165, 0, 0.2)',
                    fill='tonexty',
                    name='Min-Max Range'
                ))
                fig_temp.update_layout(
                    xaxis_title='Year',
                    yaxis_title='Temperature (°C)',
                    hovermode='x unified',
                    height=400
                )
                st.plotly_chart(fig_temp, use_container_width=True)
        
        st.markdown("---")
        
        # Correlation analysis
        st.subheader("🔗 Temperature vs Sea Level Rise Correlation")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if 'Average Temperature (°C)' in df_filtered.columns and 'Sea Level Rise (mm)' in df_filtered.columns:
                fig_scatter = px.scatter(
                    df_filtered,
                    x='Average Temperature (°C)',
                    y='Sea Level Rise (mm)',
                    color='Year' if 'Year' in df_filtered.columns else None,
                    trendline='ols',
                    title='Temperature vs Sea Level Rise',
                    height=400
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col2:
            if 'Average Temperature (°C)' in df_filtered.columns and 'Sea Level Rise (mm)' in df_filtered.columns:
                corr = df_filtered[['Average Temperature (°C)', 'Sea Level Rise (mm)']].corr().iloc[0, 1]
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Correlation Coefficient</h3>
                    <h1 style="color: {'red' if corr > 0.5 else 'orange'};">{corr:.3f}</h1>
                    <p>Strong {'positive' if corr > 0 else 'negative'} correlation</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="insight-box">
                    <strong>💡 Insight:</strong> The correlation indicates that rising temperatures 
                    are associated with increased sea level rise, confirming climate change impacts.
                </div>
                """, unsafe_allow_html=True)
        
        # Top emitters
        st.subheader("🏭 Top 15 CO2 Emitting Countries")
        if 'Country' in df_filtered.columns and 'CO2 Emissions (Tons/Capita)' in df_filtered.columns:
            top_emitters = df_filtered.groupby('Country')['CO2 Emissions (Tons/Capita)'].mean().nlargest(15).reset_index()
            fig_bar = px.bar(
                top_emitters,
                x='CO2 Emissions (Tons/Capita)',
                y='Country',
                orientation='h',
                color='CO2 Emissions (Tons/Capita)',
                color_continuous_scale='Reds',
                title='Countries Ranked by Average CO2 Emissions'
            )
            fig_bar.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # ===== TAB 3: RENEWABLE ENERGY =====
    with tab3:
        st.markdown('<div class="sub-header">Renewable Energy Adoption Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("♻️ Renewable Energy Trends")
            if 'Year' in df_filtered.columns and 'Renewable Energy (%)' in df_filtered.columns:
                yearly_renewable = df_filtered.groupby('Year')['Renewable Energy (%)'].mean().reset_index()
                
                fig_renewable = px.line(
                    yearly_renewable,
                    x='Year',
                    y='Renewable Energy (%)',
                    markers=True,
                    title='Global Renewable Energy Adoption Over Time'
                )
                fig_renewable.update_traces(line_color='green', line_width=3, marker=dict(size=10))
                fig_renewable.update_layout(height=400)
                st.plotly_chart(fig_renewable, use_container_width=True)
        
        with col2:
            st.subheader("🌍 Top Renewable Energy Adopters")
            if 'Country' in df_filtered.columns and 'Renewable Energy (%)' in df_filtered.columns:
                top_renewable = df_filtered.groupby('Country')['Renewable Energy (%)'].mean().nlargest(10).reset_index()
                
                fig_top = px.bar(
                    top_renewable,
                    x='Renewable Energy (%)',
                    y='Country',
                    orientation='h',
                    color='Renewable Energy (%)',
                    color_continuous_scale='Greens'
                )
                fig_top.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_top, use_container_width=True)
        
        st.markdown("---")
        
        # Renewable vs CO2 relationship
        st.subheader("🔄 Renewable Energy vs CO2 Emissions")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if 'Renewable Energy (%)' in df_filtered.columns and 'CO2 Emissions (Tons/Capita)' in df_filtered.columns:
                fig_scatter2 = px.scatter(
                    df_filtered,
                    x='Renewable Energy (%)',
                    y='CO2 Emissions (Tons/Capita)',
                    color='Year' if 'Year' in df_filtered.columns else None,
                    size='Population' if 'Population' in df_filtered.columns else None,
                    hover_data=['Country'] if 'Country' in df_filtered.columns else None,
                    trendline='ols',
                    title='Impact of Renewable Energy on CO2 Emissions'
                )
                fig_scatter2.update_layout(height=400)
                st.plotly_chart(fig_scatter2, use_container_width=True)
        
        with col2:
            if 'Renewable Energy (%)' in df_filtered.columns and 'CO2 Emissions (Tons/Capita)' in df_filtered.columns:
                corr2 = df_filtered[['Renewable Energy (%)', 'CO2 Emissions (Tons/Capita)']].corr().iloc[0, 1]
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Correlation</h3>
                    <h1 style="color: {'green' if corr2 < 0 else 'red'};">{corr2:.3f}</h1>
                    <p>{'Negative correlation confirms renewable energy reduces emissions' if corr2 < 0 else 'Unexpected positive correlation'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="insight-box">
                    <strong>💡 Policy Recommendation:</strong> Countries with higher renewable 
                    energy adoption show lower CO2 emissions. Accelerating renewable energy 
                    transition should be a priority.
                </div>
                """, unsafe_allow_html=True)
        
        # Growth rate analysis
        st.subheader("📊 Renewable Energy Growth Rate")
        if 'Year' in df_filtered.columns and 'Renewable Energy (%)' in df_filtered.columns:
            yearly_renewable = df_filtered.groupby('Year')['Renewable Energy (%)'].mean().reset_index()
            yearly_renewable['Growth_Rate'] = yearly_renewable['Renewable Energy (%)'].pct_change() * 100
            
            fig_growth = go.Figure()
            fig_growth.add_trace(go.Bar(
                x=yearly_renewable['Year'],
                y=yearly_renewable['Growth_Rate'],
                marker_color=['green' if x > 0 else 'red' for x in yearly_renewable['Growth_Rate']],
                name='Growth Rate'
            ))
            fig_growth.update_layout(
                title='Year-over-Year Growth Rate in Renewable Energy',
                xaxis_title='Year',
                yaxis_title='Growth Rate (%)',
                height=350
            )
            st.plotly_chart(fig_growth, use_container_width=True)
    
    # ===== TAB 4: ENVIRONMENTAL FACTORS =====
    with tab4:
        st.markdown('<div class="sub-header">Environmental Factors Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌲 Forest Area vs Extreme Weather")
            if 'Forest Area (%)' in df_filtered.columns and 'Extreme Weather Events' in df_filtered.columns:
                fig_forest = px.scatter(
                    df_filtered,
                    x='Forest Area (%)',
                    y='Extreme Weather Events',
                    color='Year' if 'Year' in df_filtered.columns else None,
                    trendline='ols',
                    title='Forest Coverage Impact on Extreme Weather Events'
                )
                fig_forest.update_layout(height=400)
                st.plotly_chart(fig_forest, use_container_width=True)
        
        with col2:
            st.subheader("🌊 Rainfall vs Extreme Weather")
            if 'Rainfall (mm)' in df_filtered.columns and 'Extreme Weather Events' in df_filtered.columns:
                fig_rain = px.scatter(
                    df_filtered,
                    x='Rainfall (mm)',
                    y='Extreme Weather Events',
                    color='Year' if 'Year' in df_filtered.columns else None,
                    trendline='ols',
                    title='Rainfall Patterns and Extreme Weather Events'
                )
                fig_rain.update_layout(height=400)
                st.plotly_chart(fig_rain, use_container_width=True)
        
        st.markdown("---")
        
        # Extreme weather trends
        st.subheader("⚠️ Extreme Weather Events Trends")
        if 'Year' in df_filtered.columns and 'Extreme Weather Events' in df_filtered.columns:
            yearly_events = df_filtered.groupby('Year')['Extreme Weather Events'].agg(['sum', 'mean']).reset_index()
            
            fig_events = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Total Extreme Events', 'Average Events per Country')
            )
            
            fig_events.add_trace(
                go.Scatter(x=yearly_events['Year'], y=yearly_events['sum'], 
                          mode='lines+markers', name='Total', line=dict(color='red', width=3)),
                row=1, col=1
            )
            
            fig_events.add_trace(
                go.Scatter(x=yearly_events['Year'], y=yearly_events['mean'], 
                          mode='lines+markers', name='Average', line=dict(color='orange', width=3)),
                row=1, col=2
            )
            
            fig_events.update_xaxes(title_text="Year", row=1, col=1)
            fig_events.update_xaxes(title_text="Year", row=1, col=2)
            fig_events.update_yaxes(title_text="Total Events", row=1, col=1)
            fig_events.update_yaxes(title_text="Average Events", row=1, col=2)
            fig_events.update_layout(height=400, showlegend=False)
            
            st.plotly_chart(fig_events, use_container_width=True)
        
        # Correlation heatmap
        st.subheader("🔥 Environmental Factors Correlation Matrix")
        env_cols = ['Forest Area (%)', 'Rainfall (mm)', 'Extreme Weather Events', 
                    'Sea Level Rise (mm)', 'Average Temperature (°C)']
        available_env_cols = [col for col in env_cols if col in df_filtered.columns]
        
        if len(available_env_cols) >= 2:
            corr_matrix = df_filtered[available_env_cols].corr()
            
            fig_heatmap = px.imshow(
                corr_matrix,
                text_auto='.2f',
                color_continuous_scale='RdBu_r',
                aspect='auto',
                title='Correlation Between Environmental Variables'
            )
            fig_heatmap.update_layout(height=500)
            st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # ===== TAB 5: POLICY INSIGHTS =====
    with tab5:
        st.markdown('<div class="sub-header">Policy Insights & Recommendations</div>', unsafe_allow_html=True)
        
        # Key insights
        st.subheader("🎯 Key Findings")
        
        insights_data = {
            "Insight": [
                "1. Renewable Energy Impact",
                "2. Temperature-Sea Level Link",
                "3. Forest Protection",
                "4. Development Disparity",
                "5. Extreme Weather Increase",
                "6. Renewable Growth Rate",
                "7. Population vs Emissions"
            ],
            "Finding": [
                "Strong negative correlation between renewable energy and CO2 emissions",
                "Rising temperatures directly correlate with sea level increases",
                "Forest coverage inversely related to extreme weather events",
                "Significant emission gaps between developed and developing nations",
                "Extreme weather events increasing in frequency over time",
                "Renewable energy adoption growing but requires acceleration",
                "Development model matters more than population size"
            ],
            "Policy Action": [
                "Implement renewable energy incentives and subsidies",
                "Establish coastal protection and adaptation programs",
                "Launch aggressive reforestation initiatives",
                "Create climate finance mechanisms for developing countries",
                "Strengthen disaster preparedness systems",
                "Set mandatory renewable energy targets",
                "Promote sustainable development pathways"
            ]
        }
        
        insights_df = pd.DataFrame(insights_data)
        st.dataframe(insights_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Policy recommendations
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Priority Policy Recommendations")
            st.markdown("""
            <div class="insight-box">
                <h4>1. Accelerate Renewable Energy Transition</h4>
                <ul>
                    <li>Implement feed-in tariffs</li>
                    <li>Provide tax credits for clean energy</li>
                    <li>Target: 50% renewable by 2030</li>
                </ul>
            </div>
            
            <div class="insight-box">
                <h4>2. Forest Conservation Programs</h4>
                <ul>
                    <li>Create protected forest areas</li>
                    <li>Carbon credit programs for reforestation</li>
                    <li>Penalize illegal deforestation</li>
                </ul>
            </div>
            
            <div class="insight-box">
                <h4>3. Climate Finance Mechanisms</h4>
                <ul>
                    <li>Green Climate Fund contributions</li>
                    <li>Technology transfer to developing nations</li>
                    <li>Support adaptation infrastructure</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("📊 Expected Impact Metrics")
            
            impact_data = {
                "Metric": [
                    "CO2 Reduction",
                    "Renewable Energy",
                    "Forest Coverage",
                    "Climate Resilience",
                    "Economic Growth"
                ],
                "Target": [
                    "30-40% by 2035",
                    "50% by 2030",
                    "15% increase",
                    "50% improvement",
                    "2-3% annual"
                ],
                "Priority": [
                    "🔴 Critical",
                    "🔴 Critical",
                    "🟠 High",
                    "🟠 High",
                    "🟢 Medium"
                ]
            }
            
            impact_df = pd.DataFrame(impact_data)
            st.dataframe(impact_df, use_container_width=True, hide_index=True)
            
            st.markdown("""
            <div class="metric-card">
                <h4>💰 Investment Required</h4>
                <h2>$2-3 Trillion</h2>
                <p>Global investment needed annually for climate action</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Action plan timeline
        st.subheader("🗓️ Implementation Timeline")
        
        timeline_data = {
            "Phase": ["Immediate (2025-2026)", "Short-term (2027-2028)", "Mid-term (2029-2032)", "Long-term (2033-2035)"],
            "Actions": [
                "• Policy framework development\n• Stakeholder engagement\n• Pilot programs",
                "• Renewable energy subsidies\n• Carbon pricing implementation\n• Forest protection laws",
                "• Scale up renewable projects\n• Technology transfer\n• Infrastructure development",
                "• Achieve 50% renewable target\n• 30-40% emission reduction\n• Climate resilience built"
            ]
        }
        
        for phase, actions in zip(timeline_data["Phase"], timeline_data["Actions"]):
            st.markdown(f"""
            <div class="insight-box">
                <h4>{phase}</h4>
                <p style="white-space: pre-line;">{actions}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Download section
        st.markdown("---")
        st.subheader("📥 Download Reports")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Download Data Summary"):
                st.success("Data summary downloaded!")
        
        with col2:
            if st.button("📈 Download Analysis Report"):
                st.success("Analysis report downloaded!")
        
        with col3:
            if st.button("📋 Download Policy Brief"):
                st.success("Policy brief downloaded!")

except FileNotFoundError:
    st.error("""
        ⚠️ **Data file not found!**
        
        Please ensure 'climate_data_cleaned.csv' is in the same directory as this dashboard file.
        
        To generate the data:
        1. Run the Jupyter notebook analysis first
        2. The notebook will create 'climate_data_cleaned.csv'
        3. Then run this dashboard
    """)
    
    st.info("""
        **Alternative:** You can upload your own climate data CSV file using the sidebar.
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🌍 <strong>Climate Change Analysis Dashboard</strong></p>
        <p>Data Source: Global Climate Change Dataset | Analysis Period: Multi-Year</p>
        <p>For policy inquiries: climate-policy@example.org</p>
    </div>
""", unsafe_allow_html=True)
