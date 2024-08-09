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
          <q-btn color="secondary" label="Upload" icon="upload" />
        </div>
      </div>
      <q-table :rows="rows" :columns="columns" row-key="name" flat bordered>
        <template v-slot:top-right>
          <q-input
            dense
            debounce="300"
            placeholder="Filter by filename"
            outlined
          >
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

<script setup>
defineOptions({
  name: "IndexPage",
});

const columns = [
  {
    name: "name",
    required: true,
    label: "Name",
    align: "left",
    field: (row) => row.name,
    format: (val) => `${val}`,
    sortable: true,
  },
  {
    name: "date",
    align: "center",
    label: "Date",
    field: "date",
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

const rows = [
  {
    name: "Document 01",
    date: "12/05/2024",
    status: "done",
    status_text: "green",
  },
  {
    name: "Document 02",
    date: "01/08/2024",
    status: "on progress",
    status_text: "purple",
  },
];
</script>
