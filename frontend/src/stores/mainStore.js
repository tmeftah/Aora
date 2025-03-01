import { defineStore } from "pinia";
import { Notify } from "quasar";
import { useAuthStore, apiRequest, showNotification } from "stores/auth";

const authStore = useAuthStore();

const baseUrl = `${process.env.API}`;

export const useMainStore = defineStore("main", {
  state: () => ({
    loading: false,
    question: "",
    solution: "",
    models: JSON.parse(localStorage.getItem("models")) || [],
    model_name: localStorage.getItem("model_name") || "",
    show_uploader: false,
  }),
  getters: {},

  actions: {
    async get_models() {
      try {
        const response = await fetch(`${baseUrl}/query/list_models`, {
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
        this.models = data;
        localStorage.setItem("models", JSON.stringify(this.models));

      } catch (error) {
        console.error(`API error: ${error.message}`);
        Notify.create({
          color: "negative",
          position: "bottom",
          message:
            "API ERROR: Unable to fetch LLM Models, please contact ADMIN",
          icon: "report_problem",
        });

        // You can rethrow the error or handle it in some way, e.g., user notification
      }
    },

    set_model_name(name) {
      localStorage.setItem("model_name", name);
    },

    async sendQA(question, model_name) {
      this.solution = "";
      this.loading = true;
      await fetch(
        `${baseUrl}/query?query=${question}&model_name=${model_name}`,
        {
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${authStore.token}`,
          },
        }
      )
        .then((response) => {
          console.log(response.body);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          } else {
            return response.body.getReader();
          }
        })
        .then((reader) => {
          const $this = this;
          let text = "";
          function readChunk(reader) {
            reader.read().then(({ done, value }) => {
              if (done) {
                console.log("All chunks processed.");
                $this.loading = false;
                return;
              }

              const chunkText = new TextDecoder("utf-8").decode(value);
              $this.solution += JSON.parse(chunkText).data;
              // console.log("Chunk received:", JSON.parse(chunkText).data);
              // outputField.value = text;

              readChunk(reader); // Loop to read the next chunk
            });
          }

          readChunk(reader, this.solution);
        })
        .catch((error) => {
          //
          if (error.status === 401) {
            authStore.clearToken();
            window.location.href = "/login"; // Or use Vue Router
            return;
          }

          //
          this.loading = false;
          console.error("Error fetching the data:", error);
        });

      //
    },

    async askLLM(question, model_name) {
      this.solution = "";
      this.loading = true;
      const responseData = await apiRequest(
        "GET",
        `/query?query=${question}&model_name=${model_name}`,
        null,
        authStore.token
      );
      console.log("Response from LLM", responseData);
      this.solution = responseData;
    },
  },
});
