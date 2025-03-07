<script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { useMainStore } from "src/stores/mainStore";
import { getValidationRules } from "src/composables/useValidations";

const isPwd = ref(true);

const authStore = useAuthStore();
const router = useRouter();

const mainStore = useMainStore();

const { passwordValidationRules, emailValidationRules } = getValidationRules();

const user = reactive({
  email: null,
  password: null,
});

const form = ref(null);

async function submitLoginForm() {

  if (!form.value.validate()) {
    console.log("Invalid form");
    return;
  }

  try {
    await authStore.login(user.email, user.password);
    await authStore.getCurrentUser();

    if (authStore.user) {
      router.push("/");
    }
  } catch (error) {
    console.error("Login failed:", error);
  }
}
</script>


<template>
  <div class="row justify-center">
    <q-card class="col-sm-5 xs-hide no-shadow" square bordered id="leftcard" style="background-color:#075070">
      <div class="row q-px-xl q-pb-xl full-height content-center">
        <div class="text-h4 text-uppercase text-white">
          <span class="text-weight-bolder">Aora.</span>

          <p class="text-caption text-weight-bold">Ahead Of Rest, Always.</p>
        </div>
        <div class="text-white q-my-sm text-subtitle1">
          Please sign in to your account to get started!
        </div>
      </div>
    </q-card>

    <q-card class="col-12 col-sm-5 no-shadow" bordered id="rightcard">
      <div class="row q-pa-sm-sm q-pa-md">
        <div class="col-12">
          <q-card-section>
            <div class="q-mb-xl">
              <div class="flex justify-center text-h4 text-uppercase q-my-none text-weight-bold" style="color:#075070">
                <!-- <span class="gt-xs">Login</span> -->
                <span class="lt-sm">Aora. </span>
              </div>
              <p class="text-caption text-weight-bold lt-sm flex justify-center " style="color:#075070">
                Ahead Of Rest, Always.
              </p>
            </div>

            <q-form ref="form" class="q-gutter-md" @submit="submitLoginForm">
              <q-input outlined v-model="user.email" label="Email" name="Email" :rules=emailValidationRules />

              <q-input outlined v-model="user.password" :type="isPwd ? 'password' : 'text'" label="Password"
                name="password" :rules=passwordValidationRules>
                <template v-slot:append>
                  <q-icon :name="isPwd ? 'visibility_off' : 'visibility'" class="cursor-pointer"
                    @click="isPwd = !isPwd" />
                </template>
              </q-input>

              <div>
                <q-btn class="full-width" label="Login" rounded type="submit" style="color:#075070" />
              </div>
            </q-form>
          </q-card-section>

          <q-card-section>
            <!-- <div>
              <q-btn class="full-width" color="light-blue-13" label="Login with sso" rounded outline type="submit" />
            </div> -->
            <div class="q-mt-sm">
              <div class="q-mt-sm">
                <span> Don't have an account yet? </span>
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

<style scoped>
#leftcard {
  border-top-left-radius: 4px !important;
  border-bottom-left-radius: 4px !important;
  z-index: 2;
  right: -3px;
}
</style>
