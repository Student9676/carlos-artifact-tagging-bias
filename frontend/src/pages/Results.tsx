import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Header from "../components/Header";

export default function Results() {
    const location = useLocation();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [debiasedText, setDebiasedText] = useState("");
    const [loadingMessage, setLoadingMessage] = useState("Analyzing text for bias...");
    
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

            if (!response.ok) {
            setDebiasedText(`API Error: ${response.status}`);
            } else {
                const data = await response.json();
                setDebiasedText(JSON.stringify(data, null, 2));
            }

        } catch (error) {
            setDebiasedText(`Error processing text: ${error}. Please try again.`);
        } finally {
            setLoading(false);
            clearInterval(messageInterval);
        }
        };

        debiasText();
        return () => clearInterval(messageInterval);
    }, [inputText]);

    return (
        // Background image
        <div
        className="relative h-screen overflow-hidden bg-slate-800"
        style={{
            backgroundImage: "url('/src/assets/bg-img-1.png')",
            backgroundSize: "cover",
            backgroundPosition: "center",
            backgroundRepeat: "no-repeat",
        }}
        >
        {/* Overlay to darken background */}
        <div className="absolute top-0 left-0 w-full h-full bg-black bg-opacity-30 z-10"></div>

        {/* Content */}
        <div className="relative z-20 h-full flex flex-col">
            {/* Header */}
            <Header />

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
                <div className="space-y-4">
                    {/* Results Section */}
                    <textarea
                    value={debiasedText}
                    readOnly
                    className="w-full h-64 p-4 bg-white bg-opacity-10 backdrop-blur-md border border-white border-opacity-20 rounded-lg shadow-lg text-white placeholder-gray-300 resize-none focus:outline-none"
                    />
                    
                    {/* copy button */}
                    <div className="flex space-x-4">
                    <button
                        className="flex-1 px-6 py-3 bg-white bg-opacity-10 backdrop-blur-md text-white text-lg font-semibold rounded-lg shadow-lg border border-white border-opacity-20 hover:bg-opacity-20 transition-all duration-300"
                        onClick={() => navigator.clipboard.writeText(debiasedText)}
                    >
                        Copy to Clipboard
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
        </div>
        </div>
    );
}
