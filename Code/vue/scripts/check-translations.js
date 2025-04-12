import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 读取语言文件
function readLocaleFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const match = content.match(/export\s+default\s+({[\s\S]*})/);
  if (!match) {
    throw new Error(`Invalid locale file format: ${filePath}`);
  }
  return eval('(' + match[1] + ')');
}

// 写入语言文件
function writeLocaleFile(filePath, data) {
  const content = `export default ${JSON.stringify(data, null, 2)};\n`;
  fs.writeFileSync(filePath, content, 'utf8');
}

// 递归获取所有 Vue 文件
function getAllVueFiles(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  
  list.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat && stat.isDirectory()) {
      results = results.concat(getAllVueFiles(filePath));
    } else if (path.extname(file) === '.vue') {
      results.push(filePath);
    }
  });
  
  return results;
}

// 从 Vue 文件中提取可能需要翻译的文本
function extractTranslatableText(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const texts = new Set();
  
  // 匹配模板中的中文文本
  const templateMatches = content.match(/>([^<>]*[\u4e00-\u9fa5]+[^<>]*)</g) || [];
  templateMatches.forEach(match => {
    const text = match.slice(1, -1).trim();
    if (text) texts.add(text);
  });
  
  // 匹配属性中的中文文本
  const attrMatches = content.match(/(?:title|placeholder|label)="([^"]*[\u4e00-\u9fa5]+[^"]*)"/g) || [];
  attrMatches.forEach(match => {
    const text = match.match(/"([^"]*)"/)[1].trim();
    if (text) texts.add(text);
  });
  
  return Array.from(texts);
}

// 生成翻译键
function generateTranslationKey(text) {
  // 简单的将中文转换为拼音或英文的逻辑
  // 这里仅作示例，您可以根据需要修改
  const key = text
    .replace(/[^\u4e00-\u9fa5]/g, '') // 只保留中文字符
    .slice(0, 5) // 取前5个字符
    .split('')
    .join('_');
  return key;
}

// 递归合并对象
function deepMerge(target, source) {
  for (const key in source) {
    if (source.hasOwnProperty(key)) {
      if (typeof source[key] === 'object' && source[key] !== null) {
        target[key] = target[key] || {};
        deepMerge(target[key], source[key]);
      } else {
        target[key] = source[key];
      }
    }
  }
  return target;
}

// 主函数
async function main() {
  // 读取现有翻译
  const zhPath = path.join(__dirname, '../src/locales/zh.js');
  const enPath = path.join(__dirname, '../src/locales/en.js');
  const zh = readLocaleFile(zhPath);
  const en = readLocaleFile(enPath);

  // 获取所有 Vue 文件
  const vueFiles = getAllVueFiles(path.join(__dirname, '../src'));
  const newTranslations = {};

  // 收集所有需要翻译的文本
  vueFiles.forEach(file => {
    const texts = extractTranslatableText(file);
    const componentName = path.basename(file, '.vue').toLowerCase();
    
    texts.forEach(text => {
      if (!Object.values(zh).flat().includes(text)) {
        const key = generateTranslationKey(text);
        if (!newTranslations[componentName]) {
          newTranslations[componentName] = {};
        }
        newTranslations[componentName][key] = text;
      }
    });
  });

  // 合并新旧翻译
  const updatedZh = deepMerge({ ...zh }, newTranslations);
  const updatedEn = deepMerge({ ...en }, newTranslations); // 英文暂时使用相同的值，需要后续人工翻译

  // 写入更新后的翻译文件
  writeLocaleFile(zhPath, updatedZh);
  writeLocaleFile(enPath, updatedEn);

  console.log('翻译文件已更新！');
  console.log(`新增翻译条目数：${Object.keys(newTranslations).reduce((acc, key) => acc + Object.keys(newTranslations[key]).length, 0)}`);
}

main().catch(console.error); 