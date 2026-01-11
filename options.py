def get_database_options():
    """
    Defines all available database options with their characteristics.
    Each option is treated as valid - no strawmen.
    """
    
    options = {
        "PostgreSQL (RDS)": {
            "description": "Managed relational database with ACID guarantees",
            "type": "relational",
            "managed": True,
            "base_complexity": "intermediate",
            "pricing_model": "instance_based",
            "scaling_model": "vertical",
            "setup_time": "medium",
            "consistency": "strong",
            "good_for": ["complex queries", "transactions", "relational data"],
            "challenges": ["scaling writes", "cost at scale", "schema migrations"]
        },
        
        "DynamoDB": {
            "description": "Serverless NoSQL database with predictable performance",
            "type": "nosql",
            "managed": True,
            "base_complexity": "beginner",
            "pricing_model": "usage_based",
            "scaling_model": "automatic",
            "setup_time": "fast",
            "consistency": "eventual_or_strong",
            "good_for": ["key-value", "high throughput", "simple queries"],
            "challenges": ["complex queries", "data modeling", "cost unpredictability"]
        },
        
        "MongoDB Atlas": {
            "description": "Flexible document database with rich query capabilities",
            "type": "document",
            "managed": True,
            "base_complexity": "beginner",
            "pricing_model": "instance_based",
            "scaling_model": "horizontal",
            "setup_time": "fast",
            "consistency": "tunable",
            "good_for": ["flexible schema", "nested data", "rapid development"],
            "challenges": ["data consistency", "query optimization", "memory usage"]
        },
        
        "Redis (ElastiCache)": {
            "description": "In-memory data store for caching and real-time applications",
            "type": "cache",
            "managed": True,
            "base_complexity": "intermediate",
            "pricing_model": "instance_based",
            "scaling_model": "vertical_and_horizontal",
            "setup_time": "medium",
            "consistency": "strong",
            "good_for": ["caching", "session store", "real-time analytics"],
            "challenges": ["data persistence", "memory costs", "not primary database"]
        }
    }
    
    return options
