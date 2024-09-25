<template>
    <div id="app" class="center-content">
        <v-app> 
            <div class="fixed-container"> 
                <v-container>
                    <h2 style="margin-top: 10px;">Προγραμματισμένες προπονήσεις</h2>
                    <v-row style="margin-top: 10px;">
                        <v-card class="card1">
                            <v-card-text>
                                <template v-if="fixedSessions && Object.keys(fixedSessions).length">
                                    <div v-for="(sessions, name) in fixedSessions" :key="name">
                                        {{ name }}:
                                        <v-btn 
                                            v-for="(session, index) in sessions" 
                                            :key="index" 
                                            @click="openDialog(name, index)" 
                                            style="font-size: 10px; padding: 0px 2px; margin: 4px;">
                                            {{ days[session[0]] + " " + session[1] + ":00" }}
                                        </v-btn>
                                    </div>
                                </template>
                                <template v-else>
                                    <div>Δεν υπάρχουν προγραμματισμένες προπονήσεις.</div>
                                </template>
                            </v-card-text>
                        </v-card>
                    </v-row>
                    <v-row>
                        <v-col class="d-flex justify-center" style="margin-top: 0px;">
                            <v-btn @click="dialog_add=true;" style="background: linear-gradient(to right, #a8d5ba, #7abf8e, #4a9e49); width: 150px; height: 30px;">ΚΑΤΑΧΩΡΗΣΗ</v-btn>
                        </v-col>
                    </v-row>
                    <v-dialog v-if="dialog" v-model="dialog" max-width="500px">
                        <v-card>
                            <v-card-title>
                                <span class="headline" style="font-size: 18px !important;">Αλλαγή Ημέρας/Ώρας</span>
                            </v-card-title>
                            <v-card-text class="d-flex justify-center">
                                <v-select
                                    label="Επίλεξε Ημέρα"
                                    :items="Object.keys(availableDays)"
                                    v-model="selectedDay"
                                    style="width: 70%;"/>
                            </v-card-text>
                            <v-card-text class="d-flex justify-center">
                                <v-select
                                    label="Επίλεξε Ώρα"
                                    :items="availableTimes"
                                    v-model="selectedTime"
                                    style="width: 70%;"/>
                            </v-card-text>
                            <v-card-text>Επιθυμείτε να συνεχίσετε με την αλλαγή;</v-card-text>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="blue darken-1" text @click="dialog = false">ΑΚΥΡΩΣΗ</v-btn>
                                <v-btn color="blue darken-1" text @click="fixedSessions[selectedName][selectedIndex] = [availableDays[selectedDay], selectedTime.slice(0,2)]; dialog=false;">ΑΛΛΑΓΗ</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                    <v-dialog v-model="dialog_add" max-width="500px">
                        <v-card>
                            <v-card-title>
                                <span class="headline" style="font-size: 18px !important;">Επιβεβαίωση Καταχώρησης</span>
                            </v-card-title>
                            <v-card-text>Επιθυμείτε να συνεχίσετε με τη καταχώρηση;</v-card-text>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="blue darken-1" text @click="dialog_del = false">ΑΚΥΡΩΣΗ</v-btn>
                                <v-btn color="blue darken-1" text @click="programFixed">ΚΑΤΑΧΩΡΗΣΗ</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </v-container>
            </div>
        </v-app>
    </div>
</template>

<script>
    import '@mdi/font/css/materialdesignicons.min.css';
    import api from '../api.js';

    export default {
        name: 'FixedProgram',
        data() {
            return {
                days: ['ΔΕΥΤΕΡΑ', 'ΤΡΙΤΗ', 'ΤΕΤΑΡΤΗ', 'ΠΕΜΠΤΗ', 'ΠΑΡΑΣΚΕΥΗ', 'ΣΑΒΒΑΤΟ'],
                fixedSessions: {},
                dialog: false,
                dialog_add: false,
                availableDays: {
                    'ΔΕΥΤΕΡΑ': 0, 
                    'ΤΡΙΤΗ': 1,  
                    'ΤΕΤΑΡΤΗ': 2,
                    'ΠΕΜΠΤΗ': 3,  
                    'ΠΑΡΑΣΚΕΥΗ': 4, 
                    'ΣΑΒΒΑΤΟ': 5,
                },
                availableTimes: [ '08:00', '09:00', '10:00', '11:00', '12:00',
                                '13:00', '14:00', '15:00', '16:00', '17:00',
                                '18:00', '19:00', '20:00', '21:00', '22:00'],
                selectedName: null,
                selectedIndex: null,
                selectedDay: null,
                selectedTime: null,
            };
        },
        methods: {
            async fetchSessions() {
                const response = await api.get('/api/fixed_sessions/');
                const newFixedSessions = {};

                for (const entry of response.data) {
                    const { user, day, hour } = entry;

                    const response2 = await api.get(`/api/users/${user}/`);
                    const fullName = response2.data.profile.name.slice(0, 5) + " " + response2.data.profile.surname.slice(0,5);
                    const sex = response2.data.profile.sex;
                    
                    if (!newFixedSessions[fullName]) {
                        this.$set(newFixedSessions, fullName, []);
                    }
                    newFixedSessions[fullName].push([day, hour, sex, user]);
                }
                this.fixedSessions = newFixedSessions;
            },
            openDialog(name, index) {
                this.selectedName = name;
                this.selectedIndex = index;
                const session = this.fixedSessions[name][index];
                this.selectedDay = this.days[session[0]];
                this.selectedTime = session[1] + ":00";
                this.dialog = true;
            },
            async programFixed() {
                let sessionsData = [];

                for (const [, value] of Object.entries(this.fixedSessions)) {
                    for (const data of value) {
                        sessionsData.push({
                            user: data[3],
                            sex: data[2],
                            hour: parseInt(data[1]),
                            date: this.getDate(data[0]),
                            fixed: true,
                        });
                    }
                }
                
                await api.post('/api/sessions/create_session/', { sessions: sessionsData }, {
                    headers: {'Content-Type': 'application/json'}});

                this.dialog_add = false;
            },
            getDate(dayNumber) {
                const today = new Date();
                const currentDay = today.getDay();
                
                const daysUntilNextWeek = 7 - currentDay + dayNumber;
                const dateOfNextWeek = new Date(today);
                dateOfNextWeek.setDate(today.getDate() + daysUntilNextWeek + 1);
                
                const year = dateOfNextWeek.getFullYear();
                const month = String(dateOfNextWeek.getMonth() + 1).padStart(2, '0');
                const day = String(dateOfNextWeek.getDate()).padStart(2, '0');
                
                return `${year}-${month}-${day}`;
            },
        },
        mounted() {
          this.fetchSessions();
        },
    }
</script>

<style scoped>
    @import '../styles/FixedProgram.css';
</style>