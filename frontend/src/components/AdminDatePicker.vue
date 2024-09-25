<template>
  <div id="app" class="center-content">
    <v-app> 
      <div class="fixed-container"> 
        <v-container>
            <h2 style="margin-top: 10px;">Αρχική Σελίδα Διαχειριστή</h2>
            <v-row style="margin-top: 10px;">
                <v-col cols="12" sm="6" id="innerbox">
                    <v-date-picker
                    v-model="date"
                    class="custom-picker"
                    locale='el'
                    header-color="blue darken-1"
                    color="blue darken-1">
                        <template v-slot:header="{ displayDate }">
                            <v-row class="fill-height">
                                <v-btn text @click="changeWeek(-1)">
                                    <v-icon>mdi-chevron-left</v-icon>
                                </v-btn>
                                <v-spacer></v-spacer>
                                <v-btn text>
                                    {{ displayDate }}
                                </v-btn>
                                <v-spacer></v-spacer>
                                <v-btn text @click="changeWeek(1)">
                                    <v-icon>mdi-chevron-right</v-icon>
                                </v-btn>
                            </v-row>
                        </template>
                    </v-date-picker>
                </v-col>
                <v-col cols="12" sm="6" id="innerbox">
                    <h2>Διάλεξε ώρα:</h2>
                    <v-btn text
                    class="ma-2"
                    v-for="time in Object.keys(availableTimesDict)"
                    :key="time"
                    @click="selectSession(time)"
                    outlined
                    :disabled="isTimeSlotTaken(time)"
                    :selected="time === hour"
                    :class="buttonColors[time]">
                        <div class="d-flex flex-column justify-center align-center" style="height: 100%; width: 100%;">
                            <span>{{ time }}</span>
                            <div class="bottom-right-text">{{ getAvailableCount(time) }}/8</div>
                        </div>
                    </v-btn>
                    <v-card class="switch-card">
                        <div class="switch-wrapper">
                            <v-switch
                            v-model="day_switch"
                            inset
                            :label="switchLabel"
                            @change="onSwitchChange">
                            </v-switch>
                        </div>
                    </v-card>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" id="clients">
                    <v-list class="custom-v-list">
                        <v-list-item v-for="(session, index) in sessionClients" :key="index"
                        :class="[
                                    'custom-v-list-item',
                                    {
                                    'male-bg': session.user.profile.sex === 'MALE',
                                    'female-bg': session.user.profile.sex === 'FEMALE' && !session.user.is_superuser,
                                    'admin-bg': session.user.is_superuser,
                                    }
                                ]">
                            <v-list-item-content v-text="session.user.profile.name + ' ' + session.user.profile.surname"></v-list-item-content>
                            <v-list-item-action>
                                <v-btn icon @click="openDeleteDialog(session)" style="background-color: rgba(0, 0, 0, 0) !important;"> 
                                    <v-icon>mdi-close</v-icon>
                                </v-btn>
                            </v-list-item-action>
                        </v-list-item>
                        <v-dialog v-model="dialog_del" max-width="500px">
                            <v-card>
                                <v-card-title>
                                    <span class="headline" style="font-size: 18px !important;">Επιβεβαίωση Διαγραφής</span>
                                </v-card-title>
                                <v-card-text>Επιθυμείτε να συνεχίσετε με τη διαγραφή;</v-card-text>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn color="blue darken-1" text @click="dialog_del = false">ΑΚΥΡΩΣΗ</v-btn>
                                    <v-btn color="blue darken-1" text @click="confirmDelete">ΕΠΙΒΕΒΑΙΩΣΗ</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                        <v-list-item v-if="isTimeSlotTaken(selectedSessionTime) && selectedSessionTime !== '' && selectedSessionTime !== null" class="custom-v-list-item">
                            <v-list-item-content>Προσθήκη χρήστη</v-list-item-content>
                            <v-list-item-action>
                                <v-btn icon @click="dialog_search = true"> 
                                    <v-icon>mdi-plus</v-icon>
                                </v-btn>
                            </v-list-item-action>
                        </v-list-item>
                        <v-list-item v-if="isTimeSlotTaken(selectedSessionTime) && selectedSessionTime !== '' && !is_disabled() && selectedSessionTime !== null" class="custom-v-list-item">
                            <v-list-item-content>Αφαίρεση ώρας</v-list-item-content>
                            <v-list-item-action>
                                <v-btn icon @click="disableDate">
                                    <v-icon>mdi-minus</v-icon>
                                </v-btn>
                            </v-list-item-action>
                        </v-list-item>
                        <v-list-item v-if="isTimeSlotTaken(selectedSessionTime) && selectedSessionTime !== '' && is_disabled() && !day_switch" class="custom-v-list-item">
                            <v-list-item-content>Προσθήκη ώρας</v-list-item-content>
                            <v-list-item-action>
                                <v-btn icon @click="enableDate">
                                    <v-icon>mdi-plus</v-icon>
                                </v-btn>
                            </v-list-item-action>
                        </v-list-item>
                        <v-dialog v-model="dialog_search" max-width="500px">
                            <v-card>
                                <v-card-title>
                                    <span class="headline" style="font-size: 18px !important;">Προσθήκη χρήστη</span>
                                </v-card-title>
                                <v-card-text>
                                    <v-autocomplete
                                        v-model="selectedUser"
                                        :items="searched_users"
                                        label="Αναζήτηση χρήστη"
                                        :search-input.sync="search">
                                    </v-autocomplete>
                                </v-card-text>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn color="blue darken-1" text @click="dialog_search = false">ΑΚΥΡΩΣΗ</v-btn>
                                    <v-btn :disabled="!selectedUser" color="blue darken-1" text @click="addSession">ΠΡΟΣΘΗΚΗ</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                    </v-list>
                </v-col>
                <v-col class="d-flex justify-center" style="margin-top: -20px;">
                    <v-btn :disabled="clicked" @click="downloadSpreadsheet" style="background: linear-gradient(to right, #a8d5ba, #7abf8e, #4a9e49);">ΕΒΔΟΜΑΔΙΑΙΟ ΠΡΟΓΡΑΜΜΑ</v-btn>
                </v-col>
            </v-row>
        </v-container>
      </div>
    </v-app>
  </div>
</template>

<script>
    import '@mdi/font/css/materialdesignicons.min.css';
    import api from '../api.js';
    import * as XLSX from 'xlsx';
    import { saveAs } from 'file-saver';

    export default {
        name: 'AdminDatePicker',
        data() {
            return {
                date: new Date(Date.now()).toLocaleDateString('en-CA'),
                hour: new Date().toLocaleString('en-CA', { hour: 'numeric', hour12: false }) + ':00',
                availableTimesDict: {
                '08:00': 0, '09:00': 0, '10:00': 0, '11:00': 0, '12:00': 0,
                '13:00': 0, '14:00': 0, '15:00': 0, '16:00': 0, '17:00': 0,
                '18:00': 0, '19:00': 0, '20:00': 0, '21:00': 0, '22:00': 0},
                day_switch: false,
                currentWeekOffset: 0,
                selectedSessionDate: null,
                selectedSessionTime: null,
                selectedUser: null,
                sessionClients: [],
                sessionToDelete: null,
                dialog_del: false,
                dialog_search: false,
                search: null,
                searched_users: [],
                searched_users_ids: [],
                daily_sessions: null,
                disabledTimes: [],
                disabledTimesIds: [],
                weekend: [],
                spreadsheetData: null,
                spreadsheetDates: null,
                clicked: false,
            };
        },
        computed: {
            buttonColors() {
                return Object.keys(this.availableTimesDict).reduce((colors, time) => {
                    const hour = parseInt(time.split(':')[0]);
                    if (this.disabledTimes.includes(hour)) {
                        colors[time] = 'grey darken-1';
                    } else {
                        const getColor = (value) => {
                        if (value < 1) {
                            return 'green lighten-1';
                        } else if (value < 3) {
                            return 'green lighten-3';
                        } else if (value < 6) {
                            return 'yellow lighten-3';
                        } else if (value < 8) {
                            return 'orange lighten-2';
                        } else {
                            return 'red lighten-1';
                        }
                        };
                        colors[time] = getColor(this.availableTimesDict[time]);
                    }
                    return colors;
                }, {});
            },
            switchLabel() {
                return `Ημέρα: ${this.day_switch ? 'Απενεργοποιημένη' : 'Ενεργοποιημένη'}`;
            },
        },
        watch: {
            search: async function(query) {
                if (query) {
                    const response = await api.get('/api/users/search/', { params: { query: query.toUpperCase() } });
                    const data = await response.data;
                    this.searched_users = [];
                    this.searched_users = data.map(user => `${user.profile.name} ${user.profile.surname}`);
                    this.searched_users_ids = data.map(user => `${user.profile.name} ${user.profile.surname} ${user.id}`);
                }
            },
            async date(newDate) {
                await this.fetchDataFromSessions(newDate);
                this.dialog_del = false;
                this.dialog_search = false;
                this.sessionClients = [];
                this.selectedSessionTime = ''
            },
        },
        methods: {
            changeWeek(offset) {
                this.currentWeekOffset += offset;
            },
            isTimeSlotTaken(time) {
                return this.selectedSessionDate === this.date && this.selectedSessionTime === time;
            },
            async selectSession(time) {
                this.selectedSessionDate = '';
                this.selectedSessionTime = '';
                this.selectedSessionDate = this.date;
                this.selectedSessionTime = time;
                const hour = parseInt(time.split(':')[0]);
                await this.fetchUsersForTimeSlot(hour, this.selectedSessionDate);
            },
            async fetchUsersForTimeSlot(hour, date) {
                const response = await api.get('/api/admsessions/by_timeslot/', {
                    params: {
                        hour: parseInt(hour),
                        date: date,
                    }
                });
                this.sessionClients = await response.data;
            },
            async fetchDataFromSessions(date) {
                this.selectedSessionDate = date;

                const response1 = await api.get('/api/sessions/by_date/',{params: {date: date,}});
                this.daily_sessions = await response1.data;

                Object.keys(this.availableTimesDict).forEach(hour => {
                    this.$set(this.availableTimesDict, hour, 0);
                });
                
                this.daily_sessions.forEach(session => {
                    if (session.hour === 8 || session.hour === 9 ) {session.hour = "0" + session.hour;}
                    this.$set(this.availableTimesDict, session.hour+":00", this.availableTimesDict[session.hour+":00"] + 1);
                });
                
                this.disabledTimes = [];
                this.disabledTimesIds = [];
                this.day_switch = false;
                const response2 = await api.get('/api/ddates/by_date/',{params: {date: date,}});
                const data = await response2.data;
                data.some(ddate => {
                    if (ddate.whole_day === true) {
                        this.disabledTimes = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22];
                        this.disabledTimesIds.push(ddate.ddate_id);
                        this.day_switch = true;
                        return true;
                    } else if (!this.disabledTimes.includes(ddate.hour)) {
                        this.disabledTimes.push(ddate.hour);
                        this.disabledTimesIds.push(ddate.ddate_id);
                    }
                    return false;
                });
            },
            async onSwitchChange(value) {
                if (this.disabledTimesIds) {
                    for (const id of this.disabledTimesIds) {
                        await api.delete(`/api/ddates/${id}/`);
                    }
                }

                if (value) { //disableDay
                    const ddateData = {
                        date: this.selectedSessionDate,
                        whole_day: true,
                    };
                    
                    const response = await api.post('/api/ddates/', ddateData , {headers: {'Content-Type': 'application/json'}});
                    const data = await response.data;
                    this.disabledTimes = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22];
                    this.disabledTimesIds = []; 
                    this.disabledTimesIds.push(data.ddate_id);
                } else { //enableDay
                    this.disabledTimes = [];
                    this.disabledTimesIds = [];
                    }
                },
            openDeleteDialog(session) {
                this.sessionToDelete = session;
                this.dialog_del = true;
            },
            async confirmDelete() {
                await api.delete(`/api/sessions/${this.sessionToDelete.session_id}/`);
                this.sessionClients.splice(this.sessionClients.indexOf(this.sessionToDelete), 1);
                this.$set(this.availableTimesDict, this.selectedSessionTime, this.availableTimesDict[this.selectedSessionTime] - 1);
                this.dialog_del = false;
                this.sessionToDelete = null;
            },
            async addSession() {
                if (this.selectedUser) {
                    const response = await api.get('/api/users/search/', {params: {query: this.selectedUser.split(' ')[1].toUpperCase(),}});
                    const fullName = this.selectedUser.split(' ')[0].toUpperCase() + ' ' + this.selectedUser.split(' ')[1].toUpperCase();
                    const data = await response.data;
                    const fullNames = data.map(item => `${item.profile.name} ${item.profile.surname}`);
                    const index = fullNames.indexOf(fullName);
                    const hour = this.selectedSessionTime.split(':')[0]; 
                    
                    //const formattedNames = this.sessionClients.map((session, ) => {
                    //    return `${session.user.profile.name} ${session.user.profile.surname}`;
                    //});
                    
                    //if (!formattedNames.includes(this.selectedUser)) {
                        const sessionData = [{
                            user: data[index].id,
                            sex: data[index].profile.sex,
                            hour: parseInt(hour),
                            date: this.selectedSessionDate,
                        }];
                        await api.post('/api/sessions/create_session/', { sessions: sessionData }, {
                            headers: {'Content-Type': 'application/json'}});
                        this.$set(this.availableTimesDict, hour+":00", this.availableTimesDict[hour+":00"] + 1);
                        this.fetchUsersForTimeSlot(hour, this.selectedSessionDate);
                    //}
                }
                this.dialog_search = false;
            },
            is_disabled() {
                if (this.selectedSessionTime !== null) {
                    const hour = this.selectedSessionTime.split(':')[0]
                    if (this.disabledTimes.includes(parseInt(hour))) {
                        return true;
                    } else {
                        return false;
                    }
                } else {
                    return false;
                }
            },
            async disableDate() {
                const hour = parseInt(this.selectedSessionTime.split(':')[0])

                const ddateData = {
                    hour: parseInt(hour),
                    date: this.selectedSessionDate,
                    whole_day: false,
                };

                const response = await api.post('/api/ddates/', ddateData , {headers: {'Content-Type': 'application/json'}});
                const data = await response.data;
                this.disabledTimes.push(hour);
                this.disabledTimesIds.push(data.ddate_id);
            },
            async enableDate() {
                const hour = parseInt(this.selectedSessionTime.split(':')[0])
                const index = this.disabledTimes.indexOf(hour);

                await api.delete(`/api/ddates/${this.disabledTimesIds[index]}/`);
                this.disabledTimes.splice(index, 1);
                this.disabledTimesIds.splice(index, 1);
            },
            getAvailableCount(time) {
                return this.availableTimesDict[time] || 0;
            },
            async downloadSpreadsheet() {
                this.clicked = true;

                const now = new Date(this.date);
                const dayOfWeek = now.getDay();
                const dayOffset = dayOfWeek === 0 ? 1 : 1 - dayOfWeek;
                const startOfWeek = now.getDate() + dayOffset;
                const baseDate = new Date(now.setDate(startOfWeek));
                this.weekend = [];
                for (let i = 0; i < 6; i++) {
                    const currentDate = new Date(baseDate);
                    currentDate.setDate(baseDate.getDate() + i);
                    const formattedDate = currentDate.getDate().toString().padStart(2, '0') + '/' +
                                        (currentDate.getMonth() + 1).toString().padStart(2, '0') + '/' +
                                        currentDate.getFullYear();
                    this.weekend.push(formattedDate);
                }
                
                const result = this.weekend.reduce((acc, date) => {
                    acc[date] = [];
                    return acc;
                }, {});

                for (const date of this.weekend) {
                    await this.fetchDataFromSessions(date.split('/').reverse().join('-'));

                    for (const session of this.daily_sessions) {
                        const [year, month, day] = session.date.split('-');
                        const response = await api.get(`/api/users/${session.user}/`);
                        const data = await response.data;
                        result[`${day}/${month}/${year}`].push([data.profile.name + " " + data.profile.surname.slice(0, 5), session.hour + ":00"]);
                    }
                }
                await this.fetchDataFromSessions(this.date);
                
                const hours = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00'];
                this.spreadsheetDates = Object.keys(result);
                this.spreadsheetData = [['', ...this.spreadsheetDates]];

                hours.forEach(hour => {
                    const row = [hour];
                    this.spreadsheetDates.forEach(date => {
                        const users = result[date]
                            .filter(entry => entry[1] === hour)
                            .map(entry => `${entry[0]}`);
                        row.push(users.join('\n'));
                    });
                    this.spreadsheetData.push(row);
                });

                const ws = XLSX.utils.aoa_to_sheet(this.spreadsheetData);

                const columnWidths = [{ wch: 10 }]; // Width for the 'Hour' column
                for (let i = 0; i < this.spreadsheetDates.length; i++) {
                    columnWidths.push({ wch: 25 }); // Increased width for date columns
                }
                ws['!cols'] = columnWidths;
                ws['!rows'] = Array(this.spreadsheetData.length).fill({ hpt: 120 });

                // Set alignment for the entire sheet
                for (let R = 0; R < this.spreadsheetData.length; R++) {
                    for (let C = 0; C < this.spreadsheetData[R].length; C++) {
                        const cellAddress = XLSX.utils.encode_cell({ r: R, c: C });
                        ws[cellAddress] = {
                            v: this.spreadsheetData[R][C],
                            t: 's',
                            s: {
                                alignment: {
                                    vertical: 'center',
                                    horizontal: 'center',
                                    wrapText: true
                                },
                                font: { name: 'Arial', sz: 11 }
                            }
                        };
                    }
                }

                const wb = XLSX.utils.book_new();
                XLSX.utils.book_append_sheet(wb, ws, "Sheet1");

                const wopts = { 
                    bookType: 'xlsx', 
                    type: 'array',
                    cellStyles: true,
                    cellDates: true,
                    bookSST: false
                };

                const wbout = XLSX.write(wb, wopts);
                const blob = new Blob([wbout], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
                saveAs(blob, "fitmotion.xlsx");

                this.clicked = false;
            },
            async initializeComponent() {
                await this.fetchDataFromSessions(this.date);
                if (Object.keys(this.availableTimesDict).includes(this.hour)) {
                    await this.selectSession(this.hour);
                }
            },
        },
        mounted() {
            this.initializeComponent();
        },
    };
</script>
  
  
<style scoped>
    @import '../styles/AdminDatePicker.css';
</style>