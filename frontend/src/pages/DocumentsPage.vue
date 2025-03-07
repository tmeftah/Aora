<script setup>
import { ref, computed } from 'vue'
import { storeToRefs } from "pinia";
import { date } from "quasar";
import { useDocumentStore } from "../stores/documentStore";
import { useTopicStore } from '../stores/topicsStore';
import { onMounted } from "vue";
import { showNotification } from 'src/stores/auth';
import BaseTable from "src/base/components/BaseTable.vue"
import BaseConfirmationDialog from "src/base/components/BaseConfirmationDialog.vue";

defineOptions({
  name: "DocumentsPage",
});

const DocumentStore = useDocumentStore();
const topicStore = useTopicStore();
const {
  get_documents_list,
  upload_documents,
  uploaded_success,
  upload_failed,
} = DocumentStore;
const { documents, show_uploader } = storeToRefs(DocumentStore);

const columns = [
  {
    name: "name",
    required: true,
    label: "Name",
    align: "left",
    field: (row) => row.filename,
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
    name: "topic_id",
    align: "center",
    label: "Topic ID",
    field: "topic_id",
    sortable: true,
  },
  {
    name: "status",
    align: "center",
    label: "Status",
    field: (row) => (row.vectorized ? "Vectorized" : "On Progress"),
    sortable: true,
  },
  {
    name: "vectorized",
    align: "center",
    label: "vectorized",
    field: "vectorized",
    format: (val) => (val ? "☑️" : "❌"),
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
const filter = ref("");

onMounted(() => {
  console.log("DocumentsPage component mounted");
  get_documents_list();
  getAllTopics();
});

const showDialog = ref(false);
const selectedTopic = ref(null);
const selectedFile = ref(null);
const AllTopicNames = computed(() => topics.value.map(topic => topic.name));
const isLoading = ref(false);
const isLoadingTopics = ref(true);

const onFileSelected = (file) => {
  if (file && !["application/pdf", "text/plain"].includes(file.type)) {
    showNotification("negative", "Only PDFs or plain txt files are allowed.", "report_problem");

    selectedFile.value = null;
    return;
  }
  selectedFile.value = file;
};

const clearFile = () => {
  selectedFile.value = null;
};

const uploadFile = async () => {
  if (!selectedFile.value || !selectedTopic.value) return;

  isLoading.value = true;
  let formData = new FormData();
  formData.append('file', selectedFile.value);
  // formData.append('topic_name', selectedTopic.value);

  try {
    const uploadConfig = await upload_documents(selectedTopic.value);

    const response = await fetch(uploadConfig.url, {
      method: uploadConfig.method,
      headers: uploadConfig.headers.reduce((acc, header) => {
        acc[header.name] = header.value;
        return acc;
      }, {}),
      body: formData
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Upload successful', data);
      showNotification("positive", "Document successfully uploaded", "done");
      uploaded_success();
      showDialog.value = false;
    } else {
      throw new Error("Upload failed");
    }
  } catch (error) {
    showDialog.value = false;
    console.error('Upload failed', error);
    showNotification("negative", "Documents could not be uploaded", "report_problem");
    upload_failed();
  } finally {
    isLoading.value = false;
    clearFile();
  }
};

const resetForm = () => {
  selectedTopic.value = null;
  selectedFile.value = null;
};

const { getAllTopics } = topicStore;
const { topics } = storeToRefs(topicStore);

const openDialog = async () => {
  isLoadingTopics.value = false;
  if (topics.value.length === 0) {
    showNotification("negative", "Please kindly add some topics before uploading any documents.", "report_problem");

    return;
  }
  showDialog.value = true;
};

const deletionDialog = ref(false);
const selectedId = ref(0);
const selectedName = ref('');

function openDeleteModal(documentName) {
  console.log("Document name: " + documentName);
  selectedName.value = documentName;
  deletionDialog.value = true;
}

function closeDeleteModal() {
  deletionDialog.value = false;
}

function deleteDocumentItem() {
  DocumentStore.deleteDocument(selectedName.value)
  deletionDialog.value = false;
}

const confirmDeletionText = computed(() => {
  return `Would you like to delete this <strong> ${selectedName.value} </strong> document?`;
});

</script>


<template>
  <BaseTable title="📑 Documents" filterPlaceholder="Search for Documents...">

    <template v-slot:customBtn>
      <q-btn label="Upload Document" icon="upload" color="primary" @click="openDialog" />
      <!-- <q-btn color="primary" label="Upload" icon="upload">
        <q-popup-proxy v-model="show_uploader">
          <q-banner>
            <q-uploader :factory="upload_documents" flat color="primary" style="max-width: 300px" fieldName="file"
              accept="application/pdf, text/plain, .md" @uploaded="uploaded_success"
              @failed="upload_failed" /></q-banner>
        </q-popup-proxy>
      </q-btn> -->
    </template>

    <template v-slot:dataTable>
      <q-table :rows="documents" :columns="columns" row-key="name" flat bordered wrap-cells dense :filter="filter"
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

        <template v-slot:body-cell-actions="props">
          <q-td :props="props">
            <q-btn icon="edit" color="primary" round dense size="sm" disabled />
            <q-btn icon="delete" color="red" round dense @click="openDeleteModal(props.row.filename)" size="sm" />
          </q-td>
        </template>

        <template v-slot:no-data>
          <div class="full-width row flex-center q-pa-md">
            <q-icon name="warning" color="red" size="md" class="q-mr-sm" />
            <span class="text-grey-8 text-h6">No Documents found, please kindly add some documents </span>
          </div>
        </template>
      </q-table>
    </template>


    <template v-slot:DialogBox>
      <q-dialog v-model="showDialog" @hide="resetForm">
        <q-card style="width: 400px">
          <q-card-section>
            <div class="text-h6">Upload Document</div>
          </q-card-section>

          <q-form @submit.prevent="uploadFile">
            <q-card-section>
              <q-select outlined v-model="selectedTopic" :options="AllTopicNames" label="Select Topic"
                :disable="isLoadingTopics" />

              <q-file outlined class="q-mt-md" v-model="selectedFile" label="Choose File"
                @update:model-value="onFileSelected" accept=".pdf, .txt" clearable />

              <div v-if="selectedFile" class="q-mt-md">
                <q-chip removable @remove="clearFile">{{ selectedFile.name }}</q-chip>
              </div>
            </q-card-section>

            <q-card-actions align="right">
              <q-btn label="Cancel" color="negative" @click="showDialog = false" />
              <q-btn label="Clear" color="warning" @click="clearFile" :disable="!selectedFile" />
              <q-btn icon="upload" label="Upload" color="primary" type="submit"
                :disable="!selectedFile || !selectedTopic || AllTopicNames.length === 0" :loading="isLoading" />
            </q-card-actions>
          </q-form>
        </q-card>
      </q-dialog>
    </template>

    <template v-slot:deleteModal>
      <BaseConfirmationDialog v-model="deletionDialog" title="Confirm Deletion?" :text="confirmDeletionText"
        @closeDailog="closeDeleteModal()" @deleteElement="deleteDocumentItem()"
        id="delete-document-confirmation-dialog" />
    </template>

  </BaseTable>
</template>
