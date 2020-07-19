<template>
  <div class="row fullscreen">
    <div class="left-panel col-7"></div>
    <div class="right-panel">
      <div>
        <img id="logo" src="../assets/logo.svg">
      </div>
      <div id="signin-btn">
        <SignIn />
      </div>
    </div>
  </div>
</template>

<script>
import SignIn from "./SignIn.vue"
export default {
  components: { SignIn }
}
</script>

<style scoped>
  .left-panel {
    background-image: url("../assets/background.svg");
    background-size: cover;
    padding: 5%;
    height: 100%;
  }
  .right-panel {
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    margin: 0 auto;
  }
  #signin-btn {
    margin: 0 auto;
  }
</style>