"""
The Referee - Tech Stack Decision Tool
Main Streamlit application - UI orchestration only
"""

import streamlit as st
from datetime import datetime
from constraints import get_user_constraints
from options import get_database_options
from evaluator import evaluate_options
from advanced_analysis import (
    ConstraintFitAssessor,
    ConstraintSensitivityAnalyzer,
    CrossOptionComparator,
    WhatIfScenarioAnalyzer
)
from explainer import generate_referee_insight

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="The Referee - Tech Stack Advisor",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# GLASSMORPHISM + PASTEL UI THEME
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    [data-testid="stSidebar"] {
        background: rgba(249, 229, 216, 0.7);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #6A5D7B !important;
        font-weight: 700;
    }
    
    h1 {
        background: linear-gradient(135deg, #6A5D7B 0%, #8B7E99 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.4);
        transition: all 0.3s ease;
        animation: fadeIn 0.6s ease-out;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .hero-section {
        background: linear-gradient(135deg, rgba(200, 184, 219, 0.6), rgba(163, 201, 168, 0.6));
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 3rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 2rem;
        animation: heroFadeIn 1s ease-out;
    }
    
    @keyframes heroFadeIn {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    
    .hero-logo {
        font-size: 4rem;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .hero-title {
        color: white !important;
        font-size: 3.5rem;
        font-weight: 900;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .hero-subtitle {
        color: white;
        font-size: 1.5rem;
        font-weight: 400;
        opacity: 0.95;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #A3C9A8 0%, #B8D4BE 100%);
        color: white;
        border-radius: 15px;
        height: 3.5em;
        width: 100%;
        font-size: 1.1em;
        font-weight: 700;
        border: none;
        box-shadow: 0 4px 15px rgba(163, 201, 168, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #9EB5A5 0%, #B0C8B7 100%);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(163, 201, 168, 0.5);
    }
    
    .metric-glass-card {
        background: linear-gradient(135deg, rgba(200, 184, 219, 0.7), rgba(212, 196, 232, 0.7));
        backdrop-filter: blur(15px);
        padding: 1.8rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .metric-glass-card:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 12px 40px rgba(200, 184, 219, 0.4);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 900;
        margin: 0.5rem 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.95;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .glass-alert-success {
        background: rgba(212, 241, 221, 0.7);
        backdrop-filter: blur(10px);
        border-left: 5px solid #A3C9A8;
        padding: 1.2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(163, 201, 168, 0.2);
    }
    
    .glass-alert-warning {
        background: rgba(255, 243, 205, 0.7);
        backdrop-filter: blur(10px);
        border-left: 5px solid #F9C74F;
        padding: 1.2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(249, 199, 79, 0.2);
    }
    
    .glass-alert-danger {
        background: rgba(255, 229, 229, 0.7);
        backdrop-filter: blur(10px);
        border-left: 5px solid #F4978E;
        padding: 1.2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(244, 151, 142, 0.2);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .glass-alert-info {
        background: rgba(227, 242, 253, 0.7);
        backdrop-filter: blur(10px);
        border-left: 5px solid #90CAF9;
        padding: 1.2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(144, 202, 249, 0.2);
    }
    
    .tech-badge {
        display: inline-block;
        background: linear-gradient(135deg, #A3C9A8, #C8B8DB);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.9rem;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
    
    .footer {
        background: rgba(234, 231, 220, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin-top: 3rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .fit-badge-strong {
        background: linear-gradient(135deg, #A3C9A8, #B8D4BE);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(163, 201, 168, 0.3);
    }
    
    .fit-badge-moderate {
        background: linear-gradient(135deg, #F9C74F, #FFD93D);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(249, 199, 79, 0.3);
    }
    
    .fit-badge-risky {
        background: linear-gradient(135deg, #F4978E, #FBB6AF);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(244, 151, 142, 0.3);
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-logo">⚖️</div>
        <h1 class="hero-title">The Referee</h1>
        <p class="hero-subtitle">
            Constraint-Driven Database Advisor — No Winners, Just Trade-offs
        </p>
        <div style="margin-top: 1.5rem;">
            <span class="tech-badge">🎯 Trade-off Analysis</span>
            <span class="tech-badge">🔍 Constraint-Aware</span>
            <span class="tech-badge">📊 Sensitivity Analysis</span>
            <span class="tech-badge">🔮 What-If Scenarios</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mission Statement
    st.markdown("""
    <div class="glass-alert-info">
        <strong>🎯 Mission:</strong> Help teams make informed database decisions by exposing trade-offs, 
        not declaring winners. Every constraint changes the game.
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # STEP 1: Get User Constraints (Sidebar) - Delegation to constraints.py
    # ========================================================================
    st.sidebar.markdown("### ⚙️ Define Your Constraints")
    
    # Get constraints from dedicated module (no duplication)
    constraints = get_user_constraints()
    
    # What-If Scenario (only UI element not in get_user_constraints)
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔮 What-If Scenario")
    scenario = st.sidebar.selectbox(
        "Test a scenario:",
        ["None", "Traffic increases 10x", "Team size doubles", "Budget cuts 30%", "Latency becomes critical"],
        help="See how choices hold up under changed conditions"
    )
    
    # ========================================================================
    # STEP 2: Load Database Options
    # ========================================================================
    options = get_database_options()
    
    # ========================================================================
    # STEP 3: Analyze Button
    # ========================================================================
    st.markdown("---")
    
    if st.button("🔍 Analyze Trade-offs", type="primary", use_container_width=True):
        st.session_state['analysis_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        st.markdown("### 📊 Trade-off Analysis")
        
        # Display constraint profile
        with st.expander("📌 Your Constraint Profile", expanded=False):
            constraint_dict = constraints.to_dict()
            for key, value in constraint_dict.items():
                st.markdown(f"**{key.replace('_', ' ').title()}:** `{value}`")
        
        # ========================================================================
        # STEP 4: Evaluate Each Option (Delegation)
        # ========================================================================
        evaluations = {}
        for option_name, option_data in options.items():
            evaluations[option_name] = evaluate_options(option_name, option_data, constraints)
        
        # ========================================================================
        # STEP 5: Run Advanced Analysis (Delegation)
        # ========================================================================
        fit_assessor = ConstraintFitAssessor(constraints)
        sensitivity_analyzer = ConstraintSensitivityAnalyzer(constraints)
        comparator = CrossOptionComparator(constraints)
        scenario_analyzer = WhatIfScenarioAnalyzer(constraints)
        
        sensitivities = sensitivity_analyzer.analyze_sensitivity()
        comparisons = comparator.generate_comparisons()
        
        # ========================================================================
        # STEP 6: Render Options with Fit Assessment
        # ========================================================================
        for option_name, evaluation in evaluations.items():
            option_data = options[option_name]
            
            # Get fit assessment
            fit_level, fit_reasoning, context_warning = fit_assessor.assess_fit(option_name)
            
            # Map fit levels to badges
            fit_badges = {
                "strong_fit": '<span class="fit-badge-strong">🟢 Strong Fit</span>',
                "moderate_fit": '<span class="fit-badge-moderate">🟡 Moderate Fit</span>',
                "risky_fit": '<span class="fit-badge-risky">🔴 Risky Fit</span>'
            }
            
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="color: #6A5D7B !important;">{option_name}</h3>
                <div style="margin: 1rem 0;">
                    {fit_badges[fit_level]}
                </div>
                <p style="color: #666; font-size: 1.1rem; margin: 1rem 0;">
                    <em>{fit_reasoning}</em>
                </p>
            """, unsafe_allow_html=True)
            
            if context_warning:
                st.markdown(f"""
                <div class="glass-alert-warning">
                    <strong>⚠️ Context Switch Warning:</strong> {context_warning}
                </div>
                """, unsafe_allow_html=True)
            
            # Option overview
            st.markdown(f"*{option_data['description']}*")
            
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"**Type:** {option_data['type']}")
                st.caption(f"**Pricing:** {option_data['pricing_model']}")
                st.caption(f"**Setup Time:** {option_data['setup_time']}")
            
            with col2:
                st.caption(f"**Scaling:** {option_data['scaling_model']}")
                st.caption(f"**Consistency:** {option_data['consistency']}")
                st.caption(f"**Complexity:** {option_data['base_complexity']}")
            
            st.markdown("---")
            
            # Trade-off analysis
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**✅ Strengths**")
                for strength in evaluation["strengths"]:
                    st.markdown(f"- {strength}")
                
                st.markdown("")
                st.markdown("**💸 Hidden Costs**")
                for cost in evaluation["hidden_costs"]:
                    st.markdown(f"- {cost}")
            
            with col2:
                st.markdown("**⚠️ Limitations**")
                for limitation in evaluation["limitations"]:
                    st.markdown(f"- {limitation}")
                
                st.markdown("")
                st.markdown("**❌ When NOT to Choose**")
                for avoid in evaluation["avoid_when"]:
                    st.markdown(f"- {avoid}")
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
        
        # ========================================================================
        # STEP 7: Constraint Sensitivity Analysis
        # ========================================================================
        st.markdown("### 🎚️ Constraint Sensitivity Analysis")
        st.markdown("*Which constraints have the most influence:*")
        
        # Sort by impact
        impact_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        sorted_sensitivities = sorted(
            sensitivities.items(),
            key=lambda x: impact_order[x[1][0]]
        )
        
        # Display as metric cards
        cols = st.columns(min(4, len(sorted_sensitivities)))
        
        impact_colors = {
            "HIGH": "rgba(244, 151, 142, 0.7)",
            "MEDIUM": "rgba(249, 199, 79, 0.7)",
            "LOW": "rgba(163, 201, 168, 0.7)"
        }
        
        for idx, (col, (constraint_name, (impact, explanation))) in enumerate(zip(cols, sorted_sensitivities[:4])):
            with col:
                display_name = constraint_name.replace("_", " ").title()
                st.markdown(f"""
                <div class="metric-glass-card" style="background: {impact_colors[impact]};">
                    <div class="metric-label">{display_name}</div>
                    <div class="metric-value">{impact}</div>
                    <div class="metric-label" style="font-size: 0.8rem;">Impact</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Explanations for HIGH impact
        st.markdown("<br>", unsafe_allow_html=True)
        for constraint_name, (impact, explanation) in sorted_sensitivities:
            if impact == "HIGH":
                st.markdown(f"""
                <div class="glass-alert-info">
                    <strong>{constraint_name.replace('_', ' ').title()}:</strong> {explanation}
                </div>
                """, unsafe_allow_html=True)
        
        # ========================================================================
        # STEP 8: Direct Comparisons
        # ========================================================================
        st.markdown("---")
        st.markdown("### 🔄 Direct Comparisons")
        
        for comparison in comparisons:
            st.markdown(f"""
            <div class="glass-alert-info">
                {comparison}
            </div>
            """, unsafe_allow_html=True)
        
        # ========================================================================
        # STEP 9: What-If Scenario Analysis
        # ========================================================================
        if scenario != "None":
            st.markdown("---")
            st.markdown(f"### 🔮 What-If Analysis: {scenario}")
            
            scenario_map = {
                "Traffic increases 10x": "traffic_10x",
                "Team size doubles": "team_doubles",
                "Budget cuts 30%": "budget_cuts",
                "Latency becomes critical": "latency_critical"
            }
            
            scenario_results = scenario_analyzer.analyze_scenario(scenario_map[scenario])
            
            # Guard against empty results
            if scenario_results:
                col1, col2 = st.columns(2)
                
                for idx, (col, (opt_name, result)) in enumerate(zip([col1, col2, col1, col2], scenario_results.items())):
                    with col:
                        st.markdown(f"""
                        <div class="glass-card">
                            <h4 style="color: #6A5D7B !important;">{opt_name}</h4>
                            <p style="color: #666;">{result}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        if idx % 2 == 1:
                            st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.warning("Scenario analysis unavailable for selected combination.")
        
        # ========================================================================
        # STEP 10: Referee Insight (Delegation)
        # ========================================================================
        st.markdown("---")
        st.markdown("### 🎯 Referee Insight")
        
        referee_insight = generate_referee_insight(
            evaluations,
            constraints.to_dict(),
            options
        )
        
        st.markdown(f"""
        <div class="glass-alert-success">
            {referee_insight.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
        
        # ========================================================================
        # STEP 11: Assumptions
        # ========================================================================
        with st.expander("📋 Analysis Assumptions", expanded=False):
            st.markdown("**This analysis assumes:**")
            assumptions = [
                "All options are managed/cloud services",
                "Standard AWS pricing without heavy discounts",
                "No existing infrastructure lock-in",
                "Team can learn new technologies with time",
                "Data sovereignty is not a constraint"
            ]
            for assumption in assumptions:
                st.markdown(f"- {assumption}")
        
        # ========================================================================
        # STEP 12: Export Summary
        # ========================================================================
        st.markdown("---")
        st.markdown("### 📥 Export Decision Summary")
        
        summary_parts = [
            f"# Database Decision Analysis\n**Generated:** {st.session_state['analysis_timestamp']}\n\n",
            "## Constraints\n"
        ]
        
        for key, value in constraints.to_dict().items():
            summary_parts.append(f"- **{key.title()}:** {value}\n")
        
        summary_parts.append("\n## Constraint Sensitivity\n")
        for name, (impact, explanation) in sorted_sensitivities:
            summary_parts.append(f"- **{name.title()} ({impact}):** {explanation}\n")
        
        summary_parts.append(f"\n## Referee Insight\n{referee_insight}\n")
        
        summary_text = "".join(summary_parts)
        
        st.download_button(
            label="📄 Download Analysis (Markdown)",
            data=summary_text,
            file_name="database_decision_analysis.md",
            mime="text/markdown"
        )
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer">
        <div class="hero-logo" style="font-size: 2.5rem;">⚖️</div>
        <h3 style="color: #6A5D7B !important; margin: 1rem 0;">The Referee</h3>
        <p style="font-size: 1.2rem; color: #8E8D8A; margin-bottom: 1.5rem;">
            Constraint-Driven Database Advisor — No Winners, Just Trade-offs
        </p>
        <div style="margin: 1.5rem 0;">
            <span class="tech-badge">🎯 Trade-off Analysis</span>
            <span class="tech-badge">🔍 Constraint-Aware</span>
            <span class="tech-badge">📊 Sensitivity Analysis</span>
            <span class="tech-badge">🔮 What-If Scenarios</span>
        </div>
        <p style="opacity: 0.7; font-size: 0.95rem; margin-top: 2rem;">
            Built for Kiro Week 6 Challenge | Rule-Driven Decision Support<br>
            Powered by Python + Streamlit | © 2026 The Referee
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()