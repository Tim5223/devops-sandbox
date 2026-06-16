# IT Asset Tracker — DevOps Portfolio Project

A full-stack IT Asset Management system built as a personal DevOps portfolio project. Demonstrates end-to-end cloud infrastructure, containerization, CI/CD automation, REST API development, and a React frontend — all running on Oracle Cloud.

**Live Demo:** `http://<your-oracle-ip>:8000`
**API Docs:** `http://<your-oracle-ip>:8000/docs`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Cloud | Oracle Cloud Infrastructure (ARM VM, Oracle Linux 9) |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions (test → deploy pipeline) |
| Backend | Python 3.12, FastAPI, SQLAlchemy, Alembic |
| Database | PostgreSQL 16 |
| DB Admin | pgAdmin 4 |
| Frontend | React 18, Vite, TanStack Query |
| Networking | Tailscale (mesh VPN) |
| Package Manager | uv |
| Testing | pytest, pytest-asyncio |

---

## Architecture

```
Local Machine (Windows)
    │
    ├── git push → GitHub
    │                │
    │         GitHub Actions
    │         ├── Run tests (pytest)
    │         └── Deploy to VM (SSH)
    │
    └── Tailscale VPN
            │
    Oracle Cloud ARM VM
            │
    Docker Compose
    ├── sandbox_api      (FastAPI — port 8000)
    ├── sandbox_postgres (PostgreSQL — port 5432)
    └── sandbox_pgadmin  (pgAdmin — port 5050)
```

---

## Features

- **IT Asset Tracker** — track devices, assignments, and maintenance logs
- **REST API** — full CRUD endpoints for assets, employees, departments, assignments, maintenance
- **React Dashboard** — live dashboard with stats, asset table with filters, employee list
- **Automated CI/CD** — every push to `main` triggers tests then auto-deploys to the VM
- **Database Migrations** — Alembic for schema version control
- **Seed Pipeline** — realistic dummy data populated via Python pipeline script

---

## Project Structure

```
devops-sandbox/
├── .github/workflows/
│   └── deploy.yml          # CI/CD: test → deploy on push to main
├── app/
│   ├── api/
│   │   ├── routers/
│   │   │   ├── assets.py       # Asset CRUD endpoints
│   │   │   ├── employees.py    # Employee CRUD endpoints
│   │   │   └── other.py        # Departments, assignments, maintenance
│   │   └── routes.py           # Router aggregator
│   ├── pipelines/
│   │   ├── seed.py             # Seed database with dummy data
│   │   └── example_pipeline.py # Example ETL pipeline
│   ├── scripts/
│   │   └── cli.py              # Typer CLI for automation
│   ├── config.py               # Pydantic settings (reads .env)
│   ├── database.py             # SQLAlchemy async engine + session
│   ├── models.py               # SQLAlchemy ORM models
│   ├── schemas.py              # Pydantic request/response schemas
│   └── main.py                 # FastAPI app entrypoint
├── frontend/                   # React + Vite frontend
│   └── src/
│       ├── pages/
│       │   ├── Dashboard.jsx   # Stats overview
│       │   ├── Assets.jsx      # Asset table with filters
│       │   └── Employees.jsx   # Employee list
│       ├── App.jsx             # App layout + navigation
│       └── api.js              # Axios API client
├── migrations/                 # Alembic migration files
├── tests/
│   └── test_api.py             # pytest tests (run in CI)
├── docker-compose.yml          # Multi-container Docker setup
├── Dockerfile                  # API container build
├── pyproject.toml              # Python project + dependencies (uv)
└── .env.example                # Environment variable template
```

---

## Getting Started

### Prerequisites
- Docker + Docker Compose
- Python 3.12+
- uv (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Node.js 20+ (for frontend)

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/devops-sandbox.git
cd devops-sandbox
```

### 2. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your actual values
nano .env
```

### 3. Start the stack
```bash
docker compose up -d
```

### 4. Run database migrations
```bash
uv run alembic upgrade head
```

### 5. Seed the database
```bash
docker exec sandbox_api uv run python -m app.pipelines.seed
```

### 6. Access the app
| Service | URL |
|---|---|
| Dashboard | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| pgAdmin | http://localhost:5050 |

---

## CI/CD Pipeline

Every push to `main` triggers the GitHub Actions workflow:

```
push to main
    ↓
[test job]
  - Install Python dependencies
  - Run pytest (4 tests)
  - If any test fails → pipeline stops, no deploy
    ↓
[deploy job]
  - SSH into Oracle Cloud VM
  - git reset --hard origin/main
  - docker compose down && docker compose up -d --build
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/assets/` | List all assets (filter by status) |
| POST | `/api/v1/assets/` | Create new asset |
| GET | `/api/v1/assets/{id}` | Get asset detail |
| PUT | `/api/v1/assets/{id}` | Update asset |
| DELETE | `/api/v1/assets/{id}` | Delete asset |
| GET | `/api/v1/employees/` | List all employees |
| GET | `/api/v1/employees/{id}/assets` | Get assets assigned to employee |
| POST | `/api/v1/assignments/` | Assign asset to employee |
| PUT | `/api/v1/assignments/{id}/return` | Return assigned asset |
| POST | `/api/v1/maintenance/` | Log maintenance event |
| GET | `/api/v1/departments/` | List departments |

Full interactive docs available at `/docs`.

---

## Roadmap

- [ ] Terraform — provision infrastructure as code
- [ ] Kubernetes — deploy via Minikube
- [ ] GitLab CI — mirror pipeline
- [ ] Ansible — automate VM configuration
- [ ] HTTPS — SSL certificate via Let's Encrypt

---

## Author

**Timothy** — DevOps / Cloud Engineering Portfolio
- GitHub: [@Tim5223](https://github.com/Tim5223)
