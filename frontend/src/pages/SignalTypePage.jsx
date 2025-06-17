import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Brain, Heart, ArrowRight } from 'lucide-react';
import Navigation from '../components/Navigation';

const SignalTypePage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { signalType } = location.state || {};

  // Redirect if no signal type is provided
  if (!signalType) {
    navigate('/');
    return null;
  }

  const handleContinue = () => {
    navigate(`/category/${signalType}`);
  };

  const getSignalInfo = () => {
    if (signalType === 'eeg') {
      return {
        title: 'EEG Generator',
        icon: <Brain className="w-8 h-8 text-blue-600" />,
        color: 'blue',
        features: [
          '16 Standard EEG Channels',
          'Normal & Abnormal Patterns',
          'Clinical-Style Multi-Channel Plots',
          'Band Power Analysis'
        ]
      };
    } else {
      return {
        title: 'ECG Generator',
        icon: <Heart className="w-8 h-8 text-red-600" />,
        description: 'Electrocardiogram signals with realistic cardiac rhythms',
        color: 'red',
        features: [
          'Single Lead ECG',
          'Normal & Abnormal Rhythms',
          'ECG Paper Style Plots',
          'HRV Analysis'
        ]
      };
    }
  };

  const signalInfo = getSignalInfo();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <Navigation 
        title={signalInfo.title}
        subtitle="Signal Type Confirmation"
      />

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white rounded-xl shadow-lg p-8">
          {/* Signal Type Confirmation */}
          <div className="text-center mb-8">
            <div className={`bg-${signalInfo.color}-100 p-6 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-6`}>
              {signalInfo.icon}
            </div>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              {signalInfo.title}
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              {signalInfo.description}
            </p>
          </div>

          {/* Features */}
          <div className="mb-8">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">What you'll get:</h3>
            <div className="grid md:grid-cols-2 gap-4">
              {signalInfo.features.map((feature, index) => (
                <div key={index} className="flex items-center p-4 bg-gray-50 rounded-lg">
                  <div className={`bg-${signalInfo.color}-500 w-2 h-2 rounded-full mr-3`}></div>
                  <span className="text-gray-700">{feature}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Next Steps */}
          <div className="bg-blue-50 rounded-lg p-6 mb-8">
            <h3 className="text-lg font-semibold text-blue-900 mb-3">Next Steps:</h3>
            <ol className="list-decimal list-inside space-y-2 text-blue-800">
              <li>Choose between Normal or Abnormal patterns</li>
              <li>Select a specific signal type</li>
              <li>Configure generation parameters</li>
              <li>Generate and download your signals</li>
            </ol>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-center">
            <button
              onClick={handleContinue}
              className={`px-8 py-3 bg-${signalInfo.color}-600 text-white rounded-lg hover:bg-${signalInfo.color}-700 transition-colors flex items-center`}
            >
              Continue
              <ArrowRight className="w-4 h-4 ml-2" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignalTypePage; 