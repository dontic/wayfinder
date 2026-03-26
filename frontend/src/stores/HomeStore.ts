import { create } from "zustand";
import { persist } from "zustand/middleware";

export type Period = "past-year" | "ytd" | string;

interface HomeStore {
  selectedPeriod: Period;
  setSelectedPeriod: (period: Period) => void;
}

export const useHomeStore = create<HomeStore>()(
  persist(
    (set) => ({
      selectedPeriod: "past-year",
      setSelectedPeriod: (period) => set({ selectedPeriod: period })
    }),
    {
      name: "home-store"
    }
  )
);
