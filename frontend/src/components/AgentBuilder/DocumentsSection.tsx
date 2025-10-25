import { useState, useCallback } from 'react'
import { Upload, FileText, Trash2, CheckCircle, XCircle, Loader } from 'lucide-react'
import { useDropzone } from 'react-dropzone'
import { toast } from 'sonner'

interface Document {
  id: string
  name: string
  type: string
  size: number
  status: 'uploading' | 'processing' | 'ready' | 'error'
  uploadedAt: string
}

interface DocumentsSectionProps {
  documents: Document[]
  onChange: (documents: Document[]) => void
}

export default function DocumentsSection({ documents, onChange }: DocumentsSectionProps) {
  const [uploading, setUploading] = useState(false)

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setUploading(true)
    
    try {
      // Simulate upload and processing
      const newDocuments = acceptedFiles.map(file => ({
        id: Math.random().toString(36).substr(2, 9),
        name: file.name,
        type: file.type,
        size: file.size,
        status: 'uploading' as const,
        uploadedAt: new Date().toISOString(),
      }))

      onChange([...documents, ...newDocuments])

      // Simulate processing
      setTimeout(() => {
        onChange([
          ...documents,
          ...newDocuments.map(doc => ({ ...doc, status: 'ready' as const }))
        ])
        toast.success(`${acceptedFiles.length} document(s) uploaded successfully`)
      }, 2000)

    } catch (error) {
      toast.error('Failed to upload documents')
    } finally {
      setUploading(false)
    }
  }, [documents, onChange])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'text/markdown': ['.md'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
  })

  const deleteDocument = (id: string) => {
    onChange(documents.filter(doc => doc.id !== id))
    toast.success('Document deleted')
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
  }

  const getStatusIcon = (status: Document['status']) => {
    switch (status) {
      case 'uploading':
      case 'processing':
        return <Loader className="w-5 h-5 text-blue-500 animate-spin" />
      case 'ready':
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case 'error':
        return <XCircle className="w-5 h-5 text-red-500" />
    }
  }

  return (
    <div className="space-y-6">
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Knowledge Base Documents</h2>
        <p className="text-gray-600 mb-6">
          Upload product documentation, FAQs, guides, and any other relevant documents
          that the agent should reference when answering questions.
        </p>

        {/* Upload Area */}
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
            isDragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
          }`}
        >
          <input {...getInputProps()} />
          <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
          {isDragActive ? (
            <p className="text-lg font-medium text-primary-600">Drop files here...</p>
          ) : (
            <>
              <p className="text-lg font-medium text-gray-900 mb-2">
                Drop files here or click to browse
              </p>
              <p className="text-sm text-gray-500">
                Supports PDF, TXT, MD, DOCX • Max 10MB per file
              </p>
            </>
          )}
        </div>

        {/* Document List */}
        {documents.length > 0 && (
          <div className="mt-6 space-y-3">
            <h3 className="text-sm font-medium text-gray-900">
              Uploaded Documents ({documents.length})
            </h3>
            {documents.map((doc) => (
              <div
                key={doc.id}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200"
              >
                <div className="flex items-center space-x-4 flex-1">
                  <FileText className="w-8 h-8 text-gray-400 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {doc.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {formatFileSize(doc.size)} • {doc.status}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  {getStatusIcon(doc.status)}
                  <button
                    onClick={() => deleteDocument(doc.id)}
                    className="p-2 text-gray-400 hover:text-red-600 transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Processing Info */}
      <div className="card bg-blue-50 border-blue-200">
        <h3 className="text-lg font-semibold text-blue-900 mb-2">Document Processing</h3>
        <p className="text-sm text-blue-700">
          Uploaded documents are automatically processed and indexed. The agent will use
          these documents to provide accurate, context-aware responses based on your
          product documentation.
        </p>
      </div>
    </div>
  )
}
