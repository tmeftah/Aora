<script setup>
import BaseTable from "src/base/components/BaseTable.vue"
import { useUserStore } from "src/stores/userStore"
import { onMounted, ref } from "vue";
import { storeToRefs } from "pinia";

defineOptions({
  name: "ProfilePage",
});

const userStore = useUserStore();
const { currentUser, users } = storeToRefs(userStore);
onMounted(async () => {
  userStore.getCurrentUser();
  userStore.getAllUsers();
})

const columns = [
  {
    name: "username",
    required: true,
    label: "User",
    align: "left",
    field: (row) => row.username,
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



</script>

<template>

  <BaseTable title="👤 Profile Management" filterPlaceholder="Search for Profiles...">

    <template v-slot:dataTable>
      <q-table :rows="users" :columns="columns" row-key="name" flat bordered wrap-cells dense :filter="filter"
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
            <q-btn icon="edit" color="primary" round dense size="sm" disabled />
            <q-btn icon="delete" color="red" round dense size="sm" disabled />
          </q-td>
        </template>

        <template v-slot:no-data>
          <div class="full-width row flex-center q-pa-md">
            <q-icon name="warning" color="red" size="md" class="q-mr-sm" />
            <span class="text-grey-8 text-h6">No Users found, please kindly add some users. </span>
          </div>
        </template>
      </q-table>
    </template>


    <template v-slot:DialogBox>

    </template>

    <template v-slot:deleteModal>
    </template>


  </BaseTable>
</template>
