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
    <q-card class="q-pa-md" style="min-width: 400px">
      <q-card-section>
        <div class="text-h6" id="dialog-title">{{ title }}</div>
      </q-card-section>

      <q-separator />

      <q-card-section>
        <span v-html="text" id="dialog-text"></span>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn label="Cancel" color="blue-grey" outline class="text-white" id="cancel-button" @click="closeDialog" />
        <q-btn label="Delete" color="red" class="text-white" id="delete-button" @click="$emit('deleteElement')" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>
