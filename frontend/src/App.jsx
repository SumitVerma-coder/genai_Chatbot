import { useState } from "react";
import Header from "./components/Header";
import ChatWindow from "./components/ChatWindow";
import InputBar from "./components/InputBar";
import SuggestedQuestions from "./components/SuggestedQuestions";
import Sidebar from "./components/Sidebar";
import Login from "./components/Login";
import Signup from "./components/Signup";
import { useChat } from "./hooks/useChat";
import { useAuth } from "./hooks/useAuth";
import "./index.css";

function App() {
  const [authMode, setAuthMode] = useState("login");

  const {
    token,
    user,
    isAuthenticated,
    login,
    signup,
    logout,
  } = useAuth();

  const {
    messages,
    input,
    setInput,
    isLoading,
    sendMessage,
    chatHistory,
    loadChat,
    startNewChat,
    removeChat,
    activeChatId,
  } = useChat(token);

  if (!isAuthenticated) {
    if (authMode === "login") {
      return (
        <Login
          onLogin={login}
          onSwitchToSignup={() => setAuthMode("signup")}
        />
      );
    }

    return (
      <Signup
        onSignup={signup}
        onSwitchToLogin={() => setAuthMode("login")}
      />
    );
  }

  return (
    <main className="flex h-screen overflow-hidden bg-slate-100 text-slate-900 transition dark:bg-slate-950 dark:text-slate-100">
      <Sidebar
        user={user}
        chatHistory={chatHistory}
        onNewChat={startNewChat}
        onLoadChat={loadChat}
        onDeleteChat={removeChat}
        activeChatId={activeChatId}
        onLogout={logout}
      />

      <div className="flex h-full min-w-0 flex-1 flex-col overflow-hidden px-4 py-6 sm:px-6 lg:px-8">
        <Header />

        <section className="mt-6 flex flex-1 flex-col gap-4 overflow-hidden">
          {messages.length === 0 && (
            <SuggestedQuestions onSelect={sendMessage} disabled={isLoading} />
          )}

          <ChatWindow messages={messages} isLoading={isLoading} />

          <InputBar
            input={input}
            setInput={setInput}
            onSend={sendMessage}
            isLoading={isLoading}
          />
        </section>
      </div>
    </main>
  );
}

export default App;