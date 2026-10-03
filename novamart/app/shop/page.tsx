'use client'

import { useMemo, useState } from 'react'
import { 
  ArrowRight, BookOpen, ChevronDown, Gamepad2, Heart, Headphones, 
  Laptop, Menu, Search, ShoppingCart, ShieldCheck, Shirt, Star, 
  Tag, Truck, Watch, X, Sparkles, Check, Filter, Utensils
} from 'lucide-react'
import Chatbot from '@/components/ui/chatbot'
import { SupportWidget } from '@/components/SupportWidget'

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

const heroImage = 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/WhatsApp%20Image%202026-10-03%20at%201.18.50%20PM-8aaRHgjOONomxenEzhSPiSQeNgCd4V.jpeg'

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

const categories = [
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

export default function ShopPage() {
  const [query, setQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<string>('All')
  const [cart, setCart] = useState<Product[]>([])
  const [liked, setLiked] = useState<number[]>([])
  const [menuOpen, setMenuOpen] = useState(false)
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
    <main className="min-h-screen bg-[#080b10] text-[#f5f7fb]">
      {/* Added to Cart Notification Toast */}
      {addedNotice && (
        <div className="fixed top-20 right-6 z-50 flex items-center gap-2 rounded-xl border border-emerald-500/30 bg-emerald-950/90 px-4 py-3 text-xs font-semibold text-emerald-300 shadow-2xl backdrop-blur-md animate-in fade-in slide-in-from-top-3">
          <Check className="size-4 text-emerald-400" />
          <span>Added to cart: <strong className="text-white">{addedNotice}</strong></span>
        </div>
      )}

      {/* Main Header */}
      <header className="sticky top-0 z-40 border-b border-white/10 bg-[#080b10]/95 backdrop-blur-xl">
        <div className="mx-auto flex h-[70px] max-w-[1440px] items-center gap-6 px-5 lg:px-12">
          <button className="lg:hidden" aria-label="Open menu" onClick={() => setMenuOpen(!menuOpen)}>
            <Menu />
          </button>
          
          <a href="/" className="flex items-center gap-3">
            <span className="grid size-10 rotate-[-8deg] place-items-center rounded-xl bg-[#ff2748] text-xl font-black text-[#080b10]">N</span>
            <span>
              <strong className="text-2xl tracking-[-0.06em]">Nova<span className="text-[#ff2748]">Mart</span></strong>
              <small className="block text-[10px] tracking-wide text-[#9da5b5]">Shop Smart. Live Better.</small>
            </span>
          </a>

          {/* Navigation Links with Category Selection */}
          <nav className="ml-8 hidden items-center gap-6 text-sm text-[#b7bfce] lg:flex">
            <a className="py-6 text-white hover:text-[#ff4260] transition-colors" href="/">Home</a>
            <button 
              onClick={() => { setSelectedCategory('All'); setQuery('') }}
              className={`py-6 font-medium transition-colors ${selectedCategory === 'All' ? 'border-b-2 border-[#ff2748] text-[#ff4260]' : 'hover:text-white'}`}
            >
              All Products
            </button>
            <a href="#categories" className="hover:text-white transition-colors">Categories</a>
            <a href="#deals" className="hover:text-white transition-colors">Deals</a>
            <Chatbot>
              <button className="flex items-center gap-1.5 font-semibold text-[#ff4260] hover:text-[#ff2748] transition-colors">
                <Sparkles className="size-4" /> AI Support
              </button>
            </Chatbot>
          </nav>

          {/* Search & Actions */}
          <div className="ml-auto flex items-center gap-4">
            <label className="hidden items-center gap-3 rounded-xl border border-white/10 bg-[#111720] px-4 py-2.5 md:flex focus-within:border-[#ff2748]/60 transition-colors">
              <Search className="size-4 text-[#aab3c3]" />
              <input 
                value={query} 
                onChange={(e) => setQuery(e.target.value)} 
                placeholder="Search products or categories..." 
                aria-label="Search for products" 
                className="w-56 bg-transparent text-sm outline-none placeholder:text-[#8993a5]" 
              />
              {query && (
                <button onClick={() => setQuery('')} className="text-xs text-zinc-500 hover:text-white">
                  <X className="size-3.5" />
                </button>
              )}
            </label>

            <button 
              aria-label="Wishlist" 
              className="relative hidden text-[#cbd4e5] hover:text-white transition-colors sm:block"
            >
              <Heart className="size-5" />
              {liked.length > 0 && (
                <span className="absolute -right-2 -top-2 grid size-4 place-items-center rounded-full bg-[#ff2748] text-[10px] font-bold text-white">
                  {liked.length}
                </span>
              )}
            </button>

            <button 
              aria-label="Shopping cart" 
              onClick={() => document.getElementById('products')?.scrollIntoView({ behavior: 'smooth' })} 
              className="relative text-[#cbd4e5] hover:text-white transition-colors"
            >
              <ShoppingCart className="size-5" />
              <span className="absolute -right-2 -top-2 grid size-4 place-items-center rounded-full bg-[#ff2748] text-[10px] font-bold text-white">
                {cart.length}
              </span>
            </button>

            <button aria-label="Account" className="grid size-9 place-items-center rounded-full bg-[#e7edff] font-semibold text-[#0a0e16]">
              S
            </button>
          </div>
        </div>

        {/* Mobile Navigation Drawer */}
        {menuOpen && (
          <nav className="flex flex-col gap-4 border-t border-white/10 px-5 py-5 text-sm text-[#cbd4e5] lg:hidden bg-[#0d1118]">
            <a href="/" className="hover:text-white">Home</a>
            <button 
              onClick={() => { setSelectedCategory('All'); setMenuOpen(false) }} 
              className="text-left hover:text-white"
            >
              All Products
            </button>
            <a href="#categories" onClick={() => setMenuOpen(false)} className="hover:text-white">Categories</a>
            <a href="#deals" onClick={() => setMenuOpen(false)} className="hover:text-white">Deals</a>
            <Chatbot>
              <button className="text-left font-semibold text-[#ff4260] w-full">AI Support</button>
            </Chatbot>
          </nav>
        )}
      </header>

      {/* Hero Banner */}
      <section 
        id="top" 
        className="relative min-h-[420px] overflow-hidden border-b border-white/10 bg-[#0b0e14] bg-cover bg-center" 
        style={{ backgroundImage: `linear-gradient(90deg, rgba(7,10,15,.98) 0%, rgba(7,10,15,.88) 42%, rgba(7,10,15,.25) 78%, rgba(7,10,15,.55)), url(${heroImage})` }}
      >
        <div className="mx-auto flex max-w-[1440px] items-center px-5 py-16 lg:px-12 lg:py-20">
          <div className="max-w-[640px]">
            <div className="mb-4 flex items-center gap-3 text-xs uppercase tracking-[0.3em] text-[#9ba5b7]">
              <span className="h-0.5 w-8 bg-[#ff2748]" /> NovaMart Storefront
            </div>
            <h1 className="text-4xl font-black leading-[1.02] tracking-[-.05em] sm:text-6xl">
              24 Verified Products.<br />
              <span className="text-[#ff2748]">8 Complete Categories.</span>
            </h1>
            <p className="mt-4 max-w-lg text-base leading-relaxed text-[#b8c0ce]">
              Browse authentic products with lightning-fast delivery, 7-day hassle-free returns, and agentic AI customer protection.
            </p>
            <div className="mt-7 flex flex-wrap items-center gap-3">
              <a 
                href="#products" 
                className="rounded-xl bg-[#ff2748] px-7 py-3 text-sm font-bold shadow-[0_10px_30px_rgba(255,39,72,.28)] transition-all hover:bg-[#d91936] hover:scale-105 active:scale-95"
              >
                Explore Collection <ArrowRight className="ml-2 inline size-4" />
              </a>
              <button 
                onClick={() => setSelectedCategory('All')} 
                className="rounded-xl border border-white/20 bg-white/5 px-6 py-3 text-sm font-semibold text-[#dbe2ee] transition hover:border-[#ff2748] hover:text-white"
              >
                Reset Filter ({selectedCategory})
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Categories Bar / Quick Filter */}
      <section id="categories" className="mx-auto max-w-[1440px] px-5 py-8 lg:px-12 border-b border-white/5">
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
      </section>

      {/* TRENDING PRODUCTS GRID */}
      <section id="products" className="mx-auto max-w-[1440px] px-5 py-12 lg:px-12">
        <div className="mb-8 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
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
            <span className="text-xs text-[#8993a5]">Active Category:</span>
            <span className="rounded-lg border border-white/10 bg-[#171d26] px-3 py-1 text-xs font-bold text-white">
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
      </section>

      {/* Trust & Guarantee Banners */}
      <section id="deals" className="mx-auto grid max-w-[1440px] gap-4 px-5 pb-16 lg:grid-cols-3 lg:px-12">
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
      </section>

      {/* Footer */}
      <footer id="support" className="border-t border-white/10 bg-[#06080c] px-5 py-8 text-center text-xs text-[#737d8d]">
        © 2026 NovaMart Inc. Official Hackathon Storefront • 8 Categories • 24 Verified Products.
      </footer>

      {/* Full 4-Tab AI Support Suite */}
      <SupportWidget />
    </main>
  )
}
