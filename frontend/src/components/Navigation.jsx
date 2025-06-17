import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Brain, Heart, ArrowLeft } from 'lucide-react';

const Navigation = ({ showBack = true, title, subtitle }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleBack = () => {
    if (location.pathname === '/signal-type') {
      navigate('/');
    } else if (location.pathname.startsWith('/category/')) {
      navigate('/signal-type', { state: { signalType: location.pathname.split('/')[2] } });
    } else if (location.pathname.startsWith('/generator/')) {
      const [, , signalType] = location.pathname.split('/');
      navigate(`/category/${signalType}`);
    } else {
      navigate('/');
    }
  };

  const getSignalIcon = () => {
    if (location.pathname.includes('/eeg') || location.pathname.includes('eeg')) {
      return <Brain className="w-6 h-6 text-blue-600" />;
    } else if (location.pathname.includes('/ecg') || location.pathname.includes('ecg')) {
      return <Heart className="w-6 h-6 text-red-600" />;
    }
    return null;
  };

  const getSignalColor = () => {
    if (location.pathname.includes('/eeg') || location.pathname.includes('eeg')) {
      return 'blue';
    } else if (location.pathname.includes('/ecg') || location.pathname.includes('ecg')) {
      return 'red';
    }
    return 'gray';
  };

  const signalColor = getSignalColor();

  return (
    <div className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center py-6">
          {showBack && (
            <button
              onClick={handleBack}
              className="flex items-center text-gray-600 hover:text-gray-900 mr-6 transition-colors"
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              Back
            </button>
          )}
          
          <div className="flex items-center space-x-3">
            {getSignalIcon() && (
              <div className={`bg-${signalColor}-100 p-2 rounded-lg`}>
                {getSignalIcon()}
              </div>
            )}
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
              {subtitle && (
                <p className="text-sm text-gray-500">{subtitle}</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Navigation; 