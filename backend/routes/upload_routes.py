from flask import Blueprint, request, jsonify
from backend.services.data_loader import DataLoader
import os
from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}

@upload_bp.route('/csv', methods=['POST'])
def upload_csv():
    """Upload and process CSV file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Ensure upload directory exists
            os.makedirs('data', exist_ok=True)
            filepath = os.path.join('data', filename)
            file.save(filepath)
            
            result = DataLoader.load_from_csv(filepath)
            
            if result['success']:
                return jsonify({
                    'message': f"Successfully loaded {result['count']} tickets",
                    'count': result['count']
                })
            else:
                return jsonify({'error': result['error']}), 500
        
        return jsonify({'error': 'Invalid file type. Please upload CSV file'}), 400
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@upload_bp.route('/sample', methods=['POST'])
def generate_sample():
    """Generate sample tickets"""
    try:
        result = DataLoader.generate_sample_tickets(50)
        if result['success']:
            return jsonify({
                'message': f"Successfully generated {result['count']} sample tickets",
                'count': result['count']
            })
        else:
            return jsonify({'error': 'Failed to generate sample tickets'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500