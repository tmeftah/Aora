<template>
  <q-layout view="FHh Lpr lFf">
    <q-header dark bordered class="bg-darkblue-1 text-white-8">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />
        <q-toolbar-title>  DOC-INFO </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      width="220"
    >

      <q-list>

        <EssentialLink
          v-for="link in linksList"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from "vue";
import EssentialLink from "components/EssentialLink.vue";

defineOptions({
  name: "MainLayout",
});

const linksList = [
  {
    title: "Dashboard",
    caption: "overview",
    icon: "line_axis",
    link: "1",
  },
  {
    title: "Ask a question",
    caption: "chat with docs",
    icon: "chat_bubble_outline",
    link: "2",
  },
  {
    title: "Alle Dokumente",
    caption: "chat with docs",
    icon: "folder_open",
    link: "/",
  },
];

const leftDrawerOpen = ref(false);
const miniState = ref(true);

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}
</script>
