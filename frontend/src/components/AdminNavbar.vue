<template>
    <nav class="navbar">
        <ul>
            <li v-if="isAuthenticated" class="nav-item">
                <router-link to="/adminpage">
                    <v-icon style="color: white;">mdi-home</v-icon>
                    <span>Αρχική</span>
                </router-link>
            </li>
            <li class="nav-item">
                <router-link v-if="isAuthenticated" to="/adminedit">
                    <v-icon style="color: white;">mdi-account-edit</v-icon>
                    <span>Επεξεργασία</span>
                </router-link>
            </li>
            <li class="nav-item">
                <router-link v-if="isAuthenticated" to="/payments">
                    <v-icon style="color: white;">mdi-currency-btc</v-icon>
                    <span>Πληρωμές</span>
                </router-link>
            </li>
            <li class="nav-item">
                <router-link v-if="isAuthenticated" to="/fixed">
                    <v-icon style="color: white;">mdi-calendar</v-icon>
                    <span>Πρόγραμμα</span>
                </router-link>
            </li>
            <li class="nav-item logout">
                <router-link v-if="isAuthenticated" to="/logout">
                    <v-icon style="color: white;">mdi-account</v-icon>
                    <span>Αποσύνδεση</span>
                </router-link>
            </li>
        </ul>
    </nav>
</template>


<script>
    import { isAuthenticated } from '../utils/auth';
    import '@mdi/font/css/materialdesignicons.min.css';

    export default {
        name: 'AdminNavbar',
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