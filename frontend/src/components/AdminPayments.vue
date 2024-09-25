<template>
    <div id="app" class="center-content">
        <v-app>
            <div class="fixed-container">
                <v-container>
                    <v-row>
                        <v-col cols="12">
                            <v-card class="pay-card" v-if="dataReady">
                                <ol>
                                    <li v-for="(day, index) in weekend" :key="index" :style="{ color: 'white' }">
                                        {{ day }}
                                        <v-list class="custom-v-list">
                                            <v-list-item class="custom-v-list-item2" v-for="(data, index2) in payments[day]" :key="index2">
                                                <v-list-item-content v-if="day === 'ΛΟΙΠΕΣ' ">
                                                    {{ data.next_payment.split('-').slice(1).reverse().join('/') + " " + data.name + " " + data.surname.slice(0,5)}}
                                                </v-list-item-content>
                                                <v-list-item-content v-else>
                                                    {{ data.name + " " + data.surname.slice(0,5) }}
                                                </v-list-item-content>
                                                <v-list-item-action>
                                                    <div>
                                                        <v-btn icon @click="session_dialog=true, selectedUser = data">
                                                            <v-icon>mdi-plus</v-icon>
                                                        </v-btn>
                                                        <v-btn icon @click="pay_dialog=true, selectedUser = data">
                                                            <v-icon>mdi-currency-btc</v-icon>
                                                        </v-btn>
                                                    </div>
                                                </v-list-item-action>
                                            </v-list-item>
                                        </v-list>
                                    </li>
                                </ol>
                                <v-dialog v-model="pay_dialog" max-width="500px">
                                    <v-card>
                                        <v-card-title>
                                            <span class="headline" style="font-size: 18px !important;">Επιβεβαίωση Πληρωμής</span>
                                        </v-card-title>
                                        <v-card-text class="d-flex justify-center">
                                        </v-card-text>
                                            <v-card-text>Επιθυμείτε να συνεχίσετε με τη πληρωμή;</v-card-text>
                                        <v-card-actions>
                                            <v-spacer></v-spacer>
                                            <v-btn color="blue darken-1" text @click="pay_dialog=false">ΑΚΥΡΩΣΗ</v-btn>
                                            <v-btn color="blue darken-1" text @click="confirmPayment()">ΠΛΗΡΩΜΗ</v-btn>
                                        </v-card-actions>
                                    </v-card>
                                </v-dialog>
                                <v-dialog v-model="session_dialog" max-width="500px">
                                    <v-card>
                                        <v-card-title>
                                            <span class="headline" style="font-size: 18px !important;">Αλλαγή Προπονήσεων</span>
                                        </v-card-title>
                                        <v-card-text class="d-flex justify-center">
                                        <v-select
                                            v-if="selectedUser !== null"
                                            label="Επίλεξε Αριθμό Προπονήσεων"
                                            :items="[0, 1, 2]"
                                            v-model="selectedUser.temp_sessions"
                                            style="width: 70%;">
                                        </v-select>
                                        </v-card-text>
                                            <v-card-text>Επιθυμείτε να συνεχίσετε με την αλλαγή;</v-card-text>
                                        <v-card-actions>
                                            <v-spacer></v-spacer>
                                            <v-btn color="blue darken-1" text @click="session_dialog=false">ΑΚΥΡΩΣΗ</v-btn>
                                            <v-btn color="blue darken-1" text @click="changeSessionsPerWeek()">ΑΛΛΑΓΗ</v-btn>
                                        </v-card-actions>
                                    </v-card>
                                </v-dialog>
                            </v-card>
                        </v-col>
                    </v-row>
                </v-container>
            </div>
        </v-app>
    </div>
</template>

<script>
    import api from '../api.js';
    import { ref, reactive, onMounted } from 'vue';

    export default {
        name: 'AdminPayments',
        setup() {
            const weekend = ref([]);
            const payments = reactive({});
            const dataReady = ref(false);
            const pay_dialog = ref(false);
            const session_dialog = ref(false);
            const selectedUser = ref(null);

            const getWeekDates = async () => {
                const now = new Date();
                const dayOfWeek = now.getDay();
                const dayOffset = dayOfWeek === 0 ? 1 : 1 - dayOfWeek;
                const startOfWeek = now.getDate() + dayOffset;
                const baseDate = new Date(now.setDate(startOfWeek));
                weekend.value = [];
                for (let i = -1; i < 7; i++) {
                    const currentDate = new Date(baseDate);
                    currentDate.setDate(baseDate.getDate() + i);
                    const formattedDate = currentDate.getDate().toString().padStart(2, '0') + '/' +
                                        (currentDate.getMonth() + 1).toString().padStart(2, '0') + '/' +
                                        currentDate.getFullYear();
                    weekend.value.push(formattedDate);
                }
                const end_date = weekend.value[0];
                weekend.value.shift();
                weekend.value.push("ΛΟΙΠΕΣ");

                const response = await api.get('/api/profiles/by_week/', {
                    params: {
                        sow: weekend.value[0],
                        eow: weekend.value[6],
                    }
                });
                let data = await response.data;

                const rest_response = await api.get('/api/profiles/until/', {
                    params: {
                        end_date: end_date,
                    }
                });
                let rest_data = await rest_response.data;
                
                data = data.filter(item => item.sessions_per_week !== 0);
                rest_data = rest_data.filter(item => item.sessions_per_week !== 0);
                
                weekend.value.forEach(key => {
                    payments[key] = [];
                });
                data.forEach(data => {
                    const [year, month, day] = data.next_payment.split("-");
                    const formattedDate = `${day}/${month}/${year}`;    
                    payments[formattedDate].push(data);
                });

                rest_data.forEach(data => {  
                    payments["ΛΟΙΠΕΣ"].push(data);
                });

                dataReady.value = true;
            };

            const confirmPayment = async () => {
                const next_payment = calculateNextPayment(selectedUser.value);
                const profileData = {next_payment: next_payment, temp_sessions: 2};
                await api.patch(`/api/profiles/${selectedUser.value.user}/`, profileData, {headers: {'Content-Type': 'application/json'}});
                const data = {reschedules: 3};
                await api.patch(`/api/reschedules/${selectedUser.value.user}/`, data, {headers: {'Content-Type': 'application/json'}});
                window.location.reload();
            };

            const calculateNextPayment = (user) => {
                let date = new Date(user.next_payment);

                if (user.pay_plan === '4WEEK') {
                    date.setDate(date.getDate() + 28);
                } else {
                    date.setMonth(date.getMonth() + 1);
                }

                const formattedDate = date.toISOString().split('T')[0];

                return formattedDate;
            };

            const changeSessionsPerWeek = async () => {
                const profileData = {temp_sessions: selectedUser.value.temp_sessions};
                await api.patch(`/api/profiles/${selectedUser.value.user}/`, profileData, {headers: {'Content-Type': 'application/json'}});
                selectedUser.value = null;
                session_dialog.value = false;
            };

            onMounted(() => {
                getWeekDates();
            });

            return {
                weekend,
                payments,
                dataReady,
                pay_dialog,
                selectedUser,
                session_dialog,
                confirmPayment,
                calculateNextPayment,
                changeSessionsPerWeek,
            };
        },
    }
</script>

<style scoped>
    @import '../styles/AdminPayments.css';
</style>