<template>
  <q-page padding>
    <q-card flat bordered>
      <q-card-section>
        <div class="text-h6">Dashboard</div>
      </q-card-section>

      <q-separator />
      <div class="q-pa-md row items-start q-gutter-md">
        <q-card class="q-mb-sm">
          <q-card-section>
            <div class="text-h6">Active Users</div>
            <div class="text-h2 text-center text-bold">100</div></q-card-section
          >
        </q-card>

        <q-card>
          <q-card-section>
            <div class="text-h6">Number of Documents</div>
            <div class="text-center text-h2 text-bold">3524</div>
          </q-card-section>
        </q-card>
      </div>
    </q-card>
  </q-page>
</template>

<script setup>
defineOptions({
  name: "1Page",
});
</script>

<style scoped>
/* Add any custom styles for the dashboard here */
</style>
