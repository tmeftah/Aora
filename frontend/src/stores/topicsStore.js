import { defineStore } from "pinia";
import { Notify } from "quasar";
import { useAuthStore, baseUrl } from "stores/auth";

const authStore = useAuthStore();

export const useTopicStore = defineStore("topics", {
  state: () => ({
    topics: [],
  }),
  getters: {},

  actions: {
    async getAllTopics() {
      try {
        const response = await fetch(`${baseUrl}/topics`, {
          method: "GET",
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${authStore.token}`,
          },
        });

        if (response.status === 401) {
          authStore.clearToken();
          window.location.href = "/login";
          return;
        }

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({})); // Parsing might fail, default to empty object
          const errorMessage =
            errorData.message || `Error: ${response.statusText}`;
          throw new Error(errorMessage);
        }

        const data = await response.json();
        this.topics = data;
      } catch (error) {
        if (error.name === "TypeError") {
          console.error("Network error: Could not reach the server");
          Notify.create({
            color: "negative",
            position: "bottom",
            message: error.message,
            icon: "report_problem",
          });
        } else {
          console.error(`API error: ${error.message}`);
          Notify.create({
            color: "negative",
            position: "bottom",
            message: error.message,
            icon: "report_problem",
          });
        }
      }
    },
    async addTopic(name, details) {
      try {
        const response = await fetch(`${baseUrl}/topics?name=${name}`, {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization: `Bearer ${authStore.token}`,
          },
        });

        if (response.status === 401) {
          authStore.clearToken();
          window.location.href = "/login";
          return;
        }

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          const errorMessage =
            errorData.message || `Error: ${response.statusText}`;
          throw new Error(errorMessage);
        }

        const data = await response.json();
        this.topics.push(data);

        Notify.create({
          color: "positive",
          position: "bottom",
          message: "Topic added successfully",
          icon: "check_circle",
        });
      } catch (error) {
        if (error.name === "TypeError") {
          console.error("Network error: Could not reach the server");
          Notify.create({
            color: "negative",
            position: "bottom",
            message: error.message,
            icon: "report_problem",
          });
        } else {
          console.error(`API error: ${error.message}`);
          Notify.create({
            color: "negative",
            position: "bottom",
            message: error.message,
            icon: "report_problem",
          });
        }
      }
    },
  },
});
