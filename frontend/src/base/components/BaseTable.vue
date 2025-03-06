<script setup>
import { ref } from "vue";
import "../../assets/css/base.css";

defineProps({
  title: String,
  filterPlaceholder: {
    type: String,
    default: "Search...",
  },
});

const filter = ref("");
</script>

<template>
  <q-page class="full-page">
    <q-card flat bordered class="full-card">
      <q-card-section class="text-black">
        <div class="text-h4 text-bold">{{ title }}</div>
      </q-card-section>

      <q-card-section class="toolbar">
        <q-input outlined v-model="filter" :label="filterPlaceholder" class="search-bar" debounce="300">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>

        <slot name="customBtn"> </slot>
      </q-card-section>

      <q-card-section class="table-container">
        <slot name="dataTable"></slot>
      </q-card-section>
    </q-card>

    <slot name="DialogBox"></slot>
    <slot name="deleteModal"></slot>
  </q-page>
</template>
