const API_BASE_URL = import.meta.env.VITE_API_URL;

export async function sendChatMessage(question, token, chatId = null) {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      question,
      chat_id: chatId,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to get response from server");
  }

  return response.json();
}

export async function fetchChats(token) {
  const response = await fetch(`${API_BASE_URL}/api/chats`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch chats");
  }

  return response.json();
}

export async function fetchChatById(chatId, token) {
  const response = await fetch(`${API_BASE_URL}/api/chats/${chatId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch chat");
  }

  return response.json();
}

export async function deleteChatById(chatId, token) {
  const response = await fetch(`${API_BASE_URL}/api/chats/${chatId}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to delete chat");
  }

  return response.json();
}