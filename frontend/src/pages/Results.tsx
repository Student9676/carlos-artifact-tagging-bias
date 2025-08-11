import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import PageLayout from "../components/PageLayout";
import BiasMetricCard from "../components/BiasMetricCard";

export default function Results() {
    const location = useLocation();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [debiasedText, setDebiasedText] = useState("");
    const [loadingMessage, setLoadingMessage] = useState("Analyzing text for bias...");
    const [jargonScore, setJargonScore] = useState(0);
    const [subjectivityScore, setSubjectivityScore] = useState(0);
    const [genderScore, setGenderScore] = useState(0);
    const [socialScore, setSocialScore] = useState(0);
    const [copySuccess, setCopySuccess] = useState(false);

    const inputText = location.state?.inputText || "";

    const loadingMessages = [
        "Analyzing text for bias...",
        "Identifying problematic language...",
        "Generating inclusive alternatives...",
        "Applying language improvements...",
        "Finalizing your results..."
    ];

    // autoupdate loading message every second
    useEffect(() => {    
        let messageIndex = 0;
        const messageInterval = setInterval(() => {
        messageIndex = (messageIndex + 1) % loadingMessages.length;
        setLoadingMessage(loadingMessages[messageIndex]);
        }, 1000);

        // Call backend API
        const debiasText = async () => {
            try {
                const response = await fetch("http://localhost:8000/api/debias/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ text: inputText }),
                });

                const data = await response.json();
                setDebiasedText(data.debiased_text);
                setJargonScore(data.classification.jargon * 100);
                setSubjectivityScore(data.classification.subjective * 100);
                setGenderScore(data.classification.gender * 100);
                setSocialScore(data.classification.social * 100);

            } catch (error) {
                setJargonScore(0);
                setSubjectivityScore(0);
                setGenderScore(0);
                setSocialScore(0);
                setDebiasedText(`Error processing text: ${error}. Please try again.`);

            } finally {
                setLoading(false);
                clearInterval(messageInterval);
            }
        };

        debiasText();
        return () => clearInterval(messageInterval);
    }, [inputText]);

    const handleCopyToClipboard = async () => {
        try {
            await navigator.clipboard.writeText(debiasedText);
            setCopySuccess(true);
            setTimeout(() => setCopySuccess(false), 1000); // Hide success message after 2 seconds
        } catch (error) {
            console.error('Failed to copy text: ', error);
        }
    };

    return (
        <PageLayout backgroundType="dark-blue">
            {/* Main content */}
            <div className="flex-1 flex items-center justify-center p-10">
            <div className="w-full max-w-5xl">
                
                {/* Show Results text if not loading */}
                {!loading && (
                    <div className="text-center mb-14">
                        <h1 className="text-white text-3xl">Results</h1>
                    </div>
                )}

                {/* If loading, show loading spinner and message else show results */}
                {loading ? (
                <div className="flex flex-col items-center justify-center">
                    {/* Loading Spinner */}
                    <img
                        src="/src/assets/loading.svg"
                        alt="Loading..."
                        className="w-20 h-20"
                    />
                    
                    {/* Loading Message */}
                    <p className="text-white text-xl font-medium animate-pulse">
                    {loadingMessage}
                    </p>
                </div>
                ) : (
                // Results Section
                <div className="space-y-4">
                    {/* Classification Metrics Row*/}
                    <div className="flex items-center justify-center space-x-4">
                        <BiasMetricCard label="Jargon" value={jargonScore} />
                        <BiasMetricCard label="Subjectivity" value={subjectivityScore} />
                        <BiasMetricCard label="Gender Bias" value={genderScore} />
                        <BiasMetricCard label="Social Bias" value={socialScore} />
                    </div>

                    {/* Debiased Text */}
                    <textarea
                    value={debiasedText}
                    readOnly
                    className="w-full h-64 p-4 bg-white bg-opacity-10 backdrop-blur-md border border-white border-opacity-20 rounded-lg shadow-lg text-white placeholder-gray-300 resize-none focus:outline-none"
                    />
                    
                    {/* copy button */}
                    <div className="flex space-x-4">
                    <button
                        className={`flex-1 px-6 py-3 bg-white bg-opacity-10 backdrop-blur-md text-white text-lg font-semibold rounded-lg shadow-lg border border-white border-opacity-20 hover:bg-opacity-20 transition-all duration-300 relative overflow-hidden ${
                            copySuccess ? 'bg-green-500 bg-opacity-20 border-green-400' : ''
                        }`}
                        onClick={handleCopyToClipboard}
                    >
                        <span className={`transition-all duration-300 ${copySuccess ? 'transform translate-y-[-100%] opacity-0' : 'transform translate-y-0 opacity-100'}`}>
                            Copy to Clipboard
                        </span>
                        <span className={`absolute inset-0 flex items-center justify-center transition-all duration-300 ${
                            copySuccess ? 'transform translate-y-0 opacity-100' : 'transform translate-y-full opacity-0'
                        }`}>
                            Copied
                        </span>
                    </button>

                    {/* retry button */}
                    <button
                        className="flex-1 px-6 py-3 bg-white bg-opacity-10 backdrop-blur-md text-white text-lg font-semibold rounded-lg shadow-lg border border-white border-opacity-20 hover:bg-opacity-20 transition-all duration-300"
                        onClick={() => navigate("/debiaser")}
                    >
                        Try Again
                    </button>
                    </div>
                </div>
                )}
            </div>
            </div>
        </PageLayout>
    );
}
