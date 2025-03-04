<template>

  <q-page class="full-page">
    <q-card flat bordered class="full-card">
      <q-card-section class="text-black">
        <div class="text-h4 text-bold">📊Dashboard </div>
      </q-card-section>

      <q-card-section class="toolbar">

      </q-card-section>

      <q-card-section class="table-container">
        <q-card flat bordered class="q-mt-sm column">

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
      </q-card-section>
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
  max-width: 200px;
  text-align: center;
  padding: 10px;
}

.model-select {
  min-width: 150px;
  max-width: 200px;
}

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
