import { defineStore } from "pinia";
import { Notify } from "quasar";
import { useAuthStore, apiRequest, showNotification } from "stores/auth";

const authStore = useAuthStore();

export const useUserStore = defineStore("user", {
  state: () => ({
    users: [],
    currentUser: "",
  }),
  getters: {},

  actions: {
    async getCurrentUser() {
      try {
        const responseData = await apiRequest(
          "GET",
          `/users/me`,
          null,
          authStore.token
        );
        this.currentUser = responseData;
      } catch (error) {
        console.log("Error in Fetching current user", error.message);
        showNotification(
          "negative",
          "Current User cannot be fecthed",
          "check_circle"
        );
      }
    },
  },
});
