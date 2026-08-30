# Skylark Drones — Monday.com Business Intelligence Agent

An AI-powered business intelligence assistant that connects to Monday.com data and answers founder-level questions about sales deals, pipeline, work orders, collections, receivables, sectors, and business performance.

The system combines deterministic analytics with an LLM-based conversational agent to provide accurate, contextual business answers while minimizing unsupported calculations or assumptions.

---

## 1. Features

### Monday.com Integration

* Reads data dynamically from two Monday.com boards:

  * Deals
  * Work Orders
* Uses the Monday.com API to retrieve board data.
* Supports paginated data retrieval.
* Does not hardcode the provided CSV/XLSX business data.

### Data Resilience

* Handles missing and null values during normalization.
* Normalizes business fields before analytics.
* Handles inconsistent text values and formats.
* Provides data-quality information where relevant.

### Query Understanding

The AI agent can understand questions such as:

* "What is our total pipeline?"
* "How much open pipeline do we have in Mining?"
* "How much have we collected from Mining work orders?"
* "Compare Mining pipeline with collections."
* "Prepare a leadership update."

The agent can also request clarification when a question is materially ambiguous.

### Business Intelligence

The system supports analysis of:

* Total and open deals
* Pipeline value
* Deal sectors
* Deal owners
* Deal stages
* Work-order counts
* Billed value
* Collected amount
* Outstanding receivables
* Execution status
* Sector-specific performance
* Leadership/business summaries

### Conversational Interface

A lightweight web interface allows users to interact with the BI agent conversationally.

The frontend provides:

* Chat interface
* Suggested business questions
* Markdown rendering
* Tables in assistant responses
* Loading state
* Connection status
* Responsive layout

---

## 2. Architecture

```text
                         ┌──────────────────────┐
                         │      Frontend        │
                         │  HTML / CSS / JS     │
                         └──────────┬───────────┘
                                    │
                                    │ HTTP POST
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │   /api/agent/chat    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     AgentService     │
                         │  Groq LLM + Tools    │
                         └──────────┬───────────┘
                                    │
                         ┌──────────┴───────────┐
                         │                      │
                         ▼                      ▼
                ┌─────────────────┐   ┌──────────────────┐
                │   Deal Tools    │   │ Work Order Tools │
                └────────┬────────┘   └────────┬─────────┘
                         │                     │
                         └──────────┬──────────┘
                                    ▼
                         ┌──────────────────────┐
                         │   Analytics Layer    │
                         │ Deterministic Python │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Data Service      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Monday.com       │
                         │   Deals + WorkOrders │
                         └──────────────────────┘
```

### Design Principle

The LLM is responsible primarily for:

1. Understanding the user's question.
2. Selecting the appropriate business intelligence tools.
3. Interpreting the returned results.
4. Presenting the answer clearly.

Business calculations are kept in deterministic Python analytics functions wherever possible.

This reduces the risk of the LLM inventing or incorrectly calculating financial metrics.

---

## 3. Project Structure

```text
skylark-bi-agent/
│
├── README.md
├── Decision_Log.md
├── .gitignore
│
├── backend/
│   ├── requirements.txt
│   ├── .env
│   │
│   └── app/
│       ├── agent/
│       │   ├── service.py
│       │   ├── tools.py
│       │   └── schemas.py
│       │
│       ├── analytics/
│       │   ├── deals.py
│       │   ├── work_orders.py
│       │   └── service.py
│       │
│       ├── data/
│       │   ├── normalizer.py
│       │   └── service.py
│       │
│       ├── monday/
│       │   └── client.py
│       │
│       ├── config.py
│       └── main.py
│
└── frontend/
    ├── index.html
    ├── style.css
    └── app.js
```

---

## 4. Technology Stack

### Backend

* Python
* FastAPI
* Uvicorn
* HTTPX
* Pandas
* python-dotenv

### AI / Agent

* Groq API
* OpenAI-compatible chat completion interface
* Tool/function calling

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript
* Marked.js for Markdown rendering

### Data Source

* Monday.com API

---

## 5. Monday.com Setup

The assignment provides two datasets:

1. Work Orders
2. Deals

These datasets should be imported into Monday.com as separate boards.

The backend expects the corresponding board IDs to be provided through environment variables.

Example:

```env
WORK_ORDERS_BOARD_ID=your_work_orders_board_id
DEALS_BOARD_ID=your_deals_board_id
```

The application retrieves the board data dynamically through the Monday.com API.

No business data is hardcoded into the application.

---

## 6. Environment Configuration

Create a `.env` file inside the `backend` directory.

Example:

```env
WORK_ORDERS_BOARD_ID=123456789
DEALS_BOARD_ID=987654321

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Replace the placeholder values with the appropriate credentials and Monday.com board IDs.

### Security

The `.env` file contains secrets and should **never be committed to Git**.

The repository should only contain configuration examples/placeholders.

---

## 7. Installation

### Clone the repository

```bash
git clone <repository-url>
cd skylark-bi-agent
```

### Create a virtual environment

From the `backend` directory:

```bash
cd backend

python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 8. Running the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/api/health
```

---

## 9. Running the Frontend

The frontend is a lightweight static application.

From the `frontend` directory:

```bash
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

The frontend sends conversational requests to:

```text
http://127.0.0.1:8000/api/agent/chat
```

For a deployed environment, update the API URL in:

```text
frontend/app.js
```

to point to the deployed backend.

---

## 10. API Endpoints

### Health

```text
GET /api/health
```

Checks whether the backend is running.

### Monday.com Data

```text
GET /api/monday/deals
GET /api/monday/work-orders
```

Retrieves the available deal and work-order records.

### Data Counts

```text
GET /api/monday/deals/count
GET /api/monday/work-orders/count
```

Returns record counts.

### Analytics

```text
GET /api/analytics/summary
```

Returns deterministic analytics for the deals and work-order datasets.

### Agent

```text
POST /api/agent/chat
```

Accepts a business question and returns the AI-generated response.

Example request:

```json
{
  "message": "How much open pipeline do we have in Mining?"
}
```

---

## 11. Example Queries

The agent was tested using questions covering different business intelligence scenarios.

### Test 1 — Total Pipeline

```text
What is our total pipeline?
```

### Test 2 — Sector Pipeline

```text
How much open pipeline do we have in Mining?
```

### Test 3 — Collections

```text
How much have we collected from Mining work orders?
```

### Test 4 — Cross-Dataset Comparison

```text
Compare the Mining pipeline with the amount collected from Mining work orders.
```

### Test 5 — Leadership Update

```text
Prepare a concise leadership update covering pipeline, work orders, collections, and key business observations.
```

Additional tests cover business-wide snapshots, sectors with no records, and comparisons across the Deals and Work Orders datasets.

---

## 12. Leadership Updates

The optional leadership-update requirement was interpreted as a conversational capability rather than a separate dashboard.

When asked for a leadership update, the agent gathers relevant business metrics and presents them in a concise executive-oriented format.

The response can include:

* Pipeline
* Work-order activity
* Billed value
* Collections
* Receivables
* Supported observations
* Relevant data-quality caveats

The agent is instructed not to invent unsupported trends, causes, or recommendations.

---

## 13. Data Quality Handling

The underlying business data contains real-world inconsistencies.

The application therefore separates:

```text
Raw Monday.com Data
        ↓
Normalization
        ↓
Analytics
        ↓
Agent Tools
        ↓
Natural-Language Response
```

Normalization and analytics are performed before the information is passed to the conversational layer.

Missing or incomplete values are handled without causing the entire query to fail.

Where data limitations materially affect an answer, the agent is instructed to communicate the limitation rather than make assumptions.

---

## 14. Error Handling

The backend includes handling for:

* Missing API credentials
* Monday.com/API failures
* Invalid agent tool requests
* Empty datasets
* Missing values
* Incomplete records
* Failed frontend/backend communication

The frontend also displays a user-friendly error message when the backend cannot be reached.

---

## 15. Deployment

The backend has been deployed as a hosted FastAPI service so that the application can be tested without requiring local backend setup.

The frontend can be hosted as a static site and configured to communicate with the deployed backend API.

### Deployed Backend

```text
https://skylark-bi-agent-9jvn.onrender.com/
```

The hosted API can be used for testing the agent without running the backend locally.

---

## 16. Key Design Decisions

The major architectural decisions and trade-offs are documented separately in:

```text
Decision_Log.md
```

Key decisions include:

* Using Monday.com API for dynamic data retrieval.
* Keeping analytics calculations deterministic.
* Using an LLM for natural-language understanding and tool selection.
* Separating Deals and Work Orders as distinct datasets.
* Handling data normalization before analytics.
* Implementing leadership updates as an agent capability instead of a separate dashboard.

---

## 17. Limitations

The current prototype has some limitations:

* Historical trend analysis is limited by the data available in the provided datasets.
* The system is primarily focused on the provided Deals and Work Orders boards.
* Authentication for end users is not implemented because it was not required for the prototype.
* The frontend is intentionally lightweight and does not use a large frontend framework.
* Business conclusions are constrained by the quality and coverage of the source data.

---

## 18. Future Improvements

With additional development time, the system could be extended with:

* Historical trend analysis
* More advanced sector and owner comparisons
* Automated anomaly detection
* Interactive charts
* Scheduled leadership reports
* Exportable executive summaries
* Role-based access control
* More sophisticated data-quality reporting
* Additional Monday.com boards and business data sources

---

## 19. Assignment Deliverables

| Requirement              | Implementation                  |
| ------------------------ | ------------------------------- |
| Monday.com integration   | Monday.com API                  |
| Dynamic data retrieval   | Implemented                     |
| Data normalization       | Implemented                     |
| Missing-data handling    | Implemented                     |
| Query understanding      | Groq-powered agent              |
| Business intelligence    | Deterministic analytics + agent |
| Cross-board queries      | Deals + Work Orders tools       |
| Conversational interface | HTML/CSS/JavaScript frontend    |
| Error handling           | Implemented                     |
| Leadership updates       | Implemented                     |
| Hosted prototype         | Deployed backend                |
| Decision Log             | `Decision_Log.md`               |
| Source code              | Repository / ZIP                |

---

## 20. Author

**Vaishnav P Nair**

Computer Science Undergraduate
Amrita Vishwa Vidyapeetham
