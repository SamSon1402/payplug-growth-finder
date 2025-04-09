import pandas as pd
import numpy as np
import random
import datetime

def generate_merchant_segments():
    """
    Generate mock data for merchant segments
    
    Returns:
        list: List of dictionaries containing segment data
    """
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

def generate_merchants_by_segment(segments, num_merchants=500):
    """
    Generate mock merchant data based on segments
    
    Args:
        segments (list): List of segment dictionaries from generate_merchant_segments()
        num_merchants (int): Total number of merchants to generate
        
    Returns:
        DataFrame: Pandas DataFrame containing merchant data
    """
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

def generate_feature_impact_data(features, segments):
    """
    Generate data showing the impact of each feature on key merchant metrics
    
    Args:
        features (list): List of feature names
        segments (list): List of segment dictionaries
        
    Returns:
        DataFrame: Pandas DataFrame containing feature impact data
    """
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

def generate_opportunity_recommendations(merchants_df, feature, target_segment=None):
    """
    Generate a list of merchants who would benefit from adopting a specific feature
    
    Args:
        merchants_df (DataFrame): DataFrame containing merchant data
        feature (str): Feature name to promote
        target_segment (str, optional): Segment ID to filter by
        
    Returns:
        DataFrame: DataFrame containing recommended merchants sorted by opportunity score
    """
    # Filter by segment if specified
    if target_segment:
        merchants = merchants_df[merchants_df['segment_id'] == target_segment].copy()
    else:
        merchants = merchants_df.copy()
    
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