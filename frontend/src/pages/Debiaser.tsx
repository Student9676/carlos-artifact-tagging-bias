import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';

export default function Debiaser() {
  const [inputText, setInputText] = useState('');
  const navigate = useNavigate();

  const handleDebiasText = () => {
    if (!inputText.trim()) {
      return;
    }
    navigate('/results', { state: { inputText } });
  };

  return (
    <div
      className="relative h-screen"
      style={{
        backgroundImage: "url('/src/assets/bg-img-1.png')",
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
      }}
    >
    <div className="absolute top-0 left-0 w-full h-full bg-black bg-opacity-30 z-10"></div>

      {/* Content Container */}
      <div className="relative z-20 h-full flex flex-col">
        {/* Header */}
        <Header />

        {/* Main content */}
        <div className="flex-1 flex items-center justify-center p-10">
          <div className="w-full max-w-5xl">
            
            <div className="text-center mb-14">
                <h1 className="text-white text-3xl">Lexicon Cleaner</h1>
                <p className="text-white text-lg">
                Enter text below to get a language analysis and an improved version.
                </p>
            </div>

              {/* Input Section */}
              <div className="space-x-0 flex items-center">
                <textarea
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Enter text here..."
                  className="w-full h-64 p-4 bg-white bg-opacity-10 backdrop-blur-md border border-white border-opacity-20 rounded-l-lg shadow-lg rounded-r-none text-white placeholder-gray-300 resize-none focus:outline-none focus:ring-0"
                />
                <button
                    className="h-64 px-6 bg-white bg-opacity-10 backdrop-blur-md text-white text-2xl font-semibold rounded-r-lg rounded-l-none shadow-lg border border-white border-opacity-20 hover:bg-opacity-20 transition-all duration-300 ml-4 flex items-center justify-center"
                    onClick={handleDebiasText}
                >
                    &gt;
                </button>
            </div>

          </div>
        </div>

      </div>
    </div>
  );
}
