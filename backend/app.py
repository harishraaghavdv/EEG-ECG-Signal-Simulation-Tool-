from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import uuid
import json
from datetime import datetime
from generator.eeg_generator import EEGGenerator
from generator.ecg_generator import ECGGenerator
from generator.utils import create_output_directories

app = Flask(__name__)
CORS(app)

# Initialize generators
eeg_generator = EEGGenerator()
ecg_generator = ECGGenerator()

# Create output directories
create_output_directories()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "EEG/ECG Generator API is running"})

@app.route('/api/eeg/types', methods=['GET'])
def get_eeg_types():
    """Get available EEG types and subtypes"""
    return jsonify({
        "normal": {
            "Normal Awake": "normal_awake",
            "Sleep Stage 1": "sleep_stage1", 
            "Sleep Stage 2": "sleep_stage2",
            "Sleep Stage 3": "sleep_stage3",
            "REM Sleep": "rem_sleep"
        },
        "abnormal": {
            "Interictal Spikes": "interictal_spikes",
            "3 Hz Spike-Wave": "spike_wave_3hz",
            "Focal Spikes": "focal_spikes", 
            "Polyspike": "polyspike",
            "Hypsarrhythmia": "hypsarrhythmia",
            "Focal Slowing": "focal_slowing",
            "Diffuse Slowing": "diffuse_slowing",
            "Triphasic Waves": "triphasic_waves",
            "Periodic Discharges": "periodic_discharges",
            "Burst Suppression": "burst_suppression",
            "Alpha Coma": "alpha_coma",
            "Flat EEG": "flat_eeg"
        }
    })

@app.route('/api/ecg/types', methods=['GET'])
def get_ecg_types():
    """Get available ECG types and subtypes"""
    return jsonify({
        "normal": {
            "Normal Sinus Rhythm": "normal_sinus",
            "Sinus Bradycardia": "sinus_bradycardia",
            "Sinus Tachycardia": "sinus_tachycardia"
        },
        "abnormal": {
            "First Degree Heart Block": "first_degree_block",
            "Second Degree Mobitz I": "second_degree_mobitz1",
            "Second Degree Mobitz II": "second_degree_mobitz2", 
            "Third Degree Heart Block": "third_degree_block",
            "Left Bundle Branch Block": "lbbb",
            "Right Bundle Branch Block": "rbbb",
            "STEMI": "stemi",
            "NSTEMI": "nstemi",
            "Atrial Fibrillation": "atrial_fibrillation",
            "Ventricular Tachycardia": "ventricular_tachycardia",
            "Hyperkalemia": "hyperkalemia",
            "Hypokalemia": "hypokalemia",
            "Pericarditis": "pericarditis",
            "Pulmonary Embolism": "pulmonary_embolism",
            "Digitalis Effect": "digitalis_effect"
        }
    })

@app.route('/api/generate/eeg', methods=['POST'])
def generate_eeg():
    """Generate synthetic EEG data"""
    try:
        data = request.get_json()
        eeg_type = data.get('type')
        duration = data.get('duration', 30)
        sampling_rate = data.get('sampling_rate', 256)
        
        if not eeg_type:
            return jsonify({"error": "EEG type is required"}), 400
            
        # Generate unique ID for this session
        session_id = str(uuid.uuid4())
        
        # Generate EEG data
        result = eeg_generator.generate(
            eeg_type=eeg_type,
            duration=duration,
            sampling_rate=sampling_rate,
            session_id=session_id
        )
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "data": result
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate/ecg', methods=['POST'])
def generate_ecg():
    """Generate synthetic ECG data"""
    try:
        data = request.get_json()
        ecg_type = data.get('type')
        duration = data.get('duration', 30)
        sampling_rate = data.get('sampling_rate', 256)
        
        if not ecg_type:
            return jsonify({"error": "ECG type is required"}), 400
            
        # Generate unique ID for this session
        session_id = str(uuid.uuid4())
        
        # Generate ECG data
        result = ecg_generator.generate(
            ecg_type=ecg_type,
            duration=duration,
            sampling_rate=sampling_rate,
            session_id=session_id
        )
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "data": result
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/download/<session_id>/<file_type>', methods=['GET'])
def download_file(session_id, file_type):
    """Download generated files"""
    try:
        file_path = None
        
        if file_type == 'csv':
            file_path = f"static/csv/{session_id}_data.csv"
        elif file_type == 'features':
            file_path = f"static/csv/{session_id}_features.csv"
        elif file_type == 'plot':
            file_path = f"static/plots/{session_id}_plot.png"
        else:
            return jsonify({"error": "Invalid file type"}), 400
            
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
            
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/session/<session_id>/files', methods=['GET'])
def get_session_files(session_id):
    """Get all files for a session"""
    try:
        files = {
            "csv": f"static/csv/{session_id}_data.csv",
            "features": f"static/csv/{session_id}_features.csv", 
            "plot": f"static/plots/{session_id}_plot.png"
        }
        
        available_files = {}
        for file_type, file_path in files.items():
            if os.path.exists(file_path):
                available_files[file_type] = file_path
                
        return jsonify({
            "session_id": session_id,
            "files": available_files
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 