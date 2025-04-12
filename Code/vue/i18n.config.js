module.exports = {
  // 指定要搜索的文件
  vueFiles: './src/**/*.?(js|vue)',
  languageFiles: './src/locales/*.js',
  
  // 输出配置
  output: true,

  // 检查配置
  check: true,
  
  // 忽略某些翻译键
  exclude: [
    // 例如忽略某些动态生成的键
    /^validations\./,
    /^errors\./
  ],

  // 添加额外的翻译键（如果有些键是动态生成的）
  add: {
    // 例如：
    // 'some.dynamic.key': { zh: '动态键', en: 'Dynamic Key' }
  }
} 