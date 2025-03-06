<script setup>
import BaseTable from "src/base/components/BaseTable.vue"
import { useUserStore } from "src/stores/userStore"
import { onMounted } from "vue";
import { storeToRefs } from "pinia";

defineOptions({
  name: "ProfilePage",
});

const userStore = useUserStore();
const { currentUser } = storeToRefs(userStore);
onMounted(async () => {
  userStore.getCurrentUser();
})


</script>

<template>

  <BaseTable title="👤 Profile Management" filterPlaceholder="Search for Profiles...">

    <template v-slot:dataTable>
    </template>


    <template v-slot:DialogBox>

    </template>

    <template v-slot:deleteModal>
    </template>


  </BaseTable>
</template>
