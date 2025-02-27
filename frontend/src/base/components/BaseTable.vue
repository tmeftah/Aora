<script setup>
import { ref } from "vue";

defineProps({
  title: String,
  filterPlaceholder: {
    type: String,
    default: "Search...",
  },
});

const emit = defineEmits(["addItem"]);

const filter = ref("");
</script>

<template>
  <q-page class="full-page">
    <q-card flat bordered class="full-card">
      <q-card-section class="text-black">
        <div class="text-h4 text-bold">{{ title }}</div>
      </q-card-section>

      <q-card-section class="toolbar">
        <q-input filled v-model="filter" :label="filterPlaceholder" class="search-bar" debounce="300">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>

        <slot name="addBtn"> </slot>
        <!-- <q-btn v-if="showAddButton" label="Add New" color="primary" icon="add" size="md" @click="$emit('addItem')" /> -->
      </q-card-section>

      <q-card-section class="table-container">
        <!-- Slot for passing in the q-table -->
        <slot name="dataTable"></slot>
      </q-card-section>
    </q-card>

    <slot name="DialogBox"></slot>
  </q-page>
</template>

<style>
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
