.PHONY: help express-local install-venv run-local rm-venv build-docker run-docker

# Переменные
DOCKER_COMPOSE = docker-compose
DOCKER = docker
PYTHON = python3

DOCKER_DIR = ./docker
PROGRAM_WORKDIR = ./program

# Цвета для вывода
GREEN = \033[0;32m
YELLOW = \033[0;33m
NC = \033[0m # No Color

help: ## Показать справку по доступным командам
	@echo "$(GREEN)Для получения информации о настройке генерации чисел прочитайте README$(NC)"
	@echo "$(GREEN)Доступные команды:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

express-local: install-venv run-local## Настраивает окружение и запускает программу локально (без Docker)

install-venv: ## Создать виртуальное окружение и установить зависимости (без Docker)
	@echo "$(GREEN)Создание виртуального окружения...$(NC)"
	$(PYTHON) -m venv $(PROGRAM_WORKDIR)/venv
	@echo "$(GREEN)Активация: source $(PROGRAM_WORKDIR)/venv/bin/activate$(NC)"
	@echo "$(GREEN)Установка зависимостей...$(NC)"
	$(PROGRAM_WORKDIR)/venv/bin/pip install -r $(PROGRAM_WORKDIR)/requirements.txt
	@echo "$(GREEN)Инициализация файла переменных окружения...$(NC)"
	test ! -f $(PROGRAM_WORKDIR)/.env && test -f program/.env.dist && cp $(PROGRAM_WORKDIR)/.env.dist $(PROGRAM_WORKDIR)/.env || true

run-local: ## Запустить приложение локально (без Docker)
	@echo "$(GREEN)Запуск приложения локально...$(NC)"
	$(PROGRAM_WORKDIR)/venv/bin/python $(PROGRAM_WORKDIR)/main.py
	@echo "$(GREEN)Результаты выполнения программы в директории output$(NC)"

rm-venv: ## Удалить виртуальное окружение (без Docker)
	@echo "$(GREEN)Удаление виртуального окружения...$(NC)"
	rm -r $(PROGRAM_WORKDIR)/venv

build-docker: ## Собрать Docker образ
	@echo "$(GREEN)Сборка Docker образа...$(NC)"
	test ! -f $(PROGRAM_WORKDIR)/.env && test -f program/.env.dist && cp $(PROGRAM_WORKDIR)/.env.dist $(PROGRAM_WORKDIR)/.env || true
	$(DOCKER_COMPOSE) -f $(DOCKER_DIR)/docker-compose.yml build

run-docker: ## Запустить программу в Docker контейнере
	@echo "$(GREEN)Запуск Docker контейнера...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_DIR)/docker-compose.yml up
	@echo "$(GREEN)Результаты выполнения программы в директории output$(NC)"
