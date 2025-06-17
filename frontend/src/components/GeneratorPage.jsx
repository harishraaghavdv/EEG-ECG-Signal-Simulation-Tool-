import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { ArrowLeft, Download, Brain, Heart, Activity, Settings } from 'lucide-react';
import { apiService } from '../services/api';

const GeneratorPage = ({ signalType, onBack, onGenerationComplete }) => {
  const [categories, setCategories] = useState({});
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [selectedType, setSelectedType] = useState(null);
  const [loading, setLoading] = useState(false);
  const [generatedData, setGeneratedData] = useState(null);
  const [settings, setSettings] = useState({
    duration: 30,
    sampling_rate: 256
  });

  useEffect(() => {
    loadSignalTypes();
  }, [signalType]);

  const loadSignalTypes = async () => {
    try {
      const response = signalType === 'eeg' 
        ? await apiService.getEEGTypes() 
        : await apiService.getECGTypes();
      setCategories(response.data);
    } catch (error) {
      console.error('Error loading signal types:', error);
    }
  };

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

  const handleDownload = async (fileType) => {
    if (!generatedData?.session_id) return;

    try {
      const response = await apiService.downloadFile(generatedData.session_id, fileType);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${signalType}_${selectedType}_${fileType}.${fileType === 'plot' ? 'png' : 'csv'}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error downloading file:', error);
    }
  };

  const getIcon = () => signalType === 'eeg' ? <Brain className="w-6 h-6" /> : <Heart className="w-6 h-6" />;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Button variant="outline" onClick={onBack} className="flex items-center gap-2">
            <ArrowLeft className="w-4 h-4" />
            Back
          </Button>
          <div className="flex items-center gap-3">
            {getIcon()}
            <h1 className="text-3xl font-bold text-gray-900">
              {signalType.toUpperCase()} Generator
            </h1>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Selection Panel */}
          <div className="lg:col-span-2 space-y-6">
            {/* Category Selection */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Activity className="w-5 h-5" />
                  Select Category
                </CardTitle>
                <CardDescription>
                  Choose between normal and abnormal patterns
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-4">
                  {Object.keys(categories).map((category) => (
                    <Button
                      key={category}
                      variant={selectedCategory === category ? "default" : "outline"}
                      className="h-20 text-lg font-medium"
                      onClick={() => {
                        setSelectedCategory(category);
                        setSelectedType(null);
                      }}
                    >
                      {category.charAt(0).toUpperCase() + category.slice(1)}
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Type Selection */}
            {selectedCategory && (
              <Card>
                <CardHeader>
                  <CardTitle>Select {signalType.toUpperCase()} Type</CardTitle>
                  <CardDescription>
                    Choose a specific pattern from the {selectedCategory} category
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {Object.entries(categories[selectedCategory]).map(([name, value]) => (
                      <Button
                        key={value}
                        variant={selectedType === value ? "default" : "outline"}
                        className="h-16 text-left justify-start px-4"
                        onClick={() => setSelectedType(value)}
                      >
                        {name}
                      </Button>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Settings */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Settings className="w-5 h-5" />
                  Generation Settings
                </CardTitle>
              </CardHeader>
              <CardContent>
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
              </CardContent>
            </Card>

            {/* Generate Button */}
            {selectedType && (
              <Button
                onClick={handleGenerate}
                disabled={loading}
                className="w-full h-12 text-lg font-medium"
              >
                {loading ? 'Generating...' : `Generate ${signalType.toUpperCase()}`}
              </Button>
            )}
          </div>

          {/* Results Panel */}
          <div className="space-y-6">
            {generatedData && (
              <Card>
                <CardHeader>
                  <CardTitle>Generated Data</CardTitle>
                  <CardDescription>
                    Session ID: {generatedData.session_id}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Plot Preview */}
                  <div className="bg-gray-100 rounded-lg p-4">
                    <img
                      src={`http://localhost:5000/${generatedData.data.plot_path}`}
                      alt="Generated Plot"
                      className="w-full h-auto rounded"
                    />
                  </div>

                  {/* Download Buttons */}
                  <div className="space-y-2">
                    <Button
                      onClick={() => handleDownload('csv')}
                      variant="outline"
                      className="w-full flex items-center gap-2"
                    >
                      <Download className="w-4 h-4" />
                      Download CSV Data
                    </Button>
                    <Button
                      onClick={() => handleDownload('features')}
                      variant="outline"
                      className="w-full flex items-center gap-2"
                    >
                      <Download className="w-4 h-4" />
                      Download Features
                    </Button>
                    <Button
                      onClick={() => handleDownload('plot')}
                      variant="outline"
                      className="w-full flex items-center gap-2"
                    >
                      <Download className="w-4 h-4" />
                      Download Plot
                    </Button>
                  </div>

                  {/* Data Info */}
                  <div className="text-sm text-gray-600 space-y-1">
                    <div>Duration: {generatedData.data.duration}s</div>
                    <div>Sampling Rate: {generatedData.data.sampling_rate} Hz</div>
                    {signalType === 'eeg' && (
                      <div>Channels: {generatedData.data.channels?.length || 0}</div>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default GeneratorPage; 