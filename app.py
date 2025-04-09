import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
from PIL import Image
import base64
from io import BytesIO
import random

# Set page configuration
st.set_page_config(
    page_title="Payplug Growth Opportunity Finder",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for retro gaming aesthetic
def local_css():
    st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary: #FF355E;        /* Hot pink */
        --secondary: #01EDED;      /* Cyan */
        --tertiary: #50FC00;       /* Bright green */
        --dark: #120458;           /* Dark blue */
        --light: #F5F5F5;          /* White-ish */
        --warning: #FF9933;        /* Orange */
        --danger: #FF0000;         /* Red */
        --background: #FFC0CB;     /* Pink */
        --sidebar-bg: #D3D3D3;     /* Light grey */
    }
    
    /* Fonts */
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono&display=swap');
    
    /* Base styles */
    .main {
        background-color: var(--background);
        color: var(--dark);
    }
    
    /* Override Streamlit's default background */
    .stApp {
        background-color: var(--background);
    }
    
    h1, h2, h3 {
        font-family: 'Press Start 2P', cursive;
        text-transform: uppercase;
        color: var(--secondary);
        text-shadow: 3px 3px 0 var(--dark);
        margin: 1.5rem 0;
    }
    
    h1 {
        color: var(--primary);
        font-size: 2.5rem;
        letter-spacing: 2px;
        text-align: center;
        padding: 20px 0;
        border-bottom: 4px solid var(--primary);
        margin-bottom: 30px;
    }
    
    .stDataFrame {
        border: 4px solid var(--secondary);
        box-shadow: 8px 8px 0 var(--dark);
    }
    
    /* Metric cards */
    .metric-card {
        background-color: var(--dark);
        border: 3px solid var(--secondary);
        border-radius: 0;
        padding: 10px;
        text-align: center;
        margin: 5px;
        box-shadow: 5px 5px 0 rgba(0,0,0,0.5);
        transition: all 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 7px 7px 0 rgba(0,0,0,0.5);
    }
    
    .metric-value {
        font-family: 'Press Start 2P', cursive;
        font-size: 2rem;
        margin: 10px 0;
    }
    
    .metric-label {
        font-family: 'VT323', monospace;
        font-size: 1.3rem;
        color: var(--light);
    }
    
    /* Game level indicators */
    .level-high {
        color: var(--tertiary);
        font-weight: bold;
    }
    
    .level-medium {
        color: var(--warning);
        font-weight: bold;
    }
    
    .level-low {
        color: var(--danger);
        font-weight: bold;
    }
    
    /* Button styles */
    .stButton button {
        font-family: 'Press Start 2P', cursive;
        background-color: var(--secondary);
        color: var(--dark);
        border: 3px solid var(--dark);
        border-radius: 0;
        box-shadow: 5px 5px 0 rgba(0,0,0,0.5);
        transition: all 0.2s;
        text-transform: uppercase;
        padding: 10px 20px;
        margin: 10px 0;
    }
    
    .stButton button:hover {
        background-color: var(--primary);
        color: white;
        transform: translateY(-2px);
        box-shadow: 7px 7px 0 rgba(0,0,0,0.5);
    }
    
    /* Select box styling */
    .stSelectbox div[data-baseweb="select"] > div {
        font-family: 'VT323', monospace;
        background-color: var(--dark);
        border: 3px solid var(--secondary);
        border-radius: 0;
        color: white;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: var(--sidebar-bg);
        border-right: 4px solid var(--secondary);
    }
    
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
    }
    
    .sidebar h2, .sidebar h3 {
        color: var(--dark);
    }
    
    .sidebar .stSelectbox div[data-baseweb="select"] > div {
        background-color: white;
        color: var(--dark);
    }
    
    .sidebar h2 {
        font-size: 1.5rem;
        color: var(--primary);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Press Start 2P', cursive;
        font-size: 0.8rem;
        background-color: var(--dark);
        border: 2px solid var(--secondary);
        border-radius: 0;
        color: var(--light);
        padding: 10px;
        box-shadow: 3px 3px 0 rgba(0,0,0,0.5);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--secondary);
        color: var(--dark);
    }
    
    /* Dataframe styling */
    .dataframe {
        font-family: 'Space Mono', monospace;
    }
    
    /* Footer */
    .footer {
        font-family: 'VT323', monospace;
        text-align: center;
        color: var(--dark);
        padding: 20px 0;
        border-top: 2px solid var(--primary);
        margin-top: 50px;
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background-color: var(--primary);
    }
    
    /* Arcade marquee effect */
    .marquee {
        background-color: var(--dark);
        overflow: hidden;
        position: relative;
        border: 3px solid var(--primary);
        box-shadow: 0 0 10px var(--primary);
        margin: 20px 0;
        padding: 10px;
    }
    
    .marquee-content {
        font-family: 'Press Start 2P', cursive;
        font-size: 1.2rem;
        color: var(--primary);
        white-space: nowrap;
        animation: marquee 15s linear infinite;
    }
    
    @keyframes marquee {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    
    /* Pixel card styling */
    .pixel-card {
        background-color: var(--dark);
        border: 3px solid var(--secondary);
        border-radius: 0;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 5px 5px 0 rgba(0,0,0,0.5);
    }
    
    .pixel-card-title {
        font-family: 'Press Start 2P', cursive;
        font-size: 1rem;
        color: var(--primary);
        margin-bottom: 10px;
        text-align: center;
    }
    
    .pixel-card-content {
        font-family: 'VT323', monospace;
        font-size: 1.2rem;
        color: var(--light);
    }
    
    /* Feature badge */
    .feature-badge {
        display: inline-block;
        font-family: 'VT323', monospace;
        background-color: var(--primary);
        color: white;
        padding: 5px 10px;
        margin: 3px;
        border: 2px solid white;
    }
    
    /* Game-like container */
    .game-container {
        background-color: var(--dark);
        border: 4px solid var(--secondary);
        padding: 20px;
        margin: 15px 0;
        box-shadow: 8px 8px 0 rgba(0,0,0,0.5);
    }
    
    /* Trophy icon/label */
    .trophy {
        font-family: 'Press Start 2P', cursive;
        color: #FFD700;
        margin-right: 10px;
    }
    
    /* Opportunity score */
    .opportunity-score {
        font-family: 'Press Start 2P', cursive;
        font-size: 1.8rem;
        color: var(--tertiary);
    }
    
    /* Pixel bars (for feature usage) */
    .pixel-bar-container {
        width: 100%;
        height: 20px;
        background-color: #333;
        border: 2px solid var(--secondary);
        margin-bottom: 15px;
    }
    
    .pixel-bar {
        height: 100%;
        background-color: var(--tertiary);
    }
    </style>
    """, unsafe_allow_html=True)

# Generate mock data for merchant segments
def generate_merchant_segments():
    segments = [
        {
            "id": "high_growth_smb",
            "name": "High-Growth SMB E-commerce",
            "description": "Small to medium e-commerce businesses experiencing rapid growth",
            "avg_monthly_volume": 42000,
            "avg_growth_rate": 0.35,  # 35% growth
            "avg_transaction_size": 85,
            "merchant_count": 215,
            "industries": {
                "Fashion": 0.32,
                "Electronics": 0.18,
                "Home Goods": 0.15,
                "Beauty": 0.12,
                "Other": 0.23
            },
            "feature_adoption": {
                "One-Click Payment": 0.75,
                "Subscription API": 0.45,
                "Advanced Fraud Tools": 0.68,
                "Mobile SDK": 0.82,
                "Embedded Checkout": 0.62
            },
            "success_metrics": {
                "retention_rate": 0.92,
                "feature_adoption_rate": 0.78,
                "avg_volume_growth": 0.35
            },
            "color": "cyan"
        },
        {
            "id": "established_retail",
            "name": "Established Retail",
            "description": "Traditional retail businesses with stable payment volumes",
            "avg_monthly_volume": 186000,
            "avg_growth_rate": 0.08,  # 8% growth
            "avg_transaction_size": 125,
            "merchant_count": 148,
            "industries": {
                "Department Stores": 0.38,
                "Specialty Retail": 0.25,
                "Grocery": 0.15,
                "Home Improvement": 0.12,
                "Other": 0.10
            },
            "feature_adoption": {
                "One-Click Payment": 0.48,
                "Subscription API": 0.22,
                "Advanced Fraud Tools": 0.75,
                "Mobile SDK": 0.35,
                "Embedded Checkout": 0.42
            },
            "success_metrics": {
                "retention_rate": 0.88,
                "feature_adoption_rate": 0.52,
                "avg_volume_growth": 0.08
            },
            "color": "green"
        },
        {
            "id": "platform_fintech",
            "name": "Platform Fintech",
            "description": "Financial technology platforms processing payments for their users",
            "avg_monthly_volume": 540000,
            "avg_growth_rate": 0.28,  # 28% growth
            "avg_transaction_size": 220,
            "merchant_count": 68,
            "industries": {
                "Payments": 0.45,
                "Lending": 0.22,
                "Investing": 0.18,
                "Banking": 0.10,
                "Other": 0.05
            },
            "feature_adoption": {
                "One-Click Payment": 0.85,
                "Subscription API": 0.78,
                "Advanced Fraud Tools": 0.92,
                "Mobile SDK": 0.65,
                "Embedded Checkout": 0.88
            },
            "success_metrics": {
                "retention_rate": 0.94,
                "feature_adoption_rate": 0.88,
                "avg_volume_growth": 0.28
            },
            "color": "hotpink"
        },
        {
            "id": "subscription_services",
            "name": "Subscription Services",
            "description": "Businesses with recurring revenue models",
            "avg_monthly_volume": 95000,
            "avg_growth_rate": 0.24,  # 24% growth
            "avg_transaction_size": 45,
            "merchant_count": 105,
            "industries": {
                "Digital Content": 0.32,
                "Box Subscriptions": 0.28,
                "SaaS": 0.22,
                "Service Subscriptions": 0.12,
                "Other": 0.06
            },
            "feature_adoption": {
                "One-Click Payment": 0.68,
                "Subscription API": 0.95,
                "Advanced Fraud Tools": 0.72,
                "Mobile SDK": 0.58,
                "Embedded Checkout": 0.45
            },
            "success_metrics": {
                "retention_rate": 0.90,
                "feature_adoption_rate": 0.72,
                "avg_volume_growth": 0.24
            },
            "color": "gold"
        },
        {
            "id": "emerging_marketplace",
            "name": "Emerging Marketplaces",
            "description": "Growing multi-vendor marketplace platforms",
            "avg_monthly_volume": 280000,
            "avg_growth_rate": 0.42,  # 42% growth
            "avg_transaction_size": 95,
            "merchant_count": 52,
            "industries": {
                "Gig Economy": 0.35,
                "Freelance Services": 0.25,
                "Product Marketplaces": 0.22,
                "Food Delivery": 0.12,
                "Other": 0.06
            },
            "feature_adoption": {
                "One-Click Payment": 0.78,
                "Subscription API": 0.32,
                "Advanced Fraud Tools": 0.82,
                "Mobile SDK": 0.75,
                "Embedded Checkout": 0.88
            },
            "success_metrics": {
                "retention_rate": 0.89,
                "feature_adoption_rate": 0.74,
                "avg_volume_growth": 0.42
            },
            "color": "coral"
        }
    ]
    
    return segments

# Generate mock data for merchants based on segments
def generate_merchants_by_segment(segments, num_merchants=500):
    np.random.seed(42)
    
    # Account Managers
    account_managers = ['Alex Thompson', 'Samantha Lee', 'Marcus Johnson', 'Rachel Chen', 'David Kim']
    
    # Contact names generator
    first_names = ['John', 'Emma', 'Michael', 'Sophia', 'James', 'Olivia', 'Robert', 'Ava', 'William', 'Isabella']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Rodriguez', 'Wilson']
    
    # Features
    features = ['One-Click Payment', 'Subscription API', 'Advanced Fraud Tools', 'Mobile SDK', 'Embedded Checkout']
    
    merchants = []
    merchant_id = 1
    
    # Generate merchants for each segment
    for segment in segments:
        # Calculate how many merchants to create for this segment
        segment_merchant_count = int(segment['merchant_count'])
        
        # Get segment attributes for reference
        segment_id = segment['id']
        segment_name = segment['name']
        feature_adoption = segment['feature_adoption']
        industries = segment['industries']
        
        # Distribution parameters
        avg_volume = segment['avg_monthly_volume']
        volume_std = avg_volume * 0.3  # 30% standard deviation
        avg_growth = segment['avg_growth_rate']
        growth_std = 0.05  # 5% standard deviation
        
        for _ in range(segment_merchant_count):
            # Generate basic merchant info
            merchant = {
                'merchant_id': f'M{merchant_id:04d}',
                'merchant_name': f'Merchant {merchant_id}',
                'segment_id': segment_id,
                'segment_name': segment_name,
                'account_manager': np.random.choice(account_managers),
                'contact_name': f"{np.random.choice(first_names)} {np.random.choice(last_names)}",
                'contact_email': f"contact{merchant_id}@example.com",
                'contact_phone': f"+1-555-{np.random.randint(100, 999)}-{np.random.randint(1000, 9999)}"
            }
            
            # Assign an industry based on segment distribution
            industry_items = list(industries.items())
            industry_names = [item[0] for item in industry_items]
            industry_weights = [item[1] for item in industry_items]
            merchant['industry'] = np.random.choice(industry_names, p=industry_weights)
            
            # Generate volume data with some randomness
            merchant['monthly_volume'] = int(np.random.normal(avg_volume, volume_std))
            merchant['growth_rate'] = max(0, min(1, np.random.normal(avg_growth, growth_std)))
            
            # Determine feature adoption
            merchant_features = {}
            for feature in features:
                # Probability of adoption based on segment characteristics
                adoption_prob = feature_adoption.get(feature, 0.5)
                merchant_features[feature] = np.random.random() < adoption_prob
            
            merchant['features'] = merchant_features
            merchant['features_adopted'] = sum(merchant_features.values())
            
            # Add success metrics
            merchant['tenure'] = np.random.randint(1, 48)  # 1-48 months
            merchant['retention_probability'] = min(0.98, max(0.5, 
                                                           0.75 + 
                                                           0.05 * (merchant['features_adopted'] / len(features)) + 
                                                           0.02 * (merchant['growth_rate'] * 10) +
                                                           0.01 * (merchant['tenure'] / 12)))
            
            # Custom metrics for opportunity scoring
            merchant['payment_success_rate'] = 0.95 + (0.04 * np.random.random())
            merchant['average_order_frequency'] = np.random.randint(1, 12)  # Average orders per customer per year
            
            merchants.append(merchant)
            merchant_id += 1
    
    # Convert to DataFrame
    merchants_df = pd.DataFrame(merchants)
    
    # Calculate the opportunity score - a combination of factors that indicate upsell potential
    merchants_df['opportunity_score'] = (
        # Higher volume means higher opportunity value
        (merchants_df['monthly_volume'] / 10000) * 0.3 +
        # Higher growth rate means higher potential
        (merchants_df['growth_rate'] * 100) * 0.3 +
        # More features adopted indicates receptiveness to new features
        (merchants_df['features_adopted'] / len(features)) * 100 * 0.2 +
        # Longer tenure means more stable relationship
        (merchants_df['tenure'] / 48) * 100 * 0.1 +
        # Higher retention probability means lower risk
        (merchants_df['retention_probability'] * 100) * 0.1
    )
    
    # Scale opportunity score to 0-100 range
    min_score = merchants_df['opportunity_score'].min()
    max_score = merchants_df['opportunity_score'].max()
    merchants_df['opportunity_score'] = ((merchants_df['opportunity_score'] - min_score) / 
                                       (max_score - min_score)) * 100
    
    # Round to integers
    merchants_df['opportunity_score'] = merchants_df['opportunity_score'].astype(int)
    
    return merchants_df

# Generate feature impact data
def generate_feature_impact_data(features, segments):
    # Create dataframe showing the impact of each feature on key metrics
    impact_data = []
    
    for feature in features:
        for segment in segments:
            segment_id = segment['id']
            segment_name = segment['name']
            
            # Base impact values
            base_values = {
                'volume_impact': np.random.uniform(0.05, 0.25),
                'retention_impact': np.random.uniform(0.02, 0.15),
                'growth_impact': np.random.uniform(0.03, 0.30)
            }
            
            # Adjust based on the feature adoption - features with higher adoption in successful segments
            # have higher impact
            adoption_rate = segment['feature_adoption'].get(feature, 0.5)
            impact_multiplier = 0.5 + adoption_rate
            
            # Create record for this feature-segment combination
            impact_record = {
                'feature': feature,
                'segment_id': segment_id,
                'segment_name': segment_name,
                'volume_impact': base_values['volume_impact'] * impact_multiplier,
                'retention_impact': base_values['retention_impact'] * impact_multiplier,
                'growth_impact': base_values['growth_impact'] * impact_multiplier,
                'adoption_rate': adoption_rate
            }
            
            impact_data.append(impact_record)
    
    return pd.DataFrame(impact_data)

# Create a pixel art segment icon
def create_pixel_segment_icon(color='cyan'):
    colors = {
        'cyan': (1, 237, 237),
        'pink': (255, 53, 94),
        'green': (80, 252, 0),
        'yellow': (255, 218, 0),
        'orange': (255, 153, 51),
        'red': (255, 0, 0),
    }
    
    rgb_color = colors.get(color, colors['cyan'])
    
    # Create a 16x16 image with transparent background
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    pixels = img.load()
    
    # Draw a simple chart/graph icon
    # Draw axes
    for y in range(4, 14):
        pixels[4, y] = rgb_color  # Y-axis
    for x in range(4, 14):
        pixels[x, 13] = rgb_color  # X-axis
    
    # Draw bars or chart elements
    pixels[6, 11] = rgb_color
    pixels[6, 12] = rgb_color
    
    pixels[8, 9] = rgb_color
    pixels[8, 10] = rgb_color
    pixels[8, 11] = rgb_color
    pixels[8, 12] = rgb_color
    
    pixels[10, 7] = rgb_color
    pixels[10, 8] = rgb_color
    pixels[10, 9] = rgb_color
    pixels[10, 10] = rgb_color
    pixels[10, 11] = rgb_color
    pixels[10, 12] = rgb_color
    
    # Convert to base64 for HTML display
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

# Generate opportunity recommendations for merchants
def generate_opportunity_recommendations(merchants_df, feature, target_segment=None):
    """Generate a list of merchants who would benefit from adopting a specific feature"""
    
    # Filter by segment if specified
    if target_segment:
        merchants = merchants_df[merchants_df['segment_id'] == target_segment].copy()
    else:
        merchants = merchants_df.copy()
    
    # Get feature column name
    feature_col = f"features.{feature}"
    
    # Filter merchants who don't have the feature yet
    non_adopters = merchants[~merchants['features'].apply(lambda x: x.get(feature, False))].copy()
    
    if len(non_adopters) == 0:
        return pd.DataFrame()
    
    # Calculate opportunity score specific to this feature
    # This simulates the model that would predict which merchants would benefit most
    feature_opportunity_score = (
        non_adopters['monthly_volume'] * 0.4 +
        non_adopters['growth_rate'] * 100 * 0.3 +
        non_adopters['retention_probability'] * 100 * 0.2 +
        non_adopters['tenure'] * 0.1
    )
    
    # Scale to 0-100
    min_score = feature_opportunity_score.min()
    max_score = feature_opportunity_score.max()
    if max_score > min_score:  # Avoid division by zero
        feature_opportunity_score = ((feature_opportunity_score - min_score) / 
                                    (max_score - min_score)) * 100
    
    non_adopters['feature_opportunity_score'] = feature_opportunity_score.astype(int)
    
    # Sort by opportunity score (descending)
    recommended_merchants = non_adopters.sort_values('feature_opportunity_score', ascending=False)
    
    # Include only relevant columns for display
    display_cols = ['merchant_id', 'merchant_name', 'segment_name', 'industry', 
                   'monthly_volume', 'growth_rate', 'account_manager', 
                   'contact_name', 'feature_opportunity_score']
    
    return recommended_merchants[display_cols].head(10)  # Return top 10 opportunities

# Main application
def main():
    local_css()
    
    # Generate mock data
    segments = generate_merchant_segments()
    merchants_df = generate_merchants_by_segment(segments)
    
    # Get features list
    features = ['One-Click Payment', 'Subscription API', 'Advanced Fraud Tools', 'Mobile SDK', 'Embedded Checkout']
    
    # Generate feature impact data
    feature_impact_df = generate_feature_impact_data(features, segments)
    
    # Application title
    st.markdown("<h1>PAYPLUG GROWTH FINDER QUEST 🎮</h1>", unsafe_allow_html=True)
    
    # Arcade marquee
    st.markdown("""
    <div class="marquee">
        <div class="marquee-content">
            LEVEL UP YOUR MERCHANT PORTFOLIO • FIND HIDDEN REVENUE OPPORTUNITIES • HIGH SCORE THIS MONTH: PLATFORM FINTECH +42% GROWTH
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with mode selection
    st.sidebar.markdown("<h2>CONTROL PANEL</h2>", unsafe_allow_html=True)
    
    # Mode selection
    st.sidebar.markdown("### 🎲 GAME MODE")
    app_mode = st.sidebar.selectbox(
        "Select Quest:",
        ["Segment Explorer", "Feature Impact Analyzer", "Opportunity Generator", "Success Profiles"]
    )
    
    # Display segment stats in sidebar
    st.sidebar.markdown("### 🏆 SEGMENT STATS")
    
    for segment in segments:
        st.sidebar.markdown(f"""
        <div style="margin-bottom: 10px; padding: 8px; border-left: 4px solid {segment['color']}; background-color: rgba(0,0,0,0.2);">
            <div style="font-family: 'VT323', monospace; font-size: 1.3rem; color: var(--dark);">
                {segment['name']}
            </div>
            <div style="font-family: 'VT323', monospace; font-size: 1.1rem; color: var(--dark);">
                {segment['merchant_count']} merchants • ${segment['avg_monthly_volume']:,} avg
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content based on selected mode
    if app_mode == "Segment Explorer":
        display_segment_explorer(segments, merchants_df, features)
    elif app_mode == "Feature Impact Analyzer":
        display_feature_impact(feature_impact_df, segments, features)
    elif app_mode == "Opportunity Generator":
        display_opportunity_generator(merchants_df, segments, features)
    elif app_mode == "Success Profiles":
        display_success_profiles(segments, merchants_df)
    
    # Footer
    st.markdown("""
    <div class="footer">
        PAYPLUG GROWTH FINDER QUEST - DEMO VERSION 1.0 | © 2025 PAYPLUG | PRESS START TO BOOST YOUR REVENUE
    </div>
    """, unsafe_allow_html=True)

# Display Segment Explorer
def display_segment_explorer(segments, merchants_df, features):
    st.markdown("## SEGMENT EXPLORER")
    st.markdown("Select a merchant segment to analyze its characteristics and performance.")
    
    # Segment selection
    segment_options = [segment['name'] for segment in segments]
    selected_segment_name = st.selectbox("Choose a segment to explore:", segment_options)
    
    # Find the selected segment data
    selected_segment = next((segment for segment in segments if segment['name'] == selected_segment_name), None)
    
    if selected_segment:
        # Get merchants in this segment
        segment_merchants = merchants_df[merchants_df['segment_id'] == selected_segment['id']]
        
        # Display segment overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">MERCHANT COUNT</div>
                <div class="metric-value">{selected_segment['merchant_count']}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">AVG MONTHLY VOLUME</div>
                <div class="metric-value">${selected_segment['avg_monthly_volume']:,}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            growth_display = f"{selected_segment['avg_growth_rate']*100:.0f}%"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">AVG GROWTH RATE</div>
                <div class="metric-value">{growth_display}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">AVG TRANSACTION SIZE</div>
                <div class="metric-value">${selected_segment['avg_transaction_size']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Segment description
        st.markdown(f"""
        <div class="pixel-card">
            <div class="pixel-card-title">SEGMENT PROFILE</div>
            <div class="pixel-card-content">
                {selected_segment['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display segment characteristics in tabs
        tab1, tab2, tab3 = st.tabs(["INDUSTRY MIX", "FEATURE ADOPTION", "MERCHANT EXAMPLES"])
        
        with tab1:
            # Industry distribution chart
            industries = list(selected_segment['industries'].keys())
            industry_shares = list(selected_segment['industries'].values())
            
            fig = px.bar(
                x=industry_shares, 
                y=industries, 
                orientation='h',
                labels={'x': 'Percentage', 'y': 'Industry'},
                title="Industry Distribution",
                color_discrete_sequence=[selected_segment['color']]
            )
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="VT323", size=16, color="#F5F5F5"),
                title_font=dict(family="Press Start 2P", size=16, color="#01EDED"),
                margin=dict(l=10, r=10, t=60, b=10),
                height=350
            )
            
            fig.update_traces(marker_line_width=2, marker_line_color="#120458")
            fig.update_xaxes(gridcolor='#333333', gridwidth=0.5)
            fig.update_yaxes(gridcolor='#333333', gridwidth=0.5)
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Feature adoption chart
            feature_names = list(selected_segment['feature_adoption'].keys())
            adoption_rates = list(selected_segment['feature_adoption'].values())
            
            fig = px.bar(
                x=adoption_rates, 
                y=feature_names, 
                orientation='h',
                labels={'x': 'Adoption Rate', 'y': 'Feature'},
                title="Feature Adoption Rates",
                color_discrete_sequence=[selected_segment['color']]
            )
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="VT323", size=16, color="#F5F5F5"),
                title_font=dict(family="Press Start 2P", size=16, color="#01EDED"),
                margin=dict(l=10, r=10, t=60, b=10),
                height=350
            )
            
            fig.update_traces(marker_line_width=2, marker_line_color="#120458")
            fig.update_xaxes(gridcolor='#333333', gridwidth=0.5, tickformat='.0%')
            fig.update_yaxes(gridcolor='#333333', gridwidth=0.5)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Feature correlations
            st.markdown(f"""
            <div class="pixel-card-title">FEATURE IMPACT ON SUCCESS</div>
            """, unsafe_allow_html=True)
            
            for feature in features:
                adoption_rate = selected_segment['feature_adoption'].get(feature, 0)
                impact_score = int(adoption_rate * 100) # Simplified impact score based on adoption
                
                st.markdown(f"""
                <div style="margin-bottom: 15px;">
                    <div style="font-family: 'VT323', monospace; font-size: 1.2rem; margin-bottom: 5px; display: flex; justify-content: space-between;">
                        <span>{feature}</span>
                        <span>Impact: {impact_score}%</span>
                    </div>
                    <div style="height: 20px; width: 100%; background-color: #333; border: 2px solid var(--secondary);">
                        <div style="height: 100%; width: {impact_score}%; background-color: var(--tertiary);"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with tab3:
            # Sample merchants from this segment
            if len(segment_merchants) > 0:
                sample_size = min(5, len(segment_merchants))
                sample_merchants = segment_merchants.sample(sample_size)
                
                for _, merchant in sample_merchants.iterrows():
                    # Calculate feature badges
                    feature_badges = ""
                    for feature, adopted in merchant['features'].items():
                        if adopted:
                            feature_badges += f'<span class="feature-badge">{feature}</span> '
                    
                    st.markdown(f"""
                    <div class="pixel-card">
                        <div class="pixel-card-title">{merchant['merchant_name']}</div>
                        <div class="pixel-card-content">
                            <div><strong>Industry:</strong> {merchant['industry']}</div>
                            <div><strong>Monthly Volume:</strong> ${merchant['monthly_volume']:,}</div>
                            <div><strong>Growth Rate:</strong> {merchant['growth_rate']*100:.1f}%</div>
                            <div><strong>Account Manager:</strong> {merchant['account_manager']}</div>
                            <div><strong>Features Adopted:</strong> {merchant['features_adopted']} of {len(features)}</div>
                            <div style="margin-top: 10px;">{feature_badges}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No merchants found in this segment.")
                
        # Volume distribution chart
        st.markdown("## VOLUME DISTRIBUTION")
        
        # Create histogram of merchant volumes
        fig = px.histogram(
            segment_merchants, 
            x="monthly_volume", 
            nbins=20,
            labels={'monthly_volume': 'Monthly Volume ($)', 'count': 'Number of Merchants'},
            color_discrete_sequence=[f"#{selected_segment['color']}"]
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="VT323", size=16, color="#F5F5F5"),
            margin=dict(l=40, r=40, t=10, b=40),
            height=300
        )
        
        fig.update_traces(marker_line_width=1, marker_line_color="#120458")
        fig.update_xaxes(gridcolor='#333333', gridwidth=0.5)
        fig.update_yaxes(gridcolor='#333333', gridwidth=0.5)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Growth vs Volume scatter plot
        st.markdown("## GROWTH vs VOLUME RELATIONSHIP")
        
        fig = px.scatter(
            segment_merchants,
            x="monthly_volume",
            y="growth_rate",
            size="tenure",
            hover_name="merchant_name",
            labels={
                'monthly_volume': 'Monthly Volume ($)',
                'growth_rate': 'Growth Rate',
                'tenure': 'Tenure (months)'
            },
            color_discrete_sequence=[f"#{selected_segment['color']}"]
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="VT323", size=16, color="#F5F5F5"),
            margin=dict(l=40, r=40, t=10, b=40),
            height=400
        )
        
        fig.update_traces(marker_line_width=1, marker_line_color="#120458")
        fig.update_xaxes(gridcolor='#333333', gridwidth=0.5)
        fig.update_yaxes(gridcolor='#333333', gridwidth=0.5, tickformat='.0%')
        
        st.plotly_chart(fig, use_container_width=True)
    
# Display Feature Impact Analyzer
def display_feature_impact(feature_impact_df, segments, features):
    st.markdown("## FEATURE IMPACT ANALYZER")
    st.markdown("Explore how different features impact key performance metrics across segments.")
    
    # Feature selection
    selected_feature = st.selectbox("Select a feature to analyze:", features)
    
    # Filter data for selected feature
    feature_data = feature_impact_df[feature_impact_df['feature'] == selected_feature]
    
    if not feature_data.empty:
        # Display feature overview
        st.markdown(f"""
        <div class="game-container">
            <div style="font-family: 'Press Start 2P', cursive; font-size: 1.3rem; color: var(--tertiary); margin-bottom: 15px; text-align: center;">
                {selected_feature} POWER-UP STATS
            </div>
            <div style="font-family: 'VT323', monospace; font-size: 1.2rem; color: var(--light); margin-bottom: 20px; text-align: center;">
                See how this feature supercharges merchant performance across different segments
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Impact metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_volume_impact = feature_data['volume_impact'].mean() * 100
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">AVG VOLUME BOOST</div>
                <div class="metric-value">+{avg_volume_impact:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            avg_retention_impact = feature_data['retention_impact'].mean() * 100
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">AVG RETENTION BOOST</div>
                <div class="metric-value">+{avg_retention_impact:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            avg_growth_impact = feature_data['growth_impact'].mean() * 100
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">AVG GROWTH BOOST</div>
                <div class="metric-value">+{avg_growth_impact:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Impact by segment chart
        st.markdown("### IMPACT BY SEGMENT")
        
        # Prepare data for grouped bar chart
        segment_names = feature_data['segment_name'].tolist()
        volume_impacts = (feature_data['volume_impact'] * 100).tolist()
        retention_impacts = (feature_data['retention_impact'] * 100).tolist()
        growth_impacts = (feature_data['growth_impact'] * 100).tolist()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=segment_names,
            y=volume_impacts,
            name='Volume Impact',
            marker_color='#01EDED'
        ))
        
        fig.add_trace(go.Bar(
            x=segment_names,
            y=retention_impacts,
            name='Retention Impact',
            marker_color='#FF355E'
        ))
        
        fig.add_trace(go.Bar(
            x=segment_names,
            y=growth_impacts,
            name='Growth Impact',
            marker_color='#50FC00'
        ))
        
        fig.update_layout(
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="VT323", size=16, color="#F5F5F5"),
            legend=dict(
                font=dict(family="VT323", size=14),
                bgcolor='rgba(0,0,0,0.5)',
                bordercolor='#01EDED',
                borderwidth=2
            ),
            margin=dict(l=40, r=40, t=10, b=40),
            height=400
        )
        
        fig.update_traces(marker_line_width=2, marker_line_color="#120458")
        fig.update_xaxes(gridcolor='#333333', gridwidth=0.5)
        fig.update_yaxes(gridcolor='#333333', gridwidth=0.5, title="Percentage Improvement")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Adoption vs Impact scatter plot
        st.markdown("### ADOPTION RATE vs IMPACT")
        
        fig = px.scatter(
            feature_data,
            x="adoption_rate",
            y="volume_impact",
            size="growth_impact",
            color="segment_name",
            hover_name="segment_name",
            labels={
                'adoption_rate': 'Adoption Rate',
                'volume_impact': 'Volume Impact',
                'growth_impact': 'Growth Impact (size)'
            }
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="VT323", size=16, color="#F5F5F5"),
            legend=dict(
                font=dict(family="VT323", size=14),
                bgcolor='rgba(0,0,0,0.5)',
                bordercolor='#01EDED',
                borderwidth=2
            ),
            margin=dict(l=40, r=40, t=10, b=40),
            height=400
        )
        
        fig.update_traces(marker_line_width=2, marker_line_color="#120458")
        fig.update_xaxes(gridcolor='#333333', gridwidth=0.5, tickformat='.0%')
        fig.update_yaxes(gridcolor='#333333', gridwidth=0.5, tickformat='.0%')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Feature recommendations
        st.markdown("### FEATURE IMPLEMENTATION RECOMMENDATIONS")
        
        # Get segment with highest impact for this feature
        best_segment = feature_data.loc[feature_data['volume_impact'].idxmax()]
        
        st.markdown(f"""
        <div class="game-container">
            <div style="font-family: 'Press Start 2P', cursive; font-size: 1.2rem; color: var(--tertiary); margin-bottom: 15px;">
                <span class="trophy">🏆</span> TOP OPPORTUNITY SEGMENT
            </div>
            <div style="font-family: 'VT323', monospace; font-size: 1.5rem; color: var(--primary); margin-bottom: 10px;">
                {best_segment['segment_name']}
            </div>
            <div style="font-family: 'VT323', monospace; font-size: 1.2rem; color: var(--light); margin-bottom: 5px;">
                Current Adoption Rate: {best_segment['adoption_rate']*100:.0f}%
            </div>
            <div style="font-family: 'VT323', monospace; font-size: 1.2rem; color: var(--light); margin-bottom: 5px;">
                Potential Volume Impact: +{best_segment['volume_impact']*100:.1f}%
            </div>
            <div style="font-family: 'VT323', monospace; font-size: 1.2rem; color: var(--light); margin-bottom: 5px;">
                Potential Growth Impact: +{best_segment['growth_impact']*100:.1f}%
            </div>
            <div style="font-family: 'VT323', monospace; font-size: 1.2rem; color: var(--light); margin-bottom: 20px;">
                Potential Retention Impact: +{best_segment['retention_impact']*100:.1f}%
            </div>
            <div style="font-family: 'VT323', monospace; font-size: 1.2rem; color: var(--secondary); margin-bottom: 10px; border-top: 2px dotted var(--secondary); padding-top: 10px;">
                <strong>Implementation Strategy:</strong> Target merchants in the {best_segment['segment_name']} segment who haven't yet adopted {selected_feature} for the highest ROI on sales efforts.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
# Display Opportunity Generator
def display_opportunity_generator(merchants_df, segments, features):
    st.markdown("## OPPORTUNITY GENERATOR")
    st.markdown("Find specific merchants who would benefit most from adopting new features.")
    
    # Select target segment and feature
    col1, col2 = st.columns(2)
    
    with col1:
        segment_options = ["All Segments"] + [segment['name'] for segment in segments]
        selected_segment_name = st.selectbox("Target Segment:", segment_options)
    
    with col2:
        selected_feature = st.selectbox("Feature to Promote:", features)
    
    # Get segment ID if a specific segment was selected
    target_segment_id = None
    if selected_segment_name != "All Segments":
        selected_segment = next((segment for segment in segments if segment['name'] == selected_segment_name), None)
        if selected_segment:
            target_segment_id = selected_segment['id']
    
    # Generate opportunity recommendations
    opportunities = generate_opportunity_recommendations(merchants_df, selected_feature, target_segment_id)
    
    if not opportunities.empty:
        # Display opportunity header
        st.markdown(f"""
        <div class="game-container">
            <div style="font-family: 'Press Start 2P', cursive; font-size: 1.3rem; color: var(--tertiary); margin-bottom: 15px; text-align: center;">
                TOP GROWTH OPPORTUNITIES FOUND!
            </div>
            <div style="font-family: 'VT323', monospace; font-size: 1.2rem; color: var(--light); margin-bottom: 20px; text-align: center;">
                These merchants are prime candidates for adopting <span style="color: var(--primary);">{selected_feature}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display opportunity cards for each merchant
        for idx, opportunity in opportunities.iterrows():
            opportunity_score = opportunity['feature_opportunity_score']
            
            # Determine score color based on value
            if opportunity_score >= 80:
                score_color = "var(--tertiary)"  # Green for high scores
            elif opportunity_score >= 50:
                score_color = "var(--warning)"   # Orange for medium scores
            else:
                score_color = "var(--danger)"    # Red for low scores
            
            # Format growth rate as percentage
            growth_display = f"{opportunity['growth_rate']*100:.1f}%"
            
            st.markdown(f"""
            <div class="pixel-card" style="display: flex; align-items: center;">
                <div style="flex: 1;">
                    <div class="pixel-card-title">{opportunity['merchant_name']}</div>
                    <div class="pixel-card-content">
                        <div><strong>Segment:</strong> {opportunity['segment_name']}</div>
                        <div><strong>Industry:</strong> {opportunity['industry']}</div>
                        <div><strong>Monthly Volume:</strong> ${opportunity['monthly_volume']:,}</div>
                        <div><strong>Growth Rate:</strong> {growth_display}</div>
                        <div><strong>Account Manager:</strong> {opportunity['account_manager']}</div>
                        <div><strong>Contact:</strong> {opportunity['contact_name']}</div>
                    </div>
                </div>
                <div style="width: 100px; text-align: center; padding: 10px;">
                    <div style="font-family: 'VT323', monospace; font-size: 1rem; color: var(--light); margin-bottom: 5px;">
                        OPPORTUNITY
                    </div>
                    <div style="font-family: 'Press Start 2P', cursive; font-size: 1.8rem; color: {score_color};">
                        {opportunity_score}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Display strategy tips
        st.markdown("### IMPLEMENTATION STRATEGY")
        
        st.markdown(f"""
        <div class="game-container">
            <div style="font-family: 'Press Start 2P', cursive; font-size: 1.2rem; color: var(--tertiary); margin-bottom: 15px;">
                <span class="trophy">💡</span> STRATEGY TIPS
            </div>
            <ul style="font-family: 'VT323', monospace; font-size: 1.2rem; color: var(--light); margin-bottom: 20px;">
                <li>Contact the top 3 merchants first for highest ROI</li>
                <li>Highlight that other similar merchants have seen {random.randint(15, 35)}% volume growth after adopting {selected_feature}</li>
                <li>Prepare customized demos showing {selected_feature} in their specific industry context</li>
                <li>Offer implementation support package to speed adoption</li>
                <li>Consider promotion or discount for the first 3 months</li>
            </ul>
            <div style="font-family: 'VT323', monospace; font-size: 1.2rem; color: var(--secondary); margin-top: 10px; text-align: center;">
                Estimated Additional Annual Revenue: ${random.randint(50000, 250000):,}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info(f"No opportunities found. All merchants in the selected segment are already using {selected_feature} or no merchants match the criteria.")

# Display Success Profiles
def display_success_profiles(segments, merchants_df):
    st.markdown("## SUCCESS PROFILES")
    st.markdown("Explore the defining characteristics of the most successful merchants in each segment.")
    
    # Segment selection
    segment_options = [segment['name'] for segment in segments]
    selected_segment_name = st.selectbox("Select a segment to view success profile:", segment_options)
    
    # Find the selected segment data
    selected_segment = next((segment for segment in segments if segment['name'] == selected_segment_name), None)
    
    if selected_segment:
        # Get merchants in this segment
        segment_merchants = merchants_df[merchants_df['segment_id'] == selected_segment['id']].copy()
        
        if not segment_merchants.empty:
            # Add a success score based on growth and volume
            segment_merchants['success_score'] = (
                segment_merchants['monthly_volume'] / segment_merchants['monthly_volume'].max() * 0.6 +
                segment_merchants['growth_rate'] / segment_merchants['growth_rate'].max() * 0.4
            ) * 100
            
            # Get top performers (top 20%)
            threshold = segment_merchants['success_score'].quantile(0.8)
            top_performers = segment_merchants[segment_merchants['success_score'] >= threshold]
            
            # Get feature adoption rates for top performers
            top_feature_adoption = {}
            for feature in ['One-Click Payment', 'Subscription API', 'Advanced Fraud Tools', 'Mobile SDK', 'Embedded Checkout']:
                top_feature_adoption[feature] = top_performers['features'].apply(
                    lambda x: x.get(feature, False)).mean()
            
            # Display success profile header
            st.markdown(f"""
            <div class="game-container">
                <div style="font-family: 'Press Start 2P', cursive; font-size: 1.3rem; color: var(--tertiary); margin-bottom: 15px; text-align: center;">
                    {selected_segment_name} SUCCESS BLUEPRINT
                </div>
                <div style="font-family: 'VT323', monospace; font-size: 1.2rem; color: var(--light); margin-bottom: 20px; text-align: center;">
                    Analysis of top {len(top_performers)} merchants in this segment
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Key metrics overview
            col1, col2, col3 = st.columns(3)
            
            with col1:
                top_avg_volume = top_performers['monthly_volume'].mean()
                segment_avg_volume = segment_merchants['monthly_volume'].mean()
                volume_diff = ((top_avg_volume / segment_avg_volume) - 1) * 100
                
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">AVG VOLUME (TOP VS AVG)</div>
                    <div class="metric-value">${top_avg_volume:,.0f}</div>
                    <div style="font-family: 'VT323', monospace; font-size: 1rem; color: var(--tertiary);">
                        +{volume_diff:.1f}% higher than segment average
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                top_avg_growth = top_performers['growth_rate'].mean() * 100
                segment_avg_growth = segment_merchants['growth_rate'].mean() * 100
                growth_diff = top_avg_growth - segment_avg_growth
                
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">AVG GROWTH RATE</div>
                    <div class="metric-value">{top_avg_growth:.1f}%</div>
                    <div style="font-family: 'VT323', monospace; font-size: 1rem; color: var(--tertiary);">
                        +{growth_diff:.1f}% higher than segment average
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with col3:
                top_avg_features = top_performers['features_adopted'].mean()
                segment_avg_features = segment_merchants['features_adopted'].mean()
                features_diff = top_avg_features - segment_avg_features
                
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">AVG FEATURES ADOPTED</div>
                    <div class="metric-value">{top_avg_features:.1f}</div>
                    <div style="font-family: 'VT323', monospace; font-size: 1rem; color: var(--tertiary);">
                        +{features_diff:.1f} more than segment average
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Feature adoption differences
            st.markdown("### KEY FEATURE ADOPTION")
            
            # Compare top performers feature adoption vs segment average
            feature_comparison = []
            for feature in ['One-Click Payment', 'Subscription API', 'Advanced Fraud Tools', 'Mobile SDK', 'Embedded Checkout']:
                top_adoption = top_performers['features'].apply(lambda x: x.get(feature, False)).mean()
                avg_adoption = segment_merchants['features'].apply(lambda x: x.get(feature, False)).mean()
                
                feature_comparison.append({
                    'feature': feature,
                    'top_adoption': top_adoption,
                    'avg_adoption': avg_adoption,
                    'difference': top_adoption - avg_adoption
                })
            
            feature_df = pd.DataFrame(feature_comparison)
            
            # Create a bar chart comparing adoption rates
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=feature_df['feature'],
                y=feature_df['top_adoption'],
                name='Top Performers',
                marker_color='#50FC00'
            ))
            
            fig.add_trace(go.Bar(
                x=feature_df['feature'],
                y=feature_df['avg_adoption'],
                name='Segment Average',
                marker_color='#01EDED'
            ))
            
            fig.update_layout(
                barmode='group',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="VT323", size=16, color="#F5F5F5"),
                legend=dict(
                    font=dict(family="VT323", size=14),
                    bgcolor='rgba(0,0,0,0.5)',
                    bordercolor='#01EDED',
                    borderwidth=2
                ),
                margin=dict(l=40, r=40, t=10, b=40),
                height=400
            )
            
            fig.update_traces(marker_line_width=2, marker_line_color="#120458")
            fig.update_xaxes(gridcolor='#333333', gridwidth=0.5)
            fig.update_yaxes(gridcolor='#333333', gridwidth=0.5, title="Adoption Rate", tickformat='.0%')
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Key success factors
            st.markdown("### SUCCESS FACTORS")
            
            # Sort features by difference in adoption
            feature_df = feature_df.sort_values('difference', ascending=False)
            
            # Identify top differentiating features
            top_differentiators = feature_df.head(3)['feature'].tolist()
            
            # Industry distribution of top performers
            top_industries = top_performers['industry'].value_counts(normalize=True).head(3)
            
            st.markdown(f"""
            <div class="game-container">
                <div style="font-family: 'Press Start 2P', cursive; font-size: 1.2rem; color: var(--tertiary); margin-bottom: 15px;">
                    <span class="trophy">🏆</span> SUCCESS RECIPE
                </div>
                
                <div style="margin-bottom: 15px;">
                    <div style="font-family: 'VT323', monospace; font-size: 1.3rem; color: var(--primary); margin-bottom: 10px;">
                        KEY DIFFERENTIATING FEATURES:
                    </div>
                    <ul style="font-family: 'VT323', monospace; font-size: 1.2rem; color: var(--light); margin-bottom: 10px;">
                        {"".join(f'<li>{feature} (+{feature_df[feature_df["feature"]==feature]["difference"].values[0]*100:.0f}% higher adoption)</li>' for feature in top_differentiators)}
                    </ul>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <div style="font-family: 'VT323', monospace; font-size: 1.3rem; color: var(--primary); margin-bottom: 10px;">
                        TOP PERFORMING INDUSTRIES:
                    </div>
                    <ul style="font-family: 'VT323', monospace; font-size: 1.2rem; color: var(--light); margin-bottom: 10px;">
                        {"".join(f'<li>{industry} ({percentage*100:.0f}% of top performers)</li>' for industry, percentage in top_industries.items())}
                    </ul>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <div style="font-family: 'VT323', monospace; font-size: 1.3rem; color: var(--primary); margin-bottom: 10px;">
                        GROWTH STRATEGIES:
                    </div>
                    <ul style="font-family: 'VT323', monospace; font-size: 1.2rem; color: var(--light); margin-bottom: 10px;">
                        <li>Focus adoption campaigns on {top_differentiators[0]} for highest impact</li>
                        <li>Target merchants in the {top_industries.index[0]} industry vertical</li>
                        <li>Create specific success playbooks featuring {top_differentiators[0]} + {top_differentiators[1]} combination</li>
                        <li>Develop case studies from top performers to share with similar merchants</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Example top performers
            st.markdown("### TOP PERFORMER EXAMPLES")
            
            # Show top 3 merchants by success score
            top_3 = top_performers.sort_values('success_score', ascending=False).head(3)
            
            for idx, merchant in top_3.iterrows():
                # Calculate feature badges
                feature_badges = ""
                for feature, adopted in merchant['features'].items():
                    if adopted:
                        feature_badges += f'<span class="feature-badge">{feature}</span> '
                
                growth_display = f"{merchant['growth_rate']*100:.1f}%"
                
                st.markdown(f"""
                <div class="pixel-card">
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <div style="flex: 1;">
                            <div class="pixel-card-title">{merchant['merchant_name']}</div>
                        </div>
                        <div style="width: 80px; text-align: center;">
                            <div style="font-family: 'VT323', monospace; font-size: 0.9rem; color: var(--light);">SCORE</div>
                            <div class="opportunity-score">{int(merchant['success_score'])}</div>
                        </div>
                    </div>
                    <div class="pixel-card-content">
                        <div><strong>Industry:</strong> {merchant['industry']}</div>
                        <div><strong>Monthly Volume:</strong> ${merchant['monthly_volume']:,}</div>
                        <div><strong>Growth Rate:</strong> {growth_display}</div>
                        <div><strong>Features Adopted:</strong> {merchant['features_adopted']} of {len(merchant['features'])}</div>
                        <div style="margin-top: 10px;">{feature_badges}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Recommendation for merchant targeting
            st.markdown("### OPPORTUNITY TARGETING")
            
            # Calculate how many merchants could benefit from this profile
            segment_size = len(segment_merchants)
            low_adoption_count = len(segment_merchants[segment_merchants['features_adopted'] < top_avg_features])
            potential_pct = (low_adoption_count / segment_size) * 100
            
            st.markdown(f"""
            <div class="game-container">
                <div style="font-family: 'Press Start 2P', cursive; font-size: 1.2rem; color: var(--tertiary); margin-bottom: 15px;">
                    <span class="trophy">💰</span> REVENUE OPPORTUNITY
                </div>
                
                <div style="font-family: 'VT323', monospace; font-size: 1.2rem; color: var(--light); margin-bottom: 20px;">
                    <p><strong>{low_adoption_count}</strong> merchants ({potential_pct:.0f}% of this segment) are using fewer features than top performers and represent growth opportunities.</p>
                    
                    <p>If these merchants adopted additional features to match the profile of top performers, the estimated annual revenue increase would be:</p>
                </div>
                
                <div style="font-family: 'Press Start 2P', cursive; font-size: 1.8rem; color: var(--tertiary); text-align: center; margin: 20px 0;">
                    ${random.randint(500000, 2000000):,}
                </div>
                
                <div style="font-family: 'VT323', monospace; font-size: 1.2rem; color: var(--secondary); margin-top: 10px;">
                    <strong>Recommended Action:</strong> Create a targeted campaign to increase adoption of {top_differentiators[0]} and {top_differentiators[1]} features among merchants in this segment.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.info(f"No merchant data available for {selected_segment_name}.")

if __name__ == "__main__":
    main()