import { defineStore } from 'pinia'

export const useFontStore = defineStore('font', {
  state: () => ({
    isStyled: true, // true 为风格字体，false 为系统字体
  }),
  
  actions: {
    setFontStyle(styled: boolean) {
      this.isStyled = styled
    }
  }
}) 