import { useState } from "react";
import ReactMarkdown from "react-markdown";
import SourceCard from "./SourceCard";

function MessageBubble({ message }) {
  const [showSources, setShowSources] = useState(false);

  const isUser = message.role === "user";
  const hasSources = message.sources && message.sources.length > 0;

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[85%] rounded-2xl px-4 py-3 shadow-sm sm:max-w-[75%] ${
          isUser
            ? "bg-violet-600 text-white"
            : "border border-slate-200 bg-slate-50 text-slate-900 dark:border-slate-900 dark:bg-slate-800 dark:text-white"
        }`}
      >
        <p
          className={`mb-1 text-xs font-semibold uppercase tracking-wide ${
            isUser ? "text-violet-100" : "text-slate-500"
          }`}
        >
          {isUser ? "You" : "Bot"}
        </p>
        <div className="text-sm leading-6 sm:text-base">
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>
        {!isUser && (
          <>
            {hasSources && (
              <div className="mt-3 border-t border-slate-200 pt-3">
                <button
                  onClick={() => setShowSources((prev) => !prev)}
                  className="text-sm cursor-pointer font-semibold text-violet-600 transition hover:text-violet-700 hover:underline disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {showSources ? "Hide sources" : "View sources"}
                </button>

                {showSources && (
                  <div className="mt-3 grid gap-2">
                    {message.sources.map((source, index) => (
                      <SourceCard key={index} source={source} />
                    ))}
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default MessageBubble;