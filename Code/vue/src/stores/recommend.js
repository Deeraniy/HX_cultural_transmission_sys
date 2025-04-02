import { defineStore } from 'pinia'

interface RecommendState {
  slides: any[];
  lastLoadTime: number | null;
}

export const useRecommendStore = defineStore('recommend', {
  state: (): RecommendState => ({
    slides: JSON.parse(localStorage.getItem('recommendSlides') || '[]'),
    lastLoadTime: Number(localStorage.getItem('recommendLastLoadTime')) || null
  }),

  actions: {
    setData(slides: any[]) {
      this.slides = slides;
      this.lastLoadTime = Date.now();
      localStorage.setItem('recommendSlides', JSON.stringify(slides));
      localStorage.setItem('recommendLastLoadTime', this.lastLoadTime.toString());
    },

    clearData() {
      this.slides = [];
      this.lastLoadTime = null;
      localStorage.removeItem('recommendSlides');
      localStorage.removeItem('recommendLastLoadTime');
    },

    needsRefresh(): boolean {
      if (!this.lastLoadTime) return true;
      const TEN_MINUTES = 10 * 60 * 1000;
      return (Date.now() - this.lastLoadTime) > TEN_MINUTES;
    }
  }
}) 