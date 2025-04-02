import { defineStore } from 'pinia'

interface UserState {
  userId: string | null;
  username: string | null;
  isLoggedIn: boolean;
  recommendSlides: any[];
  recommendLastLoadTime: number | null;
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    userId: localStorage.getItem('userId'),
    username: localStorage.getItem('username'),
    isLoggedIn: !!localStorage.getItem('userId'),
    recommendSlides: JSON.parse(localStorage.getItem('recommendSlides') || '[]'),
    recommendLastLoadTime: Number(localStorage.getItem('recommendLastLoadTime')) || null
  }),

  actions: {
    setUser(userId: string, username: string) {
      this.userId = userId;
      this.username = username;
      this.isLoggedIn = true;
      localStorage.setItem('userId', userId);
      localStorage.setItem('username', username);
    },

    logout() {
      this.userId = null;
      this.username = null;
      this.isLoggedIn = false;
      localStorage.removeItem('userId');
      localStorage.removeItem('username');
      localStorage.removeItem('rememberMe');
      this.clearRecommendData();
    },

    setRecommendData(slides: any[]) {
      this.recommendSlides = slides;
      this.recommendLastLoadTime = Date.now();
      localStorage.setItem('recommendSlides', JSON.stringify(slides));
      localStorage.setItem('recommendLastLoadTime', this.recommendLastLoadTime.toString());
    },

    clearRecommendData() {
      this.recommendSlides = [];
      this.recommendLastLoadTime = null;
      localStorage.removeItem('recommendSlides');
      localStorage.removeItem('recommendLastLoadTime');
    },

    needsRecommendRefresh(): boolean {
      if (!this.recommendLastLoadTime) return true;
      const TEN_MINUTES = 10 * 60 * 1000;
      return (Date.now() - this.recommendLastLoadTime) > TEN_MINUTES;
    }
  }
}) 