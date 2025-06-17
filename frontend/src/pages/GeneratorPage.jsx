import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Brain, Heart, ArrowLeft, Settings, Play, CheckCircle, XCircle } from 'lucide-react';
import { apiService } from '../services/api';
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from '@radix-ui/react-accordion';

const GeneratorPage = ({ onGenerationComplete }) => {
  const { signalType, category } = useParams();
  const navigate = useNavigate();
  
  const [signalTypes, setSignalTypes] = useState({});
  const [selectedType, setSelectedType] = useState(null);
  const [loading, setLoading] = useState(false);
  const [generatedData, setGeneratedData] = useState(null);
  const [settings, setSettings] = useState({
    duration: 30,
    sampling_rate: 256
  });

  const loadSignalTypes = useCallback(async () => {
    try {
      const response = signalType === 'eeg' 
        ? await apiService.getEEGTypes() 
        : await apiService.getECGTypes();
      setSignalTypes(response.data);
    } catch (error) {
      console.error('Error loading signal types:', error);
    }
  }, [signalType]);

  useEffect(() => {
    loadSignalTypes();
  }, [loadSignalTypes]);

  const handleGenerate = async () => {
    if (!selectedType) return;

    setLoading(true);
    try {
      const response = signalType === 'eeg'
        ? await apiService.generateEEG({
            type: selectedType,
            duration: settings.duration,
            sampling_rate: settings.sampling_rate
          })
        : await apiService.generateECG({
            type: selectedType,
            duration: settings.duration,
            sampling_rate: settings.sampling_rate
          });

      setGeneratedData(response.data);
      if (onGenerationComplete) {
        onGenerationComplete(response.data);
      }
    } catch (error) {
      console.error('Error generating signal:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    navigate(`/category/${signalType}`);
  };

  const handleViewResults = () => {
    navigate('/results');
  };

  const getSignalInfo = () => {
    if (signalType === 'eeg') {
      return {
        title: 'EEG Generator',
        icon: <Brain className="w-6 h-6 text-blue-600" />,
        color: 'blue'
      };
    } else {
      return {
        title: 'ECG Generator',
        icon: <Heart className="w-6 h-6 text-red-600" />,
        color: 'red'
      };
    }
  };

  const signalInfo = getSignalInfo();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center py-6">
            <button
              onClick={handleBack}
              className="flex items-center text-gray-600 hover:text-gray-900 mr-6"
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              Back
            </button>
            <div className="flex items-center space-x-3">
              <div className={`bg-${signalInfo.color}-100 p-2 rounded-lg`}>
                {signalInfo.icon}
              </div>
              <h1 className="text-2xl font-bold text-gray-900">
                {signalInfo.title} - {category.charAt(0).toUpperCase() + category.slice(1)}
              </h1>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Accordion for Normal/Abnormal Types */}
        <Accordion type="single" collapsible className="mb-8 rounded-xl shadow-lg bg-white">
          {Object.entries(signalTypes).map(([cat, types]) => (
            <AccordionItem value={cat} key={cat} className="border-b">
              <AccordionTrigger className="flex items-center justify-between w-full px-6 py-4 text-lg font-semibold focus:outline-none">
                <span className="flex items-center">
                  {cat === 'normal' ? <CheckCircle className="text-green-600 mr-2" /> : <XCircle className="text-red-600 mr-2" />}
                  {cat.charAt(0).toUpperCase() + cat.slice(1)} {signalType.toUpperCase()} Types
                </span>
              </AccordionTrigger>
              <AccordionContent className="px-8 pb-6">
                <ul className="space-y-2">
                  {Object.entries(types).map(([name, value]) => (
                    <li key={value}>
                      <button
                        className={`w-full text-left px-4 py-2 rounded-lg border-2 transition-all font-medium ${
                          selectedType === value
                            ? `border-${signalInfo.color}-500 bg-${signalInfo.color}-50 text-${signalInfo.color}-900` 
                            : 'border-gray-200 hover:border-gray-300 bg-white text-gray-900'
                        }`}
                        onClick={() => setSelectedType(value)}
                      >
                        {name}
                      </button>
                    </li>
                  ))}
                </ul>
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>

        {/* Settings */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <div className="flex items-center mb-4">
            <Settings className="w-5 h-5 text-gray-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Generation Settings</h3>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Duration (seconds)
              </label>
              <input
                type="number"
                min="10"
                max="300"
                value={settings.duration}
                onChange={(e) => setSettings(prev => ({ ...prev, duration: parseInt(e.target.value) }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Sampling Rate (Hz)
              </label>
              <input
                type="number"
                min="128"
                max="1024"
                step="128"
                value={settings.sampling_rate}
                onChange={(e) => setSettings(prev => ({ ...prev, sampling_rate: parseInt(e.target.value) }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        {/* Generate Button */}
        <button
          onClick={handleGenerate}
          disabled={!selectedType || loading}
          className={`w-full py-3 px-4 rounded-lg font-medium transition-colors flex items-center justify-center mb-8 ${
            !selectedType || loading
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : `bg-${signalInfo.color}-600 text-white hover:bg-${signalInfo.color}-700`
          }`}
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Generating...
            </>
          ) : (
            <>
              <Play className="w-4 h-4 mr-2" />
              Generate Signal
            </>
          )}
        </button>

        {/* Results Preview */}
        {generatedData && (
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Generated Signal</h2>
            <div className="bg-gray-100 rounded-lg p-4 mb-4">
              <img
                src={`http://localhost:5000/${generatedData.data.plot_path}`}
                alt="Generated Plot"
                className="w-full h-auto rounded"
              />
            </div>
            <div className="flex space-x-4">
              <button
                onClick={handleViewResults}
                className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
              >
                View Full Results
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default GeneratorPage; 