import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import PageLayout from "../components/PageLayout";
import BiasMetricCard from "../components/BiasMetricCard";

// API function for debiasing text
const debiasText = async (text: string) => {
    const response = await fetch("http://localhost:8000/api/debias/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
    });

    const data = await response.json();
    
    if (!response.ok) {
        throw new Error(data.error || 'An unexpected error occurred. Please try again.');
    }
    
    return data;
};

export default function Results() {
    const location = useLocation();
    const navigate = useNavigate();
    const [loadingMessage, setLoadingMessage] = useState("Analyzing text for bias...");
    const [copySuccess, setCopySuccess] = useState(false);

    const inputText = location.state?.inputText || "";

    // Use TanStack Query for API call
    const { data: apiData, isLoading, error } = useQuery({
        queryKey: ['debias', inputText],
        queryFn: () => debiasText(inputText),
        enabled: !!inputText, // Run only if inputText exists
        retry: false, // Disable automatic retries
    });

    // Extract data from API response
    const debiasedText = apiData?.debiased_text || (error ? `Error processing text: ${error.message}. Please try again.` : "");
    const jargonScore = apiData?.classification?.jargon * 100 || 0;
    const subjectivityScore = apiData?.classification?.subjective * 100 || 0;
    const genderScore = apiData?.classification?.gender * 100 || 0;
    const socialScore = apiData?.classification?.social * 100 || 0;

    const loadingMessages = [
        "Analyzing text for bias...",
        "Identifying problematic language...",
        "Generating inclusive alternatives...",
        "Applying language improvements...",
        "Finalizing your results..."
    ];

    // Loading message rotation effect - only when loading
    useEffect(() => {
        if (!isLoading) return;
        
        let messageIndex = 0;
        const messageInterval = setInterval(() => {
            messageIndex = (messageIndex + 1) % loadingMessages.length;
            setLoadingMessage(loadingMessages[messageIndex]);
        }, 1000);

        return () => clearInterval(messageInterval);
    }, [isLoading, loadingMessages]);

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
                {!isLoading && (
                    <div className="text-center mb-14">
                        <h1 className="text-white text-3xl">Results</h1>
                    </div>
                )}

                {/* If loading, show loading spinner and message else show results */}
                {isLoading ? (
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
