<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container class="pt-0">
      <q-page>
        <div class="row" style="height: 100vh">
          <div class="col flex content-center justify-center">
            <router-view />
          </div>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
defineOptions({
  name: "LoginLayout",
});
</script>
