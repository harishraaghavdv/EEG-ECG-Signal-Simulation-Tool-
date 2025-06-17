import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Brain, Heart, ArrowLeft, CheckCircle, AlertTriangle } from 'lucide-react';

const CategoryPage = () => {
  const { signalType } = useParams();
  const navigate = useNavigate();

  const handleCategorySelect = (category) => {
    navigate(`/generator/${signalType}/${category}`);
  };

  const handleBack = () => {
    navigate('/signal-type', { state: { signalType } });
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

  const categories = [
    {
      id: 'normal',
      title: 'Normal Patterns',
      description: 'Standard physiological signals',
      icon: <CheckCircle className="w-8 h-8 text-green-600" />,
      color: 'green',
      examples: signalType === 'eeg' 
        ? ['Normal Awake (alpha & beta)', 'Sleep Stage 1-3', 'REM Sleep']
        : ['Normal Sinus Rhythm', 'Sinus Bradycardia', 'Sinus Tachycardia']
    },
    {
      id: 'abnormal',
      title: 'Abnormal Patterns',
      description: 'Pathological and clinical conditions',
      icon: <AlertTriangle className="w-8 h-8 text-orange-600" />,
      color: 'orange',
      examples: signalType === 'eeg'
        ? ['Interictal Spikes', '3 Hz Spike-Wave', 'Focal Spikes', 'Polyspike', 'Hypsarrhythmia']
        : ['Heart Blocks', 'Bundle Branch Blocks', 'STEMI/NSTEMI', 'Arrhythmias']
    }
  ];

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
              <h1 className="text-2xl font-bold text-gray-900">{signalInfo.title}</h1>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Page Title */}
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Choose Signal Category
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Select whether you want to generate normal physiological patterns or abnormal clinical conditions
          </p>
        </div>

        {/* Category Selection */}
        <div className="grid md:grid-cols-2 gap-8 mb-12">
          {categories.map((category) => (
            <div
              key={category.id}
              className={`bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer border-2 border-transparent hover:border-${category.color}-300 group`}
              onClick={() => handleCategorySelect(category.id)}
            >
              <div className="p-8">
                {/* Header */}
                <div className="flex items-center justify-between mb-6">
                  <div className={`bg-${category.color}-100 p-4 rounded-full group-hover:bg-${category.color}-200 transition-colors`}>
                    {category.icon}
                  </div>
                  <div className={`text-${category.color}-600 font-semibold text-sm bg-${category.color}-50 px-3 py-1 rounded-full`}>
                    {category.id.toUpperCase()}
                  </div>
                </div>

                {/* Content */}
                <h3 className="text-2xl font-bold text-gray-900 mb-3">
                  {category.title}
                </h3>
                <p className="text-gray-600 mb-6">
                  {category.description}
                </p>

                {/* Examples */}
                <div className="space-y-2">
                  <h4 className="font-semibold text-gray-900 text-sm">Examples:</h4>
                  <ul className="space-y-1">
                    {category.examples.map((example, index) => (
                      <li key={index} className="text-sm text-gray-600 flex items-center">
                        <div className={`w-1.5 h-1.5 bg-${category.color}-500 rounded-full mr-2`}></div>
                        {example}
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Action */}
                <div className="mt-6 pt-6 border-t border-gray-100">
                  <button
                    className={`w-full py-3 bg-${category.color}-600 text-white rounded-lg hover:bg-${category.color}-700 transition-colors font-medium`}
                  >
                    Select {category.title}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Information Section */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h3 className="text-xl font-bold text-gray-900 mb-4">About Signal Categories</h3>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-semibold text-green-700 mb-2">Normal Patterns</h4>
              <p className="text-gray-600 text-sm">
                These represent standard physiological activity. Normal patterns are useful for 
                baseline comparisons, educational purposes, and understanding healthy signal characteristics.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-orange-700 mb-2">Abnormal Patterns</h4>
              <p className="text-gray-600 text-sm">
                These represent pathological conditions and clinical abnormalities. Abnormal patterns 
                are valuable for research, training, and developing detection algorithms.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CategoryPage; 