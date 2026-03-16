import React, { useState, useRef } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";
import { useDiagnosis } from '@/contexts/DiagnosisContext';
import { uploadXRayImage } from '@/services/api';
import { Image } from 'lucide-react';

const XRayUpload: React.FC<{ setLeftTab?: (tab: string) => void }> = ({ setLeftTab }) => {
  const { setXrayFile, setSessionId, setLoading, xrayFile } = useDiagnosis();
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      processFile(file);
    }
  };

  const processFile = (file: File) => {
    // Check if file is an image
    if (!file.type.startsWith('image/')) {
      toast({
        title: "Invalid file type",
        description: "Please upload only image files (.jpg, .png, etc.)",
        variant: "destructive",
      });
      return;
    }

    // Create a preview
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreviewUrl(e.target?.result as string);
    };
    reader.readAsDataURL(file);

    // Store the file
    setXrayFile(file);
  };

  const handleUpload = async () => {
    if (!xrayFile) {
      toast({
        title: "No file selected",
        description: "Please select an X-ray image to upload.",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);
    try {
      // Send the file to the backend
      const response = await uploadXRayImage(xrayFile);
      setSessionId(response.sessionId);
      toast({
        title: "X-ray processed",
        description: "Your X-ray has been processed successfully. Please proceed to enter patient information."
      });
      if (setLeftTab) setLeftTab('patient'); // Switch to Patient Info tab
    } catch (error) {
      toast({
        title: "Upload failed",
        description: "There was a problem uploading your X-ray. Please try again.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Upload X-ray Image</CardTitle>
        <CardDescription>
          Upload a chest X-ray image for AI analysis. Supported formats: JPEG, PNG.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div
          className={`border-2 border-dashed rounded-lg p-6 flex flex-col items-center justify-center h-64 cursor-pointer transition-colors ${
            isDragging ? 'border-medical-primary bg-medical-light' : 'border-gray-300 hover:border-medical-primary hover:bg-gray-50'
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={triggerFileInput}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="image/jpeg,image/png,image/jpg"
            className="hidden"
          />
          
          {previewUrl ? (
            <div className="w-full h-full flex flex-col items-center">
              <div className="relative w-48 h-48 mb-2">
                <img 
                  src={previewUrl} 
                  alt="X-ray preview" 
                  className="object-contain w-full h-full"
                />
              </div>
              <p className="text-sm text-gray-500">Click or drag to replace</p>
            </div>
          ) : (
            <>
              <Image className="w-12 h-12 text-gray-400 mb-3" />
              <p className="text-sm text-center text-gray-500 mb-2">
                Drag & drop your X-ray image here, or click to select a file.
              </p>
              <p className="text-xs text-gray-400">
                Max file size: 10MB
              </p>
            </>
          )}
        </div>
      </CardContent>
      <CardFooter className="flex justify-end">
        <Button variant="outline" className="mr-2">
          Cancel
        </Button>
        <Button onClick={handleUpload}>
          Upload and Process
        </Button>
      </CardFooter>
    </Card>
  );
};

export default XRayUpload;
