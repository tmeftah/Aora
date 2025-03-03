<script setup>
import { storeToRefs } from "pinia";
import { useMainStore } from "../stores/mainStore";
import { ref, onMounted } from "vue";

defineOptions({
  name: "2Page",
});

const MainStore = useMainStore();
const { loading, solution, question, model_name } = storeToRefs(MainStore);
const models = ref([]);


onMounted(async () => {
  try {
    await MainStore.get_models();
    models.value = MainStore.models || [];
  } catch (error) {
    console.error("Failed to load models:", error);
    models.value = [];
  }
});

async function getLLMResponse(question, model_name) {
  try {
    loading.value = true;
    const response = await MainStore.askLLM(question, model_name);
    console.log("Got response:", response);
  } catch (error) {
    console.error("Failed to get response:", error);
    solution.value = "Error retrieving response.";
  } finally {
    loading.value = false;
  }
}
</script>


<template>

  <q-page class="full-page">
    <q-card flat bordered class="full-card">
      <q-card-section class="text-black">
        <div class="text-h4 text-bold">🔮Aora-AI </div>
      </q-card-section>

      <q-card-section class="toolbar">
        <q-input @keydown.enter.prevent="getLLMResponse(question, model_name)" rounded outlined v-model="question"
          placeholder="Ask anything..." type="text" :disable="models.length === 0" style="width: 50%;;">
          <template v-slot:prepend>
            <q-icon name="search" class="q-mr-sm" @click="getLLMResponse(question, model_name)" />

          </template>
          <template v-slot:append>
            <q-avatar>
              <img src="https://cdn-icons-png.flaticon.com/512/4712/4712100.png">
            </q-avatar>
          </template>
        </q-input>

        <q-select dense options-dense outlined v-model="model_name" :options="models" label="Model" class="model-select"
          @update:model-value="(val) => MainStore.set_model_name(val)">
          <template v-slot:append v-if="models.length === 0">
            <q-icon name="warning" color="red">
              <q-tooltip>No models could be fetched</q-tooltip>
            </q-icon>
          </template>
        </q-select>
      </q-card-section>

      <q-card-section class="table-container">
        <q-card flat bordered class="q-mt-sm column" v-if="solution || loading">
          <q-input v-model="solution" autogrow borderless dense :loading="loading"
            class="text-weight-bolder text-body1 q-mx-sm" />

          <div class="q-ma-sm q-gutter-y-md items-start" v-if="!loading && solution">
            <q-btn-group push>
              <q-btn size="xs" icon="thumb_up" />
              <q-btn size="xs" icon="thumb_down" style="border-left: 1px black solid" />
            </q-btn-group>
          </div>
        </q-card>
      </q-card-section>
    </q-card>

  </q-page>

</template>

<style scoped>
.model-select {
  min-width: 150px;
  max-width: 200px;
}

.full-page {
  width: 100%;
  height: 70vh;
  display: flex;
  flex-direction: column;
}

.full-card {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
}

.search-bar {
  width: 40%;
}

.table-container {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding-bottom: 10px;
}

.responsive-table {
  font-size: 18px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  height: 100%;
  max-width: 100%;
}

.q-table tbody tr:nth-child(odd) {
  background-color: #f5faff;
}

.q-table tbody tr:hover {
  background-color: #e3f2fd !important;
}

.text-dark {
  color: #1a237e;
}

.text-body2 {
  font-size: 14px;
}
</style>
