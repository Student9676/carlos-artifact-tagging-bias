import PageLayout from '../components/PageLayout';

import Header from "../components/Header";

export default function Home() {
  return (
    <div className="relative h-screen overflow-hidden">
      {/* Background Video */}
      <video 
        className="absolute top-0 left-0 w-full h-full object-cover z-0"
        autoPlay 
        muted 
        loop 
        playsInline
      >
        <source src="/src/assets/bg-loop.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      {/* Overlay to darken video */}
      <div className="absolute top-0 left-0 w-full h-full bg-black bg-opacity-30 z-10"></div>

      {/* Content Container */}
      <div className="relative z-20 h-full flex flex-col">
        {/* This is the header */}
        <Header />

        {/* Main content */}
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-white text-5xl">Welcome to the Carlos Museum's Lexicon Cleaner</h1>
            <p className="text-white text-lg mt-4">A one-stop solution for rewriting museum language for clarity and inclusivity.</p>
            <button
              className="mt-8 px-6 py-3 bg-white bg-opacity-10 backdrop-blur-md text-white text-lg font-semibold rounded-full shadow-lg border border-white border-opacity-20 hover:bg-opacity-20 transition-all duration-300"
              onClick={() => window.location.href = "/debiaser"}
            >
              Get Started
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}