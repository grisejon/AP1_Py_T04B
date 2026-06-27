from flask import Blueprint, request, jsonify
from uuid import UUID
from di.container import container
from web.model.game_dto import GameDTO, BoardDTO
from web.module.game_module import GameModule
from web.model.sign_up_request import SignUpRequest
from web.auth.user_authenticator import user_authenticator

game_bp = Blueprint('game', __name__)

@game_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        if not data or 'login' not in data or 'password' not in data:
            return jsonify({"error": "Invalid request body"}), 400
        
        request_data = SignUpRequest(login=data['login'], password=data['password'])
        success = container.auth_service.register(request_data)
        
        if success:
            return jsonify({"message": "User registered successfully"}), 201
        else:
            return jsonify({"error": "User already exists"}), 409
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@game_bp.route('/login', methods=['POST'])
def login():
    auth_header = request.headers.get('Authorization')
    user_id = container.auth_service.authorize(auth_header)
    
    if user_id:
        return jsonify({"id": str(user_id)}), 200
    else:
        return jsonify({"error": "Unauthorized"}), 401

@game_bp.route('/game/create', methods=['POST'])
@user_authenticator
def create_game(user_id):
    try:
        data = request.get_json()
        if data is None or 'against_computer' not in data:
            return jsonify({"error": "Invalid request body, 'against_computer' is required"}), 400
        
        against_computer = bool(data['against_computer'])
        game = container.service.create_game(user_id, against_computer)
        
        return jsonify({
            "id": str(game.id),
            "state": game.state.value
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@game_bp.route('/game/list', methods=['GET'])
@user_authenticator
def list_all_games(user_id):
    games = container.service.get_all_games()
    return jsonify([{"id": str(g.id), "state": g.state.value} for g in games]), 200

@game_bp.route('/games', methods=['GET'])
@user_authenticator
def get_available_games(user_id):
    games = container.service.get_available_games()
    return jsonify([{"id": str(g.id)} for g in games]), 200

@game_bp.route('/game/join', methods=['POST'])
@user_authenticator
def join_game(user_id):
    try:
        data = request.get_json()
        if not data or 'game_id' not in data:
            return jsonify({"error": "Invalid request body"}), 400
        
        game_id = UUID(data['game_id'])
        game = container.service.join_game(game_id, user_id)
        
        if game:
            return jsonify({"message": "Joined game successfully", "id": str(game.id)}), 200
        else:
            return jsonify({"error": "Cannot join game"}), 400
            
    except ValueError:
        return jsonify({"error": "Invalid UUID format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@game_bp.route('/game/<uuid_id>', methods=['GET'])
@user_authenticator
def get_game(user_id, uuid_id):
    game = container.service.get_game(UUID(uuid_id))
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    return jsonify({
        "id": str(game.id),
        "board": game.board.matrix,
        "state": game.state.value,
        "player_one": str(game.player_one_id),
        "player_two": str(game.player_two_id),
        "current_turn": str(game.current_turn_user_id)
    }), 200

@game_bp.route('/user/<uuid_id>', methods=['GET'])
@user_authenticator
def get_user(user_id, uuid_id):
    target_user_id = UUID(uuid_id)
    user = container.user_service.get_user_by_id(target_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "id": str(user.id),
        "login": user.login
    }), 200

@game_bp.route('/game/<uuid_id>', methods=['POST'])
@user_authenticator
def post_game(user_id, uuid_id):
    try:
        data = request.get_json()
        if not data or 'board' not in data:
            return jsonify({"error": "Invalid request body"}), 400
            
        board_matrix = data['board']
        game_dto = GameDTO(id=UUID(uuid_id), board=BoardDTO(matrix=board_matrix))
        
        module = GameModule(container.service, container.repository)
        result_dto = module.play_move(game_dto, user_id=user_id)
        
        return jsonify({
            "id": str(result_dto.id),
            "board": result_dto.board.matrix,
            "winner": result_dto.winner
        }), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

