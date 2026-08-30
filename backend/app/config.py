import os

from dotenv import load_dotenv


load_dotenv()


WORK_ORDERS_BOARD_ID = int(
    os.getenv("WORK_ORDERS_BOARD_ID")
)

DEALS_BOARD_ID = int(
    os.getenv("DEALS_BOARD_ID")
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b",
)