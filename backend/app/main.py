from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.monday.client import MondayClient
from app.data.normalizer import normalize_deal, normalize_work_order
from app.data.service import DataService
from app.analytics.service import (
    build_deal_summary,
    build_work_order_summary,
)
from app.config import (
    WORK_ORDERS_BOARD_ID,
    DEALS_BOARD_ID,
)
from app.agent.tools import (
    query_deals,
    query_work_orders,
    get_business_overview,
)
from pydantic import BaseModel

from app.agent.service import AgentService
BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="Skylark BI Agent",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)


@app.get("/")
async def frontend():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )

monday = MondayClient()
data_service = DataService(monday)

class ChatRequest(BaseModel):
    message: str

@app.get("/api/health")
async def health():

    return {
        "status": "ok",
        "service": "skylark-bi-agent",
    }


@app.get("/api/monday/columns/{board_id}")
async def get_columns(board_id: int):

    return await monday.get_board_columns(board_id)


@app.get("/api/monday/deals")
async def get_deals():

    items = await monday.get_all_items(
        DEALS_BOARD_ID
    )

    return {
        "count": len(items),
        "items": items,
    }


@app.get("/api/monday/work-orders")
async def get_work_orders():

    items = await monday.get_all_items(
        WORK_ORDERS_BOARD_ID
    )

    return {
        "count": len(items),
        "items": items,
    }

@app.get("/api/monday/deals/count")
async def deals_count():

    items = await monday.get_all_items(
        DEALS_BOARD_ID
    )

    return {
        "count": len(items)
    }

@app.get("/api/monday/work-orders/count")
async def work_orders_count():

    items = await monday.get_all_items(
        WORK_ORDERS_BOARD_ID
    )

    return {
        "count": len(items)
    }

@app.get("/api/monday/deals/sample")
async def get_deal_sample():

    items = await monday.get_all_items(
        DEALS_BOARD_ID
    )

    return items[0] if items else {}

@app.get("/api/monday/work-orders/sample")
async def get_work_order_sample():

    items = await monday.get_all_items(
        WORK_ORDERS_BOARD_ID
    )

    return items[0] if items else {}

@app.get("/api/monday/deals/normalized-sample")
async def normalized_deal_sample():

    items = await monday.get_all_items(
        DEALS_BOARD_ID
    )

    if not items:
        return {}

    return normalize_deal(items[0])

@app.get("/api/monday/work-orders/normalized-sample")
async def normalized_work_order_sample():

    items = await monday.get_all_items(
        WORK_ORDERS_BOARD_ID
    )

    if not items:
        return {}

    return normalize_work_order(items[0])

@app.get("/api/data/summary")
async def data_summary():

    deals = await data_service.get_deals()
    work_orders = await data_service.get_work_orders()

    return {
        "deals": {
            "count": len(deals),
            "sample": deals[:3],
        },
        "work_orders": {
            "count": len(work_orders),
            "sample": work_orders[:3],
        },
    }

@app.get("/api/analytics/summary")
async def analytics_summary():

    deals = await data_service.get_deals()
    work_orders = await data_service.get_work_orders()

    return {
        "deals": build_deal_summary(
            deals
        ),
        "work_orders": build_work_order_summary(
            work_orders
        ),
    }

@app.get("/api/agent/test")
async def agent_test():

    deals = await data_service.get_deals()
    work_orders = await data_service.get_work_orders()

    return {
        "overview": get_business_overview(
            deals,
            work_orders,
        ),
        "mining_deals": query_deals(
            deals,
            sector="Mining",
            deal_status="Open",
        ),
        "mining_work_orders": query_work_orders(
            work_orders,
            sector="Mining",
        ),
    }

@app.post("/api/agent/chat")
async def agent_chat(request: ChatRequest):

    deals = await data_service.get_deals()
    work_orders = await data_service.get_work_orders()

    agent = AgentService(
        deals=deals,
        work_orders=work_orders,
    )

    return await agent.chat(
        request.message
    )