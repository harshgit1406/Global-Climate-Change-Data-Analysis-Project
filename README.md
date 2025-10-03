# 🌍 Global Climate Change Data Analysis Project

## Overview
This project provides a comprehensive Exploratory Data Analysis (EDA) of global climate change indicators to inform evidence-based policy decisions for environmental agencies and governments.

Check the live Dashboard - [Global Climate Change Analysis Dashboard](https://code-cookers-global-climate-change-data-analysis.streamlit.app/)
## 📊 Dataset

**Source**: [Climate Change Dataset - Kaggle](https://www.kaggle.com/datasets/bhadramohit/climate-change-dataset)

**Key Variables**:
- Year: Time period of observation
- Country: Geographic location
- Average Temperature (°C): Annual temperature
- CO2 Emissions (Tons/Capita): Per capita emissions
- Sea Level Rise (mm): Annual sea level change
- Rainfall (mm): Total annual precipitation
- Population: Total population
- Renewable Energy (%): Clean energy adoption rate
- Extreme Weather Events: Count of climate disasters
- Forest Area (%): Land forest coverage

---

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.8+
pip (Python package manager)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/climate-change-analysis.git
cd climate-change-analysis
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download the dataset**
- Visit: https://www.kaggle.com/datasets/bhadramohit/climate-change-dataset
- Download `climate_change_data.csv`
- Place it in the project root directory

4. **Run the analysis**
```bash
jupyter notebook climate_analysis.ipynb
```

5. **Launch the dashboard**
```bash
streamlit run dashboard.py
```

---

## 📦 Dependencies

```
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
seaborn>=0.12.0
plotly>=5.11.0
scipy>=1.9.0
streamlit>=1.25.0
jupyter>=1.0.0
```

---

## 🔍 Analysis Framework

### Phase 1: Data Understanding
- Dataset structure and statistics
- Missing value analysis
- Data type verification
- Duplicate detection

### Phase 2: Data Preparation
- Missing value imputation
- Duplicate removal
- Outlier detection using IQR method
- Data quality validation

### Phase 3: Exploratory Analysis (10+ Questions)

1. **Q1**: How have global CO2 emissions trended over time?
2. **Q2**: What is the relationship between CO2 emissions and renewable energy?
3. **Q3**: Which countries have highest/lowest CO2 emissions per capita?
4. **Q4**: How has average temperature changed globally?
5. **Q5**: Is there correlation between forest area and extreme weather?
6. **Q6**: What is the relationship between population and CO2?
7. **Q7**: How does sea level rise correlate with temperature?
8. **Q8**: What are trends in extreme weather events?
9. **Q9**: How does rainfall relate to extreme weather?
10. **Q10**: Which countries lead in renewable energy adoption?
11. **Q11**: What is the correlation matrix of climate variables?
12. **Q12**: How do developed vs developing countries compare?
13. **Q13**: What are temporal patterns in renewable energy?

### Phase 4: Insight Generation
7 key findings with policy implications

### Phase 5: Policy Recommendations
5 actionable policy proposals with implementation roadmap

---

## 📈 Key Findings

### 🎯 Insight 1: Renewable Energy Impact
**Finding**: Strong negative correlation (-0.XX) between renewable energy adoption and CO2 emissions

**Policy Recommendation**: 
- Implement feed-in tariffs for renewable energy
- Provide tax credits for solar/wind installations
- Target: 50% renewable energy by 2030

### 🎯 Insight 2: Temperature-Sea Level Link
**Finding**: Rising global temperatures correlate directly with sea level increases

**Policy Recommendation**:
- Establish coastal protection programs
- Create climate adaptation funds
- Build resilient infrastructure

### 🎯 Insight 3: Forest Protection
**Finding**: Forest coverage shows inverse relationship with extreme weather events

**Policy Recommendation**:
- Launch aggressive reforestation initiatives
- Implement carbon credit programs
- Penalize illegal deforestation

### 🎯 Insight 4: Development Disparity
**Finding**: Significant emission gaps between developed and developing nations

**Policy Recommendation**:
- Create Green Climate Fund
- Facilitate technology transfer
- Support sustainable development

### 🎯 Insight 5: Extreme Weather Increase
**Finding**: Extreme weather events increasing in frequency over study period

**Policy Recommendation**:
- Strengthen early warning systems
- Enhance disaster preparedness
- Build climate-resilient communities

### 🎯 Insight 6: Renewable Growth Rate
**Finding**: Renewable energy adoption growing but pace insufficient for targets

**Policy Recommendation**:
- Set mandatory renewable energy quotas
- Accelerate clean energy investments
- Phase out fossil fuel subsidies

### 🎯 Insight 7: Development Model Matters
**Finding**: Development approach more important than population size for emissions

**Policy Recommendation**:
- Promote green development pathways
- Support sustainable urbanization
- Encourage circular economy models

---

## 📊 Dashboard Features

### Interactive Visualizations
- Global CO2 emissions map
- Renewable energy adoption map
- Time series trends
- Correlation analysis
- Country comparisons

### Filters & Controls
- Year range selector
- Country selection
- Metric toggles
- Dynamic updates

### Tabs
1. **Overview**: Key metrics and global maps
2. **Temperature & Emissions**: Climate change trends
3. **Renewable Energy**: Clean energy analysis
4. **Environmental Factors**: Ecosystem indicators
5. **Policy Insights**: Recommendations and timeline




