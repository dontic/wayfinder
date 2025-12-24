import { defineConfig } from "orval";

export default defineConfig({
  api: {
    input: "./src/api/schemas/django/schema.yaml",
    output: {
      override: {
        header: (info: InfoObject): String[] => {
          return "// @ts-nocheck\r\n";
        },
        mutator: {
          path: "./src/api/axios.ts",
          name: "customAxiosInstance"
        }
      },
      mode: "tags-split",
      target: "src/api/django",
      prettier: true
    }
  }
});
