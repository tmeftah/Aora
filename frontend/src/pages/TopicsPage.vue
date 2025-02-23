<script setup>
import { storeToRefs } from "pinia";
import { date } from "quasar";

import { useTopicStore } from "../stores/topicsStore";
import { ref, onMounted } from "vue";


defineOptions({
  name: "TopicsPage",
});

const TopicStore = useTopicStore();
const {
  getAllTopics,
  addTopic


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

onMounted(() => {
  console.log("TopicsPage component mounted");
  getAllTopics();
});

const showDialog = ref(false);
const newTopicName = ref("");
const newTopicDetails = ref("");

const saveTopic = async () => {
  if (newTopicName.value.trim() === "") {
    return;
  }
  await addTopic(newTopicName.value, "nothing");
  newTopicName.value = "";
  newTopicDetails.value = "";
  showDialog.value = false;
};
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
          <div class="row items-center no-wrap">
            <q-btn label="+Topics" color="primary" class="q-ml-sm" @click="showDialog = true" />
          </div>
        </template>

      </q-table>
    </div>

    <q-dialog v-model="showDialog">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">Add New Topic</div>
          <q-form class="q-gutter-md">
            <q-input v-model="newTopicName" label="Topic Name" outlined required />
            <q-input v-model="newTopicDetails" label="Topic Details" outlined type="textarea" />
          </q-form>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn label="Cancel" color="red" @click="showDialog = false" />
          <q-btn label="Add Topic" color="green" @click="saveTopic" />
        </q-card-actions>
      </q-card>
    </q-dialog>

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
