import { defineConfig } from "orval";

export default defineConfig({
  api: {
    input: "../backend/schema.yaml",
    output: {
      mode: "tags-split",
      target: "src/api/endpoints",
      prettier: true
    }
  }
});
