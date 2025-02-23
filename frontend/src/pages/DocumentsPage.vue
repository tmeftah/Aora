<script setup>
import { storeToRefs } from "pinia";
import { date } from "quasar";
import { useDocumentStore } from "../stores/documentStore";
import { onMounted } from "vue";

defineOptions({
  name: "DocumentsPage",
});

const DocumentStore = useDocumentStore();
const {
  get_documents_list,
  upload_documents,
  uploaded_success,
  upload_failed,
} = DocumentStore;
const { documents, show_uploader } = storeToRefs(DocumentStore);

const columns = [
  {
    name: "filename",
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
    name: "status",
    align: "center",
    label: "Status",
    field: "status",
    sortable: true,
  },
];

onMounted(() => {
  console.log("DocumentsPage component mounted");
  get_documents_list();
});
</script>


<template>
  <q-page>
    <div class="q-pa-md">
      <div class="row q-mb-xl">
        <div class="col">
          <span class="text-h4">Documents</span>
          <p class="q-mt-sm text-caption text-weight-light">
            All documents related to
          </p>
        </div>
        <div class="col-grow q-gutter-sm">
          <q-btn color="secondary" label="Upload" icon="upload">
            <q-popup-proxy v-model="show_uploader">
              <q-banner>
                <q-uploader :factory="upload_documents" flat color="secondary" style="max-width: 300px" fieldName="file"
                  accept="application/pdf, text/plain, .md" @uploaded="uploaded_success"
                  @failed="upload_failed" /></q-banner>
            </q-popup-proxy>
          </q-btn>
        </div>
      </div>
      <q-table :rows="documents" :columns="columns" row-key="name" flat bordered>
        <template v-slot:top-right>
          <q-input dense debounce="300" placeholder="Filter by filename" outlined>
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
