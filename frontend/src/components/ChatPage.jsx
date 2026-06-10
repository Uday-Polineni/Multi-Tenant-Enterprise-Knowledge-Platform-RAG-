import { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";
import { openDocumentPdf } from "../api/documents.js";
import { askQuestionStream } from "../api/query.js";
import { SUGGESTED_PROMPTS } from "../constants.js";
import {
  buildSourceMap,
  citationLinkLabel,
  citationLinkTitle,
  firstSourceIndex,
  splitAnswerParagraphs,
  stripSourceRefs,
} from "../utils/citations.js";
import { createId } from "../utils/id.js";

function AssistantAnswer({ content, citations, onCitationError }) {
  const sourceMap = buildSourceMap(citations);
  const paragraphs = splitAnswerParagraphs(content);

  async function handleCitationClick(citation) {
    if (!citation?.document_id) return;
    try {
      await openDocumentPdf({
        documentId: citation.document_id,
        page: citation.page,
      });
    } catch (err) {
      onCitationError?.(err.message);
    }
  }

  if (paragraphs.length === 0) return null;

  return (
    <div className="chat-content chat-markdown chat-answer-paragraphs">
      {paragraphs.map((paragraph, index) => {
        const sourceIndex = firstSourceIndex(paragraph);
        const citation = sourceIndex != null ? sourceMap.get(sourceIndex) : null;
        const cleanText = stripSourceRefs(paragraph);

        return (
          <p key={index} className="answer-paragraph">
            <span className="answer-paragraph-text">
              <ReactMarkdown
                rehypePlugins={[rehypeSanitize]}
                components={{ p: ({ children }) => <span>{children}</span> }}
              >
                {cleanText}
              </ReactMarkdown>
            </span>
            {citation && (
              <>
                {" "}
                <button
                  type="button"
                  className="citation-inline"
                  onClick={() => handleCitationClick(citation)}
                  title={citationLinkTitle(citation)}
                >
                  {citationLinkLabel(citation)}
                </button>
              </>
            )}
          </p>
        );
      })}
    </div>
  );
}

function ChatMessage({ message, onCitationError }) {
  const isUser = message.role === "user";

  return (
    <div className={`chat-message ${isUser ? "user" : "assistant"}`}>
      <div className="chat-avatar" aria-hidden="true">
        {isUser ? "You" : "AI"}
      </div>
      <div className="chat-message-body">
        {isUser ? (
          <p className="chat-content">{message.content}</p>
        ) : message.streaming && !message.content ? (
          <div className="typing-indicator">
            <span />
            <span />
            <span />
          </div>
        ) : (
          <AssistantAnswer
            content={message.content}
            citations={message.citations}
            onCitationError={onCitationError}
          />
        )}
      </div>
    </div>
  );
}

export default function ChatPage({
  setError,
  loading,
  setLoading,
  messages,
  setMessages,
  input,
  setInput,
}) {
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;
    textarea.style.height = "auto";
    textarea.style.height = `${Math.min(textarea.scrollHeight, 160)}px`;
  }, [input]);

  function handleInputKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend(e);
    }
  }

  async function sendQuestion(question) {
    const trimmed = question.trim();
    if (!trimmed || loading) return;

    setError("");
    setInput("");
    const userMessage = { id: createId(), role: "user", content: trimmed };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);
    const assistantId = createId();
    setMessages((prev) => [
      ...prev,
      { id: assistantId, role: "assistant", content: "", citations: [], streaming: true },
    ]);

    try {
      await askQuestionStream({
        question: trimmed,
        onToken: (text) => {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantId ? { ...m, content: m.content + text } : m
            )
          );
        },
        onDone: (payload) => {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantId
                ? {
                    ...m,
                    content: payload.answer ?? m.content,
                    citations: payload.citations ?? m.citations,
                    streaming: false,
                  }
                : m
            )
          );
        },
      });
    } catch (err) {
      const errorMessage = err.message || "Something went wrong. Please try again.";
      setError(errorMessage);
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantId ? { ...m, content: errorMessage, streaming: false } : m
        )
      );
    } finally {
      setLoading(false);
      textareaRef.current?.focus();
    }
  }

  function handleSend(e) {
    e.preventDefault();
    sendQuestion(input);
  }

  return (
    <div className="chat-view">
      <div className="chat-messages">
        {messages.length === 0 && !loading && (
          <div className="chat-welcome">
            <div className="welcome-badge">Enterprise AI</div>
            <h1>How can I help you today?</h1>
            <p>
              Ask questions about your organization&apos;s policies and documents.
              Answers are grounded in uploaded files with source citations.
            </p>
            <div className="prompt-grid">
              {SUGGESTED_PROMPTS.map((prompt) => (
                <button
                  key={prompt.title}
                  type="button"
                  className="prompt-card"
                  onClick={() => sendQuestion(prompt.text)}
                  disabled={loading}
                >
                  <span className="prompt-title">{prompt.title}</span>
                  <span className="prompt-text">{prompt.text}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <ChatMessage
            key={msg.id}
            message={msg}
            onCitationError={setError}
          />
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-composer" onSubmit={handleSend}>
        <div className="composer-inner">
          <textarea
            ref={textareaRef}
            rows={1}
            placeholder="Ask about policies, procedures, or documents…"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleInputKeyDown}
            disabled={loading}
          />
          <button
            type="submit"
            className="btn-primary composer-send"
            disabled={loading || !input.trim()}
            aria-label="Send message"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path
                d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </button>
        </div>
        <p className="composer-hint">Press Enter to send · Shift+Enter for new line</p>
      </form>
    </div>
  );
}
