import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { useToast } from "@/hooks/use-toast";
import { useDiagnosis } from '@/contexts/DiagnosisContext';
import { Check } from 'lucide-react';
import { submitPatientData } from '@/services/api';

interface PatientFormData {
  sex: string;
  age: number;
  frontalLateral: string;
  apPa: string;
}

const PatientForm: React.FC = () => {
  const { sessionId, setPatientData, setDiagnosisResults, setLoading, setVisualization } = useDiagnosis();
  const { toast } = useToast();
  
  const [formData, setFormData] = useState<PatientFormData>({
    sex: '',
    age: 0,
    frontalLateral: 'Frontal',
    apPa: 'PA'
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSexChange = (value: string) => {
    setFormData(prev => ({ ...prev, sex: value }));
  };

  const handleFrontalLateralChange = (value: string) => {
    setFormData(prev => ({ ...prev, frontalLateral: value }));
  };

  const handleApPaChange = (value: string) => {
    setFormData(prev => ({ ...prev, apPa: value }));
  };

  const handleSubmit = async () => {
    if (!sessionId) {
      toast({
        title: "No session found",
        description: "Please upload an X-ray image first.",
        variant: "destructive",
      });
      return;
    }

    if (!formData.sex || !formData.age) {
      toast({
        title: "Missing information",
        description: "Please provide sex and age information.",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);
    try {
      // Prepare the data to send to the backend
      const patientData = {
        sessionId,
        age: formData.age,
        sex: formData.sex,
        frontalLateral: formData.frontalLateral,
        apPa: formData.apPa
      };
      
      // Send data to backend
      const response = await submitPatientData(patientData);
      
      // Update context with the response data
      setPatientData(patientData);
      setDiagnosisResults(response.results);
      setVisualization(response.visualization);
      
      toast({
        title: "Patient data submitted",
        description: "Your information has been processed. View the results tab for diagnosis.",
      });
    } catch (error) {
      toast({
        title: "Submission failed",
        description: "There was a problem submitting your information. Please try again.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Patient Information</CardTitle>
        <CardDescription>
          Please enter required information to help with the diagnosis.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="grid grid-cols-1 gap-4">
          <div className="space-y-2">
            <Label htmlFor="age">Age</Label>
            <Input
              id="age"
              name="age"
              type="number"
              placeholder="Enter patient age"
              value={formData.age || ''}
              onChange={handleChange}
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="sex">Sex</Label>
            <RadioGroup
              name="sex"
              value={formData.sex}
              onValueChange={handleSexChange}
              className="flex space-x-4"
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="male" id="male" />
                <Label htmlFor="male">Male</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="female" id="female" />
                <Label htmlFor="female">Female</Label>
              </div>
            </RadioGroup>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="frontalLateral">X-ray View</Label>
            <RadioGroup
              name="frontalLateral"
              value={formData.frontalLateral}
              onValueChange={handleFrontalLateralChange}
              className="flex space-x-4"
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="Frontal" id="frontal" />
                <Label htmlFor="frontal">Frontal</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="Lateral" id="lateral" />
                <Label htmlFor="lateral">Lateral</Label>
              </div>
            </RadioGroup>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="apPa">X-ray Technique</Label>
            <RadioGroup
              name="apPa"
              value={formData.apPa}
              onValueChange={handleApPaChange}
              className="flex space-x-4"
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="PA" id="pa" />
                <Label htmlFor="pa">PA (Posterior-Anterior)</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="AP" id="ap" />
                <Label htmlFor="ap">AP (Anterior-Posterior)</Label>
              </div>
            </RadioGroup>
          </div>
        </div>
      </CardContent>
      <CardFooter className="flex justify-end">
        <Button type="button" onClick={handleSubmit}>
          <Check className="mr-2 h-4 w-4" />
          Submit Patient Information
        </Button>
      </CardFooter>
    </Card>
  );
};

export default PatientForm;
