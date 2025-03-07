<script setup>
import { storeToRefs } from "pinia";
import { useMainStore } from "../stores/mainStore";
import { useTopicStore } from '../stores/topicsStore';
import { showNotification } from "src/stores/auth";
import { ref, onMounted, computed, watch } from "vue";
import "../assets/css/base.css"

defineOptions({
  name: "2Page",
});

const MainStore = useMainStore();
const topicStore = useTopicStore();
const { getAllTopics } = topicStore;
const { topics } = storeToRefs(topicStore);
const allTopics = computed(() => topics.value.map(topic => topic.name));
const { loading, solution, question, model_name } = storeToRefs(MainStore);
const models = ref([]);
const selectedTopics = ref([]);
const selectedValues = computed(() => Array.isArray(selectedTopics.value) ? selectedTopics.value : []);


onMounted(async () => {
  try {
    await MainStore.get_models();
    models.value = MainStore.models || [];
  } catch (error) {
    console.error("Failed to load models:", error);
    models.value = [];
  }
  getAllTopics();
});

async function getLLMResponse(question, model_name) {
  try {
    loading.value = true;
    const response = await MainStore.askLLM(question, model_name, selectedValues.value);

    console.log("Got response:", response);
  } catch (error) {
    console.error("Failed to get response:", error);
    solution.value = "Error retrieving response.";
  } finally {
    loading.value = false;
  }
}

const limitSelection = (newSelection) => {
  if (newSelection.length > 2) {
    showNotification('negative', 'Please dont select more than 2 topics', 'done')
    selectedTopics.value = newSelection.slice(0, 2);
    return;
  }
  selectedTopics.value = newSelection;
};
</script>


<template>

  <q-page class="full-page">
    <q-card flat bordered class="full-card">
      <q-card-section class="text-black">
        <div class="text-h4 text-bold" style="color:#075070">🔮Aora-AI </div>
      </q-card-section>

      <q-card-section class="toolbar">
        <q-input @keydown.enter.prevent="getLLMResponse(question, model_name)" rounded outlined v-model="question"
          placeholder="Ask anything..." type="text" :disable="models.length === 0" style="width: 50%;">

          <template v-slot:prepend>
            <q-icon name="search" class="q-mr-sm" @click="getLLMResponse(question, model_name)" />

          </template>
          <template v-slot:append>
            <q-avatar>
              <img src="https://cdn-icons-png.flaticon.com/512/4712/4712100.png">
            </q-avatar>
          </template>
        </q-input>

        <!-- <q-toggle false-value="Not Vectorized" :label="`${greenModel}`" true-value="Vectorized" color="green"
          v-model="greenModel" /> -->

        <q-select style="min-width: 250px; max-width: 300px" dense options-dense outlined v-model="selectedTopics"
          multiple :options="allTopics" use-chips stack-label label="Select Topics" required
          @update:model-value="limitSelection" clearable />



        <q-select style="min-width: 250px; max-width: 300px" dense options-dense outlined v-model="model_name"
          :options="models" label="Model" class="model-select"
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
