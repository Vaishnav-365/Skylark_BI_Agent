from app.analytics.deals import (
    total_deals,
    open_deals,
    total_pipeline_value,
    deals_by_sector,
    deals_by_owner,
    deals_by_stage,
)

from app.analytics.work_orders import (
    total_work_orders,
    work_orders_by_execution_status,
    work_orders_by_sector,
    total_billed_value,
    total_collected_amount,
    total_receivables,
    work_orders_by_billing_status,
)

from app.analytics.data_quality import (
    build_deal_data_quality,
    build_work_order_data_quality,
)

def build_deal_summary(deals: list[dict]) -> dict:
    return {
        "total_deals": total_deals(deals),
        "open_deals": open_deals(deals),
        "total_pipeline_value": total_pipeline_value(deals),
        "deals_by_sector": deals_by_sector(deals),
        "deals_by_owner": deals_by_owner(deals),
        "deals_by_stage": deals_by_stage(deals),
        "data_quality": build_deal_data_quality(deals),
    }


def build_work_order_summary(
    work_orders: list[dict],
) -> dict:

    return {
        "total_work_orders": total_work_orders(work_orders),
        "execution_status": work_orders_by_execution_status(
            work_orders
        ),
        "work_orders_by_sector": work_orders_by_sector(
            work_orders
        ),
        "total_billed_value": total_billed_value(
            work_orders
        ),
        "total_collected_amount": total_collected_amount(
            work_orders
        ),
        "total_receivables": total_receivables(
            work_orders
        ),
        "billing_status": work_orders_by_billing_status(
            work_orders
        ),
        "data_quality": build_work_order_data_quality(
            work_orders
        ),
    }