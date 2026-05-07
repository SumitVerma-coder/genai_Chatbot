function ChatHistory({ chatHistory, activeChatId, onLoadChat, onDeleteChat }) {
  return (
    <div className="mt-5 flex-1 overflow-y-auto">
      <p className="mb-2 text-xs font-semibold uppercase text-slate-500">
        Previous Chats
      </p>

      <div className="space-y-2">
        {chatHistory.length === 0 && (
          <p className="text-sm text-slate-500">No chats yet.</p>
        )}

        {chatHistory.map((chat) => (
          <div
            key={chat.id}
            className={`group flex items-center justify-between rounded-xl border px-3 py-2 ${
              activeChatId === chat.id
                ? "border-violet-300 bg-violet-50"
                : "border-slate-200 bg-white hover:bg-slate-50"
            }`}
          >
            <button
              onClick={() => onLoadChat(chat.id)}
              className="flex-1 truncate text-left text-sm font-medium text-slate-700"
            >
              {chat.title}
            </button>

            <button
              onClick={() => onDeleteChat(chat.id)}
              className="ml-2 text-shadow-xs text-slate-400 hover:text-red-500 cursor-pointer disabled:cursor-not-allowed disabled:opacity-60"
            >
              ✕
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ChatHistory;