<template>
  <div>
    <q-btn v-show="!signedIn" id="signin-button"></q-btn>
    <q-btn v-show="signedIn" @click="onSignOut">Sign Out</q-btn>
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
  },
  methods: {
    onSignIn() {
      this.signedIn = true;
    },
    onSignOut() {
      let auth2 = window.gapi.auth2.getAuthInstance();
      auth2.signOut();
      this.signedIn = false;
    }
  }
};
</script>

<style></style>
