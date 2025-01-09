import globals from "globals";
import pluginJs from "@eslint/js";
import pluginVue from "eslint-plugin-vue";

/** @type {import('eslint').Linter.Config[]} */
export default [
  {
    files: ["**/*.{js,mjs,cjs,vue}"], // 文件匹配规则
    languageOptions: {
      globals: {
        ...globals.browser, // 继承浏览器的全局变量
        jquery: "readonly",  // 设置jquery为只读（或者你可以根据需要选择不同的配置）
      },
    },
    env: {
      browser: true,  // 浏览器环境
      node: true,     // Node.js 环境
      jquery: true,   // jQuery 环境
    },
  },
  pluginJs.configs.recommended, // 推荐的 JS 配置
  ...pluginVue.configs["flat/essential"], // Vue 3 的基础配置
];
