import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import PageLayout from '../components/PageLayout';

export default function Debiaser() {
  const [inputText, setInputText] = useState('');
  const [exampleSuccess, setExampleSuccess] = useState(false);
  const [clearSuccess, setClearSuccess] = useState(false);
  const navigate = useNavigate();

  const handleDebiasText = () => {
    if (!inputText.trim()) {
      return;
    }
    navigate('/results', { state: { inputText } });
  };

  const handleAddExample = () => {
    setInputText('A Chewa boy in Malawi must undergo a three-day initiation in order to achieve full status as an adult. This rite concludes with a masquerade called Gule Wamkulu, organized and performed by the semi-secret Nyau Society into which he has been inducted. There is evidence suggesting that the Nyau initiation ceremony, which takes place after the July harvest, dates to the 17th century and Gule Wamkulu is protected as a UNESCO masterpiece of intangible heritage. Masks, such as this one, may be commissioned from a recognized carver by a friend or relative, or by the initiate himself. Nyau masks can represent spirits of the deceased, wild and unruly spirits, animals, or even caricatures of personalities from the community. The mischievous characters interact with and perform for the audience to teach moral lessons and enforce social norms. This extraordinary example is carved from a dense, oily hardwood and sparingly decorated with red European paint. Its commanding presence is marked by a strong brow, varying textures and materials in the beard, and a rather wild full head of hair.');
    setExampleSuccess(true);
    setTimeout(() => setExampleSuccess(false), 1000);
  };

  const handleClear = () => {
    setInputText('');
    setClearSuccess(true);
    setTimeout(() => setClearSuccess(false), 1000);
  };

  return (
    <PageLayout backgroundType="dark-blue">
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
          
          {/* Add Example Text and Clear buttons */}
          <div className="flex justify-center">
            <button 
            className={`mt-4 w-full px-6 py-3 bg-white bg-opacity-10 backdrop-blur-md text-white text-lg font-semibold rounded-lg shadow-lg border border-white border-opacity-20 hover:bg-opacity-20 transition-all duration-300 relative overflow-hidden ${
              exampleSuccess ? 'bg-green-500 bg-opacity-20 border-green-400' : ''
            }`}
            onClick={handleAddExample}
            >
              <span className={`transition-all duration-300 ${exampleSuccess ? 'transform translate-y-[-100%] opacity-0' : 'transform translate-y-0 opacity-100'}`}>
                Add Example Text
              </span>
              <span className={`absolute inset-0 flex items-center justify-center transition-all duration-300 ${
                exampleSuccess ? 'transform translate-y-0 opacity-100' : 'transform translate-y-full opacity-0'
              }`}>
                Added
              </span>
            </button>
            <button
              className={`mt-4 w-full px-6 py-3 bg-white bg-opacity-10 backdrop-blur-md text-white text-lg font-semibold rounded-lg shadow-lg border border-white border-opacity-20 hover:bg-opacity-20 transition-all duration-300 ml-4 relative overflow-hidden ${
                clearSuccess ? 'bg-red-500 bg-opacity-20 border-red-400' : ''
              }`}
              onClick={handleClear}
            >
              <span className={`transition-all duration-300 ${clearSuccess ? 'transform translate-y-[-100%] opacity-0' : 'transform translate-y-0 opacity-100'}`}>
                Clear
              </span>
              <span className={`absolute inset-0 flex items-center justify-center transition-all duration-300 ${
                clearSuccess ? 'transform translate-y-0 opacity-100' : 'transform translate-y-full opacity-0'
              }`}>
                Cleared
              </span>
            </button>
          </div>

        </div>
      </div>
    </PageLayout>
  );
}
