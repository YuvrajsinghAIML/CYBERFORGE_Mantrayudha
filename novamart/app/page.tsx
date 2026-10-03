import AgencyHeroSection from "@/components/ui/hero-01";
import { ProductSection } from "@/components/ProductSection";
import { SupportWidget } from "@/components/SupportWidget";

export default function Home() {
  return (
    <div className="bg-[#0a0a0a] min-h-screen text-white relative">
      <AgencyHeroSection />
      {/* 24 Products Grid with 8-Category Filtering & Smooth Animations */}
      <ProductSection />
      {/* Floating Comprehensive Support Widget (4 Tabs: Chat, Attack Mode, Policy Lab, Eval Scoreboard) */}
      <SupportWidget />
    </div>
  );
}
