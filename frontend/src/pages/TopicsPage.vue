<script setup>
import { storeToRefs } from "pinia";
import { useTopicStore } from "../stores/topicsStore";
import { ref, onMounted, computed } from "vue";
import { Notify } from "quasar";
import BaseTable from "src/base/components/BaseTable.vue"
import BaseConfirmationDialog from "src/base/components/BaseConfirmationDialog.vue";

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
  {
    name: "actions",
    label: "Actions",
    align: "left",
    field: "actions",
    sortable: false,
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

const deletionDialog = ref(false);
const selectedId = ref(0);
const selectedName = ref('');

function openDeleteModal(topicName) {
  selectedName.value = topicName;
  deletionDialog.value = true;
}

function closeDeleteModal() {
  deletionDialog.value = false;
}

function deleteTopicItem() {
  topicStore.deleteTopic(selectedName.value)
  deletionDialog.value = false;
}

const confirmDeletionText = computed(() => {
  return `Would you like to delete?`;
});


</script>

<template>

  <BaseTable title="📚 Topics Management" filterPlaceholder="Search for Topics...">

    <template v-slot:customBtn>
      <q-btn label="Topic" color="primary" icon="add" size="md" @click="showDialog = true" />
    </template>

    <template v-slot:dataTable>
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

        <template v-slot:body-cell-actions="props">
          <q-td :props="props">
            <q-btn icon="edit" color="primary" flat round dense @click="openEditDialog(props.row)" size="sm" />
            <q-btn icon="delete" color="red" flat round dense @click="openDeleteModal(props.row.name)" size="sm" />
          </q-td>
        </template>

        <template v-slot:no-data>
          <div class="full-width row flex-center q-pa-md">
            <q-icon name="warning" color="red" size="md" class="q-mr-sm" />
            <span class="text-grey-8 text-h6">No Topics found, please kindly add some topics. </span>
          </div>
        </template>
      </q-table>
    </template>


    <template v-slot:DialogBox>
      <q-dialog v-model="showDialog">
        <q-card style="min-width: 500px">
          <q-card-section class="bg-primary text-white text-center">
            <div class="text-h5"> Add New Topic</div>
          </q-card-section>

          <q-card-section>
            <q-form @submit.prevent="saveTopic" class="q-gutter-md">
              <q-input v-model="newTopicName" label="Topic Name" outlined required />
              <q-input v-model="newTopicDetails" label="Topic Details" outlined type="textarea" />
            </q-form>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn label="Cancel" color="negative" @click="showDialog = false" />
            <q-btn label="Add Topic" color="primary" @click="saveTopic" />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </template>

    <template v-slot:deleteModal>
      <BaseConfirmationDialog v-model="deletionDialog" title="Confirm Deletion?" :text="confirmDeletionText"
        @closeDailog="closeDeleteModal()" @deleteElement="deleteTopicItem()"
        id="delete-testseries-confirmation-dialog" />
    </template>


  </BaseTable>
</template>
