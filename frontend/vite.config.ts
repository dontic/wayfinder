import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import svgr from "vite-plugin-svgr";
import tailwindcss from "@tailwindcss/vite";
import path from "path";

// https://vite.dev/config/
export default defineConfig({
  plugins: [svgr(), tailwindcss(), react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src")
    }
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // Split React and React-DOM into a separate chunk
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          // Split Radix UI components into their own chunk
          'radix-ui': [
            '@radix-ui/react-avatar',
            '@radix-ui/react-checkbox',
            '@radix-ui/react-collapsible',
            '@radix-ui/react-dialog',
            '@radix-ui/react-dropdown-menu',
            '@radix-ui/react-label',
            '@radix-ui/react-popover',
            '@radix-ui/react-progress',
            '@radix-ui/react-select',
            '@radix-ui/react-separator',
            '@radix-ui/react-slot',
            '@radix-ui/react-switch',
            '@radix-ui/react-tabs',
            '@radix-ui/react-tooltip',
          ],
          // Split form libraries
          'form-vendor': ['react-hook-form', '@hookform/resolvers', 'zod'],
          // Split editor and image processing
          'editor-vendor': ['@uiw/react-md-editor', 'react-image-crop'],
          // Split other utilities
          'utils-vendor': ['axios', 'date-fns', 'lucide-react', 'sonner'],
        }
      }
    }
  }
});
