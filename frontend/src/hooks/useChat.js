import { useEffect, useState } from "react";
import {
  sendChatMessage,
  fetchChats,
  fetchChatById,
  deleteChatById,
} from "../services/api";

export function useChat(token) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [chatId, setChatId] = useState(localStorage.getItem("active_chat_id"));
  const [chatHistory, setChatHistory] = useState([]);

  function clearChatState() {
    setMessages([]);
    setInput("");
    setIsLoading(false);
    setChatId(null);
    setChatHistory([]);
    localStorage.removeItem("active_chat_id");
  }

  async function loadChatHistory() {
    if (!token) return;

    try {
      const chats = await fetchChats(token);
      setChatHistory(chats);
    } catch (error) {
      console.error("Failed to load chat history:", error);
    }
  }

  async function loadChat(selectedChatId) {
    if (!selectedChatId || !token) return;

    try {
      const chat = await fetchChatById(selectedChatId, token);

      if (chat.error) {
        clearChatState();
        return;
      }

      setChatId(chat.id);
      localStorage.setItem("active_chat_id", chat.id);

      const formattedMessages = chat.messages.map((msg, index) => ({
        id: `${chat.id}-${index}`,
        role: msg.role,
        content: msg.content,
        sources: msg.sources || [],
      }));

      setMessages(formattedMessages);
    } catch (error) {
      console.error("Failed to load chat:", error);
      clearChatState();
    }
  }

  useEffect(() => {
    if (!token){
      clearChatState();
      return;
    }

    async function initializeChats() {
      await loadChatHistory();

      const savedChatId = localStorage.getItem("active_chat_id");

      if (savedChatId) {
        await loadChat(savedChatId);
      }
    }

    initializeChats();
  }, [token]);

  async function sendMessage(questionText = input) {
    const question = questionText.trim();
    if (!question || !token) return;

    const userMessage = {
      id: Date.now(),
      role: "user",
      content: question,
      sources: [],
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const data = await sendChatMessage(question, token, chatId);

      if (data.chat_id) {
        setChatId(data.chat_id);
        localStorage.setItem("active_chat_id", data.chat_id);
      }

      const botMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content: data.answer,
        sources: data.sources || [],
      };

      setMessages((prev) => [...prev, botMessage]);

      await loadChatHistory();
    } catch (error) {
      console.error("Failed to send message:", error);

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          role: "assistant",
          content: "Something went wrong. Please try again.",
          sources: [],
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  function startNewChat() {
    setChatId(null);
    setMessages([]);
    setInput("");
    localStorage.removeItem("active_chat_id");
  }

  async function removeChat(selectedChatId) {
    try {
      await deleteChatById(selectedChatId, token);

      if (selectedChatId === chatId) {
        startNewChat();
      }

      await loadChatHistory();
    } catch (error) {
      console.error("Failed to delete chat:", error);
    }
  }

  return {
    messages,
    input,
    setInput,
    isLoading,
    sendMessage,
    chatHistory,
    loadChat,
    startNewChat,
    removeChat,
    activeChatId: chatId,
  };
}