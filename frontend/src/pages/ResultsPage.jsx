import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { ArrowLeft, Download, FileText, BarChart3, Image } from 'lucide-react';
import { apiService } from '../services/api';

const ResultsPage = ({ data }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [downloading, setDownloading] = useState({});

  // Use data from props or location state
  const resultData = data || location.state?.data;

  const handleBack = () => {
    navigate('/');
  };

  const handleDownload = async (fileType) => {
    if (!resultData?.session_id) return;

    setDownloading(prev => ({ ...prev, [fileType]: true }));
    
    try {
      const response = await apiService.downloadFile(resultData.session_id, fileType);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${resultData.signalType || 'signal'}_${fileType}.${fileType === 'plot' ? 'png' : 'csv'}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error downloading file:', error);
    } finally {
      setDownloading(prev => ({ ...prev, [fileType]: false }));
    }
  };

  if (!resultData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">No Results Found</h2>
          <p className="text-gray-600 mb-6">Please generate a signal first.</p>
          <button
            onClick={handleBack}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Go Home
          </button>
        </div>
      </div>
    );
  }

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
              Back to Home
            </button>
            <h1 className="text-2xl font-bold text-gray-900">Generation Results</h1>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Success Message */}
        <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-8">
          <div className="flex items-center">
            <div className="bg-green-100 p-2 rounded-full mr-4">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div>
              <h2 className="text-xl font-semibold text-green-900">Signal Generated Successfully!</h2>
              <p className="text-green-700">Your synthetic signal has been created and is ready for download.</p>
            </div>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Generated Plot */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Generated Signal Plot</h3>
              <div className="bg-gray-100 rounded-lg p-4">
                <img
                  src={`http://localhost:5000/${resultData.data.plot_path}`}
                  alt="Generated Signal"
                  className="w-full h-auto rounded"
                />
              </div>
            </div>

            {/* Signal Information */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Signal Information</h3>
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">Generation Parameters</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Duration:</span>
                      <span className="font-medium">{resultData.data.duration} seconds</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Sampling Rate:</span>
                      <span className="font-medium">{resultData.data.sampling_rate} Hz</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Session ID:</span>
                      <span className="font-medium text-xs">{resultData.session_id}</span>
                    </div>
                  </div>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">Generated Files</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-center text-green-600">
                      <FileText className="w-4 h-4 mr-2" />
                      <span>Raw Data CSV</span>
                    </div>
                    <div className="flex items-center text-green-600">
                      <BarChart3 className="w-4 h-4 mr-2" />
                      <span>Features CSV</span>
                    </div>
                    <div className="flex items-center text-green-600">
                      <Image className="w-4 h-4 mr-2" />
                      <span>High-Quality Plot</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Download Panel */}
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Download Files</h3>
              
              <div className="space-y-3">
                <button
                  onClick={() => handleDownload('csv')}
                  disabled={downloading.csv}
                  className="w-full flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center">
                    <FileText className="w-5 h-5 text-blue-600 mr-3" />
                    <div className="text-left">
                      <div className="font-medium text-gray-900">Raw Data</div>
                      <div className="text-sm text-gray-500">CSV format</div>
                    </div>
                  </div>
                  <Download className="w-4 h-4 text-gray-400" />
                </button>

                <button
                  onClick={() => handleDownload('features')}
                  disabled={downloading.features}
                  className="w-full flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center">
                    <BarChart3 className="w-5 h-5 text-green-600 mr-3" />
                    <div className="text-left">
                      <div className="font-medium text-gray-900">Features</div>
                      <div className="text-sm text-gray-500">Band power / HRV</div>
                    </div>
                  </div>
                  <Download className="w-4 h-4 text-gray-400" />
                </button>

                <button
                  onClick={() => handleDownload('plot')}
                  disabled={downloading.plot}
                  className="w-full flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center">
                    <Image className="w-5 h-5 text-purple-600 mr-3" />
                    <div className="text-left">
                      <div className="font-medium text-gray-900">Plot Image</div>
                      <div className="text-sm text-gray-500">High-resolution PNG</div>
                    </div>
                  </div>
                  <Download className="w-4 h-4 text-gray-400" />
                </button>
              </div>
            </div>

            {/* Generate New Signal */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Generate Another Signal</h3>
              <p className="text-gray-600 text-sm mb-4">
                Create a new signal with different parameters or patterns.
              </p>
              <button
                onClick={handleBack}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Start New Generation
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage; 