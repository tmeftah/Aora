<script setup>
import { storeToRefs } from "pinia";
import { date } from "quasar";
import { useMainStore } from "../stores/main-store";
import { useTopicStore } from "../stores/topicsStore";

defineOptions({
  name: "TopicsPage",
});

const TopicStore = useTopicStore();
const {
  getAllTopics,

} = TopicStore;
const { topics } = storeToRefs(TopicStore);



const columns = [
  {
    name: "name",
    required: true,
    label: "Topic-Name",
    align: "left",
    field: (row) => row.name,
    format: (val) => `${val}`,
    sortable: true,
  },
  {
    name: "created_at",
    align: "center",
    label: "Date",
    field: "created_at",
    format: (val) => `${date.formatDate(val, "YYYY-MM-DD HH:mm:ss")}`,
    sortable: true,
  },
  {
    name: "Details",
    align: "center",
    label: "Details",
    field: "status",
    sortable: true,
  },
];

getAllTopics();
</script>

<template>
  <q-page>
    <div class="q-pa-md">
      <div class="row q-mb-xl">
        <div class="col">
          <span class="text-h4">Topics</span>
          <p class="q-mt-sm text-caption text-weight-light">
            All defined topics
          </p>
        </div>

      </div>
      <q-table :rows="topics" :columns="columns" row-key="name" flat bordered>
        <template v-slot:top-right>
          <q-input dense debounce="300" placeholder="Filter by topic name" outlined>
            <template v-slot:prepend>
              <q-icon name="filter_list" class="q-mr-sm" />
            </template>
          </q-input>
        </template>
        <template v-slot:body-cell-status="props">
          <q-td :props="props">
            <div>
              <q-badge :color="props.row.status_text" :label="props.value" />
            </div>
            <div class="my-table-details">
              {{ props.row.details }}
            </div>
          </q-td>
        </template>
      </q-table>
    </div>
  </q-page>
</template>
