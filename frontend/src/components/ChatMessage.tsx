import { Activity, User, AlertTriangle } from 'lucide-react'
import type { Message } from '../hooks/useChat'

function formatTime(d: Date) {
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// Clean, reliable line-by-line markdown → HTML
function renderMarkdown(raw: string): JSX.Element {
  const lines = raw.split('\n')
  const elements: JSX.Element[] = []
  let i = 0

  while (i < lines.length) {
    const line = lines[i]

    // Headings
    if (line.startsWith('### ')) {
      elements.push(<h3 key={i} style={{ color: '#ddd6fe', fontWeight: 600, fontSize: 14, marginTop: 12, marginBottom: 4 }}>{inlineFormat(line.slice(4))}</h3>)
    } else if (line.startsWith('## ')) {
      elements.push(<h3 key={i} style={{ color: '#ddd6fe', fontWeight: 600, fontSize: 15, marginTop: 14, marginBottom: 4 }}>{inlineFormat(line.slice(3))}</h3>)
    } else if (line.startsWith('# ')) {
      elements.push(<h3 key={i} style={{ color: '#ede9fe', fontWeight: 700, fontSize: 16, marginTop: 16, marginBottom: 6 }}>{inlineFormat(line.slice(2))}</h3>)
    }
    // Blockquote
    else if (line.startsWith('> ')) {
      elements.push(
        <blockquote key={i} style={{
          borderLeft: '3px solid rgba(139,92,246,0.5)',
          paddingLeft: 12, margin: '8px 0',
          color: 'rgba(196,181,253,0.9)', fontStyle: 'italic', fontSize: 13.5,
        }}>
          {inlineFormat(line.slice(2))}
        </blockquote>
      )
    }
    // Bullet list — collect consecutive bullets
    else if (line.match(/^[-*] /)) {
      const items: string[] = []
      while (i < lines.length && lines[i].match(/^[-*] /)) {
        items.push(lines[i].slice(2))
        i++
      }
      elements.push(
        <ul key={`ul-${i}`} style={{ paddingLeft: 18, margin: '6px 0' }}>
          {items.map((item, j) => (
            <li key={j} style={{ marginBottom: 3, fontSize: 13.5, color: 'rgba(255,255,255,0.8)' }}>
              {inlineFormat(item)}
            </li>
          ))}
        </ul>
      )
      continue
    }
    // Numbered list
    else if (line.match(/^\d+\. /)) {
      const items: string[] = []
      while (i < lines.length && lines[i].match(/^\d+\. /)) {
        items.push(lines[i].replace(/^\d+\. /, ''))
        i++
      }
      elements.push(
        <ol key={`ol-${i}`} style={{ paddingLeft: 20, margin: '6px 0' }}>
          {items.map((item, j) => (
            <li key={j} style={{ marginBottom: 3, fontSize: 13.5, color: 'rgba(255,255,255,0.8)' }}>
              {inlineFormat(item)}
            </li>
          ))}
        </ol>
      )
      continue
    }
    // Blank line
    else if (line.trim() === '') {
      elements.push(<div key={i} style={{ height: 6 }} />)
    }
    // Regular paragraph
    else {
      elements.push(
        <p key={i} style={{ margin: '2px 0', fontSize: 13.5, lineHeight: 1.7, color: 'rgba(255,255,255,0.85)' }}>
          {inlineFormat(line)}
        </p>
      )
    }
    i++
  }

  return <>{elements}</>
}

// Inline formatting: **bold**, *italic*, `code`
function inlineFormat(text: string): JSX.Element {
  const parts: (string | JSX.Element)[] = []
  const regex = /(\*\*(.+?)\*\*)|(\*(.+?)\*)|(`(.+?)`)/g
  let last = 0
  let m: RegExpExecArray | null

  while ((m = regex.exec(text)) !== null) {
    if (m.index > last) parts.push(text.slice(last, m.index))
    if (m[1]) parts.push(<strong key={m.index} style={{ color: '#e9d5ff', fontWeight: 600 }}>{m[2]}</strong>)
    else if (m[3]) parts.push(<em key={m.index} style={{ color: '#c4b5fd' }}>{m[4]}</em>)
    else if (m[5]) parts.push(<code key={m.index} style={{
      background: 'rgba(139,92,246,0.18)', border: '1px solid rgba(139,92,246,0.25)',
      borderRadius: 4, padding: '1px 5px', fontSize: '0.82em', color: '#e9d5ff',
    }}>{m[6]}</code>)
    last = m.index + m[0].length
  }
  if (last < text.length) parts.push(text.slice(last))
  return <>{parts}</>
}

export function ChatMessage({ message }: { message: Message }) {
  const isUser = message.role === 'user'
  const isSystem = message.role === 'system'

  if (isSystem) {
    return (
      <div className="fade-up" style={{
        display: 'flex', alignItems: 'center', gap: 8,
        padding: '10px 16px', borderRadius: 12,
        background: 'rgba(239,68,68,0.08)',
        border: '1px solid rgba(239,68,68,0.2)',
        color: '#fca5a5', fontSize: 13,
        maxWidth: 480, margin: '0 auto',
      }}>
        <AlertTriangle size={14} style={{ flexShrink: 0 }} />
        {message.content}
      </div>
    )
  }

  return (
    <div className="fade-up" style={{
      display: 'flex',
      flexDirection: isUser ? 'row-reverse' : 'row',
      alignItems: 'flex-start',
      gap: 12,
    }}>
      {/* Avatar */}
      <div style={{
        flexShrink: 0, width: 34, height: 34, borderRadius: 10,
        background: isUser
          ? 'linear-gradient(135deg,#4f46e5,#3b82f6)'
          : 'linear-gradient(135deg,#7c3aed,#6d28d9)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        boxShadow: isUser
          ? '0 4px 12px rgba(79,70,229,0.3)'
          : '0 4px 12px rgba(124,58,237,0.3)',
        marginTop: 2,
      }}>
        {isUser
          ? <User size={15} color="#fff" />
          : <Activity size={15} color="#fff" />}
      </div>

      {/* Bubble + timestamp */}
      <div style={{
        display: 'flex', flexDirection: 'column',
        alignItems: isUser ? 'flex-end' : 'flex-start',
        gap: 5, maxWidth: '76%',
      }}>
        <div style={{
          padding: isUser ? '10px 16px' : '14px 18px',
          borderRadius: isUser ? '18px 4px 18px 18px' : '4px 18px 18px 18px',
          background: isUser
            ? 'linear-gradient(135deg,#7c3aed,#6d28d9)'
            : 'rgba(255,255,255,0.05)',
          border: isUser ? 'none' : '1px solid rgba(255,255,255,0.08)',
          color: '#fff',
          minWidth: isUser ? 0 : undefined,
          boxShadow: isUser ? '0 4px 20px rgba(124,58,237,0.25)' : 'none',
        }}>
          {isUser
            ? <span style={{ fontSize: 14, lineHeight: 1.6 }}>{message.content}</span>
            : renderMarkdown(message.content)
          }
        </div>
        <span style={{ fontSize: 11, color: 'rgba(255,255,255,0.22)', padding: '0 4px' }}>
          {formatTime(message.timestamp)}
        </span>
      </div>
    </div>
  )
}

export function TypingIndicator() {
  return (
    <div className="fade-up" style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
      <div style={{
        flexShrink: 0, width: 34, height: 34, borderRadius: 10,
        background: 'linear-gradient(135deg,#7c3aed,#6d28d9)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        boxShadow: '0 4px 12px rgba(124,58,237,0.3)', marginTop: 2,
      }}>
        <Activity size={15} color="#fff" />
      </div>
      <div style={{
        padding: '14px 20px',
        borderRadius: '4px 18px 18px 18px',
        background: 'rgba(255,255,255,0.05)',
        border: '1px solid rgba(255,255,255,0.08)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
          <span className="dot-1" style={{ width: 7, height: 7, borderRadius: '50%', background: '#a78bfa', display: 'block' }} />
          <span className="dot-2" style={{ width: 7, height: 7, borderRadius: '50%', background: '#a78bfa', display: 'block' }} />
          <span className="dot-3" style={{ width: 7, height: 7, borderRadius: '50%', background: '#a78bfa', display: 'block' }} />
        </div>
      </div>
    </div>
  )
}
