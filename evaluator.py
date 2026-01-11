def evaluate_options(option_name, option_data, constraints):
    """
    Evaluates a database option against user constraints.
    Returns strengths, limitations, hidden costs, and when to avoid.
    
    This is the TRADE-OFF ENGINE - the heart of The Referee.
    
    Args:
        constraints: Can be either a dict or Constraints dataclass
    """
    
    # Convert dataclass to dict if needed
    if hasattr(constraints, 'to_dict'):
        constraints = constraints.to_dict()
    
    evaluation = {
        "strengths": [],
        "limitations": [],
        "hidden_costs": [],
        "avoid_when": []
    }
    
    # ==========================
    # BUDGET-DRIVEN EVALUATION
    # ==========================
    
    if constraints["budget"] == "low":
        if option_data["pricing_model"] == "usage_based":
            evaluation["strengths"].append("Pay only for what you use - great for variable workloads")
        else:
            evaluation["limitations"].append("Always-on instance costs even during low usage")
        
        if option_name == "PostgreSQL (RDS)":
            evaluation["hidden_costs"].append("Multi-AZ deployment doubles costs but often necessary for production")
        
        if option_name == "MongoDB Atlas":
            evaluation["hidden_costs"].append("Memory usage can spike with poor indexing, increasing cluster size")
        
        if option_name == "Redis (ElastiCache)":
            evaluation["hidden_costs"].append("High memory costs for large datasets - RAM is expensive")
    
    elif constraints["budget"] == "high":
        if option_data["pricing_model"] == "instance_based":
            evaluation["strengths"].append("Predictable costs with reserved instances available")
        
        if option_name == "PostgreSQL (RDS)":
            evaluation["strengths"].append("Can afford performance insights, read replicas, and optimized instances")
    
    # ==========================
    # PERFORMANCE-DRIVEN EVALUATION
    # ==========================
    
    if constraints["performance_priority"] == "latency":
        if option_name == "Redis (ElastiCache)":
            evaluation["strengths"].append("Sub-millisecond latency for reads and writes")
        elif option_name == "DynamoDB":
            evaluation["strengths"].append("Single-digit millisecond latency at any scale")
        else:
            evaluation["limitations"].append("Higher latency than in-memory or pure key-value stores")
    
    elif constraints["performance_priority"] == "throughput":
        if option_name == "DynamoDB":
            evaluation["strengths"].append("Unlimited throughput with on-demand mode")
        elif option_name == "MongoDB Atlas":
            evaluation["strengths"].append("Horizontal scaling handles high write throughput well")
        elif option_name == "PostgreSQL (RDS)":
            evaluation["limitations"].append("Write throughput limited by single-master architecture")
    
    elif constraints["performance_priority"] == "balanced":
        if option_name == "MongoDB Atlas":
            evaluation["strengths"].append("Good balance of read/write performance with flexible queries")
    
    # ==========================
    # SCALE-DRIVEN EVALUATION
    # ==========================
    
    if constraints["scale"] == "small":
        if option_data["setup_time"] == "fast":
            evaluation["strengths"].append("Quick to set up - perfect for small scale")
        
        if option_name == "DynamoDB":
            evaluation["avoid_when"].append("Your data access patterns are simple and cost matters more than auto-scaling")
    
    elif constraints["scale"] == "medium":
        if option_data["scaling_model"] in ["horizontal", "automatic"]:
            evaluation["strengths"].append("Scales smoothly as your user base grows")
    
    elif constraints["scale"] == "massive":
        if option_name == "DynamoDB":
            evaluation["strengths"].append("Proven at massive scale - handles millions of requests per second")
        elif option_name == "MongoDB Atlas":
            evaluation["strengths"].append("Sharding enables horizontal scaling to massive datasets")
        elif option_name == "PostgreSQL (RDS)":
            evaluation["limitations"].append("Vertical scaling has limits - eventual need for sharding or read replicas")
            evaluation["hidden_costs"].append("Read replica lag and synchronization complexity at scale")
        elif option_name == "Redis (ElastiCache)":
            evaluation["hidden_costs"].append("Memory costs become prohibitive at massive scale")
            evaluation["avoid_when"].append("You need to store terabytes of data - Redis is best for hot data")
    
    # ==========================
    # TEAM SKILL EVALUATION
    # ==========================
    
    if constraints["team_skill"] == "beginner":
        if option_data["base_complexity"] == "beginner":
            evaluation["strengths"].append("Gentle learning curve - good for teams new to databases")
        else:
            evaluation["limitations"].append("Requires database expertise for optimization and troubleshooting")
        
        if option_name == "PostgreSQL (RDS)":
            evaluation["avoid_when"].append("Your team lacks SQL and query optimization experience")
        
        if option_name == "Redis (ElastiCache)":
            evaluation["avoid_when"].append("Your team isn't familiar with caching strategies and data eviction policies")
    
    elif constraints["team_skill"] == "intermediate":
        if option_name == "MongoDB Atlas":
            evaluation["strengths"].append("Intuitive document model bridges SQL and NoSQL paradigms")
    
    elif constraints["team_skill"] == "expert":
        if option_name == "PostgreSQL (RDS)":
            evaluation["strengths"].append("Rich feature set rewards deep expertise - advanced indexing, partitioning, extensions")
        
        if option_data["base_complexity"] == "beginner":
            evaluation["limitations"].append("May feel limiting if team wants fine-grained control")
    
    # ==========================
    # TIME TO MARKET EVALUATION
    # ==========================
    
    if constraints["time_to_market"] == "urgent":
        if option_data["setup_time"] == "fast":
            evaluation["strengths"].append("Minimal setup time - deploy and iterate quickly")
        else:
            evaluation["limitations"].append("Setup and configuration takes time away from feature development")
        
        if option_data["managed"]:
            evaluation["strengths"].append("Fully managed - no time spent on database operations")
    
    elif constraints["time_to_market"] == "flexible":
        if option_name == "PostgreSQL (RDS)":
            evaluation["strengths"].append("Time to design proper schema and indexes pays off long-term")
    
    # ==========================
    # DATA COMPLEXITY EVALUATION
    # ==========================
    
    if constraints["data_complexity"] == "simple":
        if option_name == "DynamoDB":
            evaluation["strengths"].append("Perfect for simple key-value and single-table design")
        elif option_name == "PostgreSQL (RDS)":
            evaluation["avoid_when"].append("Your data model is just key-value - simpler databases cost less")
    
    elif constraints["data_complexity"] == "moderate":
        if option_name == "MongoDB Atlas":
            evaluation["strengths"].append("Document model handles moderate complexity without rigid schemas")
        elif option_name == "PostgreSQL (RDS)":
            evaluation["strengths"].append("Relational model enforces data integrity for moderate complexity")
    
    elif constraints["data_complexity"] == "complex":
        if option_name == "PostgreSQL (RDS)":
            evaluation["strengths"].append("JOINs, constraints, and transactions handle complex relationships well")
        elif option_name == "DynamoDB":
            evaluation["limitations"].append("Complex queries require multiple round-trips or denormalization")
            evaluation["avoid_when"].append("You need complex JOINs or ad-hoc queries across multiple entities")
        elif option_name == "MongoDB Atlas":
            evaluation["limitations"].append("Lack of JOINs requires embedding or multiple queries for complex data")
    
    # ==========================
    # CONSISTENCY EVALUATION
    # ==========================
    
    if constraints["consistency"] == "strong":
        if option_data["consistency"] == "strong":
            evaluation["strengths"].append("Strong consistency guarantees - no stale reads")
        elif option_data["consistency"] == "eventual_or_strong":
            evaluation["limitations"].append("Requires explicit strong consistency mode - comes with latency trade-off")
        else:
            evaluation["limitations"].append("Eventual consistency may cause race conditions in critical operations")
    
    elif constraints["consistency"] == "eventual":
        if option_name == "DynamoDB":
            evaluation["strengths"].append("Eventual consistency mode offers lower latency and higher throughput")
    
    # ==========================
    # GENERAL STRENGTHS & RISKS
    # ==========================
    
    # PostgreSQL specific
    if option_name == "PostgreSQL (RDS)":
        evaluation["strengths"].append("ACID compliance and mature ecosystem with extensive tooling")
        evaluation["hidden_costs"].append("Schema migrations on large tables can cause downtime")
        evaluation["hidden_costs"].append("Connection pooling (RDS Proxy) costs extra but often needed")
    
    # DynamoDB specific
    if option_name == "DynamoDB":
        evaluation["strengths"].append("Zero operational overhead - AWS handles everything")
        evaluation["hidden_costs"].append("Global Secondary Indexes (GSIs) double storage and write costs")
        evaluation["limitations"].append("Data modeling requires upfront planning - hard to change access patterns")
    
    # MongoDB specific
    if option_name == "MongoDB Atlas":
        evaluation["strengths"].append("Schema flexibility enables rapid iteration during development")
        evaluation["hidden_costs"].append("Unplanned queries without proper indexes can crush performance")
        evaluation["limitations"].append("Transactions across shards have performance overhead")
    
    # Redis specific
    if option_name == "Redis (ElastiCache)":
        evaluation["strengths"].append("Ideal for session storage, rate limiting, and leaderboards")
        evaluation["limitations"].append("Data loss risk without proper persistence configuration")
        evaluation["avoid_when"].append("You need it as your primary database - Redis is best as a complement")
    
    return evaluation
