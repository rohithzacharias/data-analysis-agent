"""
Web Interface for Data Analysis Agent
Streamlit app with ScaleDown API integration
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.eda_agent import EDAAgent
from src.schema_compressor import SchemaCompressor
from src.scaledown_api import ScaleDownIntegration, save_api_key, load_api_key
from src.visualizations import plot_missing_values, plot_correlation_matrix

# Page configuration
st.set_page_config(
    page_title="🧠 Data Analysis Agent",
    page_icon="🧠",
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
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = load_api_key() or ""
if 'df' not in st.session_state:
    st.session_state.df = None
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'results' not in st.session_state:
    st.session_state.results = None

# Header
st.markdown('<div class="main-header">🧠 Data Analysis Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Efficient Exploratory Data Analysis with AI-Powered Compression</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key input
    st.subheader("ScaleDown API")
    api_key_input = st.text_input(
        "API Key",
        value=st.session_state.api_key,
        type="password",
        help="Enter your ScaleDown API key for ultra-compression"
    )
    
    if st.button("💾 Save API Key"):
        st.session_state.api_key = api_key_input
        save_api_key(api_key_input)
        st.success("API key saved!")
    
    st.divider()
    
    # Compression settings
    st.subheader("Compression Settings")
    compression_model = st.selectbox(
        "Target Model",
        ["gpt-4o", "gpt-4", "gpt-3.5-turbo", "claude-3"],
        help="Select the LLM model you'll use"
    )
    
    compression_rate = st.select_slider(
        "Compression Rate",
        options=["low", "medium", "high", "auto"],
        value="auto",
        help="Higher rate = more compression, less detail"
    )
    
    st.divider()
    
    # Info
    st.subheader("ℹ️ About")
    st.info("""
    **Data Analysis Agent** combines:
    - Schema compression (50-2000x)
    - History compression (5-20x)
    - ScaleDown API (additional 2-10x)
    
    **Total compression: up to 99.9%!**
    """)

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📊 Upload Data", "🔍 Analysis", "📈 Visualizations", "🚀 API Integration"])

# Tab 1: Upload Data
with tab1:
    st.header("Upload Your Dataset")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload your dataset for analysis"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.df = df
                st.session_state.agent = EDAAgent(df, name="Web Analysis")
                
                st.success(f"✅ Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")
                
                # Show preview
                st.subheader("Data Preview")
                st.dataframe(df.head(10))
                
                # Basic info
                st.subheader("Dataset Info")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Rows", df.shape[0])
                with col_b:
                    st.metric("Columns", df.shape[1])
                with col_c:
                    st.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
                
            except Exception as e:
                st.error(f"Error loading file: {e}")
    
    with col2:
        st.subheader("Sample Datasets")
        if st.button("🌸 Load Iris"):
            from src.utils import load_sample_data
            df = load_sample_data('iris')
            st.session_state.df = df
            st.session_state.agent = EDAAgent(df, name="Iris Analysis")
            st.rerun()
        
        if st.button("🚢 Load Titanic"):
            from src.utils import load_sample_data
            df = load_sample_data('titanic')
            st.session_state.df = df
            st.session_state.agent = EDAAgent(df, name="Titanic Analysis")
            st.rerun()
        
        if st.button("💵 Load Tips"):
            from src.utils import load_sample_data
            df = load_sample_data('tips')
            st.session_state.df = df
            st.session_state.agent = EDAAgent(df, name="Tips Analysis")
            st.rerun()

# Tab 2: Analysis
with tab2:
    if st.session_state.agent is None:
        st.warning("⚠️ Please upload a dataset first!")
    else:
        st.header("Exploratory Data Analysis")
        
        # Run analysis button
        if st.button("🚀 Run Automated Analysis", type="primary"):
            with st.spinner("Analyzing dataset..."):
                results = st.session_state.agent.run_automated_eda()
                st.session_state.results = results
        
        if st.session_state.results:
            results = st.session_state.results
            
            # Show compressed schema
            st.subheader("📋 Compressed Schema")
            schema_text = st.session_state.agent.get_schema_context()
            st.text_area("Schema", schema_text, height=200)
            
            # Token efficiency
            compressor = SchemaCompressor()
            stats = compressor.estimate_token_reduction(st.session_state.df)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Schema Tokens", f"{stats['schema_tokens']:,}")
            with col2:
                st.metric("Full Dataset Tokens", f"{stats['estimated_full_tokens']:,}")
            with col3:
                st.metric("Reduction", f"{stats['reduction_ratio']:.1f}x")
            with col4:
                st.metric("Tokens Saved", f"{stats['tokens_saved']:,}")
            
            # Analysis results
            st.subheader("🔍 Analysis Results")
            
            # Missing values
            with st.expander("Missing Values", expanded=True):
                missing = results['analyses']['missing_values']
                for insight in missing['insights']:
                    st.write(f"• {insight}")
            
            # Distributions
            with st.expander("Distributions"):
                dist = results['analyses']['distributions']
                for insight in dist['insights'][:5]:
                    st.write(f"• {insight}")
            
            # Correlations
            with st.expander("Correlations"):
                corr = results['analyses']['correlations']
                for insight in corr['insights'][:5]:
                    st.write(f"• {insight}")
            
            # Outliers
            with st.expander("Outliers"):
                outlier = results['analyses']['outliers']
                for insight in outlier['insights'][:5]:
                    st.write(f"• {insight}")

# Tab 3: Visualizations
with tab3:
    if st.session_state.agent is None:
        st.warning("⚠️ Please upload a dataset first!")
    else:
        st.header("Data Visualizations")
        
        df = st.session_state.df
        
        # Missing values plot
        st.subheader("Missing Values")
        try:
            fig, ax = plt.subplots(figsize=(10, 4))
            missing_data = df.isnull().sum()
            missing_data = missing_data[missing_data > 0]
            if len(missing_data) > 0:
                missing_data.plot(kind='bar', ax=ax, color='coral')
                ax.set_title('Missing Values by Column')
                ax.set_ylabel('Count')
                st.pyplot(fig)
            else:
                st.success("✅ No missing values!")
        except Exception as e:
            st.error(f"Error creating plot: {e}")
        
        # Correlation matrix
        st.subheader("Correlation Matrix")
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if len(numeric_cols) >= 2:
            try:
                import matplotlib.pyplot as plt
                import seaborn as sns
                fig, ax = plt.subplots(figsize=(10, 8))
                corr = df[numeric_cols].corr()
                sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, ax=ax, fmt='.2f')
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Error creating correlation matrix: {e}")
        else:
            st.info("Not enough numeric columns for correlation analysis")

# Tab 4: API Integration
with tab4:
    if st.session_state.agent is None:
        st.warning("⚠️ Please upload a dataset and run analysis first!")
    elif not st.session_state.api_key:
        st.warning("⚠️ Please enter your ScaleDown API key in the sidebar!")
    else:
        st.header("🚀 ScaleDown API Integration")
        st.write("Apply additional compression to your analysis for maximum token efficiency!")
        
        # Initialize API
        scaledown = ScaleDownIntegration(st.session_state.api_key)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Compress Schema")
            if st.button("🗜️ Compress Schema with ScaleDown"):
                with st.spinner("Compressing..."):
                    schema_text = st.session_state.agent.get_schema_context()
                    result = scaledown.compress_schema(
                        schema_text,
                        model=compression_model,
                        rate=compression_rate
                    )
                    
                    if "error" in result:
                        st.error(f"API Error: {result['error']}")
                    else:
                        compressed_content = result.get("compressed", {}).get("content", "")
                        st.success("✅ Schema compressed!")
                        st.text_area("Ultra-Compressed Schema", compressed_content, height=200)
                        
                        # Stats
                        stats = scaledown.get_compression_stats(schema_text, result)
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.metric("Original", f"{stats['original_tokens']} tokens")
                        with c2:
                            st.metric("Compressed", f"{stats['compressed_tokens']} tokens")
                        with c3:
                            st.metric("Reduction", f"{stats['reduction_ratio']:.1f}x")
        
        with col2:
            st.subheader("Compress History")
            if st.button("🗜️ Compress History with ScaleDown"):
                with st.spinner("Compressing..."):
                    history = st.session_state.agent.get_history_context()
                    result = scaledown.compress_analysis_context(
                        history,
                        model=compression_model,
                        rate=compression_rate
                    )
                    
                    if "error" in result:
                        st.error(f"API Error: {result['error']}")
                    else:
                        compressed_content = result.get("compressed", {}).get("content", "")
                        st.success("✅ History compressed!")
                        st.text_area("Ultra-Compressed History", compressed_content, height=200)
                        
                        # Stats
                        stats = scaledown.get_compression_stats(history, result)
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.metric("Original", f"{stats['original_tokens']} tokens")
                        with c2:
                            st.metric("Compressed", f"{stats['compressed_tokens']} tokens")
                        with c3:
                            st.metric("Reduction", f"{stats['reduction_ratio']:.1f}x")
        
        # Full report compression
        st.divider()
        st.subheader("Compress Full Report")
        if st.button("🗜️ Compress Complete Report", type="primary"):
            with st.spinner("Compressing full report..."):
                report = st.session_state.agent.generate_summary_report()
                result = scaledown.compress_full_report(
                    report,
                    model=compression_model,
                    rate=compression_rate
                )
                
                if "error" in result:
                    st.error(f"API Error: {result['error']}")
                else:
                    compressed_content = result.get("compressed", {}).get("content", "")
                    st.success("✅ Full report compressed!")
                    st.text_area("Ultra-Compressed Report", compressed_content, height=300)
                    
                    # Stats
                    stats = scaledown.get_compression_stats(report, result)
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Original Tokens", f"{stats['original_tokens']:,}")
                    with col2:
                        st.metric("Compressed Tokens", f"{stats['compressed_tokens']:,}")
                    with col3:
                        st.metric("Reduction", f"{stats['reduction_ratio']:.1f}x")
                    with col4:
                        cost_saved = stats['tokens_saved'] * 0.002 / 1000
                        st.metric("Cost Saved", f"${cost_saved:.4f}")

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        🧠 <b>Data Analysis Agent</b> | Efficient EDA with AI-Powered Compression<br>
        Built with ❤️ for reducing token costs
    </div>
""", unsafe_allow_html=True)
