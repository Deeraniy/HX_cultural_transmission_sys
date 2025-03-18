import { defineStore } from 'pinia'

interface UserState {
  userId: string | null;
  username: string | null;
  isLoggedIn: boolean;
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    userId: localStorage.getItem('userId'),
    username: localStorage.getItem('username'),
    isLoggedIn: !!localStorage.getItem('userId')
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
    }
  }
}) 