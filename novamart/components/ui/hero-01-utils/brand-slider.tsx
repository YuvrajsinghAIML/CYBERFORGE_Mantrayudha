import React from 'react';

export interface BrandList {
  image: string;
  lightimg: string;
  name: string;
}

export default function BrandSlider({ brandList }: { brandList: BrandList[] }) {
  const repeatedBrands = [...brandList, ...brandList, ...brandList];

  return (
    <section className="w-full bg-[#0a0a0a] pb-20 overflow-hidden">
      <div className="container mx-auto px-4 mb-10 text-center">
        <div className="flex items-center justify-center gap-4 text-xs font-medium text-zinc-500">
          <div className="h-[1px] w-12 bg-zinc-800" />
          Loved by 1000+ big and small brands around the worlds
          <div className="h-[1px] w-12 bg-zinc-800" />
        </div>
      </div>
      
      <div 
        className="relative flex w-full overflow-hidden"
        style={{
          maskImage: 'linear-gradient(to right, transparent, black 15%, black 85%, transparent)',
          WebkitMaskImage: 'linear-gradient(to right, transparent, black 15%, black 85%, transparent)'
        }}
      >
        <div className="flex w-max animate-marquee space-x-20 items-center">
          {repeatedBrands.map((brand, i) => (
            <div 
              key={i} 
              className="flex-shrink-0 h-8 relative flex items-center justify-center opacity-50 hover:opacity-100 transition-opacity duration-300"
            >
              <img 
                src={brand.lightimg || brand.image} 
                alt={brand.name} 
                className="max-h-full max-w-full object-contain filter invert grayscale"
              />
            </div>
          ))}
        </div>
      </div>
      
      <style dangerouslySetInnerHTML={{__html: `
        @keyframes marquee {
          0% { transform: translateX(0%); }
          100% { transform: translateX(-33.33%); }
        }
        .animate-marquee {
          animation: marquee 30s linear infinite;
        }
      `}} />
    </section>
  );
}
