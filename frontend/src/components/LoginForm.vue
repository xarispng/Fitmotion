<template>
    <form @submit.prevent="handleSubmit" class="form-container">
        <h1>Σύνδεση</h1>
        <input
            class="form-input"
            type="text"
            v-model="username"
            placeholder="Όνομα χρήστη"
            autocomplete="username"
            required
            style="margin-top: 10px;"/>
        <input
            class="form-input"
            type="password"
            v-model="password"
            placeholder="Κωδικός χρήστη"
            autocomplete="current-password"
            required/>
        <v-btn class="form-button" type="submit" style="margin-top: 0px;">
            Συνδεση
        </v-btn>
    </form>
</template>

<script>
    import api from '../api';
    import { ACCESS_TOKEN, REFRESH_TOKEN } from '../constants';

    export default {
        name: 'LoginForm',
        data() {
            return {
                username: '',
                password: '',
            };
        },
        methods: {
            async handleSubmit() {
                try {
                    const res = await api.post('/api/token/', {
                        username: this.username,
                        password: this.password,});

                    localStorage.setItem(ACCESS_TOKEN, res.data.access);
                    localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
                    
                    const userRes = await api.get('/api/users/me/', {
                        headers: {
                            'Authorization': `Bearer ${res.data.access}`
                        }
                    });

                    localStorage.setItem('user', JSON.stringify(userRes.data));
                    
                    if (userRes.data.is_superuser) {
                        this.$router.push('/adminpage');
                    } else {
                        this.$router.push('/userpage');
                    }
                } catch (error) {
                    this.username = '';
                    this.password = '';
                    alert('Λάθος όνομα χρήστη ή κωδικός.\nΠροσπαθήστε ξανά!');
                }
            },
        },
    };
</script>

<style scoped>
    @import '../styles/LoginForm.css';
</style>