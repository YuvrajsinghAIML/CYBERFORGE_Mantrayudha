import AgencyHeroSection from "@/components/ui/hero-01";
import Chatbot from "@/components/ui/chatbot";
import { SupportWidget } from "@/components/SupportWidget";
import { MessageCircle } from "lucide-react";

export default function Home() {
  return (
    <div className="bg-[#0a0a0a] min-h-screen text-white relative">
      <AgencyHeroSection />
      {/* Floating Comprehensive Support Widget (4 Tabs: Chat, Attack Mode, Policy Lab, Eval Scoreboard) */}
      <SupportWidget />
    </div>
  );
}
