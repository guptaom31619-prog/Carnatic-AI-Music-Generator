.PHONY: install install-backend install-frontend run stop backend frontend test test-backend test-frontend lint clean

# ─── Install ──────────────────────────────────────────
install: install-backend install-frontend

install-backend:
	cd backend && pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

# ─── Run ──────────────────────────────────────────────
run: stop
	@echo "Starting Carnatic AI Music Generator (demo)..."
	@cd backend && uvicorn app.main:app --reload &
	@sleep 2
	@cd frontend && npm run dev &
	@sleep 3
	@echo ""
	@echo "========================================="
	@echo "  Backend  → http://localhost:8000"
	@echo "  Frontend → http://localhost:5173"
	@echo "  API Docs → http://localhost:8000/docs"
	@echo "========================================="

backend:
	cd backend && uvicorn app.main:app --reload

frontend:
	cd frontend && npm run dev

stop:
	@-kill $$(lsof -ti :8000) 2>/dev/null || true
	@-kill $$(lsof -ti :5173) 2>/dev/null || true
	@sleep 1
	@echo "Stopped all servers."

# ─── Test ─────────────────────────────────────────────
test: test-backend test-frontend

test-backend:
	cd backend && python -m pytest tests/ -v

test-frontend:
	cd frontend && npm run build

# ─── Clean ────────────────────────────────────────────
clean: stop
	rm -rf backend/generated/*.mid
	rm -rf backend/__pycache__ backend/app/__pycache__ backend/app/models/__pycache__
	rm -rf backend/.pytest_cache backend/tests/__pycache__
	rm -rf frontend/node_modules frontend/dist
	@echo "Cleaned."
