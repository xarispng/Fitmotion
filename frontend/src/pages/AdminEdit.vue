<template>
    <main>
        <AdminNavbar />
        <router-view></router-view>
        <div class="bg-page">
            <AdminTab />
        </div>
    </main>
</template>

<script>
    import AdminNavbar from '../components/AdminNavbar.vue';
    import AdminTab from "../components/AdminTab.vue";

    export default {
        name: 'AdminPage',
        components: {
            AdminNavbar,
            AdminTab,
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