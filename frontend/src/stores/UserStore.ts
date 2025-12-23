import { create } from "zustand";

import type { UserDetails } from "@/api/django/api.schemas";

interface UserStore {
  user: (UserDetails & { full_name?: string }) | undefined;
  setUser: (user: UserDetails & { full_name?: string }) => void;

  clearUser: () => void;
}

export const useUserStore = create<UserStore>((set, get) => ({
  user: undefined,
  setUser: (user) =>
    set({
      user: {
        ...user,
        full_name:
          user.full_name ??
          ([user.first_name, user.last_name].filter(Boolean).join(" ").trim() ||
            undefined)
      }
    }),
  clearUser: () => set({ user: undefined })
}));
