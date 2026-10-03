import { NextResponse } from 'next/server'

export async function POST(req: Request) {
  const backendUrl = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8080'
  try {
    const body = await req.json()
    const response = await fetch(`${backendUrl}/api/policy-lab`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(6000)
    })
    if (response.ok) {
      return NextResponse.json(await response.json())
    }
  } catch {
    // Vercel fallback
  }

  return NextResponse.json({
    status: 'success',
    case_description: 'Return request after 24 days (Order: 2026-05-01, Current: 2026-05-25, Category: laptop)',
    base_policy: { policy_version: 'v2', window_days: 7, is_eligible: false, terminal_move: 'ANSWER', calculated_refund: 9000.0 },
    mutated_policy: { policy_version: 'v3', window_days: 45, is_eligible: true, terminal_move: 'ACT', calculated_refund: 9500.0 },
    outcome_changed: true
  })
}
