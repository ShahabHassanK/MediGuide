import { useState, useRef } from 'react'
import { Upload, FileText, CheckCircle, XCircle, Loader2, X } from 'lucide-react'
import { uploadDocument } from '../lib/api'

interface UploadedFile {
  name: string
  chunks: number
  status: 'success' | 'error'
  error?: string
}

interface DocumentUploadProps {
  sessionId: string
}

export function DocumentUpload({ sessionId }: DocumentUploadProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [files, setFiles] = useState<UploadedFile[]>([])
  const inputRef = useRef<HTMLInputElement>(null)

  async function handleFile(file: File) {
    if (!(file.name.endsWith('.txt') || file.name.endsWith('.pdf'))) {
      setFiles((prev) => [
        ...prev,
        { name: file.name, chunks: 0, status: 'error', error: 'Only .txt and .pdf supported' },
      ])
      return
    }
    setUploading(true)
    try {
      const res = await uploadDocument(sessionId, file)
      setFiles((prev) => [
        ...prev,
        { name: res.filename, chunks: res.chunks_stored, status: 'success' },
      ])
    } catch (err: unknown) {
      setFiles((prev) => [
        ...prev,
        {
          name: file.name,
          chunks: 0,
          status: 'error',
          error: err instanceof Error ? err.message : 'Upload failed',
        },
      ])
    } finally {
      setUploading(false)
    }
  }

  function onDrop(e: React.DragEvent) {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer.files[0]
    if (file) handleFile(file)
  }

  function onChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (file) handleFile(file)
    e.target.value = ''
  }

  return (
    <div className="space-y-2.5">
      <p className="text-xs text-white/35 uppercase tracking-widest font-semibold">
        Documents
      </p>

      {/* Drop zone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true) }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={onDrop}
        onClick={() => !uploading && inputRef.current?.click()}
        className={`
          relative rounded-xl border border-dashed py-6 px-4 text-center cursor-pointer transition-all duration-200
          ${isDragging
            ? 'border-violet-400/60 bg-violet-500/10'
            : 'border-white/[0.08] hover:border-violet-500/35 hover:bg-white/[0.03]'}
        `}
      >
        {uploading ? (
          <div className="flex flex-col items-center gap-2">
            <Loader2 size={22} className="text-violet-400 animate-spin" />
            <span className="text-sm text-white/45">Uploading…</span>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-2">
            <Upload size={22} className="text-white/25" />
            <span className="text-sm text-white/40">Drop a .txt or .pdf file here</span>
            <span className="text-xs text-violet-400/65 font-medium">or click to browse</span>
          </div>
        )}
        <input
          ref={inputRef}
          type="file"
          accept=".txt,.pdf"
          className="hidden"
          onChange={onChange}
        />
      </div>

      {/* Uploaded files list */}
      {files.length > 0 && (
        <div className="space-y-2">
          {files.map((f, i) => (
            <div
              key={i}
              className={`flex items-start gap-2.5 rounded-xl px-3.5 py-3 text-sm ${
                f.status === 'success'
                  ? 'bg-green-500/8 border border-green-500/20'
                  : 'bg-red-500/8 border border-red-500/20'
              }`}
            >
              <FileText size={14} className={f.status === 'success' ? 'text-green-400 mt-0.5 shrink-0' : 'text-red-400 mt-0.5 shrink-0'} />
              <div className="flex-1 min-w-0">
                <p className="text-white/65 truncate text-sm">{f.name}</p>
                {f.status === 'success' ? (
                  <p className="text-green-400/65 text-xs mt-0.5">{f.chunks} chunks indexed</p>
                ) : (
                  <p className="text-red-400/65 text-xs mt-0.5">{f.error}</p>
                )}
              </div>
              {f.status === 'success' ? (
                <CheckCircle size={14} className="text-green-400 mt-0.5 shrink-0" />
              ) : (
                <XCircle size={14} className="text-red-400 mt-0.5 shrink-0" />
              )}
              <button
                onClick={(e) => { e.stopPropagation(); setFiles((prev) => prev.filter((_, j) => j !== i)) }}
                className="text-white/20 hover:text-white/50 transition-colors mt-0.5"
              >
                <X size={13} />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
