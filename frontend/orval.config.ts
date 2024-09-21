import { defineConfig } from "orval";

export default defineConfig({
  api: {
    input: "../backend/schema.yaml",
    output: {
      override: {
        mutator: {
          path: "./src/api/axios.ts",
          name: "customAxiosInstance"
        }
      },
      mode: "tags-split",
      target: "src/api/endpoints",
      prettier: true
    }
  }
});
