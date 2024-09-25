<template>
    <main>
        <AdminNavbar />
        <router-view></router-view>
        <div class="bg-page">
            <AdminPayments />
        </div>
    </main>
</template>

<script>
    import AdminNavbar from '../components/AdminNavbar.vue';
    import AdminPayments from "../components/AdminPayments.vue";

    export default {
        name: 'AdminPay',
        components: {
            AdminNavbar,
            AdminPayments,
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