from PIL import Image
import base64
from io import BytesIO

def create_pixel_segment_icon(color='cyan'):
    """
    Create a pixel art segment icon.
    
    Args:
        color (str): Color name for the icon ('cyan', 'pink', 'green', 'yellow', 'orange', 'red')
        
    Returns:
        str: Base64 encoded image data URI
    """
    colors = {
        'cyan': (1, 237, 237),
        'pink': (255, 53, 94),
        'green': (80, 252, 0),
        'yellow': (255, 218, 0),
        'orange': (255, 153, 51),
        'red': (255, 0, 0),
        'hotpink': (255, 105, 180),
        'gold': (255, 215, 0),
        'coral': (255, 127, 80),
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

def apply_retro_styling():
    """
    Returns the CSS styling for the retro gaming aesthetic.
    
    Returns:
        str: CSS styling for Streamlit
    """
    return """
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
    """