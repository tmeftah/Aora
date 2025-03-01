<script setup>
import { ref } from 'vue'
import { storeToRefs } from "pinia";
import { date } from "quasar";
import { useDocumentStore } from "../stores/documentStore";
import { onMounted } from "vue";
import BaseTable from "src/base/components/BaseTable.vue"

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
const filter = ref("");

onMounted(() => {
  console.log("DocumentsPage component mounted");
  get_documents_list();
});
</script>


<template>
  <BaseTable title="📑 Documents" filterPlaceholder="Search for Documents...">

    <template v-slot:customBtn>
      <q-btn color="primary" label="Upload" icon="upload">
        <q-popup-proxy v-model="show_uploader">
          <q-banner>
            <q-uploader :factory="upload_documents" flat color="primary" style="max-width: 300px" fieldName="file"
              accept="application/pdf, text/plain, .md" @uploaded="uploaded_success"
              @failed="upload_failed" /></q-banner>
        </q-popup-proxy>
      </q-btn>
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
      </q-table>
    </template>

    <template v-slot:DialogBox></template>

  </BaseTable>
</template>
