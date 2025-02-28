import { defineStore } from "pinia";
import {
  useAuthStore,
  baseUrl,
  apiRequest,
  showNotification,
} from "stores/auth";

const authStore = useAuthStore();

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
        const responseData = await apiRequest(
          "GET",
          "/documents",
          null,
          authStore.token
        );

        this.documents = responseData;
      } catch (error) {
        console.log("Error in fetching documents", error.message);
        showNotification(
          "negative",
          "Documents could not be fetched at the moment",
          "check_circle"
        );

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
      showNotification("positive", "Document successfully uploaded", "done");

      setTimeout(() => {
        this.show_uploader = false;
      }, 2000);

      this.get_documents_list();
    },

    async upload_failed() {
      // FIXME: chech if token is not valid anymore

      showNotification(
        "negative",
        "Documents could not be uploaded",
        "report_problem"
      );
      this.show_uploader = true;
    },
  },
});
