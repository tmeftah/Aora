import { defineStore } from "pinia";
import { useAuthStore, apiRequest, showNotification } from "stores/auth";

const authStore = useAuthStore();

export const useTopicStore = defineStore("topics", {
  state: () => ({
    topics: [],
  }),
  getters: {},

  actions: {
    async getAllTopics() {
      try {
        const responseData = await apiRequest(
          "GET",
          "/topics",
          null,
          authStore.token
        );
        this.topics = responseData;
      } catch (error) {
        console.log("Error in Fetching topics", error.message);
        showNotification(
          "negative",
          "Topic could not be fetched",
          "check_circle"
        );
      }
    },

    async addTopic(name, details = null) {
      try {
        const formData = new URLSearchParams({
          name: name,
        });
        const responseData = await apiRequest(
          "POST",
          `/topics?name=${name}`,
          formData,
          authStore.token
        );

        this.topics.push(responseData);
        showNotification(
          "positive",
          "Topic added successfully",
          "check_circle"
        );
      } catch (error) {
        console.log("Error in adding topic", error.message);
        showNotification(
          "negative",
          "Topic could not be added",
          "check_circle"
        );
      }
    },

    async deleteTopic(topicName) {
      try {
        await apiRequest(
          "DELETE",
          `/topics/${topicName}`,
          null,
          authStore.token
        );

        this.topics = this.topics.filter((topic) => topic.name !== topicName);

        showNotification(
          "positive",
          "Topic deleted successfully",
          "check_circle"
        );
      } catch (error) {
        console.error(`API error: ${error.message}`);
        showNotification(
          "negative",
          "Topic could not be deleted",
          "report_problem"
        );
      }
    },
  },
});
