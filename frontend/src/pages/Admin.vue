<template>
    <main>
        <AdminNavbar />
        <router-view></router-view>
        <div class="bg-page">
            <AdminDatePicker />
        </div>
    </main>
</template>

<script>
    import AdminNavbar from '../components/AdminNavbar.vue';
    import AdminDatePicker from "../components/AdminDatePicker.vue";

    export default {
        name: 'AdminPage',
        components: {
            AdminNavbar,
            AdminDatePicker,
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