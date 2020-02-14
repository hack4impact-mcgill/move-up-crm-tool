<template>
  <div class="p-3 m-3">
    <q-btn color="primary" id="signin-button"></q-btn>
    <q-btn v-if="signedIn" color="primary" @click="onSignOut">Sign Out</q-btn>
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
    onSignIn(googleUser) {
      this.signedIn = true;
      // eslint-disable-next-line
      console.log("Logged in as: " + googleUser.getBasicProfile().getName());
    },
    onSignOut() {
      let auth2 = window.gapi.auth2.getAuthInstance();
      // eslint-disable-next-line
      auth2.signOut().then(() => console.log("User logged out."));
    }
  }
};
</script>

<style></style>
