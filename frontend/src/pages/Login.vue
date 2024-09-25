<template>
  <div class="bg-page">
    <LoginForm :route="apiRoute" :method="method" />
  </div>
</template>

<script>
  import LoginForm from "../components/LoginForm.vue";

  export default {
    name: "LoginPage",
    components: {
      LoginForm,
    },
    data() {
      return {
        apiRoute: "/api/token/",
        method: "login",
      };
    },
  };
</script>

<style scoped>
  @import '../styles/BackgroundImage.css'; 
</style>