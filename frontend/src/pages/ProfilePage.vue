<script setup>
import BaseTable from "src/base/components/BaseTable.vue"

defineOptions({
  name: "ProfilePage",
});



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
