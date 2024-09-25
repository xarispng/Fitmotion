<template>
  <main>
    <UserNavbar />
    <router-view></router-view>
    <div class="bg-page">
      <UserDatePicker />
    </div>
  </main>
</template>
  
<script>
  import UserNavbar from '../components/UserNavbar.vue';
  import UserDatePicker from "../components/UserDatePicker.vue";

  export default {
    name: 'UserPage',
    components: {
      UserDatePicker,
      UserNavbar,
    },
  };
</script>

<style scoped>
  @import '../styles/BackgroundImage.css'; 

  main {
    display: flex;
    flex-direction: column;
    height: 100vh;
    margin: 0;
  }
</style>