import AgencyHeroSection from "@/components/ui/hero-01";
import Chatbot from "@/components/ui/chatbot";
import { MessageCircle } from "lucide-react";

export default function Home() {
  return (
    <div className="bg-[#0a0a0a] min-h-screen text-white relative">
      <AgencyHeroSection />
      <Chatbot>
        <button className="fixed bottom-6 right-6 flex items-center justify-center gap-2 bg-[#ff2748] hover:bg-[#ff4c68] text-white px-5 py-3 rounded-full font-semibold shadow-lg shadow-[#ff2748]/30 transition-all z-50">
          <MessageCircle className="w-5 h-5" /> Support
        </button>
      </Chatbot>
    </div>
  );
}
