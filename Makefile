init:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

setup:
	@echo "Registering user..."
	curl -s -X POST http://localhost:5000/signup -H "Content-Type: application/json" -d '{"login": "$(user)", "password": "$(pass)"}'
	@echo "Generating auth token..."
	@echo "export AUTH_TOKEN=Basic $$(echo -n $(user):$(pass) | base64)"

create_game:
	@echo "Command to create a game:"
	@echo "curl -s -X POST http://localhost:5000/create -H \"Authorization: $$AUTH_TOKEN\" -H \"Content-Type: application/json\" -d '{\"against_computer\": true}'"

join_game:
	@echo "Command to join a game:"
	@echo "curl -s -X POST http://localhost:5000/game/join -H \"Authorization: $$AUTH_TOKEN\" -H \"Content-Type: application/json\" -d '{\"game_id\": \"<game_uuid>\"}'"

make_move:
	@echo "Command to make a move:"
	@echo "curl -s -X POST http://localhost:5000/game/<game_uuid> -H \"Authorization: $$AUTH_TOKEN\" -H \"Content-Type: application/json\" -d '{\"board\": [[1, 0, 0], [0, 0, 0], [0, 0, 0]]}'"

clean:
	rm -rf venv
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete
