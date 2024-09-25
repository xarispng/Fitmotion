<template>
    <nav class="navbar">
        <ul>
            <li v-if="isAuthenticated" class="nav-item">
                <router-link to="/userpage">
                    <v-icon style="color: white;">mdi-calendar-clock</v-icon>
                    Προπονήσεις
                </router-link>
            </li>
            <li v-if="isAuthenticated" class="nav-item">
                <router-link to="/gymrules">
                    <v-icon style="color: white;">mdi-book-variant</v-icon>
                    Κανόνες
                </router-link>
            </li>
            <li class="nav-item logout">
                <router-link v-if="isAuthenticated" to="/logout">
                    <v-icon style="color: white;">mdi-account</v-icon>Αποσύνδεση
                </router-link>
            </li>
        </ul>
    </nav>
</template>


<script>
    import { isAuthenticated } from '../utils/auth';
    import '@mdi/font/css/materialdesignicons.min.css';

    export default {
        name: 'UserNavbar',
        computed: {
            isAuthenticated() {
                return isAuthenticated();
            }
        },
    }
</script>

<style scoped>
    @import '../styles/UserNavbar.css';
</style>