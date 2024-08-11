<template>
  <div class="row">
    <q-card class="col-0 col-sm-5 bg-primary xs-hide">
      <div class="row q-px-xl q-pb-xl full-height flex flex-center">
        <div class="text-h4 text-uppercase text-white" style="min-width: 220px">
          <span class="text-weight-bolder">Aora.</span>

          <p class="text-caption text-weight-bold">Ahead Of Rest, Always.</p>
        </div>
        <div class="text-white q-my-sm text-subtitle1">
          Please sign in to your account to get started!
        </div>
      </div>
    </q-card>

    <q-card class="col-12 col-sm-5">
      <div class="row q-pa-sm-sm q-pa-md">
        <div class="col-12">
          <q-card-section>
            <div class="q-mb-xl">
              <div
                class="flex justify-center text-h4 text-uppercase q-my-none text-weight-bold text-primary"
              >
                <span class="gt-xs">Login</span>
                <span class="lt-sm">Aora. </span>
              </div>
              <p
                class="text-caption text-weight-bold lt-sm flex justify-center text-primary"
              >
                Ahead Of Rest, Always.
              </p>
            </div>

            <q-form ref="form" class="q-gutter-md" @submit="submit">
              <q-input
                dense
                v-model="user.email"
                label="Email"
                name="Email"
                :rules="[
                  (val) => !!val || 'Email required!',
                  (val, rules) =>
                    rules.email(val) || 'Please enter a valid email address',
                ]"
              />

              <q-input
                dense
                v-model="user.password"
                :type="isPwd ? 'password' : 'text'"
                label="Password"
                name="password"
                :rules="[
                  (val) => !!val || 'Please enter a password',
                  (val) =>
                    !(val.length <= 8) || 'Please type more than 8 characters',
                ]"
              >
                <template v-slot:append>
                  <q-icon
                    :name="isPwd ? 'visibility_off' : 'visibility'"
                    class="cursor-pointer"
                    @click="isPwd = !isPwd"
                  />
                </template>
              </q-input>

              <div>
                <q-btn
                  class="full-width"
                  color="primary"
                  label="Login"
                  rounded
                  type="submit"
                />
              </div>
            </q-form>
          </q-card-section>
          <q-separator />
          <q-card-section>
            <div>
              <q-btn
                class="full-width"
                color="primary"
                label="Login with sso"
                rounded
                outline
                type="submit"
              />
            </div>
            <div class="q-mt-lg">
              <div class="q-mt-sm">
                Don't have an account yet?
                <router-link class="text-primary" to="/register">
                  Register
                </router-link>
              </div>
            </div>
          </q-card-section>
        </div>
      </div>
    </q-card>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
const isPwd = ref(true);

const user = reactive({
  email: null,
  password: null,
});

const form = ref(null);

const submit = async () => {
  if (form.value.validate()) {
    console.log("valid..");
  } else {
    console.log("err validate form...");
  }
};
</script>
