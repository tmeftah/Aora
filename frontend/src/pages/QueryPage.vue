<template>
  <div class="q-pa-md example-row-equal-width">
    <div class="row items-center justify-between">
      <!-- Search Box (Left) -->
      <div class="col-6">
        <q-input @keydown.enter.prevent="MainStore.askLLM(question, model_name)" rounded outlined v-model="question"
          placeholder="Ask anything..." type="text" class="full-width" :disable="models.length === 0">
          <template v-slot:prepend>
            <q-icon name="search" class="q-mr-sm" @click="MainStore.askLLM(question, model_name)" />
          </template>
          <template v-slot:append>
            <q-avatar>
              <img src="https://cdn.quasar.dev/logo-v2/svg/logo.svg">
            </q-avatar>
          </template>
        </q-input>
      </div>

      <!-- Model Selection (Right) -->
      <div class="col-3-auto q-ml-md">
        <q-select transition-show="flip-up" transition-hide="flip-down" dense options-dense outlined
          v-model="model_name" :options="models" label="Model" class="model-select"
          @update:model-value="(val) => MainStore.set_model_name(val)">
          <template v-slot:append v-if="models.length === 0">
            <q-icon name="warning" color="red">
              <q-tooltip>No models could be fetched</q-tooltip>
            </q-icon>
          </template>
        </q-select>
      </div>
    </div>

    <!-- Response Card -->
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
  </div>
</template>

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
</script>

<style scoped>
.model-select {
  min-width: 150px;
  max-width: 200px;
}
</style>
