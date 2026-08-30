from datetime import datetime
from typing import Optional

DEAL_COLUMN_MAP = {
    "text_mm6qt3ee": "owner_code",
    "text_mm6qr65d": "client_code",
    "text_mm6q37xm": "deal_status",
    "text_mm6qb4s0": "close_date",
    "text_mm6qkmjn": "closure_probability",
    "text_mm6qc5z3": "deal_value",
    "text_mm6q3fav": "tentative_close_date",
    "text_mm6qwzrt": "deal_stage",
    "text_mm6qn1qt": "product_deal",
    "text_mm6qdyfh": "sector",
    "text_mm6qcw33": "created_date",
}

WORK_ORDER_COLUMN_MAP = {
    "text_mm6qcv2e": "customer_name_code",
    "text_mm6qqgfs": "serial_number",
    "text_mm6qa88m": "nature_of_work",
    "text_mm6qt9mx": "last_executed_month",
    "text_mm6q7d9x": "execution_status",
    "text_mm6q5rra": "data_delivery_date",
    "text_mm6qbr8r": "po_loi_date",
    "text_mm6qjjn0": "document_type",
    "text_mm6qzvx3": "probable_start_date",
    "text_mm6q115n": "probable_end_date",
    "text_mm6qzdnv": "bd_kam_personnel_code",
    "text_mm6qr7t5": "sector",
    "text_mm6q6m33": "type_of_work",
    "text_mm6q3e1y": "software_platform",
    "text_mm6qarym": "last_invoice_date",
    "text_mm6q3m67": "latest_invoice_number",
    "text_mm6q34c6": "amount_excl_gst",
    "text_mm6qrsa6": "amount_incl_gst",
    "text_mm6qzh3d": "billed_value_excl_gst",
    "text_mm6qrkae": "billed_value_incl_gst",
    "text_mm6qms20": "collected_amount",
    "text_mm6q7gkm": "amount_to_be_billed_excl_gst",
    "text_mm6qq48p": "amount_to_be_billed_incl_gst",
    "text_mm6qdkjk": "amount_receivable",
    "text_mm6q616p": "ar_priority_account",
    "text_mm6qyn5x": "quantity_by_ops",
    "text_mm6qh446": "quantity_as_per_po",
    "text_mm6qd5rd": "quantity_billed",
    "text_mm6q10w5": "balance_quantity",
    "text_mm6qfdgy": "invoice_status",
    "text_mm6qp4k0": "expected_billing_month",
    "text_mm6qsxpr": "actual_billing_month",
    "text_mm6qch5n": "actual_collection_month",
    "text_mm6qp8n2": "wo_status_billed",
    "text_mm6qdbqa": "collection_status",
    "text_mm6qtaky": "collection_date",
    "text_mm6qn0pf": "billing_status",
}

def clean_text(value) -> Optional[str]:
    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    if value.upper() in {"N/A", "NA", "NULL", "NONE"}:
        return None

    return value


def parse_number(value) -> Optional[float]:
    value = clean_text(value)

    if value is None:
        return None

    # Remove common formatting
    value = (
        value
        .replace(",", "")
        .replace("₹", "")
        .strip()
    )

    try:
        return float(value)
    except ValueError:
        return None


def parse_date(value) -> Optional[str]:
    value = clean_text(value)

    if value is None:
        return None

    # monday's imported text format:
    # Thu Feb 26 2026 00:00:00 GMT+0000
    try:
        parsed = datetime.strptime(
            value[:24],
            "%a %b %d %Y %H:%M:%S"
        )

        return parsed.strftime("%Y-%m-%d")

    except ValueError:
        return None

def normalize_deal(item: dict) -> dict:
    """
    Convert one raw monday.com Deal item into our
    normalized internal representation.
    """

    result = {
        "id": item.get("id"),
        "deal_name": clean_text(item.get("name")),
        "owner_code": None,
        "client_code": None,
        "deal_status": None,
        "close_date": None,
        "closure_probability": None,
        "deal_value": None,
        "tentative_close_date": None,
        "deal_stage": None,
        "product_deal": None,
        "sector": None,
        "created_date": None,
    }

    for column in item.get("column_values", []):
        column_id = column.get("id")
        field_name = DEAL_COLUMN_MAP.get(column_id)

        if not field_name:
            continue

        value = column.get("text")

        if field_name == "deal_value":
            result[field_name] = parse_number(value)

        elif field_name in {
            "close_date",
            "tentative_close_date",
            "created_date",
        }:
            result[field_name] = parse_date(value)

        else:
            result[field_name] = clean_text(value)

    return result

def normalize_work_order(item: dict) -> dict:
    """
    Convert one raw monday.com Work Order item into our
    normalized internal representation.
    """

    result = {
        "id": item.get("id"),
        "work_order_name": clean_text(item.get("name")),

        "customer_name_code": None,
        "serial_number": None,
        "nature_of_work": None,
        "last_executed_month": None,
        "execution_status": None,
        "data_delivery_date": None,
        "po_loi_date": None,
        "document_type": None,
        "probable_start_date": None,
        "probable_end_date": None,
        "bd_kam_personnel_code": None,
        "sector": None,
        "type_of_work": None,
        "software_platform": None,
        "last_invoice_date": None,
        "latest_invoice_number": None,

        "amount_excl_gst": None,
        "amount_incl_gst": None,
        "billed_value_excl_gst": None,
        "billed_value_incl_gst": None,
        "collected_amount": None,
        "amount_to_be_billed_excl_gst": None,
        "amount_to_be_billed_incl_gst": None,
        "amount_receivable": None,

        "ar_priority_account": None,

        "quantity_by_ops": None,
        "quantity_as_per_po": None,
        "quantity_billed": None,
        "balance_quantity": None,

        "invoice_status": None,
        "expected_billing_month": None,
        "actual_billing_month": None,
        "actual_collection_month": None,
        "wo_status_billed": None,
        "collection_status": None,
        "collection_date": None,
        "billing_status": None,
    }

    numeric_fields = {
        "amount_excl_gst",
        "amount_incl_gst",
        "billed_value_excl_gst",
        "billed_value_incl_gst",
        "collected_amount",
        "amount_to_be_billed_excl_gst",
        "amount_to_be_billed_incl_gst",
        "amount_receivable",
        "quantity_by_ops",
        "quantity_billed",
        "balance_quantity",
    }

    date_fields = {
        "data_delivery_date",
        "po_loi_date",
        "probable_start_date",
        "probable_end_date",
        "last_invoice_date",
        "collection_date",
    }

    for column in item.get("column_values", []):

        column_id = column.get("id")
        field_name = WORK_ORDER_COLUMN_MAP.get(column_id)

        if not field_name:
            continue

        value = column.get("text")

        if field_name in numeric_fields:
            result[field_name] = parse_number(value)

        elif field_name in date_fields:
            result[field_name] = parse_date(value)

        else:
            result[field_name] = clean_text(value)

    return result

def normalize_deals(items: list[dict]) -> list[dict]:
    return [
        normalize_deal(item)
        for item in items
    ]


def normalize_work_orders(items: list[dict]) -> list[dict]:
    return [
        normalize_work_order(item)
        for item in items
    ]