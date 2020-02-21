<template>
  <div>
    <q-btn v-show="!signedIn" id="signin-button"></q-btn>
    <q-btn v-show="signedIn" @click="onSignOut">Sign Out</q-btn>
  </div>
</template>

<script>
export default {
  data() {
    return { signedIn: this.$store.state.userExists };
  },
  mounted() {
    window.gapi.signin2.render("signin-button", {
      onsuccess: this.onSignIn
    });
  },
  methods: {
    onSignIn() {
      let auth2 = window.gapi.auth2.getAuthInstance();
      let user = auth2.currentUser.get().getBasicProfile();
      this.$store.dispatch("login", user);
      this.signedIn = this.$store.state.userExists;
    },
    onSignOut() {
      let auth2 = window.gapi.auth2.getAuthInstance();
      this.$store.dispatch("logout");
      this.signedIn = this.$store.state.userExists;
      auth2.signOut();
    }
  }
};
</script>

<style></style>
