import React from 'react';
import Link from 'next/link';
import { ArrowUpRight } from 'lucide-react';

export interface NavigationSection {
  title: string;
  href: string;
  isActive?: boolean;
}

export default function Header({ navigationData }: { navigationData: NavigationSection[] }) {
  return (
    <header className="absolute top-0 w-full z-50 pt-6">
      <div className="container mx-auto flex items-center justify-between px-4 md:px-8">
        {/* Logo */}
        <div className="flex items-center gap-1.5 cursor-pointer">
          <div className="w-7 h-7 bg-white rounded-full flex items-center justify-center relative -mr-3 z-10 mix-blend-difference" />
          <span className="text-xl font-bold tracking-tight text-white z-20 mix-blend-difference">NovaMart.</span>
        </div>
        
        {/* Navigation Pill */}
        <nav className="hidden lg:flex items-center gap-2 bg-[#1a1a1a] rounded-full px-2 py-1.5 border border-white/5 shadow-lg">
          {navigationData.map((item, index) => (
            <Link 
              key={index} 
              href={item.href}
              className={`text-sm px-4 py-1.5 rounded-full font-medium transition-colors ${item.isActive ? 'text-white bg-white/10' : 'text-zinc-400 hover:text-white'}`}
            >
              {item.title}
            </Link>
          ))}
        </nav>
        
        {/* Right Button */}
        <Link href="/shop" className="hidden sm:flex items-center gap-2 bg-white text-black rounded-full pl-4 pr-1.5 py-1.5 font-medium text-sm transition-transform hover:scale-105">
          Get Started
          <div className="bg-black text-white p-1 rounded-full">
            <ArrowUpRight className="w-4 h-4" />
          </div>
        </Link>
      </div>
    </header>
  );
}
