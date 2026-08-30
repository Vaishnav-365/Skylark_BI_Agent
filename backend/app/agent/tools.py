from app.analytics.deals import (
    filter_deals,
    total_pipeline_value,
)

from app.analytics.work_orders import (
    filter_work_orders,
    total_billed_value,
    total_collected_amount,
    total_receivables,
)
from app.agent.formatting import format_inr


def query_deals(
    deals: list[dict],
    sector: str | None = None,
    owner_code: str | None = None,
    deal_status: str | None = None,
) -> dict:

    filtered = filter_deals(
        deals,
        sector=sector,
        owner_code=owner_code,
        deal_status=deal_status,
    )

    pipeline_value = total_pipeline_value(filtered)

    open_count = sum(
        1
        for deal in filtered
        if (deal.get("deal_status") or "").lower() == "open"
    )

    return {
        "count": len(filtered),
        "open_deals_count": open_count,
        "pipeline_value": pipeline_value,
        "pipeline_value_inr": format_inr(pipeline_value),
        "filters": {
            "sector": sector,
            "owner_code": owner_code,
            "deal_status": deal_status,
        },
    }

def query_work_orders(
    work_orders: list[dict],
    sector: str | None = None,
    execution_status: str | None = None,
) -> dict:

    filtered = filter_work_orders(
        work_orders,
        sector=sector,
        execution_status=execution_status,
    )

    billed_value = total_billed_value(filtered)
    collected_amount = total_collected_amount(filtered)
    receivables = total_receivables(filtered)

    return {
        "count": len(filtered),
        "billed_value": billed_value,
        "billed_value_inr": format_inr(billed_value),
        "collected_amount": collected_amount,
        "collected_amount_inr": format_inr(collected_amount),
        "receivables": receivables,
        "receivables_inr": format_inr(receivables),
        "filters": {
            "sector": sector,
            "execution_status": execution_status,
        },
    }

def get_business_overview(
    deals: list[dict],
    work_orders: list[dict],
) -> dict:

    open_deals = sum(
        1
        for deal in deals
        if (deal.get("deal_status") or "").lower()
        == "open"
    )

    pipeline_value = total_pipeline_value(deals)
    billed_value = total_billed_value(work_orders)
    collected_amount = total_collected_amount(work_orders)
    receivables = total_receivables(work_orders)

    return {
        "deals": {
            "total": len(deals),
            "open": open_deals,
            "pipeline_value": pipeline_value,
            "pipeline_value_inr": format_inr(
                pipeline_value
            ),
        },
        "work_orders": {
            "total": len(work_orders),
            "billed_value": billed_value,
            "billed_value_inr": format_inr(
                billed_value
            ),
            "collected_amount": collected_amount,
            "collected_amount_inr": format_inr(
                collected_amount
            ),
            "receivables": receivables,
            "receivables_inr": format_inr(
                receivables
            ),
        },
    }