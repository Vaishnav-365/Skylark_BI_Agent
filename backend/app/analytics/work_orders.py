from collections import Counter


def total_work_orders(work_orders: list[dict]) -> int:
    return len(work_orders)


def work_orders_by_execution_status(
    work_orders: list[dict],
) -> dict:

    counter = Counter(
        wo.get("execution_status")
        for wo in work_orders
        if wo.get("execution_status")
    )

    return dict(counter)


def work_orders_by_sector(
    work_orders: list[dict],
) -> dict:

    counter = Counter(
        wo.get("sector")
        for wo in work_orders
        if wo.get("sector")
    )

    return dict(counter)


def total_billed_value(
    work_orders: list[dict],
) -> float:

    return sum(
        wo.get("billed_value_incl_gst") or 0
        for wo in work_orders
    )


def total_collected_amount(
    work_orders: list[dict],
) -> float:

    return sum(
        wo.get("collected_amount") or 0
        for wo in work_orders
    )


def total_receivables(
    work_orders: list[dict],
) -> float:

    return sum(
        wo.get("amount_receivable") or 0
        for wo in work_orders
    )


def work_orders_by_billing_status(
    work_orders: list[dict],
) -> dict:

    counter = Counter(
        wo.get("billing_status")
        for wo in work_orders
        if wo.get("billing_status")
    )

    return dict(counter)


def filter_work_orders(
    work_orders: list[dict],
    sector: str | None = None,
    execution_status: str | None = None,
) -> list[dict]:

    result = work_orders

    if sector:
        result = [
            wo for wo in result
            if (wo.get("sector") or "").lower()
            == sector.lower()
        ]

    if execution_status:
        result = [
            wo for wo in result
            if wo.get("execution_status", "").lower()
            == execution_status.lower()
        ]

    return result