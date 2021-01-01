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
      // Sign into Google OAuth and retrieve profile
      let auth2 = window.gapi.auth2.getAuthInstance();
      let user = auth2.currentUser.get().getBasicProfile();
      // Update state and navigate to Home page
      this.$store
        .dispatch("login", user)
        .then(() => {
          const path = "/home";
          if (this.$router.currentRoute.path !== path) {
            this.$router.push({ path });
          }
        })
        .catch(() => {
          alert(
            "No Move Up user exists for this Google account! Please add user info to Airtable to log in."
          );
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
