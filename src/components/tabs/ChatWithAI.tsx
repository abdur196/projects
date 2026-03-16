import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { SendHorizontal, Bot, User } from 'lucide-react';
import { useDiagnosis } from '@/contexts/DiagnosisContext';
import { sendChatMessage, ChatMessage } from '@/services/api';
import { useToast } from '@/hooks/use-toast';
import { format } from 'date-fns';

const ChatWithAI: React.FC = () => {
  const { sessionId, chatHistory, addChatMessage, diagnosisResults, setLoading } = useDiagnosis();
  const [message, setMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();
  
  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  // Generate initial AI message about results if we have diagnosis results
  useEffect(() => {
    if (diagnosisResults.length > 0 && chatHistory.length === 0) {
      // Find the highest probability result
      const topCondition = [...diagnosisResults].sort((a, b) => b.confidence - a.confidence)[0];
      const initialMessage: ChatMessage = {
        role: 'assistant',
        content: `Based on your X-ray and patient information, I've detected signs of ${topCondition.ailment} with ${Math.round(topCondition.confidence * 100)}% confidence. ${topCondition.description} Would you like to discuss these findings or do you have any questions?`,
        timestamp: new Date().toISOString()
      };
      addChatMessage(initialMessage);
    }
  }, [diagnosisResults, chatHistory.length, addChatMessage]);

  const handleSendMessage = async () => {
    if (!message.trim()) return;
    
    if (!sessionId) {
      toast({
        title: "No active session",
        description: "Please complete the diagnosis process first.",
        variant: "destructive",
      });
      return;
    }

    // Add user message to chat
    const userMessage: ChatMessage = {
      role: 'user',
      content: message,
      timestamp: new Date().toISOString()
    };
    addChatMessage(userMessage);
    
    // Clear input
    setMessage('');
    
    setLoading(true);
    try {
      // Send the message to the backend and get AI response
      const response = await sendChatMessage(sessionId, message);
      
      const aiMessage: ChatMessage = {
        role: 'assistant',
        content: response.message,
        timestamp: new Date().toISOString()
      };
      addChatMessage(aiMessage);
      setLoading(false);
    } catch (error) {
      toast({
        title: "Message failed to send",
        description: "There was a problem sending your message. Please try again.",
        variant: "destructive",
      });
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  const formatTime = (timestamp: string) => {
    return format(new Date(timestamp), 'HH:mm');
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Chat with Medical AI</CardTitle>
        <CardDescription>
          Discuss your diagnosis results and ask medical questions.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-[400px] overflow-y-auto border rounded-md p-4 mb-4 bg-gray-50">
          {chatHistory.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-gray-400">
              <Bot className="h-12 w-12 mb-4" />
              <p className="text-center max-w-xs">
                Complete your diagnosis first to chat with the AI about your results.
              </p>
            </div>
          ) : (
            chatHistory.map((chat, index) => (
              <div
                key={index}
                className={`mb-4 flex ${chat.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-lg p-3 ${
                    chat.role === 'user'
                      ? 'bg-medical-primary text-white'
                      : 'bg-white border border-gray-200'
                  }`}
                >
                  <div className="flex items-center gap-2 mb-1">
                    {chat.role === 'assistant' ? (
                      <Bot className="h-4 w-4" />
                    ) : (
                      <User className="h-4 w-4" />
                    )}
                    <span className="text-xs font-medium">
                      {chat.role === 'assistant' ? 'Medical AI' : 'You'}
                    </span>
                    <span className="text-xs opacity-70 ml-auto">
                      {formatTime(chat.timestamp)}
                    </span>
                  </div>
                  <p className={`text-sm ${chat.role === 'user' ? 'text-white' : 'text-gray-800'}`}>
                    {chat.content}
                  </p>
                </div>
              </div>
            ))
          )}
          <div ref={messagesEndRef} />
        </div>
      </CardContent>
      <CardFooter className="flex items-center space-x-2">
        <Input
          placeholder="Type your question here..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyPress}
          disabled={!sessionId || chatHistory.length === 0}
        />
        <Button 
          size="icon" 
          onClick={handleSendMessage}
          disabled={!sessionId || !message.trim() || chatHistory.length === 0}
        >
          <SendHorizontal className="h-4 w-4" />
        </Button>
      </CardFooter>
    </Card>
  );
};

export default ChatWithAI;
