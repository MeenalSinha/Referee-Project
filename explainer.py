def generate_referee_insight(evaluations, constraints, options):
    """
    Generates the 'Referee Insight' - an objective analysis without declaring a winner.
    Shows which options align with which constraints and highlights critical trade-offs.
    """
    
    insight = []
    
    # Analyze constraint alignment
    insight.append("## 🎯 Constraint Alignment Analysis\n")
    
    # Budget Analysis
    if constraints["budget"] == "low":
        insight.append("**Budget Considerations (Low Budget):**")
        insight.append("- DynamoDB's usage-based pricing can be cost-effective for variable workloads, but watch for unexpected spikes with GSIs")
        insight.append("- PostgreSQL RDS has predictable costs but runs 24/7 even at low traffic")
        insight.append("- Redis ElastiCache memory costs add up quickly - only use for hot data\n")
    elif constraints["budget"] == "high":
        insight.append("**Budget Considerations (High Budget):**")
        insight.append("- All options are viable - focus on technical fit over cost")
        insight.append("- Consider reserved instances for RDS/ElastiCache for 40-60% savings")
        insight.append("- Budget allows for optimal configurations (Multi-AZ, read replicas, performance insights)\n")
    
    # Scale Analysis
    if constraints["scale"] == "massive":
        insight.append("**Scale Considerations (Massive Scale):**")
        insight.append("- DynamoDB and MongoDB Atlas are purpose-built for massive horizontal scaling")
        insight.append("- PostgreSQL RDS requires architectural workarounds (sharding, read replicas) at this scale")
        insight.append("- Redis ElastiCache works best for hot data caching, not primary storage at massive scale\n")
    elif constraints["scale"] == "small":
        insight.append("**Scale Considerations (Small Scale):**")
        insight.append("- Any option works at small scale - prioritize ease of use and development speed")
        insight.append("- Avoid over-engineering - DynamoDB's auto-scaling may be overkill")
        insight.append("- Consider total operational burden over raw performance\n")
    
    # Performance Priority Analysis
    if constraints["performance_priority"] == "latency":
        insight.append("**Performance Priority (Latency):**")
        insight.append("- Redis ElastiCache provides sub-millisecond latency but requires architecture planning")
        insight.append("- DynamoDB offers single-digit millisecond latency with consistent performance")
        insight.append("- PostgreSQL and MongoDB have higher latency, especially under load\n")
    elif constraints["performance_priority"] == "throughput":
        insight.append("**Performance Priority (Throughput):**")
        insight.append("- DynamoDB excels at high write throughput with unlimited on-demand capacity")
        insight.append("- MongoDB Atlas handles high throughput through sharding")
        insight.append("- PostgreSQL RDS hits write bottlenecks due to single-master architecture\n")
    
    # Team Skill Analysis
    if constraints["team_skill"] == "beginner":
        insight.append("**Team Skill Considerations (Beginner):**")
        insight.append("- DynamoDB and MongoDB have gentler learning curves and good documentation")
        insight.append("- PostgreSQL requires SQL expertise and query optimization knowledge")
        insight.append("- Redis requires understanding of caching strategies and eviction policies")
        insight.append("- Managed services reduce operational burden for all skill levels\n")
    elif constraints["team_skill"] == "expert":
        insight.append("**Team Skill Considerations (Expert):**")
        insight.append("- PostgreSQL rewards expertise with powerful features (advanced indexing, extensions, partitioning)")
        insight.append("- Your team can handle the complexity of any option and optimize for specific workloads")
        insight.append("- Consider whether simpler options might be limiting for advanced use cases\n")
    
    # Data Complexity Analysis
    if constraints["data_complexity"] == "complex":
        insight.append("**Data Complexity (Complex):**")
        insight.append("- PostgreSQL handles complex relationships, JOINs, and constraints natively")
        insight.append("- DynamoDB requires denormalization and application-side JOINs for complex queries")
        insight.append("- MongoDB can embed related data but struggles with many-to-many relationships\n")
    elif constraints["data_complexity"] == "simple":
        insight.append("**Data Complexity (Simple):**")
        insight.append("- DynamoDB is ideal for simple key-value patterns")
        insight.append("- PostgreSQL may be over-engineered for simple data models")
        insight.append("- Consider whether you're paying for features you won't use\n")
    
    # Critical Trade-offs Section
    insight.append("---\n")
    insight.append("## ⚖️ Critical Trade-Offs to Consider\n")
    
    # Identify the key tensions
    if constraints["budget"] == "low" and constraints["scale"] == "massive":
        insight.append("**⚠️ Budget vs Scale Tension:**")
        insight.append("- Massive scale on low budget is challenging")
        insight.append("- DynamoDB's auto-scaling can get expensive fast")
        insight.append("- Consider PostgreSQL with careful capacity planning, but expect manual scaling work\n")
    
    if constraints["time_to_market"] == "urgent" and constraints["data_complexity"] == "complex":
        insight.append("**⚠️ Speed vs Complexity Tension:**")
        insight.append("- Complex data models take time to design properly")
        insight.append("- MongoDB's flexible schema enables faster iteration but may cause consistency issues later")
        insight.append("- PostgreSQL forces upfront design but reduces refactoring pain\n")
    
    if constraints["consistency"] == "strong" and constraints["performance_priority"] == "latency":
        insight.append("**⚠️ Consistency vs Latency Tension:**")
        insight.append("- Strong consistency adds latency due to coordination overhead")
        insight.append("- DynamoDB's strongly consistent reads are slower than eventually consistent")
        insight.append("- Consider if eventual consistency is acceptable for your use case\n")
    
    if constraints["team_skill"] == "beginner" and constraints["scale"] == "massive":
        insight.append("**⚠️ Team Skill vs Scale Tension:**")
        insight.append("- Massive scale systems are inherently complex")
        insight.append("- Managed services (DynamoDB, MongoDB Atlas) reduce operational burden")
        insight.append("- Budget for training or senior database expertise as you scale\n")
    
    # Situational Guidance
    insight.append("---\n")
    insight.append("## 💡 Situational Guidance\n")
    
    # Create scenario-based guidance
    if constraints["budget"] == "low" and constraints["team_skill"] == "beginner" and constraints["time_to_market"] == "urgent":
        insight.append("**Your Profile: Cost-Conscious Startup**")
        insight.append("- MongoDB Atlas or DynamoDB align best with your constraints")
        insight.append("- Both offer fast setup, managed operations, and scale when needed")
        insight.append("- MongoDB provides more query flexibility; DynamoDB requires upfront access pattern design")
        insight.append("- **Critical consideration:** MongoDB becomes expensive if queries aren't optimized")
        insight.append("- **Critical consideration:** DynamoDB becomes expensive if you add many GSIs\n")
    
    elif constraints["budget"] == "high" and constraints["scale"] == "massive" and constraints["team_skill"] == "expert":
        insight.append("**Your Profile: Enterprise at Scale**")
        insight.append("- All options are viable - choose based on data model and access patterns")
        insight.append("- PostgreSQL works if you can architect around single-master limitations")
        insight.append("- DynamoDB handles unlimited scale but requires expert data modeling")
        insight.append("- **Critical consideration:** Migration difficulty increases with scale - choose carefully")
        insight.append("- **Critical consideration:** Multi-region complexity differs significantly across options\n")
    
    elif constraints["data_complexity"] == "complex" and constraints["consistency"] == "strong":
        insight.append("**Your Profile: Transaction-Heavy Application**")
        insight.append("- PostgreSQL RDS aligns best with complex relational data and strong consistency")
        insight.append("- ACID guarantees, JOINs, and constraints are native to PostgreSQL")
        insight.append("- MongoDB and DynamoDB require architectural workarounds for complex transactions")
        insight.append("- **Critical consideration:** PostgreSQL scaling limitations may require future sharding")
        insight.append("- **Critical consideration:** Strong consistency across distributed databases adds latency\n")
    
    elif constraints["performance_priority"] == "latency" and constraints["scale"] == "small":
        insight.append("**Your Profile: Low-Latency Application**")
        insight.append("- Redis ElastiCache provides the best latency but isn't a primary database")
        insight.append("- Consider Redis + another database (PostgreSQL or DynamoDB) for architecture")
        insight.append("- DynamoDB alone offers good latency at single-digit milliseconds")
        insight.append("- **Critical consideration:** Redis requires persistence strategy for data durability")
        insight.append("- **Critical consideration:** Two-database architecture increases complexity\n")
    
    else:
        insight.append("**Your Profile: Balanced Requirements**")
        insight.append("- No single option dominates - each brings different trade-offs")
        insight.append("- PostgreSQL RDS: Best for complex queries, worse for write-heavy workloads")
        insight.append("- DynamoDB: Best for scale and throughput, worse for complex queries")
        insight.append("- MongoDB Atlas: Best for flexibility, worse for strict consistency")
        insight.append("- Redis ElastiCache: Best for caching, not suitable as primary database\n")
    
    # Final Referee Statement
    insight.append("---\n")
    insight.append("## 🏁 Final Referee Statement\n")
    insight.append("**We don't declare a winner because the 'best' choice depends on what you're willing to trade off.**\n")
    
    # Provide decision framework
    insight.append("**Ask yourself:**")
    insight.append("1. What failure mode am I LEAST willing to accept? (Cost overruns? Downtime? Slow queries?)")
    insight.append("2. Which complexity am I most prepared to handle? (SQL optimization? NoSQL data modeling? Caching strategies?)")
    insight.append("3. What might change in 12 months? (Team size? User scale? Feature complexity?)")
    insight.append("4. Where is migration difficulty acceptable? (Some choices are harder to migrate away from)\n")
    
    insight.append("**Remember:** The right choice is one that aligns with your constraints AND your team's ability to manage the trade-offs. ")
    insight.append("There's no perfect database - only trade-offs you can live with.")
    
    return "\n".join(insight)
