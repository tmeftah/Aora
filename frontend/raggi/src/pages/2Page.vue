<template>
  <div class="q-pa-md example-row-equal-width">
    <div class="row">
      <div class="col">
        <q-input
          outlined
          bottom-slots
          v-model="question"
          label="ask a question..."
          type="textarea"
          autogrow
        >
          <template v-slot:after>
            <q-btn dense flat icon="send" @click="MainStore.sendQA(question)" />
          </template>
        </q-input>

        <q-input
          v-model="solution"
          outlined
          autogrow
          type="textarea"
          :loading="loading"
        />
      </div>
      <div class="col"></div>
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from "pinia";
import { useMainStore } from "../stores/main-store";
defineOptions({
  name: "2Page",
});

const MainStore = useMainStore();
const { loading, solution, question } = storeToRefs(MainStore);
</script>
