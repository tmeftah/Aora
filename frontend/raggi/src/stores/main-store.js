import { defineStore } from "pinia";

const baseUrl = `${process.env.API}`;

export const useMainStore = defineStore("main", {
  state: () => ({
    loading: false,
    question: "",
    solution: "",
  }),
  getters: {},

  actions: {
    async sendQA(question) {
      this.solution = "";
      this.loading = true;
      await fetch(`${baseUrl}/query?query=${question}`)
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
          this.loading = false;
          console.error("Error fetching the data:", error);
        });

      //
    },
  },
});
