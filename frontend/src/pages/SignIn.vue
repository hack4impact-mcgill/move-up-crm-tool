<template>
  <div>
    <q-btn
      v-show="!signedIn"
      @click="onSignIn"
      no-caps
      flat
      id="signin-button"
    />
    <q-btn v-show="signedIn" @click="onSignOut" no-caps flat label="Sign out" />
    <button
      @click="onSignOut"
    >test sign out</button>
  </div>
</template>

<script>
export default {
  data() {
    return { signedIn: this.$store.state.userExists };
  },
  mounted() {
    window.gapi.signin2.render("signin-button", {
      longtitle: true,
      onsuccess: this.onSignIn
    });
  },
  methods: {
    async onSignIn() {
      let auth2 = window.gapi.auth2.getAuthInstance();
      let user = auth2.currentUser.get().getBasicProfile();
      await this.$store.dispatch("login", user).then(() => {
        this.signedIn = this.$store.state.userExists;
      })
      .then(() => this.$router.push("/home"))
    },
    onSignOut() {
      let auth2 = window.gapi.auth2.getAuthInstance();
      this.$store.dispatch("logout");
      this.signedIn = this.$store.state.userExists;
      auth2.signOut().then(() => {
        this.$router.push("/");
      })
    }
  }
};
</script>

<style></style>
