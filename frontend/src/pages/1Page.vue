<template>
  <q-page padding>
    <q-card>
      <q-card-section>
        <div class="text-h6">Dashboard</div>
      </q-card-section>

      <q-separator />

      <q-card-section>
        <q-gutter class="q-mb-md">
          <q-card>
            <q-card-section>
              Widget 1
            </q-card-section>
          </q-card>

          <q-card>
            <q-card-section>
              Widget 2
            </q-card-section>
          </q-card>
        </q-gutter>
      </q-card-section>
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
