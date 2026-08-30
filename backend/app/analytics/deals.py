from collections import Counter


def total_deals(deals: list[dict]) -> int:
    return len(deals)


def open_deals(deals: list[dict]) -> int:
    return sum(
        1
        for deal in deals
        if (deal.get("deal_status") or "").lower() == "open"
    )


def total_pipeline_value(deals: list[dict]) -> float:
    return sum(
        deal.get("deal_value") or 0
        for deal in deals
        if (deal.get("deal_status") or "").lower() == "open"
    )


def deals_by_sector(deals: list[dict]) -> dict:
    counter = Counter(
        deal.get("sector")
        for deal in deals
        if deal.get("sector")
    )

    return dict(counter)


def deals_by_owner(deals: list[dict]) -> dict:
    counter = Counter(
        deal.get("owner_code")
        for deal in deals
        if deal.get("owner_code")
    )

    return dict(counter)


def deals_by_stage(deals: list[dict]) -> dict:
    counter = Counter(
        deal.get("deal_stage")
        for deal in deals
        if deal.get("deal_stage")
    )

    return dict(counter)


def filter_deals(
    deals: list[dict],
    sector: str | None = None,
    owner_code: str | None = None,
    deal_status: str | None = None,
) -> list[dict]:

    result = deals

    if sector:
        result = [
            deal for deal in result
            if (deal.get("sector") or "").lower() == sector.lower()
        ]

    if owner_code:
        result = [
            deal for deal in result
            if (deal.get("owner_code") or "").lower()
            == owner_code.lower()
        ]

    if deal_status:
        result = [
            deal for deal in result
            if (deal.get("deal_status") or "").lower()
            == deal_status.lower()
        ]

    return result