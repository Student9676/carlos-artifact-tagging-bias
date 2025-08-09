import { useState } from 'react';
import Header from '../components/Header';

export default function Debiaser() {
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');

  const handleDebiasText = () => {
    // Placeholder for debias functionality
    setOutputText("Debiased text will appear here...");
  };

  return (
    <div className="relative min-h-screen bg-slate-800">
      {/* Content Container */}
      <div className="relative z-20 h-full flex flex-col">
        {/* Header */}
        <Header />

        {/* Main content */}
        <div className="flex-1 flex items-center justify-center p-10">
          <div className="w-full max-w-4xl">
            <h1 className="text-white text-4xl font-bold text-center mb-8">Museum Language Debiaser</h1>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Input Section */}
              <div className="space-y-4">
                <h2 className="text-white text-2xl font-semibold">Input Text</h2>
                <textarea
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Enter your museum text here to check for bias..."
                  className="w-full h-64 p-4 bg-white bg-opacity-10 backdrop-blur-md border border-white border-opacity-20 rounded-lg text-white placeholder-gray-300 resize-none focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
                />
                <button
                  onClick={handleDebiasText}
                  className="w-full px-6 py-3 bg-white bg-opacity-10 backdrop-blur-md text-white text-lg font-semibold rounded-lg shadow-lg border border-white border-opacity-20 hover:bg-opacity-20 transition-all duration-300"
                >
                  Analyze & Debias Text
                </button>
              </div>

              {/* Output Section */}
              <div className="space-y-4">
                <h2 className="text-white text-2xl font-semibold">Debiased Text</h2>
                <textarea
                  value={outputText}
                  readOnly
                  placeholder="Debiased text will appear here..."
                  className="w-full h-64 p-4 bg-white bg-opacity-10 backdrop-blur-md border border-white border-opacity-20 rounded-lg text-white placeholder-gray-300 resize-none focus:outline-none"
                />
                <button
                  className="w-full px-6 py-3 bg-white bg-opacity-10 backdrop-blur-md text-white text-lg font-semibold rounded-lg shadow-lg border border-white border-opacity-20 hover:bg-opacity-20 transition-all duration-300"
                  onClick={() => navigator.clipboard.writeText(outputText)}
                >
                  Copy to Clipboard
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
