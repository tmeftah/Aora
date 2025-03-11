<script setup>
import "../assets/css/base.css"

defineOptions({
  name: "comingSoon",
});


</script>

<template>
  <q-page class="full-page flex flex-center">
    <q-card flat bordered class="full-card q-pa-lg text-center">
      <q-card-section>
        <h1 class="text-h3 text-weight-bold" style="color:#075070">Coming Soon</h1>
        <p class=" text-h6 q-mt-md text-grey-7">
          This feature is under development. Stay tuned!
        </p>
      </q-card-section>

      <q-card-section>
        <slot name="errorMessageModal" id="error-msg-slot"></slot>
      </q-card-section>
    </q-card>
  </q-page>
</template>
