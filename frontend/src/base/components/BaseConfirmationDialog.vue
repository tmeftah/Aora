<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  text: {
    type: String,
    required: true,
  },
});

const emit = defineEmits(['update:modelValue', 'closeDialog', 'deleteElement']);
const internalDialog = ref(props.modelValue);

watch(
  () => props.modelValue,
  (newValue) => {
    internalDialog.value = newValue;
  }
);

function updateDialog(value) {
  emit('update:modelValue', value);
}

function closeDialog() {
  emit('closeDialog');
  emit('update:modelValue', false);
}
</script>

<template>
  <q-dialog id="confirmation-dialog" v-model="internalDialog" persistent @update:modelValue="updateDialog">
    <q-card style="width: 700px; max-width: 80vw;">
      <q-card-section class="row items-center text-white" style="background-color: #075070;">
        <q-icon name="delete" icon="delete" color="red" size="2rem" class="q-mr-sm" />
        <div class="text-h5 text-bold" id="dialog-title">{{ title }}</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>

      <q-separator />

      <q-card-section style="max-height: 50vh">
        <div class="text-h7" v-html="text" id="dialog-text"></div>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn label="Cancel" outline class="text-black" id="cancel-button" @click="closeDialog" style="color: #075070;"
          v-close-popup />
        <q-btn label="Delete" color="red" class="text-white" id="delete-button" @click="$emit('deleteElement')" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>
