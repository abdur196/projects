import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import XRayUpload from './tabs/XRayUpload';
import PatientForm from './tabs/PatientForm';
import DiagnosisResults from './tabs/DiagnosisResults';
import ChatWithAI from './tabs/ChatWithAI';
import { Card } from "@/components/ui/card";
import { useDiagnosis } from '@/contexts/DiagnosisContext';

const TabContent: React.FC = () => {
  const [rightTab, setRightTab] = useState('results');
  const [leftTab, setLeftTab] = useState('upload');
  const { xrayFile, patientData } = useDiagnosis();

  const hasXray = !!xrayFile;
  const hasPatientInfo = !!(patientData && patientData.age && patientData.sex);

  // Show left box if either is missing, otherwise show right box
  if (!hasXray || !hasPatientInfo) {
    return (
      <div className="grid grid-cols-1 gap-6 h-full">
        <Card className="h-full shadow-md">
          <Tabs value={leftTab} onValueChange={setLeftTab} className="w-full h-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="upload">Upload X-ray</TabsTrigger>
              <TabsTrigger value="patient">Patient Info</TabsTrigger>
            </TabsList>
            <TabsContent value="upload" className="h-[calc(100%-45px)]">
              <XRayUpload setLeftTab={setLeftTab} />
            </TabsContent>
            <TabsContent value="patient" className="h-[calc(100%-45px)]">
              <PatientForm />
            </TabsContent>
          </Tabs>
        </Card>
      </div>
    );
  }

  // Show right box only when both are present
  return (
    <div className="grid grid-cols-1 gap-6 h-full">
      <Card className="h-full shadow-md">
        <Tabs value={rightTab} onValueChange={setRightTab} className="w-full h-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="results">Results</TabsTrigger>
            <TabsTrigger value="chat">Chat with AI</TabsTrigger>
          </TabsList>
          <TabsContent value="results" className="h-[calc(100%-45px)]">
            <DiagnosisResults setRightTab={setRightTab} />
          </TabsContent>
          <TabsContent value="chat" className="h-[calc(100%-45px)]">
            <ChatWithAI />
          </TabsContent>
        </Tabs>
      </Card>
    </div>
  );
};

export default TabContent;
