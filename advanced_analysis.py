"""
Advanced analysis modules for The Referee
- Constraint Fit Assessment
- Sensitivity Analysis  
- Cross-Option Comparison
- What-If Scenario Analysis
"""

from typing import Dict, List, Tuple
from constraints import Constraints, Budget, Performance, Scale, TeamSkill, TimeToMarket

# ============================================================================
# CONSTRAINT FIT ASSESSOR
# ============================================================================

class ConstraintFitAssessor:
    """Assesses how well each option fits the user's constraints"""
    
    def __init__(self, constraints: Constraints):
        self.constraints = constraints
    
    def assess_fit(self, option_key: str) -> Tuple[str, str, str]:
        """
        Returns:
        - fit_level: "strong_fit", "moderate_fit", "risky_fit"
        - reasoning: Why this fit level
        - context_warning: Situations where fit degrades
        """
        
        constraints_dict = self.constraints.to_dict()
        
        if option_key == "PostgreSQL (RDS)":
            return self._assess_postgres()
        elif option_key == "DynamoDB":
            return self._assess_dynamodb()
        elif option_key == "MongoDB Atlas":
            return self._assess_mongodb()
        elif option_key == "Redis (ElastiCache)":
            return self._assess_redis()
        
        return "moderate_fit", "Evaluation pending", ""
    
    def _assess_postgres(self) -> Tuple[str, str, str]:
        c = self.constraints.to_dict()
        
        # Strong fit conditions
        if (c["data_complexity"] == "complex" and 
            c["consistency"] == "strong" and
            c["team_skill"] in ["intermediate", "expert"]):
            return (
                "strong_fit",
                "Excellent match for complex relational data with strong consistency needs",
                "Fit degrades if traffic scales beyond single-master capacity"
            )
        
        # Risky fit conditions
        if (c["budget"] == "low" and c["scale"] == "massive"):
            return (
                "risky_fit",
                "Expensive at massive scale with always-on costs",
                "Cost escalates quickly with Multi-AZ and read replicas"
            )
        
        if c["team_skill"] == "beginner":
            return (
                "risky_fit",
                "Requires SQL expertise and query optimization knowledge",
                "Team may struggle with schema migrations and performance tuning"
            )
        
        return (
            "moderate_fit",
            "Solid general-purpose choice with proven reliability",
            "Watch for scaling challenges beyond 100K concurrent connections"
        )
    
    def _assess_dynamodb(self) -> Tuple[str, str, str]:
        c = self.constraints.to_dict()
        
        # Strong fit conditions
        if (c["scale"] == "massive" and 
            c["data_complexity"] == "simple" and
            c["performance_priority"] in ["latency", "throughput"]):
            return (
                "strong_fit",
                "Purpose-built for massive scale with simple access patterns",
                "Fit degrades if query patterns become complex or unpredictable"
            )
        
        if (c["budget"] == "low" and c["scale"] == "small"):
            return (
                "strong_fit",
                "Free tier covers small workloads with pay-per-use pricing",
                "Watch costs if you add multiple GSIs"
            )
        
        # Risky fit conditions
        if c["data_complexity"] == "complex":
            return (
                "risky_fit",
                "Complex queries require denormalization and application-side joins",
                "Data model changes are expensive once in production"
            )
        
        return (
            "moderate_fit",
            "Versatile NoSQL option with excellent scaling characteristics",
            "Costs can spike unexpectedly with poor access pattern design"
        )
    
    def _assess_mongodb(self) -> Tuple[str, str, str]:
        c = self.constraints.to_dict()
        
        # Strong fit conditions
        if (c["time_to_market"] == "urgent" and 
            c["data_complexity"] in ["simple", "moderate"] and
            c["team_skill"] == "beginner"):
            return (
                "strong_fit",
                "Flexible schema enables rapid iteration with gentle learning curve",
                "Fit degrades if strict consistency or complex transactions become critical"
            )
        
        # Risky fit conditions
        if (c["budget"] == "low" and c["team_skill"] == "beginner"):
            return (
                "risky_fit",
                "Costs escalate quickly with poor query patterns and indexing",
                "Requires expertise to avoid expensive memory spikes"
            )
        
        return (
            "moderate_fit",
            "Good balance of flexibility and query capability",
            "Transaction performance degrades across shards"
        )
    
    def _assess_redis(self) -> Tuple[str, str, str]:
        c = self.constraints.to_dict()
        
        # Strong fit conditions
        if (c["performance_priority"] == "latency" and 
            c["scale"] in ["small", "medium"]):
            return (
                "strong_fit",
                "Sub-millisecond latency perfect for caching and session storage",
                "NOT suitable as primary database - requires persistence strategy"
            )
        
        # Risky fit conditions
        if c["scale"] == "massive":
            return (
                "risky_fit",
                "Memory costs become prohibitive at massive dataset sizes",
                "Best for hot data caching, not primary storage at scale"
            )
        
        return (
            "moderate_fit",
            "Excellent complement to other databases for performance boost",
            "Requires careful data eviction and persistence configuration"
        )


# ============================================================================
# CONSTRAINT SENSITIVITY ANALYZER
# ============================================================================

class ConstraintSensitivityAnalyzer:
    """Analyzes which constraints have the most impact on decision"""
    
    def __init__(self, constraints: Constraints):
        self.constraints = constraints
    
    def analyze_sensitivity(self) -> Dict[str, Tuple[str, str]]:
        """
        Returns dict of constraint_name -> (impact_level, explanation)
        Impact levels: "HIGH", "MEDIUM", "LOW"
        """
        c = self.constraints.to_dict()
        sensitivities = {}
        
        # Budget sensitivity
        if c["budget"] == "low":
            sensitivities["budget"] = (
                "HIGH",
                "Low budget significantly limits options - usage-based pricing becomes critical"
            )
        else:
            sensitivities["budget"] = (
                "MEDIUM",
                "Budget allows flexibility - focus on technical fit over cost"
            )
        
        # Scale sensitivity
        if c["scale"] == "massive":
            sensitivities["scale"] = (
                "HIGH",
                "Massive scale eliminates options without proven horizontal scaling"
            )
        elif c["scale"] == "small":
            sensitivities["scale"] = (
                "LOW",
                "All options work at small scale - prioritize other factors"
            )
        else:
            sensitivities["scale"] = (
                "MEDIUM",
                "Medium scale requires careful capacity planning"
            )
        
        # Performance priority sensitivity
        if c["performance_priority"] == "latency":
            sensitivities["performance_priority"] = (
                "HIGH",
                "Latency requirements strongly favor in-memory or low-latency options"
            )
        else:
            sensitivities["performance_priority"] = (
                "MEDIUM",
                "Performance needs are flexible - most options can work"
            )
        
        # Team skill sensitivity
        if c["team_skill"] == "beginner":
            sensitivities["team_skill"] = (
                "HIGH",
                "Beginner team needs managed services with low operational complexity"
            )
        else:
            sensitivities["team_skill"] = (
                "LOW",
                "Experienced team can handle complexity - focus on technical requirements"
            )
        
        # Data complexity sensitivity
        if c["data_complexity"] == "complex":
            sensitivities["data_complexity"] = (
                "HIGH",
                "Complex data model strongly favors relational databases with JOIN support"
            )
        else:
            sensitivities["data_complexity"] = (
                "MEDIUM",
                "Simple data model offers flexibility across database types"
            )
        
        # Time to market sensitivity
        if c["time_to_market"] == "urgent":
            sensitivities["time_to_market"] = (
                "MEDIUM",
                "Urgency favors fast setup but shouldn't override technical fit"
            )
        else:
            sensitivities["time_to_market"] = (
                "LOW",
                "Flexible timeline allows proper evaluation - prioritize long-term fit"
            )
        
        # Consistency sensitivity
        if c["consistency"] == "strong":
            sensitivities["consistency"] = (
                "HIGH",
                "Strong consistency requirement eliminates eventually-consistent options"
            )
        else:
            sensitivities["consistency"] = (
                "LOW",
                "Eventual consistency acceptable - opens up high-performance options"
            )
        
        return sensitivities


# ============================================================================
# CROSS-OPTION COMPARATOR
# ============================================================================

class CrossOptionComparator:
    """Generates direct comparisons between options"""
    
    def __init__(self, constraints: Constraints):
        self.constraints = constraints
    
    def generate_comparisons(self) -> List[str]:
        """Returns list of comparison statements"""
        c = self.constraints.to_dict()
        comparisons = []
        
        # PostgreSQL vs DynamoDB
        if c["data_complexity"] == "complex":
            comparisons.append(
                "**PostgreSQL vs DynamoDB:** For complex data, PostgreSQL's JOINs and "
                "transactions are native, while DynamoDB requires denormalization and "
                "application-side logic. PostgreSQL wins on data modeling flexibility."
            )
        else:
            comparisons.append(
                "**PostgreSQL vs DynamoDB:** For simple data, DynamoDB's auto-scaling "
                "and pay-per-use pricing is more cost-effective than PostgreSQL's "
                "always-on instances. DynamoDB wins on operational simplicity."
            )
        
        # MongoDB vs PostgreSQL
        comparisons.append(
            "**MongoDB vs PostgreSQL:** MongoDB offers schema flexibility for rapid "
            "iteration, while PostgreSQL enforces structure for data integrity. "
            "Choose MongoDB for evolving schemas, PostgreSQL for stable data models."
        )
        
        # DynamoDB vs Redis
        if c["performance_priority"] == "latency":
            comparisons.append(
                "**DynamoDB vs Redis:** Redis provides sub-millisecond latency but "
                "isn't a primary database. DynamoDB offers single-digit millisecond "
                "latency as a full database. Use Redis for caching + another DB for storage."
            )
        
        # Scale-based comparison
        if c["scale"] == "massive":
            comparisons.append(
                "**At Massive Scale:** DynamoDB and MongoDB Atlas are purpose-built "
                "for horizontal scaling. PostgreSQL requires architectural workarounds "
                "(sharding, read replicas) that increase complexity significantly."
            )
        
        return comparisons


# ============================================================================
# WHAT-IF SCENARIO ANALYZER
# ============================================================================

class WhatIfScenarioAnalyzer:
    """Analyzes how options perform under changed conditions"""
    
    def __init__(self, constraints: Constraints):
        self.constraints = constraints
    
    def analyze_scenario(self, scenario: str) -> Dict[str, str]:
        """
        Analyzes specific scenarios:
        - traffic_10x: Traffic increases 10x
        - team_doubles: Team size doubles
        - budget_cuts: Budget reduced 30%
        - latency_critical: Latency requirement becomes <50ms
        """
        
        if scenario == "traffic_10x":
            return self._scenario_traffic_spike()
        elif scenario == "team_doubles":
            return self._scenario_team_growth()
        elif scenario == "budget_cuts":
            return self._scenario_budget_cuts()
        elif scenario == "latency_critical":
            return self._scenario_latency_critical()
        
        return {}
    
    def _scenario_traffic_spike(self) -> Dict[str, str]:
        return {
            "PostgreSQL (RDS)": 
                "⚠️ **Struggles** - Requires manual scaling, potential downtime for vertical "
                "scaling. Read replicas help but write bottleneck remains.",
            
            "DynamoDB": 
                "✅ **Excels** - Auto-scales seamlessly. Costs increase but performance "
                "remains consistent. No intervention needed.",
            
            "MongoDB Atlas": 
                "✅ **Handles Well** - Auto-scaling enabled. May need shard rebalancing "
                "but generally transparent. Some manual tuning beneficial.",
            
            "Redis (ElastiCache)": 
                "⚠️ **Depends** - If used for caching, helps other databases handle spike. "
                "If primary store, memory limits hit quickly. Manual scaling needed."
        }
    
    def _scenario_team_growth(self) -> Dict[str, str]:
        return {
            "PostgreSQL (RDS)": 
                "✅ **Better** - More hands available for optimization, schema management. "
                "Team can leverage PostgreSQL's advanced features effectively.",
            
            "DynamoDB": 
                "➡️ **Neutral** - Managed service benefit diminishes with larger team. "
                "Team may desire more control that DynamoDB doesn't offer.",
            
            "MongoDB Atlas": 
                "✅ **Better** - Larger team can optimize queries, manage sharding. "
                "Flexibility becomes more valuable with diverse use cases.",
            
            "Redis (ElastiCache)": 
                "➡️ **Neutral** - Additional expertise helps with cache strategies "
                "but operational complexity remains manageable."
        }
    
    def _scenario_budget_cuts(self) -> Dict[str, str]:
        return {
            "PostgreSQL (RDS)": 
                "⚠️ **Painful** - Always-on costs can't be reduced easily. May need to "
                "downgrade instance size, impacting performance. Reserved instances help but lock in costs.",
            
            "DynamoDB": 
                "✅ **Flexible** - Can switch to on-demand or reduce provisioned capacity. "
                "Costs scale down with usage. Most adaptable to budget cuts.",
            
            "MongoDB Atlas": 
                "⚠️ **Moderate Pain** - Can downgrade cluster but may impact performance. "
                "Watch for unexpected costs from unoptimized queries under constraints.",
            
            "Redis (ElastiCache)": 
                "⚠️ **Difficult** - Memory-intensive so hard to cut costs without "
                "removing functionality. May need to reduce cache size or scope."
        }
    
    def _scenario_latency_critical(self) -> Dict[str, str]:
        return {
            "PostgreSQL (RDS)": 
                "❌ **Struggles** - Typical latency 10-50ms under load. Optimization helps "
                "but can't match in-memory solutions. Would need Redis caching layer.",
            
            "DynamoDB": 
                "⚠️ **Borderline** - Single-digit milliseconds typical but may spike. "
                "DAX (DynamoDB Accelerator) adds cost but provides microsecond latency.",
            
            "MongoDB Atlas": 
                "❌ **Struggles** - Similar to PostgreSQL, typically 10-50ms. Would need "
                "caching layer or architectural changes to meet <50ms consistently.",
            
            "Redis (ElastiCache)": 
                "✅ **Excels** - Sub-millisecond latency is Redis's strength. Perfect for "
                "latency-critical operations but remember it's a cache, not primary DB."
        }
