import { useNavigate } from 'react-router-dom'
import {
  Activity, Brain, Mic, FileText, Shield, Zap,
  ChevronRight, Search, MessageSquare,
} from 'lucide-react'

const features = [
  {
    icon: Brain,
    title: 'AI-Powered Reasoning',
    desc: 'LangGraph ReAct agent with multi-step reasoning across 22,000+ medical Q&A records.',
  },
  {
    icon: Search,
    title: 'Dual Knowledge Base',
    desc: 'Semantic vector search (Qdrant) combined with a medical knowledge graph (Neo4j).',
  },
  {
    icon: Mic,
    title: 'Voice Conversations',
    desc: 'Speak naturally. Whisper STT transcribes, the agent responds, Edge TTS speaks back.',
  },
  {
    icon: FileText,
    title: 'Document Analysis',
    desc: 'Upload your lab reports or medical records. The agent references them in context.',
  },
  {
    icon: Shield,
    title: 'Evidence-Based',
    desc: 'Grounded in MedlinePlus and MedQuAD — authoritative, peer-reviewed sources.',
  },
  {
    icon: Zap,
    title: 'Instant Responses',
    desc: "Powered by Groq's ultra-fast LLaMA 3.3 70B inference for real-time replies.",
  },
]

export function Landing() {
  const navigate = useNavigate()

  return (
    <>
      {/* ── Static backgrounds ── */}
      <div style={{ position: 'fixed', inset: 0, background: '#07040f', zIndex: -2 }} />
      <div
        style={{
          position: 'fixed', inset: 0, zIndex: -1,
          backgroundImage:
            'linear-gradient(rgba(139,92,246,0.05) 1px,transparent 1px),' +
            'linear-gradient(90deg,rgba(139,92,246,0.05) 1px,transparent 1px)',
          backgroundSize: '60px 60px',
        }}
      />
      {/* Corner glows — pushed to edges so they don't bleed onto text */}
      <div style={{
        position: 'fixed', top: -200, right: -200, width: 500, height: 500,
        borderRadius: '50%', background: 'rgba(109,40,217,0.18)',
        filter: 'blur(80px)', zIndex: -1, pointerEvents: 'none',
      }} />
      <div style={{
        position: 'fixed', bottom: -200, left: -200, width: 460, height: 460,
        borderRadius: '50%', background: 'rgba(88,28,135,0.16)',
        filter: 'blur(80px)', zIndex: -1, pointerEvents: 'none',
      }} />

      {/* ── Spacer: exactly navbar height ── */}
      <div style={{ height: 64 }} />

      {/* ════════ HERO ════════ */}
      <section
        style={{ padding: '80px 24px 96px' }}
        className="flex flex-col items-center text-center"
      >
        {/* Badge */}
        <div
          style={{
            display: 'inline-flex', alignItems: 'center', gap: 8,
            background: 'rgba(255,255,255,0.05)',
            border: '1px solid rgba(139,92,246,0.25)',
            borderRadius: 999, padding: '6px 16px',
            marginBottom: 28, fontSize: 13, color: '#c4b5fd',
          }}
        >
          <Activity size={13} />
          AI-Powered Medical Assistant
        </div>

        {/* Headline */}
        <h1
          style={{
            fontSize: 'clamp(42px, 6vw, 72px)',
            fontWeight: 700, lineHeight: 1.08,
            letterSpacing: '-1.5px', marginBottom: 24,
            maxWidth: 700,
          }}
        >
          <span style={{ color: '#fff' }}>Your Intelligent</span>
          <br />
          <span
            style={{
              background: 'linear-gradient(135deg,#a78bfa,#818cf8,#c084fc)',
              WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
            }}
          >
            Medical Guide
          </span>
        </h1>

        {/* Subtitle */}
        <p
          style={{
            fontSize: 17, color: 'rgba(255,255,255,0.5)',
            maxWidth: 520, lineHeight: 1.7, marginBottom: 40,
          }}
        >
          Ask medical questions in text or voice. Get evidence-based answers powered by a
          knowledge graph, semantic search, and LLaMA 3.3 — all in one seamless interface.
        </p>

        {/* CTA buttons */}
        <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap', justifyContent: 'center', marginBottom: 72 }}>
          <button
            onClick={() => navigate('/chat')}
            className="btn-primary"
            style={{
              display: 'inline-flex', alignItems: 'center', gap: 8,
              padding: '13px 28px', borderRadius: 12,
              color: '#fff', fontWeight: 600, fontSize: 15,
              boxShadow: '0 16px 40px rgba(124,58,237,0.25)',
            }}
          >
            <MessageSquare size={18} />
            Start Chatting
            <ChevronRight size={16} />
          </button>
          <button
            onClick={() => navigate('/chat')}
            style={{
              display: 'inline-flex', alignItems: 'center', gap: 8,
              padding: '13px 28px', borderRadius: 12,
              color: 'rgba(255,255,255,0.65)', fontWeight: 500, fontSize: 15,
              background: 'rgba(255,255,255,0.04)',
              border: '1px solid rgba(255,255,255,0.1)',
              transition: 'all 0.2s',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.color = '#fff'
              e.currentTarget.style.borderColor = 'rgba(139,92,246,0.4)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.color = 'rgba(255,255,255,0.65)'
              e.currentTarget.style.borderColor = 'rgba(255,255,255,0.1)'
            }}
          >
            <Mic size={18} />
            Try Voice Mode
          </button>
        </div>

        {/* Stats */}
        <div style={{ display: 'flex', gap: 64, flexWrap: 'wrap', justifyContent: 'center' }}>
          {[
            { value: '22K+', label: 'Medical Q&As indexed' },
            { value: '50+', label: 'Conditions mapped' },
            { value: 'Real-time', label: 'Voice responses' },
          ].map(({ value, label }) => (
            <div key={label} style={{ textAlign: 'center' }}>
              <div
                style={{
                  fontSize: 26, fontWeight: 700,
                  background: 'linear-gradient(135deg,#a78bfa,#818cf8,#c084fc)',
                  WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
                }}
              >
                {value}
              </div>
              <div style={{ fontSize: 13, color: 'rgba(255,255,255,0.35)', marginTop: 4 }}>
                {label}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ════════ FEATURES ════════ */}
      <section style={{ padding: '0 24px 96px' }}>
        {/* Section header */}
        <div style={{ textAlign: 'center', marginBottom: 56 }}>
          <h2
            style={{
              fontSize: 'clamp(26px,4vw,38px)', fontWeight: 700,
              color: '#fff', marginBottom: 14,
            }}
          >
            Everything you need
          </h2>
          <p style={{ fontSize: 15, color: 'rgba(255,255,255,0.4)', maxWidth: 460, margin: '0 auto' }}>
            Built on a modern AI stack designed for accuracy, speed, and safety.
          </p>
        </div>

        {/* Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
            gap: 20,
            maxWidth: 1100,
            margin: '0 auto',
          }}
        >
          {features.map(({ icon: Icon, title, desc }) => (
            <div
              key={title}
              style={{
                background: 'rgba(255,255,255,0.03)',
                border: '1px solid rgba(255,255,255,0.07)',
                borderRadius: 20, padding: '28px 24px',
                transition: 'all 0.25s',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'rgba(255,255,255,0.055)'
                e.currentTarget.style.borderColor = 'rgba(139,92,246,0.22)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'rgba(255,255,255,0.03)'
                e.currentTarget.style.borderColor = 'rgba(255,255,255,0.07)'
              }}
            >
              <div
                style={{
                  width: 44, height: 44, borderRadius: 12, marginBottom: 20,
                  background: 'linear-gradient(135deg,rgba(109,40,217,0.2),rgba(88,28,135,0.2))',
                  border: '1px solid rgba(139,92,246,0.2)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                }}
              >
                <Icon size={20} color="#a78bfa" />
              </div>
              <h3 style={{ fontWeight: 600, color: '#fff', fontSize: 15, marginBottom: 10 }}>
                {title}
              </h3>
              <p style={{ fontSize: 13.5, color: 'rgba(255,255,255,0.4)', lineHeight: 1.65 }}>
                {desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* ════════ CTA BANNER ════════ */}
      <section style={{ padding: '0 24px 112px' }}>
        <div
          style={{
            maxWidth: 860, margin: '0 auto',
            background: 'rgba(255,255,255,0.03)',
            border: '1px solid rgba(139,92,246,0.12)',
            borderRadius: 28, padding: '64px 48px',
            textAlign: 'center', position: 'relative', overflow: 'hidden',
          }}
        >
          {/* Inner corner glows clipped to card */}
          <div style={{
            position: 'absolute', top: -80, right: -80, width: 240, height: 240,
            borderRadius: '50%', background: 'rgba(109,40,217,0.18)', filter: 'blur(50px)',
            pointerEvents: 'none',
          }} />
          <div style={{
            position: 'absolute', bottom: -60, left: -60, width: 200, height: 200,
            borderRadius: '50%', background: 'rgba(88,28,135,0.14)', filter: 'blur(40px)',
            pointerEvents: 'none',
          }} />
          <Activity size={36} color="#a78bfa" style={{ margin: '0 auto 20px' }} />
          <h2 style={{ fontSize: 30, fontWeight: 700, color: '#fff', marginBottom: 12 }}>
            Ready to get started?
          </h2>
          <p style={{ fontSize: 15, color: 'rgba(255,255,255,0.45)', marginBottom: 36, maxWidth: 360, margin: '0 auto 36px' }}>
            Ask your first medical question — it's free, instant, and evidence-based.
          </p>
          <button
            onClick={() => navigate('/chat')}
            className="btn-primary"
            style={{
              display: 'inline-flex', alignItems: 'center', gap: 8,
              padding: '13px 32px', borderRadius: 12,
              color: '#fff', fontWeight: 600, fontSize: 15,
              boxShadow: '0 16px 40px rgba(124,58,237,0.25)',
            }}
          >
            Open MediGuide <ChevronRight size={16} />
          </button>
        </div>
      </section>
    </>
  )
}
