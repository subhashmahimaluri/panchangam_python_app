# Panchangam Calendar App - Makefile
# Cross-platform development commands

.PHONY: help dev install clean backend frontend build

# Default target
help:
	@echo "Panchangam Calendar App Commands:"
	@echo "=================================="
	@echo "make dev        - Start both frontend and backend servers"
	@echo "make backend    - Start only backend server"
	@echo "make frontend   - Start only frontend server"
	@echo "make install    - Install all dependencies"
	@echo "make build      - Build frontend for production"
	@echo "make clean      - Clean build files and cache"
	@echo "make help       - Show this help message"

# Start both servers (uses npm script with concurrently)
dev:
	@echo "🚀 Starting both servers..."
	npm run dev

# Start only backend
backend:
	@echo "🐍 Starting backend server..."
	cd backend && python run_server.py

# Start only frontend
frontend:
	@echo "⚛️ Starting frontend server..."
	cd frontend && pnpm dev

# Install all dependencies
install:
	@echo "📦 Installing all dependencies..."
	npm run install:all

# Build frontend
build:
	@echo "🔨 Building frontend..."
	cd frontend && pnpm build

# Clean build files
clean:
	@echo "🧹 Cleaning build files..."
	npm run clean