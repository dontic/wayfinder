import { create } from "zustand";

interface User {
  pk: number;
  username: string;
  email?: string;
  first_name?: string;
  last_name?: string;
}

interface UserStore {
  user: User | undefined;
  setUser: (user: User) => void;
  clearUser: () => void;
}

export const useUserStore = create<UserStore>((set) => ({
  user: undefined,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: undefined })
}));
