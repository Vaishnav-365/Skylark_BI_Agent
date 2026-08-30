import os
import httpx
from dotenv import load_dotenv

load_dotenv()

MONDAY_API_URL = "https://api.monday.com/v2"
MONDAY_API_TOKEN = os.getenv("MONDAY_API_TOKEN")


class MondayClient:

    def __init__(self):
        if not MONDAY_API_TOKEN:
            raise RuntimeError("MONDAY_API_TOKEN is not configured")

        self.url = MONDAY_API_URL
        self.headers = {
            "Authorization": MONDAY_API_TOKEN,
            "Content-Type": "application/json",
        }

    async def query(self, query: str, variables: dict | None = None):

        payload = {
            "query": query,
            "variables": variables or {},
        }

        async with httpx.AsyncClient(timeout=30.0) as client:

            response = await client.post(
                self.url,
                json=payload,
                headers=self.headers,
            )

        response.raise_for_status()

        data = response.json()

        if "errors" in data:
            raise RuntimeError(data["errors"])

        return data["data"]

    async def get_board_columns(self, board_id: int):

        query = """
        query ($board_id: ID!) {
            boards(ids: [$board_id]) {
                id
                name
                columns {
                    id
                    title
                    type
                }
            }
        }
        """

        data = await self.query(
            query,
            {"board_id": str(board_id)}
        )

        if not data["boards"]:
            raise ValueError(f"Board {board_id} not found")

        return data["boards"][0]

    async def get_all_items(self, board_id: int):

        first_query = """
        query ($board_id: ID!, $limit: Int!) {
            boards(ids: [$board_id]) {
                id
                name

                items_page(limit: $limit) {
                    cursor

                    items {
                        id
                        name

                        column_values {
                            id
                            text
                        }
                    }
                }
            }
        }
        """

        data = await self.query(
            first_query,
            {
                "board_id": str(board_id),
                "limit": 50,
            }
        )

        board = data["boards"][0]
        items_page = board["items_page"]

        items = items_page["items"]
        cursor = items_page.get("cursor")
        print(f"First page: {len(items)} items")

        # Safety mechanism to prevent an infinite loop
        seen_cursors = set()

        while cursor:

            if cursor in seen_cursors:
                raise RuntimeError(
                    "Pagination cursor repeated. "
                    "Stopping to prevent infinite loop."
                )

            seen_cursors.add(cursor)

            next_query = """
            query ($cursor: String!) {

                next_items_page(cursor: $cursor) {

                    cursor

                    items {
                        id
                        name

                        column_values {
                            id
                            text
                        }
                    }
                }
            }
            """

            data = await self.query(
                next_query,
                {
                    "cursor": cursor
                }
            )

            page = data["next_items_page"]

            new_items = page["items"]

            print(
                    f"Next page: {len(new_items)} items | "
                    f"Total: {len(items) + len(new_items)}"
                )

            items.extend(new_items)

            new_cursor = page.get("cursor")

            # Stop if monday gives us the same cursor
            if new_cursor == cursor:
                break

            cursor = new_cursor

        return items