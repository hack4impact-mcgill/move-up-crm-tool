<template>
  <div>
    <div v-show="!signedIn">
      <q-btn no-caps id="signin-button" label="Log In" />
    </div>
    <div v-show="signedIn">
      <q-btn @click="onSignOut" no-caps flat label="Sign out" />
    </div>
  </div>
</template>

<script>
export default {
  name: "SignIn",
  data() {
    return { signedIn: false };
  },
  mounted() {
    window.gapi.signin2.render("signin-button", {
      onsuccess: this.onSignIn
    });
    this.signedIn = this.$store.getters.getSignedIn;
  },
  computed: {
    signedInState() {
      // Compute and watch auth state from Vuex
      let sign = this.$store.getters.getSignedIn;
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
      // Sign into Google OAuth and retrieve profile
      const auth2 = window.gapi.auth2.getAuthInstance();
      const user = auth2.currentUser.get().getBasicProfile();
      const idToken = auth2.currentUser.get().getAuthResponse().id_token;
      // Update state and navigate to Home page
      this.$store
        .dispatch("login", { email: user.getEmail(), token: idToken })
        .then(() => {
          const path = "/home";
          if (this.$router.currentRoute.path !== path) {
            this.$router.push({ path });
          }
        })
        .catch(err => {
          alert(err.response.data);
        });
    },
    onSignOut() {
      // Sign out of Google Auth2 object and update state
      let auth2 = window.gapi.auth2.getAuthInstance();
      auth2.signOut();
      // Update state and navigate to sign in page
      this.$store.dispatch("logout").then(() =>
        this.$router.push({ path: "/" }).catch(e => {
          console.log(e);
        })
      );
    }
  }
};
</script>

<style></style>
