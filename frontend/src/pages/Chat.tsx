import {
  useState, useRef, useEffect, useCallback,
  type KeyboardEvent, type FormEvent,
} from 'react'
import { Link } from 'react-router-dom'
import {
  Send, Activity, Trash2, Copy, Check,
  Mic, MicOff, Loader2, ChevronRight,
  Hash, Info, Home, AlignJustify,
} from 'lucide-react'
import { useSession } from '../hooks/useSession'
import { useChat } from '../hooks/useChat'
import { useVoice } from '../hooks/useVoice'
import { ChatMessage, TypingIndicator } from '../components/ChatMessage'
import { DocumentUpload } from '../components/DocumentUpload'

const SUGGESTED = [
  'What are symptoms of type 2 diabetes?',
  'How is hypertension treated?',
  'What does a high CRP level indicate?',
  'Viral vs bacterial infections — what\'s the difference?',
]

// Sidebar section label
function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <p style={{
      fontSize: 10, fontWeight: 700, letterSpacing: '0.14em',
      textTransform: 'uppercase', color: 'rgba(255,255,255,0.3)',
      marginBottom: 10,
    }}>
      {children}
    </p>
  )
}

// Small icon button in top bar
function IconBtn({
  onClick, title, children,
}: { onClick?: () => void; title: string; children: React.ReactNode }) {
  return (
    <button
      onClick={onClick}
      title={title}
      style={{
        width: 36, height: 36, borderRadius: 10, display: 'flex',
        alignItems: 'center', justifyContent: 'center', cursor: 'pointer',
        background: 'rgba(255,255,255,0.04)',
        border: '1px solid rgba(255,255,255,0.08)',
        color: 'rgba(255,255,255,0.4)', transition: 'all 0.15s',
      }}
      onMouseEnter={e => {
        e.currentTarget.style.background = 'rgba(255,255,255,0.08)'
        e.currentTarget.style.color = 'rgba(255,255,255,0.75)'
      }}
      onMouseLeave={e => {
        e.currentTarget.style.background = 'rgba(255,255,255,0.04)'
        e.currentTarget.style.color = 'rgba(255,255,255,0.4)'
      }}
    >
      {children}
    </button>
  )
}

export function Chat() {
  const { sessionId } = useSession()
  const {
    messages, isLoading, send,
    injectUserMessage, injectAssistantMessage, clearMessages,
  } = useChat(sessionId)
  const [input, setInput] = useState('')
  const [copied, setCopied] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  const handleSend = useCallback((e?: FormEvent) => {
    e?.preventDefault()
    const text = input.trim()
    if (!text || isLoading) return
    setInput('')
    send(text)
  }, [input, isLoading, send])

  function handleKey(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend() }
  }

  function copyLast() {
    const last = [...messages].reverse().find(m => m.role === 'assistant')
    if (last) {
      navigator.clipboard.writeText(last.content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  const { voiceState, toggleRecording } = useVoice({
    sessionId,
    onTranscript: t => injectUserMessage(t),
    onResponse: r => injectAssistantMessage(r),
    onError: msg => console.error('Voice error:', msg),
  })

  const isRecording = voiceState === 'recording'
  const isProcessing = voiceState === 'processing'
  const shortSession = sessionId.slice(-8)

  // ─── Sidebar width ───
  const SW = 300

  return (
    <div style={{
      display: 'flex', height: '100vh', overflow: 'hidden',
      background: '#07040f',
    }}>
      {/* Subtle mesh bg */}
      <div style={{
        position: 'fixed', inset: 0, zIndex: 0, pointerEvents: 'none',
        backgroundImage:
          'linear-gradient(rgba(139,92,246,0.04) 1px,transparent 1px),' +
          'linear-gradient(90deg,rgba(139,92,246,0.04) 1px,transparent 1px)',
        backgroundSize: '60px 60px',
      }} />

      {/* ══════════════ SIDEBAR ══════════════ */}
      <aside style={{
        flexShrink: 0, width: sidebarOpen ? SW : 0, overflow: 'hidden',
        transition: 'width 0.28s cubic-bezier(0.4,0,0.2,1)',
        position: 'relative', zIndex: 10,
        background: '#0b0719',
        borderRight: '1px solid rgba(255,255,255,0.07)',
        display: 'flex', flexDirection: 'column',
      }}>
        {/* Sidebar inner — fixed width so content doesn't squish during animation */}
        <div style={{
          width: SW, height: '100%', display: 'flex', flexDirection: 'column',
          overflow: 'hidden',
        }}>
          {/* ── Logo header — same height as top bar ── */}
          <div style={{
            height: 64, flexShrink: 0, display: 'flex', alignItems: 'center',
            padding: '0 20px',
            borderBottom: '1px solid rgba(255,255,255,0.07)',
          }}>
            <Link to="/" style={{
              display: 'flex', alignItems: 'center', gap: 10,
              textDecoration: 'none',
            }}>
              <div style={{
                width: 36, height: 36, borderRadius: 10, flexShrink: 0,
                background: 'linear-gradient(135deg,#7c3aed,#6d28d9)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                boxShadow: '0 4px 16px rgba(124,58,237,0.3)',
              }}>
                <Activity size={17} color="#fff" />
              </div>
              <div>
                <div style={{ fontWeight: 700, fontSize: 15, color: '#fff', lineHeight: 1.2 }}>
                  Medi<span style={{
                    background: 'linear-gradient(135deg,#a78bfa,#818cf8)',
                    WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
                  }}>Guide</span>
                </div>
                <div style={{
                  fontSize: 11, color: 'rgba(255,255,255,0.35)',
                  display: 'flex', alignItems: 'center', gap: 4, marginTop: 1,
                }}>
                  <Home size={9} /> Return home
                </div>
              </div>
            </Link>
          </div>

          {/* ── Scrollable content ── */}
          <div style={{
            flex: 1, overflowY: 'auto', padding: '24px 18px',
            display: 'flex', flexDirection: 'column', gap: 28,
          }}>

            {/* SESSION */}
            <div>
              <SectionLabel>Session</SectionLabel>
              <div style={{
                background: 'rgba(255,255,255,0.04)',
                border: '1px solid rgba(255,255,255,0.08)',
                borderRadius: 12, padding: '10px 14px',
                display: 'flex', alignItems: 'center', gap: 10,
              }}>
                <Hash size={14} color="#a78bfa" style={{ flexShrink: 0 }} />
                <span style={{
                  fontSize: 13, color: 'rgba(255,255,255,0.5)',
                  fontFamily: 'monospace', flex: 1, overflow: 'hidden',
                  textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                }}>
                  {shortSession}
                </span>
                <span style={{
                  fontSize: 11, fontWeight: 600,
                  background: 'rgba(34,197,94,0.12)',
                  color: '#4ade80',
                  border: '1px solid rgba(34,197,94,0.22)',
                  borderRadius: 999, padding: '2px 8px', flexShrink: 0,
                }}>
                  active
                </span>
              </div>
            </div>

            {/* SUGGESTIONS */}
            <div>
              <SectionLabel>Suggestions</SectionLabel>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                {SUGGESTED.map(q => (
                  <button
                    key={q}
                    onClick={() => { setInput(q); setTimeout(() => inputRef.current?.focus(), 50) }}
                    style={{
                      width: '100%', textAlign: 'left', cursor: 'pointer',
                      padding: '11px 14px', borderRadius: 12,
                      background: 'rgba(255,255,255,0.03)',
                      border: '1px solid rgba(255,255,255,0.07)',
                      display: 'flex', alignItems: 'flex-start', gap: 10,
                      transition: 'all 0.15s',
                    }}
                    onMouseEnter={e => {
                      e.currentTarget.style.background = 'rgba(139,92,246,0.08)'
                      e.currentTarget.style.borderColor = 'rgba(139,92,246,0.22)'
                    }}
                    onMouseLeave={e => {
                      e.currentTarget.style.background = 'rgba(255,255,255,0.03)'
                      e.currentTarget.style.borderColor = 'rgba(255,255,255,0.07)'
                    }}
                  >
                    <ChevronRight size={14} color="#a78bfa" style={{ flexShrink: 0, marginTop: 2 }} />
                    <span style={{
                      fontSize: 13, color: 'rgba(255,255,255,0.6)',
                      lineHeight: 1.45,
                    }}>
                      {q}
                    </span>
                  </button>
                ))}
              </div>
            </div>

            {/* DOCUMENTS */}
            <DocumentUpload sessionId={sessionId} />

            {/* DISCLAIMER — pushed to bottom */}
            <div style={{ marginTop: 'auto' }}>
              <div style={{
                background: 'rgba(251,191,36,0.05)',
                border: '1px solid rgba(251,191,36,0.12)',
                borderRadius: 12, padding: '12px 14px',
                display: 'flex', alignItems: 'flex-start', gap: 10,
              }}>
                <Info size={13} color="rgba(251,191,36,0.55)" style={{ flexShrink: 0, marginTop: 1 }} />
                <p style={{
                  fontSize: 12, color: 'rgba(255,255,255,0.35)',
                  lineHeight: 1.6, margin: 0,
                }}>
                  MediGuide provides general health information only. Always consult a qualified
                  healthcare professional for medical advice.
                </p>
              </div>
            </div>
          </div>
        </div>
      </aside>

      {/* ══════════════ MAIN AREA ══════════════ */}
      <div style={{
        flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column',
        position: 'relative', zIndex: 5,
      }}>

        {/* ── Top bar ── */}
        <header style={{
          height: 64, flexShrink: 0, display: 'flex',
          alignItems: 'center', justifyContent: 'space-between',
          padding: '0 24px',
          background: 'rgba(11,7,25,0.85)',
          backdropFilter: 'blur(16px)',
          borderBottom: '1px solid rgba(255,255,255,0.07)',
        }}>
          {/* Left: hamburger + title */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <button
              onClick={() => setSidebarOpen(v => !v)}
              title="Toggle sidebar"
              style={{
                width: 36, height: 36, borderRadius: 10, display: 'flex',
                alignItems: 'center', justifyContent: 'center', cursor: 'pointer',
                background: 'rgba(255,255,255,0.04)',
                border: '1px solid rgba(255,255,255,0.08)',
                color: 'rgba(255,255,255,0.5)', transition: 'all 0.15s',
              }}
              onMouseEnter={e => {
                e.currentTarget.style.background = 'rgba(255,255,255,0.08)'
                e.currentTarget.style.color = 'rgba(255,255,255,0.8)'
              }}
              onMouseLeave={e => {
                e.currentTarget.style.background = 'rgba(255,255,255,0.04)'
                e.currentTarget.style.color = 'rgba(255,255,255,0.5)'
              }}
            >
              <AlignJustify size={16} />
            </button>
            <div>
              <div style={{ fontSize: 14, fontWeight: 600, color: '#fff' }}>
                Medical Assistant
              </div>
              <div style={{ fontSize: 11, color: 'rgba(255,255,255,0.3)', marginTop: 1 }}>
                Powered by LLaMA 3.3 · Qdrant · Neo4j
              </div>
            </div>
          </div>

          {/* Right: action buttons */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <IconBtn onClick={copyLast} title="Copy last response">
              {copied
                ? <Check size={15} color="#4ade80" />
                : <Copy size={15} />}
            </IconBtn>
            <IconBtn onClick={clearMessages} title="Clear conversation">
              <Trash2 size={15} />
            </IconBtn>
          </div>
        </header>

        {/* ── Messages ── */}
        <div style={{
          flex: 1, overflowY: 'auto', padding: '32px 28px 16px',
        }}>
          <div style={{ maxWidth: 860, margin: '0 auto', display: 'flex', flexDirection: 'column', gap: 22 }}>
            {messages.map(msg => (
              <ChatMessage key={msg.id} message={msg} />
            ))}
            {isLoading && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* ── Input area ── */}
        <div style={{
          flexShrink: 0, padding: '16px 28px 20px',
          background: 'rgba(11,7,25,0.7)',
          backdropFilter: 'blur(16px)',
          borderTop: '1px solid rgba(255,255,255,0.07)',
        }}>
          <div style={{ maxWidth: 860, margin: '0 auto' }}>

            {/* Voice recording banner */}
            {(isRecording || isProcessing) && (
              <div className="fade-up" style={{
                marginBottom: 12, display: 'flex', alignItems: 'center', gap: 10,
                padding: '10px 16px', borderRadius: 12, fontSize: 13,
                ...(isRecording
                  ? { background: 'rgba(239,68,68,0.08)', border: '1px solid rgba(239,68,68,0.2)', color: '#fca5a5' }
                  : { background: 'rgba(139,92,246,0.08)', border: '1px solid rgba(139,92,246,0.2)', color: '#c4b5fd' }),
              }}>
                {isRecording
                  ? <><span className="recording-pulse" style={{ width: 8, height: 8, borderRadius: '50%', background: '#ef4444', display: 'block' }} /> Recording — click mic to stop</>
                  : <><Loader2 size={14} className="animate-spin" /> Processing voice response…</>}
              </div>
            )}

            <form onSubmit={handleSend} style={{ display: 'flex', alignItems: 'flex-end', gap: 10 }}>
              {/* Textarea */}
              <div style={{
                flex: 1, display: 'flex', alignItems: 'flex-end',
                background: 'rgba(255,255,255,0.05)',
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: 16, padding: '14px 18px',
                transition: 'border-color 0.2s',
              }}
                onFocusCapture={e => (e.currentTarget.style.borderColor = 'rgba(139,92,246,0.45)')}
                onBlurCapture={e => (e.currentTarget.style.borderColor = 'rgba(255,255,255,0.1)')}
              >
                <textarea
                  ref={inputRef}
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  onKeyDown={handleKey}
                  placeholder="Ask a medical question… (Enter to send)"
                  rows={1}
                  disabled={isLoading || isRecording || isProcessing}
                  style={{
                    flex: 1, background: 'transparent', border: 'none', outline: 'none',
                    resize: 'none', fontSize: 14, color: '#fff', lineHeight: 1.6,
                    maxHeight: 140, fontFamily: 'inherit',
                    opacity: (isLoading || isRecording || isProcessing) ? 0.5 : 1,
                  } as React.CSSProperties}
                />
              </div>

              {/* Voice button */}
              <button
                type="button"
                onClick={toggleRecording}
                disabled={isLoading}
                title={isRecording ? 'Stop recording' : 'Voice conversation'}
                style={{
                  width: 48, height: 48, borderRadius: 14, flexShrink: 0, cursor: 'pointer',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  transition: 'all 0.2s',
                  ...(isRecording
                    ? { background: 'rgba(239,68,68,0.12)', border: '1px solid rgba(239,68,68,0.35)' }
                    : { background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)' }),
                  opacity: (isLoading || isProcessing) ? 0.45 : 1,
                }}
              >
                {isProcessing
                  ? <Loader2 size={19} color="#a78bfa" className="animate-spin" />
                  : isRecording
                    ? <MicOff size={19} color="#f87171" />
                    : <Mic size={19} color="rgba(255,255,255,0.5)" />}
              </button>

              {/* Send button */}
              <button
                type="submit"
                disabled={!input.trim() || isLoading || isRecording || isProcessing}
                style={{
                  width: 48, height: 48, borderRadius: 14, flexShrink: 0, cursor: 'pointer',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  background: 'linear-gradient(135deg,#7c3aed,#6d28d9)',
                  border: '1px solid rgba(167,139,250,0.25)',
                  boxShadow: '0 4px 20px rgba(124,58,237,0.3)',
                  transition: 'all 0.2s',
                  opacity: (!input.trim() || isLoading || isRecording || isProcessing) ? 0.35 : 1,
                }}
              >
                {isLoading
                  ? <Loader2 size={18} color="#fff" className="animate-spin" />
                  : <Send size={17} color="#fff" />}
              </button>
            </form>

            <p style={{
              textAlign: 'center', fontSize: 11,
              color: 'rgba(255,255,255,0.15)', marginTop: 10,
            }}>
              General health information only · Not a substitute for professional medical advice
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
