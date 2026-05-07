function InputBar({ input, setInput, onSend, isLoading }) {
  return (
    <div className="flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white p-3 shadow-sm sm:flex-row transition dark:border-slate-800 dark:bg-slate-900 ">
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") onSend();
        }}
        placeholder="Ask about GitLab's Handbook..."
        disabled={isLoading}
        className="min-h-12 flex-1 rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-violet-500 focus:bg-white focus:ring-4 focus:ring-violet-100 disabled:cursor-not-allowed disabled:opacity-60 sm:text-base dark:border-slate-800 dark:bg-slate-900 "
      />

      <button
        onClick={() => onSend()}
        disabled={isLoading}
        className="min-h-12 cursor-pointer rounded-xl bg-violet-600 px-6 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-violet-700 active:scale-95 disabled:cursor-not-allowed disabled:opacity-60 sm:text-base"
      >
        {isLoading ? "Sending..." : "Send"}
      </button>
    </div>
  );
}

export default InputBar;