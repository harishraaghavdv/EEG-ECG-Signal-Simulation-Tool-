import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Brain, Heart, Activity, Zap, ArrowRight } from 'lucide-react';

const HomePage = () => {
  const navigate = useNavigate();

  const handleSignalTypeSelect = (signalType) => {
    navigate('/signal-type', { state: { signalType } });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-3">
              <div className="bg-blue-600 p-2 rounded-lg">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <h1 className="text-2xl font-bold text-gray-900">EEG & ECG Generator</h1>
            </div>
            <div className="text-sm text-gray-500">
              Synthetic Signal Generation Tool
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Generate Realistic Medical Signals
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Create synthetic EEG and ECG signals for research, education, and development. 
            Choose from a wide range of normal and abnormal patterns with clinical accuracy.
          </p>
        </div>

        {/* Signal Type Selection */}
        <div className="grid md:grid-cols-2 gap-8 mb-16">
          {/* EEG Card */}
          <div 
            className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer border border-gray-200 hover:border-blue-300 group"
            onClick={() => handleSignalTypeSelect('eeg')}
          >
            <div className="p-8">
              <div className="flex items-center justify-between mb-6">
                <div className="bg-blue-100 p-4 rounded-full group-hover:bg-blue-200 transition-colors">
                  <Brain className="w-8 h-8 text-blue-600" />
                </div>
                <ArrowRight className="w-6 h-6 text-gray-400 group-hover:text-blue-600 transition-colors" />
              </div>
              
              <h3 className="text-2xl font-bold text-gray-900 mb-3">EEG Generator</h3>
              <p className="text-gray-600 mb-6">
                Generate electroencephalogram signals with multiple channels and clinical patterns.
              </p>
              
              <div className="space-y-3">
                <div className="flex items-center text-sm text-gray-600">
                  <Activity className="w-4 h-4 mr-2" />
                  <span>16 Standard Channels</span>
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <Zap className="w-4 h-4 mr-2" />
                  <span>Normal & Abnormal Patterns</span>
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <Brain className="w-4 h-4 mr-2" />
                  <span>Clinical-Style Plots</span>
                </div>
              </div>
            </div>
          </div>

          {/* ECG Card */}
          <div 
            className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer border border-gray-200 hover:border-red-300 group"
            onClick={() => handleSignalTypeSelect('ecg')}
          >
            <div className="p-8">
              <div className="flex items-center justify-between mb-6">
                <div className="bg-red-100 p-4 rounded-full group-hover:bg-red-200 transition-colors">
                  <Heart className="w-8 h-8 text-red-600" />
                </div>
                <ArrowRight className="w-6 h-6 text-gray-400 group-hover:text-red-600 transition-colors" />
              </div>
              
              <h3 className="text-2xl font-bold text-gray-900 mb-3">ECG Generator</h3>
              <p className="text-gray-600 mb-6">
                Generate electrocardiogram signals with realistic cardiac rhythms and abnormalities.
              </p>
              
              <div className="space-y-3">
                <div className="flex items-center text-sm text-gray-600">
                  <Activity className="w-4 h-4 mr-2" />
                  <span>Multiple Rhythms</span>
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <Zap className="w-4 h-4 mr-2" />
                  <span>HRV Analysis</span>
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <Heart className="w-4 h-4 mr-2" />
                  <span>ECG Paper Style</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">Key Features</h3>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="bg-green-100 p-3 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                <Zap className="w-6 h-6 text-green-600" />
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Real-time Generation</h4>
              <p className="text-gray-600 text-sm">
                Generate signals instantly with customizable parameters
              </p>
            </div>
            <div className="text-center">
              <div className="bg-purple-100 p-3 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                <Activity className="w-6 h-6 text-purple-600" />
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Clinical Accuracy</h4>
              <p className="text-gray-600 text-sm">
                Realistic patterns based on medical literature
              </p>
            </div>
            <div className="text-center">
              <div className="bg-orange-100 p-3 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                <Brain className="w-6 h-6 text-orange-600" />
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Export Options</h4>
              <p className="text-gray-600 text-sm">
                Download CSV data, features, and high-quality plots
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage; 