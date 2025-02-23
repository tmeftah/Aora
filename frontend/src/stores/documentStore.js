import { defineStore } from "pinia";
import { Notify } from "quasar";
import { useAuthStore } from "stores/auth";

const authStore = useAuthStore();

const baseUrl = `${process.env.API}`;

export const useDocumentStore = defineStore("documentStore", {
  state: () => ({
    loading: false,
    documents: [],
    show_uploader: false,
  }),
  getters: {},

  actions: {
    async get_documents_list() {
      try {
        const response = await fetch(`${baseUrl}/documents`, {
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
          const errorData = await response.json().catch(() => ({}));
          const errorMessage =
            errorData.message || `Error: ${response.statusText}`;
          throw new Error(errorMessage);
        }

        const data = await response.json();
        this.documents = data;

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

        // You can rethrow the error or handle it in some way, e.g., user notification
      }
    },

    async upload_documents() {
      // returning a Promise

      return new Promise((resolve) => {
        // simulating a delay of 2 seconds
        setTimeout(() => {
          resolve({
            url: `${baseUrl}/documents/upload`,
            method: "POST",
            headers: [
              {
                name: "Authorization",
                value: `Bearer ${authStore.token}`,
              },
            ],
          });
        }, 2000);
      });
    },

    async uploaded_success() {
      Notify.create({
        color: "positive",
        position: "bottom",
        message: "uploaded",
        icon: "done",
      });

      setTimeout(() => {
        this.show_uploader = false;
      }, 2000);

      this.get_documents_list();
    },

    async upload_failed() {
      // FIXME: chech if token is not valid anymore
      Notify.create({
        color: "negative",
        position: "bottom",
        message: "could not be uploaded",
        icon: "report_problem",
      });
      this.show_uploader = true;
    },
  },
});
