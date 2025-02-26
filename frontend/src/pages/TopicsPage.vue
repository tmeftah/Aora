<script setup>
import { storeToRefs } from "pinia";
import { useTopicStore } from "../stores/topicsStore";
import { ref, onMounted } from "vue";
import { Notify } from "quasar";

defineOptions({
  name: "TopicsPage",
});

const topicStore = useTopicStore();
const { getAllTopics, addTopic } = topicStore;
const { topics } = storeToRefs(topicStore);

const columns = [
  {
    name: "name",
    required: true,
    label: "Topic Name",
    align: "left",
    field: (row) => row.name,
    sortable: true,
  },
  {
    name: "details",
    align: "left",
    label: "Details",
    field: (row) => row.details || "No details available",
    sortable: true,
  },
];

onMounted(() => {
  getAllTopics();
});

const showDialog = ref(false);
const newTopicName = ref("");
const newTopicDetails = ref("");
const filter = ref("");

const saveTopic = async () => {
  if (!newTopicName.value.trim()) {
    Notify.create({
      message: "Topic Name is required!",
      type: "negative",
      position: "top",
    });
    return;
  }

  try {
    await addTopic(newTopicName.value, newTopicDetails.value || "No details provided");
    Notify.create({
      message: "Topic added successfully!",
      type: "positive",
      position: "top",
    });

    newTopicName.value = "";
    newTopicDetails.value = "";
    showDialog.value = false;
  } catch (error) {
    Notify.create({
      message: "Failed to add topic",
      type: "negative",
      position: "top",
    });
  }
};
</script>

<template>
  <q-page class="full-page">
    <q-card flat bordered class="full-card">
      <q-card-section class="bg-primary text-white">
        <div class="text-h4 text-bold">📚 Topics Management</div>
      </q-card-section>

      <q-card-section class="toolbar">
        <q-input filled v-model="filter" label="Search Topics..." class="search-bar" debounce="300">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>

        <q-btn label="Add New Topic" color="primary" icon="add" size="md" @click="showDialog = true" />
      </q-card-section>

      <q-card-section class="table-container">
        <q-table :rows="topics" :columns="columns" row-key="name" flat bordered wrap-cells dense :filter="filter"
          :pagination="{ rowsPerPage: 10 }" class="responsive-table">
          <template v-slot:body-cell-name="props">
            <q-td :props="props">
              <q-chip>{{ props.value }}</q-chip>
            </q-td>
          </template>

          <template v-slot:body-cell-details="props">
            <q-td :props="props">
              <q-badge color="blue" class="text-body2">{{ props.value }}</q-badge>
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>

    <!-- Dialog for adding new topics -->
    <q-dialog v-model="showDialog">
      <q-card style="min-width: 500px">
        <q-card-section class="bg-secondary text-white text-center">
          <div class="text-h5"> Add New Topic</div>
        </q-card-section>

        <q-card-section>
          <q-form @submit.prevent="saveTopic" class="q-gutter-md">
            <q-input v-model="newTopicName" label="Topic Name" outlined required />
            <q-input v-model="newTopicDetails" label="Topic Details" outlined type="textarea" />
          </q-form>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="negative" @click="showDialog = false" />
          <q-btn label="Add Topic" color="positive" @click="saveTopic" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<style scoped>
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
