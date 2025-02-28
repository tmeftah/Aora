import { defineStore } from "pinia";
import { Notify } from "quasar";

export const baseUrl = `${process.env.API}`;

export function showNotification(color, message, icon) {
  Notify.create({
    color,
    position: "bottom",
    message,
    icon,
  });
}

export async function apiRequest(method, endpoint, body = null, token = null) {
  const headers = {
    Accept: "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${baseUrl}${endpoint}`, {
    method,
    headers,
    body: body ? body.toString() : null,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Error: ${response.statusText}`);
  }

  return response.json();
}

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
    clearToken() {
      this.token = null;
      localStorage.removeItem("token");
    },

    async login(email, password) {
      /** Login functionality of AORA */

      const formData = new URLSearchParams({
        grant_type: "password",
        username: email,
        password: password,
      });

      try {
        const data = await apiRequest("POST", "/token", formData, this.token);

        this.token = data.access_token;
        localStorage.setItem("token", this.token);
        showNotification("positive", "You are successfully logged in", "done");
      } catch (error) {
        showNotification("negative", error.message, "report_problem");
        throw error;
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
