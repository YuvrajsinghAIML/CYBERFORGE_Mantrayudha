"use client"

import React, { useEffect, useRef, useState } from 'react';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, Bot, User, Loader2 } from 'lucide-react';
import { useChat } from '@ai-sdk/react';

export default function Chatbot({ children }: { children: React.ReactNode }) {
  const [messages, setMessages] = useState([
    { id: 'welcome', role: 'assistant', content: 'Hi there! Welcome to NovaMart Support. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    
    const userMessage = { id: Date.now().toString(), role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Mock a response after a short delay
    setTimeout(() => {
      setMessages(prev => [
        ...prev, 
        { id: Date.now().toString(), role: 'assistant', content: "Thanks for reaching out! We are currently experiencing high volume, but a support agent will be with you shortly. In the meantime, you can track your orders or check our FAQ." }
      ]);
      setIsLoading(false);
    }, 1500);
  };

  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <Sheet>
      <SheetTrigger asChild>
        {children}
      </SheetTrigger>
      <SheetContent className="w-full sm:max-w-md flex flex-col h-full bg-[#10151c] border-white/10 text-[#f5f7fb]">
        <SheetHeader className="border-b border-white/10 pb-4 text-left">
          <SheetTitle className="text-white flex items-center gap-2 text-xl font-bold">
            <div className="w-8 h-8 rounded-full bg-[#ff2748] flex items-center justify-center">
              <Bot className="w-5 h-5 text-[#080b10]" />
            </div>
            NovaMart Support
          </SheetTitle>
        </SheetHeader>
        
        <div ref={scrollRef} className="flex-1 overflow-y-auto py-4 space-y-5 px-1 scrollbar-hide">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              {msg.role !== 'user' && (
                <div className="w-8 h-8 rounded-full bg-[#ff2748]/20 flex items-center justify-center flex-shrink-0 mt-1">
                  <Bot className="w-4 h-4 text-[#ff2748]" />
                </div>
              )}
              
              <div className={`px-4 py-3 rounded-2xl max-w-[80%] text-sm leading-relaxed ${
                msg.role === 'user' 
                  ? 'bg-[#ff2748] text-white rounded-br-none' 
                  : 'bg-white/5 text-[#dbe2ee] border border-white/10 rounded-bl-none'
              }`}>
                {msg.content}
              </div>

              {msg.role === 'user' && (
                <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center flex-shrink-0 mt-1">
                  <User className="w-4 h-4 text-white" />
                </div>
              )}
            </div>
          ))}
          {isLoading && messages[messages.length - 1]?.role === 'user' && (
            <div className="flex gap-3 justify-start">
              <div className="w-8 h-8 rounded-full bg-[#ff2748]/20 flex items-center justify-center flex-shrink-0 mt-1">
                <Bot className="w-4 h-4 text-[#ff2748]" />
              </div>
              <div className="px-4 py-3 rounded-2xl max-w-[80%] text-sm leading-relaxed bg-white/5 text-[#dbe2ee] border border-white/10 rounded-bl-none flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin text-[#ff2748]" /> Thinking...
              </div>
            </div>
          )}
        </div>

        <div className="border-t border-white/10 pt-4 pb-2 mt-auto">
          <form 
            onSubmit={onSubmit} 
            className="flex items-center gap-2 relative"
          >
            <Input 
              value={input}
              onChange={handleInputChange}
              placeholder="Type your message..." 
              className="bg-[#171d26] border-white/10 text-white placeholder:text-[#8993a5] focus-visible:ring-[#ff2748] pr-12 rounded-xl h-12"
              disabled={isLoading}
            />
            <Button type="submit" size="icon" disabled={isLoading || !(input || '').trim()} className="absolute right-1.5 top-1.5 h-9 w-9 bg-[#ff2748] hover:bg-[#ff4c68] text-white rounded-lg disabled:opacity-50">
              <Send className="w-4 h-4 ml-0.5" />
            </Button>
          </form>
        </div>
      </SheetContent>
    </Sheet>
  );
}
