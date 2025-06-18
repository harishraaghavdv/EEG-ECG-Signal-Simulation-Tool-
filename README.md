# Mantra Brainwave Dataset Demo

A comprehensive web application for generating synthetic EEG (Electroencephalogram) and ECG (Electrocardiogram) signals with both normal and abnormal patterns. This project provides a Flask backend API and React frontend for easy signal generation and visualization.

## Features

### EEG Signal Generation
- **Normal Patterns**: Awake, Sleep Stages 1-3, REM Sleep
- **Abnormal Patterns**: 
  - Epileptic: Interictal spikes, Spike-wave 3Hz, Focal spikes, Polyspikes, Hypsarrhythmia
  - Slowing: Focal slowing, Diffuse slowing
  - Encephalopathy: Triphasic waves, Periodic discharges, Burst suppression
  - Coma: Alpha coma, Flat EEG

### ECG Signal Generation
- **Normal Patterns**: Normal sinus rhythm, Sinus bradycardia, Sinus tachycardia
- **Abnormal Patterns**:
  - Conduction blocks: First-degree, Second-degree (Mobitz I/II), Third-degree
  - Bundle branch blocks: Left BBB, Right BBB
  - Ischemia: STEMI, NSTEMI
  - Arrhythmias: Atrial fibrillation, Ventricular tachycardia
  - Electrolyte disorders: Hyperkalemia, Hypokalemia
  - Other: Pericarditis, Pulmonary embolism, Digitalis effect

### Key Features
- 🧠 **Multi-channel EEG generation** (16 channels)
- ❤️ **Realistic ECG patterns** with HRV analysis
- 📊 **Interactive web interface** with real-time generation
- 📈 **Automatic feature extraction** and visualization
- 💾 **Data export** in CSV format
- 🖼️ **High-quality plots** for analysis
- 🔧 **Configurable parameters** (duration, sampling rate)

## Technology Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **NeuroKit2** - Signal processing
- **MNE** - EEG/EMG processing
- **NumPy/SciPy** - Scientific computing
- **Pandas** - Data manipulation
- **Matplotlib** - Plotting

### Frontend
- **React 18** - UI framework
- **Tailwind CSS** - Styling
- **Radix UI** - Accessible components
- **Axios** - HTTP client
- **React Router** - Navigation

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mantra_dataset_demo
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend server**
   ```bash
   python start_backend.py
   ```
   
   The API will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```
   
   The application will be available at `http://localhost:3000`

## Usage

### Web Interface

1. **Open the application** in your browser at `http://localhost:3000`
2. **Choose signal type**: EEG or ECG
3. **Select category**: Normal or Abnormal
4. **Pick specific pattern** from the available options
5. **Configure parameters**:
   - Duration (10-300 seconds)
   - Sampling rate (128-1024 Hz)
6. **Generate signal** and view results
7. **Download data** in CSV format or view plots

### API Endpoints

#### Health Check
```bash
GET /api/health
```

#### Get Signal Types
```bash
GET /api/eeg/types
GET /api/ecg/types
```

#### Generate Signals
```bash
POST /api/generate/eeg
POST /api/generate/ecg
```

**Request Body:**
```json
{
  "type": "normal_awake",
  "duration": 30,
  "sampling_rate": 256
}
```

#### Download Files
```bash
GET /api/download/{session_id}/csv
GET /api/download/{session_id}/features
GET /api/download/{session_id}/plot
```

## Project Structure

```
mantra_dataset_demo/
├── backend/
│   ├── app.py                 # Flask application
│   │   ├── generator/
│   │   │   ├── eeg_generator.py   # EEG signal generation
│   │   │   ├── ecg_generator.py   # ECG signal generation
│   │   │   └── utils.py          # Utility functions
│   │   └── static/
│   │       ├── csv/              # Generated CSV files
│   │       └── plots/            # Generated plots
│   ├── frontend/
│   │   ├── src/
│   │   │   ├── components/       # React components
│   │   │   ├── pages/           # Page components
│   │   │   ├── services/        # API services
│   │   │   └── lib/             # Utility libraries
│   │   └── public/              # Static assets
│   ├── mantra_brainwave_dataset/ # Sample dataset
│   ├── requirements.txt          # Python dependencies
│   ├── requirements-dev.txt      # Development dependencies
│   └── README.md                # This file
```

## Development

### Code Quality
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
flake8 backend/
black backend/
isort backend/

# Run tests
pytest backend/tests/
```

### Adding New Signal Types

1. **EEG Patterns**: Add new methods in `backend/generator/eeg_generator.py`
2. **ECG Patterns**: Add new methods in `backend/generator/ecg_generator.py`
3. **Update API**: Add new types to the signal type endpoints
4. **Update Frontend**: Add new options in the React components



## Acknowledgments

- **NeuroKit2** for signal processing capabilities
- **MNE** for EEG/EMG processing tools
- **React** and **Flask** communities for excellent documentation

## Support

For questions, issues, or contributions, please open an issue on GitHub or contact 
