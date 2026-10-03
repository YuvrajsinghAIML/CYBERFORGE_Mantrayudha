import { NextResponse } from 'next/server'

export async function GET() {
  const backendUrl = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8080'
  try {
    const response = await fetch(`${backendUrl}/api/customers`, { signal: AbortSignal.timeout(4000) })
    if (response.ok) {
      return NextResponse.json(await response.json())
    }
  } catch {
    // Vercel fallback
  }

  return NextResponse.json({
    customers: [
      { customer_id: 'CUST-00001', name: 'Aarav Sharma', email: 'aarav.sharma@example.com', status: 'active', loyalty_tier: 'standard', sample_orders: ['ORD-000606', 'ORD-001042'] },
      { customer_id: 'CUST-00002', name: 'Diya Patel', email: 'diya.patel@example.com', status: 'active', loyalty_tier: 'gold', sample_orders: ['ORD-000607', 'ORD-001550'] },
      { customer_id: 'CUST-00003', name: 'Kabir Mehta', email: 'kabir.mehta@example.com', status: 'suspended', loyalty_tier: 'standard', sample_orders: ['ORD-000608'] },
      { customer_id: 'CUST-00004', name: 'Ananya Verma', email: 'ananya.verma@example.com', status: 'active', loyalty_tier: 'platinum', sample_orders: ['ORD-000609'] }
    ]
  })
}
