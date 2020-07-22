<template>
  <div>
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
