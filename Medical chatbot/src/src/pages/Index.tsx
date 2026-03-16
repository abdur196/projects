
import React from 'react';
import Header from '@/components/Header';
import TabContent from '@/components/TabContent';
import { DiagnosisProvider } from '@/contexts/DiagnosisContext';

const Index = () => {
  return (
    <DiagnosisProvider>
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <Header />
        <main className="flex-1 container mx-auto p-6">
          <div className="h-[calc(100vh-200px)]">
            <TabContent />
          </div>
        </main>
      </div>
    </DiagnosisProvider>
  );
};

export default Index;
