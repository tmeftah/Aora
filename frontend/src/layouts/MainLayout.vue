<template>
  <q-layout view="FHh Lpr lFf">
    <q-header dark bordered class="bg-grey-1 text-grey-8">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />
        <q-img
          src="https://suite.knowron.com/_next/image?url=https%3A%2F%2Fd2ccnoziqedwbs.cloudfront.net%2Flogos%2Flogo-kardex-group.png&w=256&q=75"
          width="140px"
        />


        <q-toolbar-title>  RAGGI </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      :mini="miniState"
      @mouseover="miniState = false"
      @mouseout="miniState = true"
      width="220"
    >

      <q-list>
        <q-img
          src="https://suite.knowron.com/_next/image?url=https%3A%2F%2Fd2ccnoziqedwbs.cloudfront.net%2Flogos%2Flogo-kardex-group.png&w=256&q=75"
          width="140px"
        />

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
