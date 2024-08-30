<template>
  <q-layout view="hHh lpR fFf">
    <q-header dark bordered class="bg-white text-grey-8">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title
          class="text-bold text-weight-bolder text-h3"
          style="color: #507295"
        >
          Aora.
        </q-toolbar-title>
        <!-- Orion Inova -->
        <q-btn flat round icon="logout" class="q-mr-xs" @click="logout" />
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered :width="220">
      <q-list>
        <EssentialLink
          v-for="link in linksList"
          :key="link.title"
          v-bind="link"
        />
      </q-list>

      <q-separator />
      <div class="q-ma-sm fixed-bottom">
        <q-select
          transition-show="flip-up"
          transition-hide="flip-down"
          dense
          options-dense
          outlined
          v-model="model_name"
          :options="models"
          label="Model"
          @update:model-value="(val) => mainStore.set_model_name(val)"
        />
      </div>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "../stores/auth";
import { useMainStore } from "src/stores/main-store";
import { useRouter } from "vue-router";

import EssentialLink from "components/EssentialLink.vue";

defineOptions({
  name: "MainLayout",
});

const linksList = [
  {
    title: "Dashboard",
    caption: "overview",
    icon: "line_axis",
    link: "/",
  },
  {
    title: "Ask a question",
    caption: "chat with docs",
    icon: "chat_bubble_outline",
    link: "/query",
  },
  {
    title: "Alle Dokumente",
    caption: "chat with docs",
    icon: "folder_open",
    link: "documents",
  },
];

const leftDrawerOpen = ref(false);
const miniState = ref(true);
const authStore = useAuthStore();
const router = useRouter();

const mainStore = useMainStore();
const { model_name, models } = storeToRefs(mainStore);

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}
function logout() {
  authStore.logout();

  router.push("/login");
}
</script>
