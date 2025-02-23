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
        </div>
      </div>

      <div class="row no-wrap">
        <q-btn label="+Topics" color="primary" class="q-mb-sm " @click="showDialog = true" />
      </div>
      <q-table :rows="topics" :columns="columns" row-key="name" flat bordered />

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
  </q-page>
</template>
