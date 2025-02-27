<template>
  <div class="q-pa-md example-row-equal-width">
    <div class="row">
      <div class="col col-sm-6">
        <q-input @keydown.enter.prevent="MainStore.sendQA(question, model_name)" rounded outlined v-model="question"
          placeholder="Ask anything..." type="text">
          <template v-slot:prepend>
            <q-icon name="search" class="q-mr-sm" @click="MainStore.sendQA(question, model_name)" />
          </template>
          <template v-slot:append>
            <q-avatar>
              <img src="https://cdn.quasar.dev/logo-v2/svg/logo.svg">
            </q-avatar>
          </template>
        </q-input>

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
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from "pinia";
import { useMainStore } from "../stores/mainStore";

defineOptions({
  name: "2Page",
});

const MainStore = useMainStore();
const { loading, solution, question, model_name } = storeToRefs(MainStore);
</script>
