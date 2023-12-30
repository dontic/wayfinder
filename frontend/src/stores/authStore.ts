import { create } from "zustand";
import axios from "../api/axios";

type BasicUserInfo = {
  pk: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
};

export interface AuthState {
  basicUserInfo: BasicUserInfo | null;
  loginStatus: "idle" | "loading" | "failed";
  logoutStatus: "idle" | "loading" | "failed";
  getUserStatus: "idle" | "loading" | "failed";
  error: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  getUser: () => Promise<void>;
}

const useAuthStore = create<AuthState>()((set) => ({
  basicUserInfo: null,
  loginStatus: "idle",
  logoutStatus: "idle",
  getUserStatus: "idle",
  error: null,
  login: async (username: string, password: string) => {
    set({ loginStatus: "loading" });
    try {
      await axios.post("/auth/login/", { username, password });
      set({ loginStatus: "idle" });
    } catch (error) {
      set({ loginStatus: "failed" });
      throw error;
    }
  },
  logout: async () => {
    set({ logoutStatus: "loading" });
    try {
      await axios.post("/auth/logout/", {});
      set({ basicUserInfo: null });
      set({ logoutStatus: "idle" });
    } catch (error) {
      set({ logoutStatus: "failed" });
      throw error;
    }
  },
  getUser: async () => {
    set({ getUserStatus: "loading" });
    try {
      const response = await axios.get(`/auth/user/`);
      const resData = response.data;
      set({ basicUserInfo: resData });
      set({ getUserStatus: "idle" });
    } catch (error) {
      set({ basicUserInfo: null });
      set({ getUserStatus: "failed" });
      throw error;
    }
  }
}));

export default useAuthStore;
