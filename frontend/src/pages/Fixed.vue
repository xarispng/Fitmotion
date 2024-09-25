<template>
    <main>
        <AdminNavbar />
        <router-view></router-view>
        <div class="bg-page">
            <FixedProgram />
        </div>
    </main>
</template>

<script>
    import AdminNavbar from '../components/AdminNavbar.vue';
    import FixedProgram from "../components/FixedProgram.vue";

    export default {
        name: 'FixedProg',
        components: {
            AdminNavbar,
            FixedProgram,
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