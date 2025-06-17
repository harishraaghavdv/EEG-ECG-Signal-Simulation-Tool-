import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Brain, Heart, Activity, Zap } from 'lucide-react';

const HomePage = ({ onSelectType }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Synthetic EEG & ECG Generator
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Generate realistic synthetic brainwave and cardiac signals for research, 
            education, and development purposes
          </p>
        </div>

        {/* Main Selection Cards */}
        <div className="grid md:grid-cols-2 gap-8 mb-12">
          {/* EEG Card */}
          <Card className="hover:shadow-lg transition-shadow duration-300 cursor-pointer group"
                onClick={() => onSelectType('eeg')}>
            <CardHeader className="text-center">
              <div className="mx-auto mb-4 p-4 bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center group-hover:bg-blue-200 transition-colors">
                <Brain className="w-8 h-8 text-blue-600" />
              </div>
              <CardTitle className="text-2xl text-blue-900">EEG Generator</CardTitle>
              <CardDescription className="text-blue-700">
                Generate synthetic electroencephalogram signals
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <div className="space-y-2 text-sm text-gray-600">
                <div className="flex items-center justify-center gap-2">
                  <Activity className="w-4 h-4" />
                  <span>Normal & Abnormal Patterns</span>
                </div>
                <div className="flex items-center justify-center gap-2">
                  <Zap className="w-4 h-4" />
                  <span>Multiple Channel Support</span>
                </div>
                <div className="flex items-center justify-center gap-2">
                  <Brain className="w-4 h-4" />
                  <span>Clinical-Style Plots</span>
                </div>
              </div>
              <Button className="mt-6 w-full bg-blue-600 hover:bg-blue-700">
                Generate EEG
              </Button>
            </CardContent>
          </Card>

          {/* ECG Card */}
          <Card className="hover:shadow-lg transition-shadow duration-300 cursor-pointer group"
                onClick={() => onSelectType('ecg')}>
            <CardHeader className="text-center">
              <div className="mx-auto mb-4 p-4 bg-red-100 rounded-full w-16 h-16 flex items-center justify-center group-hover:bg-red-200 transition-colors">
                <Heart className="w-8 h-8 text-red-600" />
              </div>
              <CardTitle className="text-2xl text-red-900">ECG Generator</CardTitle>
              <CardDescription className="text-red-700">
                Generate synthetic electrocardiogram signals
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <div className="space-y-2 text-sm text-gray-600">
                <div className="flex items-center justify-center gap-2">
                  <Activity className="w-4 h-4" />
                  <span>Normal & Abnormal Rhythms</span>
                </div>
                <div className="flex items-center justify-center gap-2">
                  <Zap className="w-4 h-4" />
                  <span>HRV Analysis</span>
                </div>
                <div className="flex items-center justify-center gap-2">
                  <Heart className="w-4 h-4" />
                  <span>ECG Paper Style</span>
                </div>
              </div>
              <Button className="mt-6 w-full bg-red-600 hover:bg-red-700">
                Generate ECG
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Features Section */}
        <div className="bg-white rounded-lg p-8 shadow-sm">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6 text-center">
            Key Features
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="mx-auto mb-3 p-3 bg-green-100 rounded-full w-12 h-12 flex items-center justify-center">
                <Zap className="w-6 h-6 text-green-600" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Real-time Generation</h3>
              <p className="text-gray-600 text-sm">
                Generate signals instantly with customizable parameters
              </p>
            </div>
            <div className="text-center">
              <div className="mx-auto mb-3 p-3 bg-purple-100 rounded-full w-12 h-12 flex items-center justify-center">
                <Activity className="w-6 h-6 text-purple-600" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Clinical Accuracy</h3>
              <p className="text-gray-600 text-sm">
                Realistic patterns based on medical literature and clinical data
              </p>
            </div>
            <div className="text-center">
              <div className="mx-auto mb-3 p-3 bg-orange-100 rounded-full w-12 h-12 flex items-center justify-center">
                <Brain className="w-6 h-6 text-orange-600" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Export Options</h3>
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