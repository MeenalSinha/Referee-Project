import streamlit as st
from dataclasses import dataclass
from typing import Dict
from enum import Enum

# ============================================================================
# ENUMS - Constraint Type Definitions
# ============================================================================

class Budget(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Performance(Enum):
    LATENCY = "latency"
    THROUGHPUT = "throughput"
    BALANCED = "balanced"

class Scale(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    MASSIVE = "massive"

class TeamSkill(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"

class TimeToMarket(Enum):
    URGENT = "urgent"
    FLEXIBLE = "flexible"

class DataComplexity(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"

class Consistency(Enum):
    EVENTUAL = "eventual"
    STRONG = "strong"

# ============================================================================
# DATACLASS - Structured Constraints
# ============================================================================

@dataclass
class Constraints:
    budget: Budget
    performance: Performance
    scale: Scale
    team_skill: TeamSkill
    time_to_market: TimeToMarket
    data_complexity: DataComplexity
    consistency: Consistency
    
    def to_dict(self) -> Dict[str, str]:
        """Convert constraints to dictionary for easy access"""
        return {
            "budget": self.budget.value,
            "performance_priority": self.performance.value,
            "scale": self.scale.value,
            "team_skill": self.team_skill.value,
            "time_to_market": self.time_to_market.value,
            "data_complexity": self.data_complexity.value,
            "consistency": self.consistency.value
        }

# ============================================================================
# UI FUNCTION - Streamlit Input Handling
# ============================================================================

def get_user_constraints() -> Constraints:
    """
    Captures user constraints through Streamlit UI components.
    Returns a structured Constraints dataclass object.
    """
    
    # Budget Constraint
    st.sidebar.subheader("💵 Budget")
    budget_val = st.sidebar.select_slider(
        "What's your budget level?",
        options=["low", "medium", "high"],
        value="medium",
        help="Low: Cost-sensitive, Medium: Balanced, High: Performance over cost"
    )
    
    # Performance Priority
    st.sidebar.subheader("⚡ Performance Priority")
    perf_val = st.sidebar.selectbox(
        "What matters most for performance?",
        ["latency", "throughput", "balanced"],
        index=2,
        help="Latency: Fast response times, Throughput: High volume processing, Balanced: Both"
    )
    
    # Scale
    st.sidebar.subheader("📈 Expected Scale")
    scale_val = st.sidebar.select_slider(
        "How big will your application scale?",
        options=["small", "medium", "massive"],
        value="small",
        help="Small: <10K users, Medium: 10K-1M users, Massive: >1M users"
    )
    
    # Team Skill Level
    st.sidebar.subheader("👥 Team Skill Level")
    skill_val = st.sidebar.selectbox(
        "What's your team's database expertise?",
        ["beginner", "intermediate", "expert"],
        index=0,
        help="Be honest - this affects operational complexity"
    )
    
    # Time to Market
    st.sidebar.subheader("⏰ Time to Market")
    time_val = st.sidebar.radio(
        "How urgent is your launch?",
        ["urgent", "flexible"],
        index=0,
        help="Urgent: Need to ship fast, Flexible: Can spend time on setup"
    )
    
    # Data Complexity
    st.sidebar.subheader("🗂️ Data Complexity")
    complexity_val = st.sidebar.selectbox(
        "How complex is your data model?",
        ["simple", "moderate", "complex"],
        index=1,
        help="Simple: Key-value, Moderate: Relational, Complex: Multi-model/Graph"
    )
    
    # Consistency Requirements
    st.sidebar.subheader("🔒 Consistency Needs")
    consistency_val = st.sidebar.selectbox(
        "What are your consistency requirements?",
        ["eventual", "strong"],
        index=1,
        help="Eventual: Can tolerate slight delays, Strong: Must be immediately consistent"
    )
    
    # Create and return Constraints dataclass
    return Constraints(
        budget=Budget(budget_val),
        performance=Performance(perf_val),
        scale=Scale(scale_val),
        team_skill=TeamSkill(skill_val),
        time_to_market=TimeToMarket(time_val),
        data_complexity=DataComplexity(complexity_val),
        consistency=Consistency(consistency_val)
    )
