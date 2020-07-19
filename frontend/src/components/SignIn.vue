<template>
  <div>
    <div v-show="!signedIn">
      <q-btn @click="onSignIn" no-caps flat id="signin-button" label="Sign in" />
    </div>
    <div v-show="signedIn">
      <q-btn @click="onSignOut" no-caps flat label="Sign out" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return { signedIn: false };
  },
  mounted() {
    window.gapi.signin2.render("signin-button", {
      onsuccess: this.onSignIn
    });
    this.signedIn = this.$store.getters.getSign;
  },
  computed: {
    signedInState() {
      // Compute and watch auth state from Vuex
      let sign = this.$store.getters.getSign;
      return sign;
    }
  },
  watch: {
    signedInState(newState) {
      this.signedIn = newState;
    }
  },
  methods: {
    async onSignIn() {
      // Sign into Google Auth2 and retrieve profile
      let auth2 = window.gapi.auth2.getAuthInstance();
      let user = auth2.currentUser.get().getBasicProfile();
      // Update state and navigate to Home page
      this.$store.dispatch("login", user);
      this.$router.push("home").catch(() => {});
    },
    onSignOut() {
      // Sign out of Google Auth2 object and update state
      let auth2 = window.gapi.auth2.getAuthInstance();
      auth2.signOut();
      // Update state and navigate to sign in page
      this.$store.dispatch("logout");
      this.$router.push("/");
    }
  }
};
</script>

<style></style>
