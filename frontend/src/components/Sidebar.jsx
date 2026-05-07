import ChatHistory from "./ChatHistory";
import ProfileCard from "./ProfileCard";
import ThemeToggle from "./ThemeToggle";
function Sidebar({
  user,
  chatHistory,
  onNewChat,
  onLoadChat,
  onDeleteChat,
  activeChatId,
  onLogout,
}) {
  return (
    <aside className="flex h-screen w-80 flex-col border-r border-slate-200 bg-white p-4 transition dark:border-slate-800 dark:bg-slate-900">
      <ProfileCard user={user} />

      <button
        onClick={onNewChat}
        className="mt-4 cursor-pointer rounded-xl bg-violet-600 px-4 py-3 text-sm font-semibold text-white hover:bg-violet-700 disabled:cursor-not-allowed disabled:opacity-60"
      >
        + New Chat
      </button>

      <ChatHistory
        chatHistory={chatHistory}
        activeChatId={activeChatId}
        onLoadChat={onLoadChat}
        onDeleteChat={onDeleteChat}
      />
      <ThemeToggle />
      <button
        onClick={onLogout}
        className="mt-4 cursor-pointer rounded-xl border border-slate-300 px-4 py-3 text-sm font-semibold text-slate-900 hover:bg-red-300 hover:text-slate-900 disabled:cursor-not-allowed disabled:opacity-60 dark:text-slate-100"
      >
        Logout
      </button>
    </aside>
  );
}

export default Sidebar;