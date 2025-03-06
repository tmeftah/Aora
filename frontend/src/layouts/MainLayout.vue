<script setup>
import { ref } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "../stores/auth";
import { useMainStore } from "src/stores/mainStore";
import { useRouter } from "vue-router";
import { Notify } from "quasar";
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
    link: "/documents",
  },
  {
    title: "Alle Topics",
    caption: "All topics",
    icon: "library_books",
    link: "/topics",
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


const handleLogout = async () => {
  try {
    await authStore.logout();
    router.push("/login");
    Notify.create({
      color: "positive",
      position: "bottom",
      message: "You are successfully logged out",
      icon: "done",
    });
  } catch (error) {
    console.error("Logout failed:", error);
  } finally {
    logoutDialog.value = false;
  }
};

const logoutDialog = ref(false);
</script>


<template>
  <q-layout view="hHh lpR fFf" class="bg-grey-1">
    <q-header elevated class="bg-white text-grey-4 q-py-xs" height-hint="58">
      <q-toolbar>
        <q-btn dense flat round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" />

        <q-btn flat no-caps no-wrap class="q-ml-xs" v-if="$q.screen.gt.xs">
          <q-toolbar-title class="text-bold text-weight-bolder text-h4" style="color: #507295">
            Aora.
          </q-toolbar-title>
        </q-btn>
        <q-space />

        <!-- Orion Inova -->
        <div class="q-gutter-sm row items-center no-wrap">

          <q-btn round dense flat color="grey-8" icon="apps" v-if="$q.screen.gt.sm">
            <q-tooltip>Apps</q-tooltip>
          </q-btn>
          <q-btn round flat>
            <q-avatar size="26px">
              <img src="https://cdn.quasar.dev/img/boy-avatar.png">
            </q-avatar>
            <q-menu auto-close>
              <q-list style="min-width: 150px">
                <q-item clickable>
                  <q-item-section>Profile</q-item-section>
                </q-item>
                <q-item clickable>
                  <q-item-section>Settings</q-item-section>
                </q-item>
                <q-item clickable>
                  <q-item-section @click="logoutDialog = true">Logout</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
            <q-tooltip>Account</q-tooltip>
          </q-btn>
        </div>
        <q-btn flat round icon="logout" color="grey-8" class="q-mr-xs" @click="logoutDialog = true" />
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered class="bg-white-2" :width="240">
      <q-list>
        <EssentialLink v-for="link in linksList" :key="link.title" v-bind="link" />
      </q-list>

      <q-separator />

    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <!-- Logout Confirmation Dialog -->
    <q-dialog :backdrop-filter="60" v-model="logoutDialog">
      <q-card style="width: 700px; max-width: 80vw;">
        <q-card-section class="row items-center q-pb-none text-h6">
          <q-icon name="warning" color="warning" size="2rem" class="q-mr-sm" />
          <span class="text-h6">Logout?</span>
        </q-card-section>

        <q-card-section>
          Are you sure you want to Logout??
        </q-card-section>

        <q-card-actions align="right">
          <q-btn label="Cancel" color="grey" v-close-popup />
          <q-btn label="Logout" color="red" @click="handleLogout" />
        </q-card-actions>
      </q-card>
    </q-dialog>

  </q-layout>
</template>
