DEAL_TOOL = {
    "type": "function",
    "function": {
        "name": "query_deals",
        "description": (
            "Query sales deals using optional sector, owner, "
            "and deal status filters. Returns the number of "
            "matching deals, number of matching open deals, "
            "and total pipeline value from open deals."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "sector": {
                    "type": "string",
                    "description": (
                        "Sector to filter by, such as Mining, "
                        "Energy, or Infrastructure."
                    ),
                },
                "owner_code": {
                    "type": "string",
                    "description": (
                        "Sales owner code to filter by."
                    ),
                },
                "deal_status": {
                    "type": "string",
                    "description": (
                        "Deal status such as Open or Closed."
                    ),
                },
            },
            "required": [],
            "additionalProperties": False,
        },
    },
}

WORK_ORDER_TOOL = {
    "type": "function",
    "function": {
        "name": "query_work_orders",
        "description": (
            "Query work orders using optional sector and "
            "execution status filters. Returns the number "
            "of matching work orders, total billed value, "
            "total collected amount, and total receivables."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "sector": {
                    "type": "string",
                    "description": "Sector to filter by.",
                },
                "execution_status": {
                    "type": "string",
                    "description": (
                        "Execution status such as Active, "
                        "Completed, or Delayed."
                    ),
                },
            },
            "required": [],
            "additionalProperties": False,
        },
    },
}

OVERVIEW_TOOL = {
    "type": "function",
    "function": {
        "name": "get_business_overview",
        "description": (
            "Return high-level business metrics across "
            "the entire deals and work-order datasets."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    },
}


AGENT_TOOLS = [
    DEAL_TOOL,
    WORK_ORDER_TOOL,
    OVERVIEW_TOOL,
]