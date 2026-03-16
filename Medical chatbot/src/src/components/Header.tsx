import React from 'react';
import { useToast } from "@/hooks/use-toast";

const Header: React.FC = () => {
  const { toast } = useToast();
  
  const handleResetClick = () => {
    // This would be connected to our context in a real application
    toast({
      title: "Feature coming soon",
      description: "Reset functionality will be available in the next update."
    });
  };

  return (
    <header className="w-full py-4 px-6 bg-white shadow-sm border-b">
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-md bg-medical-primary flex items-center justify-center">
            <img
              src="/x-ray-svgrepo-com.svg"
              alt="X-ray icon"
              className="h-6 w-6"
            />
          </div>
          <h1 className="text-xl font-bold text-medical-dark">MedVision AI</h1>
        </div>
        <button
          onClick={handleResetClick}
          className="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-100 transition-colors"
        >
          Reset Session
        </button>
      </div>
    </header>
  );
};

export default Header;
