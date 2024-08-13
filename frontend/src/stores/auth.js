import { defineStore } from "pinia";
import { Notify } from "quasar";

const baseUrl = `${process.env.API}`;

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: JSON.parse(localStorage.getItem("user")) || null,
    token: localStorage.getItem("token") || null,
    refreshTokenTimeout: localStorage.getItem("refreshTokenTimeout") || null,
  }),

  getters: {
    current_user(state) {
      return state.user;
    },
  },

  actions: {
    async login(email, password) {
      const formData = new URLSearchParams();
      formData.append("grant_type", "password");
      formData.append("username", email);
      formData.append("password", password);
      try {
        const response = await fetch(`${baseUrl}/token`, {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: formData.toString(),
        });

        // Check for HTTP errors
        if (!response.ok) {
          // Extract error message if available
          const errorData = await response.json().catch(() => ({})); // Parsing might fail, default to empty object
          const errorMessage =
            errorData.detail || `Error: ${response.statusText}`;

          throw new Error(errorMessage);
        }

        // Parse the success response
        const data = await response.json();
        this.token = data.access_token;
        localStorage.setItem("token", this.token);

        Notify.create({
          color: "positive",
          position: "bottom",
          message: "you are loged in",
          icon: "done",
        });

        //
      } catch (error) {
        // Handle network errors and HTTP errors
        if (error.name === "TypeError") {
          // This typically indicates a network error
          console.error("Network error: Could not reach the server");
          Notify.create({
            color: "negative",
            position: "bottom",
            message: error.message,
            icon: "report_problem",
          });
        } else {
          // HTTP error, or some other error
          console.error(`API error: ${error.message}`);
          Notify.create({
            color: "negative",
            position: "bottom",
            message: error.message,
            icon: "report_problem",
          });
        }

        // You can rethrow the error or handle it in some way, e.g., user notification
        throw error; // Optionally rethrow if you want to propagate the error
      }
    },

    async getCurrentUser() {
      try {
        const response = await fetch(`${baseUrl}/users/me/`, {
          method: "GET",
          headers: {
            Accept: "application/json",
            Authorization: "Bearer " + this.token,
          },
        });

        if (!response.ok) {
          // Extract error message if available
          const errorData = await response.json().catch(() => ({})); // Parsing might fail, default to empty object
          const errorMessage =
            errorData.message || `Error: ${response.statusText}`;
          throw new Error(errorMessage);
        }

        const data = await response.json();
        this.user = data;
        localStorage.setItem("user", JSON.stringify(this.user));

        //
      } catch (error) {
        // Handle network errors and HTTP errors
        if (error.name === "TypeError") {
          // This typically indicates a network error
          console.error("Network error: Could not reach the server");
          Notify.create({
            color: "negative",
            position: "bottom",
            message: error.message,
            icon: "report_problem",
          });
        } else {
          // HTTP error, or some other error
          console.error(`API error: ${error.message}`);
          Notify.create({
            color: "negative",
            position: "bottom",
            message: error.message,
            icon: "report_problem",
          });
        }

        // You can rethrow the error or handle it in some way, e.g., user notification
      }
    },

    logout() {
      // api.post(`${baseUrl}/revoke-token`, {}, { credentials: "include" });

      this.stopRefreshTokenTimer();
      this.token = null;
      this.user = null;
      localStorage.removeItem("token");
      localStorage.removeItem("user");
    },

    startRefreshTokenTimer() {
      // parse json object from base64 encoded jwt token
      const jwtBase64 = this.token.split(".")[1];
      const jwtToken = JSON.parse(atob(jwtBase64));

      // set a timeout to refresh the token a minute before it expires
      const expires = new Date(jwtToken.exp * 1000);
      const timeout = expires.getTime() - Date.now() - 60 * 1000;
      this.refreshTokenTimeout = setTimeout(this.refreshToken, timeout);
    },

    async refreshToken() {
      this.token = await api.post(
        `${baseUrl}/refresh-token`,
        {
          headers: {
            Authorization: "Bearer " + this.token,
          },
        },
        { credentials: "include" }
      );
      this.startRefreshTokenTimer();
    },

    stopRefreshTokenTimer() {
      clearTimeout(this.refreshTokenTimeout);
    },
  },
});
