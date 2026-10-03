import React from 'react';
import Link from 'next/link';
import { ArrowUpRight, Star } from 'lucide-react';

export interface AvatarList {
  image: string;
}

export default function HeroSection({ avatarList }: { avatarList: AvatarList[] }) {
  return (
    <section className="relative w-full min-h-[85vh] bg-[#0a0a0a] flex flex-col items-center justify-center text-center px-4 overflow-hidden pt-32 pb-16">
      {/* Subtle Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-500/10 rounded-full blur-[120px] pointer-events-none" />

      <div className="relative z-10 flex flex-col items-center max-w-4xl mx-auto">
        
        <h1 className="text-5xl sm:text-7xl md:text-8xl font-medium tracking-tight text-white leading-[1.05]">
          Building bold brands <br />
          with <span className="font-serif italic tracking-normal">thoughtful design</span>
        </h1>
        
        <p className="max-w-2xl mt-8 text-lg text-zinc-400 leading-relaxed">
          At NovaMart, we help modern businesses tackle the world's biggest challenges with tailored solutions, guiding you from strategy to success in a competitive market.
        </p>
        
        <div className="mt-12 flex flex-col sm:flex-row items-center gap-8">
          <Link href="/shop" className="flex items-center gap-2 bg-white text-black rounded-full pl-6 pr-2 py-2 font-medium text-base transition-transform hover:scale-105">
            Get Started
            <div className="bg-black text-white p-2 rounded-full">
              <ArrowUpRight className="w-5 h-5" />
            </div>
          </Link>

          <div className="flex items-center gap-4">
            <div className="flex -space-x-3">
              {avatarList.map((avatar, i) => (
                <img 
                  key={i}
                  src={avatar.image}
                  alt="Client avatar"
                  className="w-11 h-11 rounded-full border-[3px] border-[#0a0a0a] object-cover relative z-10"
                  style={{ zIndex: avatarList.length - i }}
                />
              ))}
            </div>
            <div className="flex flex-col items-start text-sm">
              <div className="flex gap-1 text-[#F97316] mb-0.5">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="w-4 h-4 fill-current" />
                ))}
              </div>
              <span className="text-zinc-400 text-xs font-medium">Trusted by 1000+ clients</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
