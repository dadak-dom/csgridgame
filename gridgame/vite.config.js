import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vite.dev/config/
export default defineConfig({
  server: {
    proxy: {
      "/board/today": {
        target: "http://192.168.0.248:8000",
        changeOrigin: true,
      },
    },
  },
  plugins: [vue()],
});
