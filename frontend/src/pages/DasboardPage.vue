<template>
  <q-page padding>
    <q-card flat bordered>
      <q-card-section>
        <div class="text-h5 text-primary">Dashboard</div>
      </q-card-section>

      <q-separator />

      <div class="q-pa-md row q-gutter-md">
        <q-card class="dashboard-card">
          <q-card-section>
            <div class="text-h6 text-secondary">Active Users</div>
            <q-icon name="people" color="primary" size="lg" class="q-mt-sm" />
            <div class="text-h3 text-bold text-center text-primary">100</div>
          </q-card-section>
        </q-card>

        <q-card class="dashboard-card">
          <q-card-section>
            <div class="text-h6 text-secondary">Number of Documents</div>
            <q-icon name="description" color="blue" size="lg" class="q-mt-sm" />
            <div class="text-h3 text-bold text-center text-blue">3,524</div>
          </q-card-section>
        </q-card>

        <q-card class="dashboard-card">
          <q-card-section>
            <div class="text-h6 text-secondary">Storage Usage</div>
            <q-icon name="storage" color="orange" size="lg" class="q-mt-sm" />
            <div class="text-h3 text-bold text-center text-orange">75%</div>
          </q-card-section>
        </q-card>

        <q-card class="dashboard-card">
          <q-card-section>
            <div class="text-h6 text-secondary">System Status</div>
            <q-icon name="check_circle" color="green" size="lg" class="q-mt-sm" />
            <div class="text-h3 text-bold text-center text-green">OK</div>
          </q-card-section>
        </q-card>
      </div>
    </q-card>
  </q-page>
</template>

<script setup>
defineOptions({
  name: "DashboardPage",
});
</script>

<style scoped>
.dashboard-card {
  width: 100%;
  max-width: 250px;
  text-align: center;
  padding: 10px;
}
</style>
