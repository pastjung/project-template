import js from "@eslint/js";
import vue from "eslint-plugin-vue";
import globals from "globals";
import tseslint from "typescript-eslint";

export default tseslint.config(
  { ignores: ["dist", "coverage"] },
  {
    files: ["**/*.{ts,mts,tsx,vue}"],
    extends: [
      js.configs.recommended,
      ...tseslint.configs.recommended,
      ...vue.configs["flat/recommended"],
    ],
    languageOptions: {
      globals: globals.browser,
      parserOptions: {
        parser: tseslint.parser,
      },
    },
  },
);
