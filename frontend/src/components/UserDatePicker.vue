<template>
  <div id="app" class="center-content">
    <v-app>
      <div class="fixed-container">
        <v-container>
          <v-row>
            <v-col cols="12" v-if="reschedules">
              <v-list v-if="chechDate()" class="custom-v-list">
                <v-list-item class="custom-v-list-item" style="background: linear-gradient(45deg, azure, cyan);">
                  <v-list-item-content class="d-flex justify-center align-center" style="width: 100%;">
                      <span style="font-size:large;">Επόμενη πληρωμή: {{ userInfo.profile.next_payment.split('-').reverse().slice(0, 2).join('/') }}</span>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
              <v-list v-else class="custom-v-list">
                <v-list-item class="custom-v-list-item" style="background: linear-gradient(45deg, #ff8080, pink);">
                  <v-list-item-content class="d-flex justify-center align-center">
                    <div>
                      <span style="font-size:large;">Εκκρεμεί πληρωμή</span>
                    </div>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
              <h3 style="margin-top: 10px;">Εβδομαδιαίες προπονήσεις ({{ weekSessions.length }}/{{ sessionsPerWeek }}):</h3>
              <v-list class="custom-v-list">
                <v-list-item v-for="(session, index) in weekSessions" :key="index" class="custom-v-list-item">
                  <v-list-item-content>
                    {{ formatSessionDate(session.date) }} {{ session.hour+":00" }}
                  </v-list-item-content>
                  <v-list-item-action>
                    <div>
                      <v-btn icon @click="setHourToDelete(index)">
                        <v-icon>mdi-clock</v-icon>
                      </v-btn>
                      <v-btn icon @click="setSessionToDelete(index)">
                        <v-icon>mdi-close</v-icon>
                      </v-btn>
                    </div>
                  </v-list-item-action>
                </v-list-item>
                <v-dialog v-model="dialog_hour" max-width="500px">
                  <v-card>
                    <v-card-title>
                      <span class="headline" style="font-size: 18px !important;">Αλλαγή Ώρας</span>
                    </v-card-title>
                    <v-card-text class="d-flex justify-center">
                      <v-select
                        label="Επίλεξε Ώρα"
                        :items="availableTimes"
                        v-model="selectedTime"
                        style="width: 70%;">
                      </v-select>
                    </v-card-text>
                    <v-card-text>
                      Προσοχή: Έχετε τη δυνατότητα να αλλάξετε την ώρα της προπόνησης το αργότερο 3 ώρες πριν την εναρξή της. Επιθυμείτε να συνεχίσετε με την αλλαγή ώρας;
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue darken-1" text @click="closeVDialogHour()">ΑΚΥΡΩΣΗ</v-btn>
                      <v-btn :disabled="selectedTime === null" color="blue darken-1" text @click="changeHour(sessionToDelete, selectedTime)">ΑΛΛΑΓΗ</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
                <v-dialog v-model="dialog_del" max-width="500px">
                  <v-card>
                    <v-card-title>
                      <span class="headline" style="font-size: 18px !important;">Διαγραφή Προπόνησης</span>
                    </v-card-title>
                    <v-card-text>
                      Προσοχή: Έχετε τη δυνατότητα τριών αναπληρώσεων (3) το μήνα.Επιθυμείτε να συνεχίσετε με τη διαγραφή;
                      <br><br>Διαθέσιμες Αναπληρώσεις: {{ reschedules.reschedules }}
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue darken-1" text @click="dialog_del = false">ΑΚΥΡΩΣΗ</v-btn>
                      <v-btn :disabled="this.reschedules.reschedules === 0" color="blue darken-1" text @click="removeSessionId(sessionToDelete)">ΔΙΑΓΡΑΦΗ</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-list>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="6" id="innerbox">
              <v-date-picker
              v-model="date"
              class="custom-picker"
              @input="updateAvailableTimes(date)"
              :allowed-dates="allowedDates"
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
            <v-col cols="12" sm="6" id="innerbox" v-show="availableTimes.length > 0 && sunday !== date && !selectedSessions.some(session => session.date === date)">
              <h2>Επίλεξε ώρα:</h2>
              <v-btn v-for="time in availableTimes" :key="time" @click="selectSession(time)" 
              class="ma-2" outlined :disabled="isTimeSlotTaken(time) 
              || weekSessions.length === sessionsPerWeek
              || weekSessions.some(obj => obj.reg_date === date)">
                {{ time }}
              </v-btn>
            </v-col>
          </v-row>
          <v-row v-if="selectedSessions.length > 0" style="margin-top: 30px; padding-bottom: 0px;">
            <v-col cols="12">
              <h2>Επιλεγμένες προπονήσεις:</h2>
              <v-list class="custom-v-list">
                <v-list-item v-for="(session, index) in selectedSessions" :key="index" class="custom-v-list-item">
                  <v-list-item-content>
                    {{ formatSessionDate(session.date) }} {{ session.time }}
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-btn icon @click="removeSession(index)">
                      <v-icon>mdi-close</v-icon>
                    </v-btn>
                  </v-list-item-action>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>
          <v-row v-if="selectedSessions.length > 0" style="margin-bottom: 80px;">
            <v-col cols="12" class="d-flex justify-center" style="padding-top: 0px;">
              <v-btn @click="dialog_add = true" :disabled="selectedSessions.length === 0" color="primary">
                ΚΑΤΑΧΩΡΗΣΗ
              </v-btn>
            </v-col>
            <v-dialog v-model="dialog_add" max-width="500px">
              <v-card>
                <v-card-title>
                  <span class="headline" style="font-size: 18px !important;">Καταχώρηση Προπονήσεων</span>
                </v-card-title>
                <v-card-text>Επιθυμείτε να συνεχίσετε με τη καταχώρηση;</v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="dialog_add = false">ΑΚΥΡΩΣΗ</v-btn>
                  <v-btn color="blue darken-1" text @click="submitSessions">ΚΑΤΑΧΩΡΗΣΗ</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-row>
        </v-container>
      </div>
    </v-app>
  </div>
</template>

<script>
    import '@mdi/font/css/materialdesignicons.min.css';
    import api from '../api.js';

    export default {
        name: 'UserDatePicker',
        data() {
            return {
                date: new Date(Date.now()).toLocaleDateString('en-CA'),
                availableTimesDict: {
                    '08:00': [0, 0], '09:00': [0, 0], '10:00': [0, 0], '11:00': [0, 0], '12:00': [0, 0],
                    '13:00': [0, 0], '14:00': [0, 0], '15:00': [0, 0], '16:00': [0, 0], '17:00': [0, 0],
                    '18:00': [0, 0], '19:00': [0, 0], '20:00': [0, 0], '21:00': [0, 0], '22:00': [0, 0]},
                currentWeekOffset: 0,
                sunday: null,
                weekStart: null,
                weekEnd: null,
                availableDates: [],
                availableTimes: [],
                selectedSessions: [],
                sessionsPerWeek: null,
                userInfo: null,
                weekSessions: [],
                ddates: {},
                dialog_add: false,
                dialog_del: false,
                dialog_hour: false,
                sessionToDelete: null,
                selectedTime: null,
                reschedules: null,
            };
        },
        methods: {
            async changeWeek(offset) {
                this.currentWeekOffset += offset;
                this.updateAvailableDates();
            },
            async updateAvailableDates() {
              const now = new Date();
              const dayOfWeek = now.getDay();
              const dayOffset = dayOfWeek === 0 ? 1 : 1 - dayOfWeek;
              const startOfWeek = now.getDate() + dayOffset;
              const baseDate = new Date(now.setDate(startOfWeek));
              this.weekStart = baseDate.toLocaleDateString('en-CA');
              this.weekEnd = new Date(baseDate.setDate(baseDate.getDate() + 5)).toLocaleDateString('en-CA');
              const today = (new Date(Date.now())).toLocaleDateString('en-CA');

              const sunday = new Date(now.setDate(startOfWeek - 1));
              this.sunday = sunday.toLocaleDateString('en-CA');

              const response = await api.get('/api/ddates/by_range/', {
                params: {
                  start: this.formatDateToDMY(this.weekStart),
                  end: this.formatDateToDMY(this.weekEnd),
                }});

              this.ddates = response.data.reduce((acc, { date, hour, whole_day }) => {
                if (!acc[date]) {acc[date] = [];}
                if (whole_day) {
                  acc[date] = "whole_day";
                } else if (hour !== null) {
                  if (hour === 8 || hour == 9) {
                    acc[date].push('0'+hour+':00');
                  } else {
                    acc[date].push(hour+':00');
                  }
                }
                return acc;
              }, {});

              const wholeDays = Object.keys(this.ddates).filter(key => this.ddates[key] === "whole_day");
              this.availableDates = [];
              let tempDate = (new Date(this.weekStart)).toLocaleDateString('en-CA');
              while (tempDate <= this.weekEnd) {
                if (tempDate >= today && !wholeDays.includes(tempDate)) {
                  this.availableDates.push(new Date(tempDate));
                }
                let interDate = (new Date(tempDate));
                interDate.setDate(interDate.getDate() + 1);
                tempDate = interDate.toLocaleDateString('en-CA');
              }

              this.selectedSessions = [];
            },
            allowedDates(val) {
                return this.availableDates.some(date => date.toLocaleDateString('en-CA') === val);
            },
            async updateAvailableTimes(date) {
              const now = new Date();
              const selectedDate = new Date(date);
              const isToday = selectedDate.toDateString() === now.toDateString();
              const cutoffTime = new Date(now.getTime() + 3 * 60 * 60 * 1000); // Calculate the cutoff time (3 hours from now)  
              this.availableTimes = [
              '08:00', '09:00', '10:00', '11:00', '12:00',
              '13:00', '14:00', '15:00', '16:00', '17:00',
              '18:00', '19:00', '20:00', '21:00', '22:00'
              ].filter(time => {
              if (isToday) {
                  const [hours, minutes] = time.split(':').map(Number);
                  const timeDate = new Date(now.getFullYear(), now.getMonth(), now.getDate(), hours, minutes);
                  return timeDate > cutoffTime;
              }
              return true;
              });

              const response = await api.get('/api/sessions/by_date/',{params: {date: this.date,}});
              const data = await response.data;

              Object.keys(this.availableTimesDict).forEach(hour => {
                this.$set(this.availableTimesDict, hour, [0,0]);
              });
                
              data.forEach(session => {
                if (session.hour === 8 || session.hour === 9) {session.hour = "0" + session.hour;}
                const timeSlot = session.hour + ":00";
                this.availableTimesDict[timeSlot][0] += 1;
                if (session.sex === 'MALE' && this.userInfo.profile.sex === 'MALE') {this.availableTimesDict[timeSlot][1] += 1;}
              });

              const fullHours = Object.keys(this.availableTimesDict).filter(key => 
                this.availableTimesDict[key][0] >= 8 || this.availableTimesDict[key][1] >= 3);

              if (this.ddates[this.date]) {
                this.availableTimes = this.availableTimes.filter(
                  value => !this.ddates[this.date].includes(value)
                  && !fullHours.includes(value));}

              if (fullHours.length > 0) {
                this.availableTimes = this.availableTimes.filter(
                  value => !fullHours.includes(value));}
            },
            chechDate() {
              const today = (new Date(Date.now())).toLocaleDateString('en-CA');
              const payment = this.userInfo.profile.next_payment;
              const todayDate = new Date(today);
              const paymentDate = new Date(payment);

              return todayDate <= paymentDate;
            },
            selectSession(time) {
                if (this.selectedSessions.length + this.weekSessions.length < this.sessionsPerWeek) {
                  if (!this.isDateTaken(this.date)) {
                    this.selectedSessions.push({ date: this.date, time: time });
                  }
                } else {
                  alert("Έχεις επιλέξει τον μέγιστο αριθμό προπονήσεων για αυτή την εβδομάδα.");
                }
            }, 
            async setHourToDelete(index) { // ΕΠΗΡΕΑΖΕΙ ΤΟ SELECT ΣΤΗΝ ΑΛΛΑΓΗ ΩΡΑΣ
              this.sessionToDelete = index;
              await this.updateAvailableTimes(this.weekSessions[index].reg_date);
              this.dialog_hour = true;
            },
            async closeVDialogHour() {
              await this.updateAvailableTimes(this.date);
              this.dialog_hour = false;
            },
            async changeHour(index, selectedTime) {
              await api.delete(`/api/sessions/${this.weekSessions[index].id}/`);
              const sessionData = [{
                user: this.userInfo.id,
                sex: this.userInfo.profile.sex,
                hour: parseInt(selectedTime.split(':')[0]),
                date: this.weekSessions[index].reg_date }];
              await api.post('/api/sessions/create_session/', { sessions: sessionData }, {
                  headers: {'Content-Type': 'application/json'}});
              await this.initializeComponent();
              this.dialog_hour = false;
            },
            setSessionToDelete(index) {
              this.sessionToDelete = index;
              this.dialog_del = true;
            },
            async removeSession(index) {
                this.selectedSessions.splice(index, 1);
                await this.updateAvailableTimes(this.date);
            },
            async removeSessionId(index) {
              const id = this.weekSessions[index].id;
              await api.delete(`/api/sessions/${id}/`);

              const data = {reschedules: this.reschedules.reschedules - 1};
              await api.patch(`/api/reschedules/${this.reschedules.user}/`, data, {headers: {'Content-Type': 'application/json'}});

              await this.initializeComponent();
              this.dialog_del = false;
            },
            async submitSessions() {
              if (this.selectedSessions.length > 0) {
                const sessionsData = this.selectedSessions.map(session => ({
                  user: this.userInfo.id,
                  sex: this.userInfo.profile.sex,
                  hour: parseInt(session.time.split(':')[0]),
                  date: session.date
                }));

                console.log(sessionsData);

                await api.post('/api/sessions/create_session/', { sessions: sessionsData }, {
                    headers: {'Content-Type': 'application/json'}});
                await this.initializeComponent();
              }
              this.dialog_add = false;
            },
            isDateTaken(date) {
                return this.selectedSessions.some(session => session.date === date);
            },
            isTimeSlotTaken(time) {
                return this.selectedSessions.some(session => session.date === this.date && session.time === time);
            },
            formatSessionDate(date) {
                return new Date(date).toLocaleDateString('el-GR', { weekday: 'long', day: 'numeric', month: 'short' });
            },
            formatDateToDMY(dateString) {
              const [year, month, day] = dateString.split('-');
              return `${day}/${month}/${year}`;
            },
            async fetchUserInfo() {
              const response = await api.get('/api/users/me/');
              this.userInfo = await response.data;
              if (!this.chechDate()) {
                this.userInfo.profile.sessions_per_week = this.userInfo.profile.temp_sessions
              }
              this.sessionsPerWeek= this.userInfo.profile.sessions_per_week;
              const response2 = await api.get('/api/reschedules/me/');
              this.reschedules = await response2.data;
            },
            async fetchSessions() {
              const response = await api.get('/api/sessions/by_week/', {
                params: {
                  sow: this.formatDateToDMY(this.weekStart),
                  eow: this.formatDateToDMY(this.weekEnd),
                  user: this.userInfo.id
                }});
              this.weekSessions = await response.data.map(item => ({
                  date: new Date(item.date),
                  hour: item.hour,
                  id: item.session_id,
                  reg_date: item.date,}));
            },
            async initializeComponent() {
              await this.fetchUserInfo();
              await this.updateAvailableDates();
              await this.updateAvailableTimes(this.date);
              await this.fetchSessions();
            },
          },
          mounted() {
            this.initializeComponent();
          },
    };
</script>

<style scoped>
    @import '../styles/UserDatePicker.css';
</style>