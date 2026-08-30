from collections import Counter


def count_missing(
    records: list[dict],
    field: str,
) -> int:

    return sum(
        1
        for record in records
        if record.get(field) in (None, "")
    )


def value_distribution(
    records: list[dict],
    field: str,
) -> dict:

    counter = Counter(
        record.get(field)
        for record in records
        if record.get(field) not in (None, "")
    )

    return dict(counter)


def build_deal_data_quality(deals: list[dict]) -> dict:

    return {
        "total_records": len(deals),

        "missing_deal_status": count_missing(
            deals,
            "deal_status",
        ),

        "missing_deal_value": count_missing(
            deals,
            "deal_value",
        ),

        "missing_sector": count_missing(
            deals,
            "sector",
        ),

        "missing_owner": count_missing(
            deals,
            "owner_code",
        ),

        "missing_deal_stage": count_missing(
            deals,
            "deal_stage",
        ),
    }


def build_work_order_data_quality(
    work_orders: list[dict],
) -> dict:

    return {
        "total_records": len(work_orders),

        "missing_execution_status": count_missing(
            work_orders,
            "execution_status",
        ),

        "missing_sector": count_missing(
            work_orders,
            "sector",
        ),

        "missing_billing_status": count_missing(
            work_orders,
            "billing_status",
        ),

        "missing_amount_receivable": count_missing(
            work_orders,
            "amount_receivable",
        ),

        "missing_collection_status": count_missing(
            work_orders,
            "collection_status",
        ),
    }