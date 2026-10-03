import AgencyHeroSection from "@/components/ui/hero-01";
import { SupportWidget } from "@/components/SupportWidget";

export default function Home() {
  return (
    <div className="bg-[#0a0a0a] min-h-screen text-white relative">
      <AgencyHeroSection />
      <SupportWidget />
    </div>
  );
}
