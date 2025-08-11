import React from 'react';
import Header from './Header';

interface PageLayoutProps {
  children: React.ReactNode;
  showHeader?: boolean;
  backgroundType?: 'video' | 'image' | 'dark-blue';
  className?: string;
}

export default function PageLayout({ 
  children, 
  showHeader = true, 
  backgroundType = 'dark-blue',
  className = ''
}: PageLayoutProps) {
  const getBackgroundClasses = () => {
    switch (backgroundType) {
      case 'video':
        return 'relative h-screen overflow-hidden';
      case 'image':
        return 'relative h-screen overflow-hidden bg-slate-800';
      case 'dark-blue':
        return 'relative h-screen overflow-hidden bg-slate-800';
      default:
        return 'relative h-screen overflow-hidden bg-slate-800';
    }
  };

  const getBackgroundImage = () => {
    if (backgroundType === 'image') {
      return {
        backgroundImage: "url('/src/assets/bg-img-1.png')",
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
      };
    }
    return {};
  };

  return (
    <div
      className={`${getBackgroundClasses()} ${className}`}
      style={getBackgroundImage()}
    >
      {/* Video Background (only for video type) */}
      {backgroundType === 'video' && (
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
      )}

      {/* Overlay (for video and image backgrounds) */}
      {(backgroundType === 'video' || backgroundType === 'image') && (
        <div className="absolute top-0 left-0 w-full h-full bg-black bg-opacity-30 z-10"></div>
      )}

      {/* Content Container */}
      <div className="relative z-20 h-full flex flex-col">
        {/* Header */}
        {showHeader && <Header />}
        
        {/* Main Content */}
        <div className="flex-1 flex">
          {children}
        </div>
      </div>
    </div>
  );
}
