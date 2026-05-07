import { useEffect, useState } from "react";
import { loginUser, signupUser } from "../services/authApi";

export function useAuth() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [user, setUser] = useState(
    JSON.parse(localStorage.getItem("user")) || null
  );

  function saveSession(data) {
    localStorage.setItem("token", data.token);
    localStorage.setItem("user", JSON.stringify(data.user));
    setToken(data.token);
    setUser(data.user);
  }

  async function login(email, password) {
    const data = await loginUser(email, password);
    saveSession(data);
  }

  async function signup(name, email, password) {
    const data = await signupUser(name, email, password);
    saveSession(data);
  }

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    localStorage.removeItem("active_chat_id");
    setToken(null);
    setUser(null);
  }

  return {
    token,
    user,
    isAuthenticated: Boolean(token),
    login,
    signup,
    logout,
  };
}