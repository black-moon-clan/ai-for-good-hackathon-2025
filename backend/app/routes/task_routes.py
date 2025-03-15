from flask import Blueprint, request, jsonify
from app.services.task_service import TaskService

task_bp = Blueprint('tasks', __name__)

@task_bp.route('', methods=['GET'])
def get_all_tasks():
    tasks = TaskService.get_all_tasks()
    return jsonify(tasks)

@task_bp.route('/<task_id>', methods=['GET'])
def get_task(task_id):
    task = TaskService.get_task_by_id(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task)

@task_bp.route('', methods=['POST'])
def create_task():
    print("Creating task")
    task_data = request.json
    task = TaskService.create_task(task_data)
    return jsonify(task), 201

@task_bp.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    task_data = request.json
    task = TaskService.update_task(task_id, task_data)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task)

@task_bp.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    success = TaskService.delete_task(task_id)
    if not success:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': 'Task deleted successfully'})

@task_bp.route('/<task_id>/start', methods=['POST'])
def start_task(task_id):
    success = TaskService.start_task(task_id)
    if not success:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': 'Task started successfully'}) 