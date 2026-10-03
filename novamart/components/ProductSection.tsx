'use client'

import { useMemo, useState } from 'react'
import { 
  ArrowRight, BookOpen, Check, Filter, Gamepad2, Heart, 
  Laptop, Search, ShoppingCart, Shirt, Sparkles, Star, Tag, 
  Truck, Watch, X, ShieldCheck
} from 'lucide-react'

export type Product = {
  id: number
  title: string
  name: string
  category: string
  price: number
  originalPrice: number
  oldPrice: number
  rating: number
  reviews: string
  image: string
  badge?: string
  tag?: string
}

export const products: Product[] = [
  // 1. Electronics (3 items)
  {
    id: 1,
    title: 'Samsung Galaxy S24 Ultra 5G',
    name: 'Samsung Galaxy S24 Ultra 5G',
    category: 'Electronics',
    price: 129999,
    originalPrice: 144999,
    oldPrice: 144999,
    rating: 4.8,
    reviews: '4.5K',
    image: 'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?auto=format&fit=crop&w=800&q=85',
    badge: 'Bestseller',
    tag: 'Bestseller'
  },
  {
    id: 2,
    title: 'Sony WH-1000XM5 Wireless Headphones',
    name: 'Sony WH-1000XM5 Wireless Headphones',
    category: 'Electronics',
    price: 29990,
    originalPrice: 34990,
    oldPrice: 34990,
    rating: 4.7,
    reviews: '2.8K',
    image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=85',
    badge: 'Trending',
    tag: 'Trending'
  },
  {
    id: 3,
    title: 'Apple MacBook Air M3 (16GB, 512GB)',
    name: 'Apple MacBook Air M3 (16GB, 512GB)',
    category: 'Electronics',
    price: 114900,
    originalPrice: 124900,
    oldPrice: 124900,
    rating: 4.9,
    reviews: '3.1K',
    image: 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=85',
    badge: 'New',
    tag: 'New'
  },

  // 2. Fashion (3 items)
  {
    id: 4,
    title: "Nike Air Force 1 '07 Sneakers",
    name: "Nike Air Force 1 '07 Sneakers",
    category: 'Fashion',
    price: 7999,
    originalPrice: 9995,
    oldPrice: 9995,
    rating: 4.6,
    reviews: '5.2K',
    image: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=85',
    badge: 'Bestseller',
    tag: 'Bestseller'
  },
  {
    id: 5,
    title: "Levi's 511 Slim Fit Stretch Denim",
    name: "Levi's 511 Slim Fit Stretch Denim",
    category: 'Fashion',
    price: 2799,
    originalPrice: 4599,
    oldPrice: 4599,
    rating: 4.4,
    reviews: '1.9K',
    image: 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=800&q=85',
    badge: 'Trending',
    tag: 'Trending'
  },
  {
    id: 6,
    title: 'Zara Oversized Double-Breasted Trench',
    name: 'Zara Oversized Double-Breasted Trench',
    category: 'Fashion',
    price: 5990,
    originalPrice: 8990,
    oldPrice: 8990,
    rating: 4.5,
    reviews: '890',
    image: 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=800&q=85',
    badge: 'New',
    tag: 'New'
  },

  // 3. Home & Living (3 items)
  {
    id: 7,
    title: 'Dyson V12 Detect Slim Cordless Vacuum',
    name: 'Dyson V12 Detect Slim Cordless Vacuum',
    category: 'Home & Living',
    price: 45900,
    originalPrice: 55900,
    oldPrice: 55900,
    rating: 4.7,
    reviews: '1.4K',
    image: 'https://images.unsplash.com/photo-1558317374-067fb5f30001?auto=format&fit=crop&w=800&q=85',
    badge: 'Bestseller',
    tag: 'Bestseller'
  },
  {
    id: 8,
    title: 'Philips Hue Smart Play Light Bar',
    name: 'Philips Hue Smart Play Light Bar',
    category: 'Home & Living',
    price: 4999,
    originalPrice: 7499,
    oldPrice: 7499,
    rating: 4.5,
    reviews: '2.3K',
    image: 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=800&q=85',
    badge: 'Trending',
    tag: 'Trending'
  },
  {
    id: 9,
    title: 'SleepyCat Orthopedic Memory Foam Mattress',
    name: 'SleepyCat Orthopedic Memory Foam Mattress',
    category: 'Home & Living',
    price: 12499,
    originalPrice: 18999,
    oldPrice: 18999,
    rating: 4.6,
    reviews: '3.7K',
    image: 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=800&q=85',
    badge: '',
    tag: ''
  },

  // 4. Beauty & Personal Care (3 items)
  {
    id: 10,
    title: 'Minimalist 10% Vitamin C Face Glow Serum',
    name: 'Minimalist 10% Vitamin C Face Glow Serum',
    category: 'Beauty & Personal Care',
    price: 649,
    originalPrice: 799,
    oldPrice: 799,
    rating: 4.6,
    reviews: '6.8K',
    image: 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&w=800&q=85',
    badge: 'Bestseller',
    tag: 'Bestseller'
  },
  {
    id: 11,
    title: 'Forest Essentials Soundarya Radiance Cream',
    name: 'Forest Essentials Soundarya Radiance Cream',
    category: 'Beauty & Personal Care',
    price: 3450,
    originalPrice: 4200,
    oldPrice: 4200,
    rating: 4.8,
    reviews: '1.1K',
    image: 'https://images.unsplash.com/photo-1608248597359-577885b54203?auto=format&fit=crop&w=800&q=85',
    badge: 'Trending',
    tag: 'Trending'
  },
  {
    id: 12,
    title: 'Dyson Supersonic Ionic Hair Dryer',
    name: 'Dyson Supersonic Ionic Hair Dryer',
    category: 'Beauty & Personal Care',
    price: 34900,
    originalPrice: 39900,
    oldPrice: 39900,
    rating: 4.7,
    reviews: '2.4K',
    image: 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=85',
    badge: 'New',
    tag: 'New'
  },

  // 5. Sports & Fitness (3 items)
  {
    id: 13,
    title: 'Fitbit Charge 6 Advanced Fitness Tracker',
    name: 'Fitbit Charge 6 Advanced Fitness Tracker',
    category: 'Sports & Fitness',
    price: 12999,
    originalPrice: 16999,
    oldPrice: 16999,
    rating: 4.4,
    reviews: '1.8K',
    image: 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?auto=format&fit=crop&w=800&q=85',
    badge: 'Trending',
    tag: 'Trending'
  },
  {
    id: 14,
    title: 'Domyos Hex Dumbbells (10kg Pair, Rubber)',
    name: 'Domyos Hex Dumbbells (10kg Pair, Rubber)',
    category: 'Sports & Fitness',
    price: 3299,
    originalPrice: 4999,
    oldPrice: 4999,
    rating: 4.6,
    reviews: '2.5K',
    image: 'https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?auto=format&fit=crop&w=800&q=85',
    badge: 'Bestseller',
    tag: 'Bestseller'
  },
  {
    id: 15,
    title: 'Cosco Aerobic Non-Slip Yoga Mat (8mm)',
    name: 'Cosco Aerobic Non-Slip Yoga Mat (8mm)',
    category: 'Sports & Fitness',
    price: 899,
    originalPrice: 1499,
    oldPrice: 1499,
    rating: 4.3,
    reviews: '4.1K',
    image: 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?auto=format&fit=crop&w=800&q=85',
    badge: '',
    tag: ''
  },

  // 6. Books & Stationery (3 items)
  {
    id: 16,
    title: 'Atomic Habits by James Clear (Hardcover)',
    name: 'Atomic Habits by James Clear (Hardcover)',
    category: 'Books & Stationery',
    price: 499,
    originalPrice: 799,
    oldPrice: 799,
    rating: 4.9,
    reviews: '12.4K',
    image: 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=800&q=85',
    badge: 'Bestseller',
    tag: 'Bestseller'
  },
  {
    id: 17,
    title: 'Lamy Safari Fountain Pen - Charcoal Matte',
    name: 'Lamy Safari Fountain Pen - Charcoal Matte',
    category: 'Books & Stationery',
    price: 2190,
    originalPrice: 2800,
    oldPrice: 2800,
    rating: 4.7,
    reviews: '950',
    image: 'https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?auto=format&fit=crop&w=800&q=85',
    badge: 'Trending',
    tag: 'Trending'
  },
  {
    id: 18,
    title: 'Moleskine Classic Hardcover Dotted Journal',
    name: 'Moleskine Classic Hardcover Dotted Journal',
    category: 'Books & Stationery',
    price: 1499,
    originalPrice: 2199,
    oldPrice: 2199,
    rating: 4.8,
    reviews: '1.6K',
    image: 'https://images.unsplash.com/photo-1531346878377-a5be20888e57?auto=format&fit=crop&w=800&q=85',
    badge: 'New',
    tag: 'New'
  },

  // 7. Toys & Games (3 items)
  {
    id: 19,
    title: 'LEGO Star Wars Millennium Falcon Starship',
    name: 'LEGO Star Wars Millennium Falcon Starship',
    category: 'Toys & Games',
    price: 14999,
    originalPrice: 19999,
    oldPrice: 19999,
    rating: 4.9,
    reviews: '3.2K',
    image: 'https://images.unsplash.com/photo-1585366119957-e9730b6d0f60?auto=format&fit=crop&w=800&q=85',
    badge: 'Bestseller',
    tag: 'Bestseller'
  },
  {
    id: 20,
    title: 'PlayStation 5 DualSense Wireless Controller',
    name: 'PlayStation 5 DualSense Wireless Controller',
    category: 'Toys & Games',
    price: 5490,
    originalPrice: 6390,
    oldPrice: 6390,
    rating: 4.8,
    reviews: '7.1K',
    image: 'https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?auto=format&fit=crop&w=800&q=85',
    badge: 'Trending',
    tag: 'Trending'
  },
  {
    id: 21,
    title: 'Hot Wheels 10-Car Die-Cast Collector Pack',
    name: 'Hot Wheels 10-Car Die-Cast Collector Pack',
    category: 'Toys & Games',
    price: 1199,
    originalPrice: 1699,
    oldPrice: 1699,
    rating: 4.5,
    reviews: '5.6K',
    image: 'https://images.unsplash.com/photo-1594787318286-3d835c1d207f?auto=format&fit=crop&w=800&q=85',
    badge: '',
    tag: ''
  },

  // 8. Groceries (3 items)
  {
    id: 22,
    title: 'Tata Sampann Organic Unpolished Toor Dal (1kg)',
    name: 'Tata Sampann Organic Unpolished Toor Dal (1kg)',
    category: 'Groceries',
    price: 199,
    originalPrice: 260,
    oldPrice: 260,
    rating: 4.6,
    reviews: '8.9K',
    image: 'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=800&q=85',
    badge: 'Bestseller',
    tag: 'Bestseller'
  },
  {
    id: 23,
    title: 'Blue Tokai Vienna Roast Coffee Beans (250g)',
    name: 'Blue Tokai Vienna Roast Coffee Beans (250g)',
    category: 'Groceries',
    price: 470,
    originalPrice: 550,
    oldPrice: 550,
    rating: 4.7,
    reviews: '2.2K',
    image: 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?auto=format&fit=crop&w=800&q=85',
    badge: 'Trending',
    tag: 'Trending'
  },
  {
    id: 24,
    title: 'Organic India Tulsi Green Tea (100 Infusion Bags)',
    name: 'Organic India Tulsi Green Tea (100 Infusion Bags)',
    category: 'Groceries',
    price: 320,
    originalPrice: 395,
    oldPrice: 395,
    rating: 4.5,
    reviews: '4.7K',
    image: 'https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=800&q=85',
    badge: '',
    tag: ''
  }
]

export const categories = [
  ['Electronics', Laptop], 
  ['Fashion', Shirt], 
  ['Home & Living', Watch], 
  ['Beauty & Personal Care', Tag], 
  ['Sports & Fitness', Watch], 
  ['Books & Stationery', BookOpen], 
  ['Toys & Games', Gamepad2], 
  ['Groceries', ShoppingCart],
] as const

function formatPrice(value: number) { 
  return `₹${value.toLocaleString('en-IN')}` 
}

export function ProductSection() {
  const [query, setQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<string>('All')
  const [cart, setCart] = useState<Product[]>([])
  const [liked, setLiked] = useState<number[]>([])
  const [addedNotice, setAddedNotice] = useState<string | null>(null)

  const filtered = useMemo(() => {
    return products.filter((p) => {
      const q = query.toLowerCase()
      const matchesSearch = !q || p.title.toLowerCase().includes(q) || p.category.toLowerCase().includes(q)
      const matchesCategory = selectedCategory === 'All' || p.category.toLowerCase() === selectedCategory.toLowerCase()
      return matchesSearch && matchesCategory
    })
  }, [query, selectedCategory])

  const toggleWishlist = (id: number) => {
    setLiked((prev) => prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id])
  }

  const addToCart = (product: Product) => {
    setCart((prev) => [...prev, product])
    setAddedNotice(product.title)
    setTimeout(() => setAddedNotice(null), 2500)
  }

  const getBadgeStyle = (badge?: string) => {
    if (!badge) return ''
    if (badge === 'Bestseller') return 'bg-[#ff2748] text-white shadow-sm shadow-[#ff2748]/40'
    if (badge === 'Trending') return 'bg-amber-500 text-black shadow-sm shadow-amber-500/30'
    if (badge === 'New') return 'bg-emerald-500 text-white shadow-sm shadow-emerald-500/30'
    return 'bg-blue-600 text-white'
  }

  return (
    <section className="w-full bg-[#080b10] text-[#f5f7fb] py-12 border-t border-white/5">
      {/* Added to Cart Notification Toast */}
      {addedNotice && (
        <div className="fixed top-20 right-6 z-50 flex items-center gap-2 rounded-xl border border-emerald-500/30 bg-emerald-950/90 px-4 py-3 text-xs font-semibold text-emerald-300 shadow-2xl backdrop-blur-md animate-in fade-in slide-in-from-top-3">
          <Check className="size-4 text-emerald-400" />
          <span>Added to cart: <strong className="text-white">{addedNotice}</strong></span>
        </div>
      )}

      {/* Categories Bar / Quick Filter */}
      <div id="categories" className="mx-auto max-w-[1440px] px-5 pb-8 lg:px-12 border-b border-white/5">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Filter className="size-4 text-[#ff2748]" />
            <h3 className="text-sm font-bold uppercase tracking-wider text-zinc-300">Shop by Category</h3>
          </div>
          {selectedCategory !== 'All' && (
            <button 
              onClick={() => setSelectedCategory('All')} 
              className="text-xs text-[#ff4260] hover:underline flex items-center gap-1"
            >
              <span>Clear Filter</span>
              <X className="size-3" />
            </button>
          )}
        </div>

        <div className="flex overflow-x-auto gap-3 pb-2 scrollbar-hide">
          {/* "All" button */}
          <button
            onClick={() => setSelectedCategory('All')}
            className={`flex min-w-[120px] flex-1 flex-col items-center justify-center gap-2 rounded-xl border px-3 py-3.5 text-center text-xs font-semibold transition-all duration-300 hover:scale-[1.03] ${
              selectedCategory === 'All'
                ? 'border-[#ff2748] bg-[#ff2748]/15 text-white shadow-lg shadow-[#ff2748]/20'
                : 'border-white/10 bg-[#10151c] text-[#cbd4e5] hover:border-white/25 hover:text-white'
            }`}
          >
            <Sparkles className={`size-5 ${selectedCategory === 'All' ? 'text-[#ff2748]' : 'text-[#8993a5]'}`} />
            <span>All Products ({products.length})</span>
          </button>

          {/* Individual Category Buttons */}
          {categories.map(([name, Icon]) => {
            const count = products.filter(p => p.category === name).length
            const isSelected = selectedCategory.toLowerCase() === name.toLowerCase()
            return (
              <button
                key={name}
                onClick={() => setSelectedCategory(name)}
                className={`flex min-w-[140px] flex-1 flex-col items-center justify-center gap-2 rounded-xl border px-3 py-3.5 text-center text-xs font-semibold transition-all duration-300 hover:scale-[1.03] ${
                  isSelected
                    ? 'border-[#ff2748] bg-[#ff2748]/15 text-white shadow-lg shadow-[#ff2748]/20'
                    : 'border-white/10 bg-[#10151c] text-[#cbd4e5] hover:border-white/25 hover:text-white'
                }`}
              >
                <Icon className={`size-5 ${isSelected ? 'text-[#ff2748]' : 'text-[#8993a5]'}`} />
                <span>{name} ({count})</span>
              </button>
            )
          })}
        </div>
      </div>

      {/* TRENDING PRODUCTS GRID */}
      <div id="products" className="mx-auto max-w-[1440px] px-5 pt-8 lg:px-12">
        <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[#ff2748]">
              <span>Curated Selection</span>
              <span>•</span>
              <span>Showing {filtered.length} of {products.length} Products</span>
            </div>
            <h2 className="text-3xl font-black uppercase tracking-tight text-white mt-1">
              Trending <span className="text-[#ff2748]">Products</span>
              {selectedCategory !== 'All' && <span className="text-lg font-normal text-zinc-400 capitalize"> — {selectedCategory}</span>}
            </h2>
          </div>

          <div className="flex items-center gap-3">
            <label className="flex items-center gap-2 rounded-xl border border-white/10 bg-[#111720] px-3.5 py-2 text-xs text-[#aab3c3] focus-within:border-[#ff2748]/60 transition-colors">
              <Search className="size-3.5" />
              <input 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search items..."
                className="w-40 bg-transparent text-xs text-white outline-none placeholder:text-[#8993a5]"
              />
            </label>
            <span className="rounded-lg border border-white/10 bg-[#171d26] px-3 py-2 text-xs font-bold text-white">
              {selectedCategory}
            </span>
          </div>
        </div>

        {/* Empty Search/Filter State */}
        {filtered.length === 0 ? (
          <div className="rounded-2xl border border-white/10 bg-[#10151c] p-12 text-center">
            <div className="mx-auto grid size-12 place-items-center rounded-full bg-white/5 text-[#8993a5] mb-3">
              <Search className="size-6" />
            </div>
            <h3 className="text-lg font-bold text-white">No products found</h3>
            <p className="text-xs text-[#8993a5] mt-1">No items matched your search query &quot;{query}&quot; in {selectedCategory}.</p>
            <button 
              onClick={() => { setSelectedCategory('All'); setQuery('') }}
              className="mt-4 rounded-xl bg-[#ff2748] px-5 py-2 text-xs font-bold text-white hover:bg-[#d91936] transition"
            >
              Reset Filters
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6">
            {filtered.map((p) => {
              const isLiked = liked.includes(p.id)
              return (
                <article 
                  key={p.id} 
                  className="group relative flex flex-col rounded-2xl border border-white/10 bg-[#10151c] p-3 transition-all duration-300 ease-out hover:-translate-y-1.5 hover:scale-[1.02] hover:shadow-[0_12px_32px_rgba(0,0,0,0.55)] hover:border-[#ff2748]/60"
                >
                  {/* Image Container with Badges */}
                  <div className="relative aspect-square w-full overflow-hidden rounded-xl bg-[#171d26]">
                    <img 
                      src={p.image} 
                      alt={p.title} 
                      loading="lazy"
                      className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105" 
                    />
                    
                    {/* Badge */}
                    {p.badge && (
                      <span className={`absolute left-2 top-2 rounded-full px-2.5 py-0.5 text-[9px] font-black uppercase tracking-wider ${getBadgeStyle(p.badge)}`}>
                        {p.badge}
                      </span>
                    )}

                    {/* Interactive Wishlist Heart with Pop Animation */}
                    <button 
                      aria-label={`Wishlist ${p.title}`} 
                      onClick={() => toggleWishlist(p.id)} 
                      className="absolute right-2 top-2 grid size-8 place-items-center rounded-full bg-black/50 backdrop-blur-sm text-white transition-transform duration-200 active:scale-125 hover:scale-110 hover:bg-black/80"
                    >
                      <Heart 
                        className={`size-4 transition-colors duration-200 ${isLiked ? 'text-[#ff2748] fill-[#ff2748]' : 'text-white fill-none'}`} 
                      />
                    </button>
                  </div>

                  {/* Product Details */}
                  <div className="mt-3 flex flex-1 flex-col">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-[#8d98aa]">
                      {p.category}
                    </span>
                    <h3 className="mt-1 line-clamp-2 text-xs font-bold leading-snug text-white group-hover:text-[#ff4260] transition-colors" title={p.title}>
                      {p.title}
                    </h3>

                    {/* Rating & Reviews */}
                    <div className="mt-2 flex items-center gap-1.5 text-xs">
                      <div className="flex items-center gap-0.5 rounded bg-amber-500/10 px-1.5 py-0.5 text-[10px] font-bold text-amber-300">
                        <Star className="size-3 fill-amber-400 text-amber-400" />
                        <span>{p.rating}</span>
                      </div>
                      <span className="text-[10px] text-[#737d8d]">({p.reviews})</span>
                    </div>

                    {/* Pricing */}
                    <div className="mt-2 flex items-baseline gap-2">
                      <strong className="text-sm font-black text-white">{formatPrice(p.price)}</strong>
                      {p.originalPrice > p.price && (
                        <del className="text-[11px] text-[#6b7688] font-medium">{formatPrice(p.originalPrice)}</del>
                      )}
                    </div>

                    {/* Add to Cart Button with Hover and Active Animation */}
                    <button 
                      onClick={() => addToCart(p)} 
                      className="mt-3 w-full rounded-xl bg-[#ff2748] py-2 text-xs font-bold text-white transition-all duration-200 hover:bg-[#d91936] active:scale-95 shadow-md shadow-[#ff2748]/25 flex items-center justify-center gap-1.5"
                    >
                      <ShoppingCart className="size-3.5" />
                      <span>Add to Cart</span>
                    </button>
                  </div>
                </article>
              )
            })}
          </div>
        )}
      </div>

      {/* Trust Badges */}
      <div id="deals" className="mx-auto grid max-w-[1440px] gap-4 px-5 pt-16 lg:grid-cols-3 lg:px-12">
        {[
          ['Great Deals, Every Day', 'Upto 50% off on top brands', Tag],
          ['Secure Payments', '100% safe UPI, Cards & NetBanking', ShieldCheck],
          ['Easy Returns', '7-day return policy backed by AI Support', Truck]
        ].map(([title, text, Icon]) => (
          <div key={title as string} className="flex items-center gap-4 rounded-2xl border border-white/10 bg-[#10151c] p-5 transition-transform hover:-translate-y-1">
            <span className="grid size-12 place-items-center rounded-xl bg-[#ff2748]/10 text-[#ff2748]">
              <Icon className="size-6" />
            </span>
            <div>
              <strong className="block text-sm text-white">{title as string}</strong>
              <small className="text-xs text-[#8993a5]">{text as string}</small>
            </div>
            <ArrowRight className="ml-auto size-4 text-[#8993a5]" />
          </div>
        ))}
      </div>
    </section>
  )
}
