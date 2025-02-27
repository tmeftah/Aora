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
  <BaseTable title="Documents" filterPlaceholder="Search for Documents...">

    <template v-slot:customBtn>
      <q-btn color="secondary" label="Upload" icon="upload">
        <q-popup-proxy v-model="show_uploader">
          <q-banner>
            <q-uploader :factory="upload_documents" flat color="secondary" style="max-width: 300px" fieldName="file"
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
  <!-- <q-page>
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
</q-page> -->
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
