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
