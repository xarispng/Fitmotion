<template>
  <div id="app" class="center-content">
    <v-app>
      <div class="fixed-container">
        <v-container>
          <v-card class="main-card">
            <v-toolbar color="blue darken-1" dark flat>
                <v-toolbar-title class="text-center mx-auto">Επεξεργασία Χρηστών</v-toolbar-title>
            </v-toolbar>
            <template v-if="$vuetify.breakpoint.xsOnly">
              <v-btn-toggle v-model="tab" mandatory>
                <v-btn v-for="item in displayItems" :key="item" :value="item" text>{{ item }}</v-btn>
              </v-btn-toggle>
            </template>
            <template v-else>
              <v-tabs grow v-model="tab" wrap>
                <v-tab v-for="item in displayItems" :key="item" v-text="item"></v-tab>
              </v-tabs>
            </template>
            <v-tabs-items v-model="tab">
              <v-tab-item v-for="item in items" :key="item">
                <v-card flat>
                  <v-card v-if='item === "ΑΝΑΖΗΤΗΣΗ"'>
                    <v-card-text>
                      <v-autocomplete v-model="selectedUser" :items="searched_users"
                        label="Αναζήτηση χρήστη" :search-input.sync="search">
                      </v-autocomplete>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn :disabled="search === null" color="blue darken-1" text @click="showSessions">ΑΝΑΖΗΤΗΣΗ</v-btn>
                    </v-card-actions>
                    <v-card-text v-if="showSessionsClicked">
                      <template v-if="weeklySessions.info.length > 0">
                        Εβδομαδιαίες προπονήσεις:
                        <v-btn
                          v-for="(info,index) in weeklySessions.info"
                          :key="index"
                          class="ma-2"
                          @click="handleButtonClick(weeklySessions.ids[index])"
                          v-text="info">
                        </v-btn>
                      </template>
                      <template v-else> Δεν υπάρχουν προγραμματισμένες προπονήσεις για αυτή την εβδομάδα.</template>
                    </v-card-text>
                  </v-card>
                  <v-card v-if='item === "ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ"'>
                    <v-card-text>
                      <v-autocomplete v-model="selectedUser" :items="searched_users"
                        label="Αναζήτηση χρήστη" :search-input.sync="search2">
                      </v-autocomplete>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn :disabled="search2 === null" color="blue darken-1" text @click="showFixedSessions">ΑΝΑΖΗΤΗΣΗ</v-btn>
                    </v-card-actions>  
                    <v-card-text v-if="showSessionsClicked2">
                      <v-row>   
                        <v-col cols="12" sm="6" id="innerbox">
                          <v-btn
                            class="ma-2" outlined block :disabled="selectedFixedDay === day"
                            v-for="day in days" :key="day" v-text="day"
                            @click="selectFixedDay(day)" :class="dayButtonColor[day]">
                          </v-btn>
                        </v-col>
                        <v-col cols="12" sm="6" id="innerbox" v-if="selectedFixedDay">
                          <v-btn text
                            class="ma-2" outlined :disabled="isDisabled(time)"
                            v-for="time in availableTimes" :key="time" v-text="time"
                            :class="timeButtonColor[time]" @click="handleButtonClick(time)">
                          </v-btn>
                        </v-col>
                      </v-row>
                    </v-card-text>
                  </v-card>
                </v-card>
                <v-card v-if='item === "ΤΡΟΠΟΠΟΙΗΣΗ"'>
                  <v-card-text>
                    <v-autocomplete
                      v-model="selectedUser"
                      :items="searched_users"
                      label="Αναζήτηση χρήστη"
                      :search-input.sync="search3">
                    </v-autocomplete>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer> 
                    <v-btn :disabled="search3 === null" color="blue darken-1" text @click="displayForm">ΑΝΑΖΗΤΗΣΗ</v-btn>
                  </v-card-actions>
                  <v-card v-if='formClicked === true'>
                    <form @submit.prevent="submitForm" class="custom-form-container">
                      <label>
                        Όνομα:
                        <input type="text" v-model="form.name" required style="text-transform: uppercase;">
                      </label>
                      <label>
                        Επώνυμο:
                        <input type="text" v-model="form.surname" required style="text-transform: uppercase;">
                      </label>
                      <label>
                        Φύλλο:
                        <select v-model="form.sex" required>
                          <option value="MALE">Άνδρας</option>
                          <option value="FEMALE">Γυναίκα</option>
                        </select>
                      </label>
                      <label>
                        Εβδομαδιαίες προπονήσεις: (0: Ανενεργός χρήστης)
                        <input type="number" v-model="form.sessions_per_week" min="0" max="20" required>
                      </label>
                      <label>
                        Τηλέφωνο (προεραιτικό):
                        <input
                          type="text"
                          v-model="form.phone"
                          pattern="\d{10}"
                          title="Αριθμός 10 ψηφίων.">
                      </label>
                      <label>
                        Πλάνο Πληρωμής:
                        <select v-model="form.pay_plan" required>
                          <option value="MONTHLY">Μηνιαίο</option>
                          <option value="4WEEK">Ανά 4 εβδομάδες</option>
                        </select>
                      </label>
                      <label>
                        Ημέρα πληρωμής: (-∞ έως {{ payDayMax }})
                        <input 
                          type="number" 
                          v-model="form.pay_day"
                          :max="payDayMax">
                      </label>
                      <label>
                        Επόμενη Πληρωμή:
                        <input type="text" v-model="form.next_payment" required disabled style="background-color: #e0e0e0">
                      </label>
                      <label>
                        Username:
                        <input type="text" v-model="form.username" required>
                      </label>
                      <div>
                        <label>
                          Κωδικός πρόσβασης:
                        </label>
                        <div style="display: flex; align-items: center;">
                          <input style="width: 90%; margin-left: 20px;" type="text" v-model="form.password">
                          <span @click="generateRandomPassword" style="cursor: pointer; margin-left: 5px;">
                            <i class="mdi mdi-dialpad"></i>
                          </span>
                        </div>
                      </div>
                      <v-btn type="submit">ΤΡΟΠΟΠΟΙΗΣΗ</v-btn>
                    </form>
                  </v-card>
                </v-card>
                <v-card v-if='item === "ΕΙΣΑΓΩΓΗ"'>
                  <form @submit.prevent="submitForm" class="custom-form-container">
                    <label>
                      Όνομα:
                      <input type="text" v-model="form.name" required style="text-transform: uppercase;">
                    </label>
                    <label>
                      Επώνυμο:
                      <input type="text" v-model="form.surname" required style="text-transform: uppercase;">
                    </label>
                    <label>
                      Φύλλο:
                      <select v-model="form.sex" required>
                        <option value="MALE">Άνδρας</option>
                        <option value="FEMALE">Γυναίκα</option>
                      </select>
                    </label>
                    <label>
                      Εβδομαδιαίες προπονήσεις: (0: Ανενεργός χρήστης)
                      <input type="number" v-model="form.sessions_per_week" min="0" max="20" required>
                    </label>
                    <label>
                      Τηλέφωνο (προεραιτικό):
                      <input
                        type="text"
                        v-model="form.phone"
                        pattern="\d{10}"
                        title="Αριθμός 10 ψηφίων.">
                    </label>
                    <label>
                      Πλάνο Πληρωμής:
                      <select v-model="form.pay_plan" required>
                        <option value="MONTHLY">Μηνιαίο</option>
                        <option value="4WEEK">Ανά 4 εβδομάδες</option>
                      </select>
                    </label>
                    <label>
                      Ημέρα πληρωμής: (-∞ έως {{ payDayMax }})
                      <input 
                        type="number" 
                        v-model="form.pay_day"
                        :max="payDayMax" 
                        required>
                    </label>
                    <label>
                      Επόμενη Πληρωμή:
                      <input type="text" v-model="form.next_payment" required disabled style="background-color: #e0e0e0">
                    </label>
                    <label>
                      Username:
                      <input type="text" v-model="form.username" required>
                    </label>
                    <div>
                      <label>
                        Κωδικός πρόσβασης:
                      </label>
                      <div style="display: flex; align-items: center;">
                        <input style="width: 90%; margin-left: 20px;" type="text" v-model="form.password">
                        <span @click="generateRandomPassword" style="cursor: pointer; margin-left: 5px;">
                          <i class="mdi mdi-dialpad"></i>
                        </span>
                      </div>
                    </div>
                    <v-btn type="submit">ΕΙΣΑΓΩΓΗ</v-btn>
                  </form>
                </v-card>
              </v-tab-item>
            </v-tabs-items>
            <v-dialog v-model="dialog" max-width="500px">
              <v-card v-if="fixedSessionToDelete !== null || weeklySessions.info.length > 0">
                <v-card-title>
                  <span class="headline" style="font-size: 18px !important;">Επιβεβαίωση διαγραφής</span>
                </v-card-title>
                <v-card-text>Επιθυμείτε να συνεχίσετε με τη διαγραφή;</v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="dialog = false">ΑΚΥΡΩΣΗ</v-btn>
                  <v-btn v-if="fixedSessionToDelete !== null" color="blue darken-1" text @click="deleteFixedSession">ΕΠΙΒΕΒΑΙΩΣΗ</v-btn>
                  <v-btn v-if="weeklySessions.info.length > 0" color="blue darken-1" text  @click="deleteSession">ΕΠΙΒΕΒΑΙΩΣΗ</v-btn>
                </v-card-actions>
              </v-card>
              <v-card v-if="fixedSessionToDelete === null && weeklySessions.info.length <= 0">
                <v-card-title>
                  <span class="headline" style="font-size: 18px !important;">Επιβεβαίωση εισαγωγής</span>
                </v-card-title>
                <v-card-text>Επιθυμείτε να συνεχίσετε με την εισαγωγή;</v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="dialog = false">ΑΚΥΡΩΣΗ</v-btn>
                  <v-btn color="blue darken-1" text @click="addFixedSession">ΕΠΙΒΕΒΑΙΩΣΗ</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-card>
        </v-container>
      </div>
    </v-app>
  </div>
</template>
  
<script>
    import '@mdi/font/css/materialdesignicons.min.css';
    import api from '../api.js';

    export default {
        name: 'AdminTab',
        data() {
          return {
            items: ['ΑΝΑΖΗΤΗΣΗ', 'ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ', 'ΤΡΟΠΟΠΟΙΗΣΗ', 'ΕΙΣΑΓΩΓΗ'],
            days: ['ΔΕΥΤΕΡΑ', 'ΤΡΙΤΗ', 'ΤΕΤΑΡΤΗ', 'ΠΕΜΠΤΗ', 'ΠΑΡΑΣΚΕΥΗ', 'ΣΑΒΒΑΤΟ'],
            availableTimes: [ '08:00', '09:00', '10:00', '11:00', '12:00',
                              '13:00', '14:00', '15:00', '16:00', '17:00',
                              '18:00', '19:00', '20:00', '21:00', '22:00'], 
            tab: null, selectedUser: null,
            startOfWeek: null, endOfWeek: null,
            search: null, search2: null, search3: null,
            searched_users: [], searched_users_ids: [],
            weeklySessions: {info: [], ids: [],},
            showSessionsClicked: false, showSessionsClicked2: false,
            selectedFixedDay: null, selectedFixedTime: null,
            SessionToDelete: null, fixedSessionToDelete: null,
            fixed_sessions: {}, fixed_sessions_info: [],
            form: {user_id: '', username: '', password: '',
              name: '', surname: '', sex: '', sessions_per_week: '',
              phone: '', pay_plan: '', pay_day: '',
              next_payment: '',},
            dialog: false, formClicked: false, password: '',
          };
        },
        computed: {
          displayItems() {
            return this.$vuetify.breakpoint.smAndDown 
              ? ['ΑΝΑΖ', 'ΠΡΟΓΡ', 'ΤΡΟΠ', 'ΕΙΣΑΓ']
              : this.items;
          },
          dayButtonColor() {
            return this.days.reduce((colors, day) => {
              const index = this.days.indexOf(day);
              colors[day] = this.fixed_sessions[index] ? 'green lighten-3' : '';
              return colors;
            }, {});
          },
          timeButtonColor() {
            return this.availableTimes.reduce((colors, time) => {
              const index = this.days.indexOf(this.selectedFixedDay);
              colors[time] = this.fixed_sessions[index] === time ? 'green lighten-3' : '';
              return colors;
            }, {});
          },
          payDayMax() {
            return this.form.pay_plan === '4WEEK' ? 31 : 28;
          },
        },
        watch: {
          search: async function(query) {
            this.search_users(query);
          },
          search2: async function(query) {
            this.search_users(query);
          },
          search3: async function(query) {
            this.search_users(query);
          },
          tab(newValue) {
            if (newValue !== null) {
              this.selectedUser = null; this.formClicked = false;
              this.searched_users = []; this.searched_users_ids = [];
              this.showSessionsClicked = false; this.showSessionsClicked2 = false;
              this.weeklySessions = {info: [], ids: [],},
              this.selectedFixedDay = null; this.selectedFixedTime = null;
              this.fixed_sessions_info = []; this.fixed_sessions = {};
              this.fixedSessionToDelete = null; this.SessionToDelete = null;
              this.form = {user_id: '', username: '', password: '', name: '', surname: '',
              sex: '', sessions_per_week: '', phone: '', pay_plan: '', pay_day: '',
              next_payment: '',}
            }
          },
          'form.pay_day'(newDay) {
            this.form.next_payment = this.calculateNextPayment(newDay);
          },
          'form.pay_plan'() {
            this.form.next_payment = this.calculateNextPayment(this.form.pay_day);
          },
        },
        methods: {
          getCurrentWeek() {
            const currentDate = new Date();  // Current date and time
            const currentDay = currentDate.getDay();  // Get the current day of the week (0-6, 0 is Sunday)
            
            const sow = new Date();  
            sow.setDate(currentDate.getDate() - currentDay);  // Calculate the start of the week (Sunday)
            const eow = new Date(); 
            eow.setDate(sow.getDate() + 6);  // Calculate the end of the week (Saturday)

            this.startOfWeek = (sow.getDate()) + '/' + (sow.getMonth() + 1) + '/' + (sow.getFullYear());
            this.endOfWeek = (eow.getDate()) + '/' + (eow.getMonth() + 1) + '/' + (eow.getFullYear());
          },
          async search_users(query) {
            if (query) {
              const response = await api.get('/api/users/search/', { params: { query: query.toUpperCase() } });
              const data = await response.data;
              this.searched_users = [];
              this.searched_users = data.map(user => `${user.profile.name} ${user.profile.surname}`);
              this.searched_users_ids = data.map(user => `${user.profile.name} ${user.profile.surname} ${user.id}`);
            }
          },
          formatDateToDMY(dateString) {
            const [year, month, day] = dateString.split('-');
            return `${day}/${month}/${year}`;
          },
          async showSessions() {
            const response1 = await api.get('/api/users/search/', {params: {query: this.selectedUser.split(' ')[1].toUpperCase(),}});
            const fullName = this.selectedUser.split(' ')[0].toUpperCase() + ' ' + this.selectedUser.split(' ')[1].toUpperCase();
            const data = await response1.data;
            const fullNames = data.map(item => `${item.profile.name} ${item.profile.surname}`);
            const index = fullNames.indexOf(fullName);
            const user_id = data[index].id;
            const response2 = await api.get('/api/admsessions/by_week/', {
              params: {
                sow: this.startOfWeek,
                eow: this.endOfWeek,
                user: user_id
              }});
            const data2 = await response2.data;
            this.weeklySessions = {
              info: data2.map(entry => `${this.formatDateToDMY(entry.date)} ${entry.hour}:00`),
              ids: data2.map(entry => entry.session_id),
            };
            this.showSessionsClicked = true;
          },
          handleButtonClick(temp) {
            if (this.weeklySessions.info.length <= 0) {
              this.selectedFixedTime = temp;
              if (this.timeButtonColor[temp] === 'green lighten-3') {
                const day = this.days.indexOf(this.selectedFixedDay);
                this.fixedSessionToDelete = this.fixed_sessions_info.find(item => item.day === day);
                this.dialog = true;
              } else {
                this.fixedSessionToDelete = null;
                this.dialog = true;
              }
            }else {
              this.SessionToDelete = temp;
              this.dialog = true;
            }
          },
          async deleteSession() {
            await api.delete(`/api/sessions/${this.SessionToDelete}/`);
            const index = this.weeklySessions.ids.indexOf(this.SessionToDelete);
            if (index !== -1) {
              this.weeklySessions.ids.splice(index, 1);
              this.weeklySessions.info.splice(index, 1);
            }
            this.dialog = false;
            this.SessionToDelete = null;
          },
          async showFixedSessions() {
            const response1 = await api.get('/api/users/search/', {params: {query: this.selectedUser.split(' ')[1].toUpperCase(),}});
            const fullName = this.selectedUser.split(' ')[0].toUpperCase() + ' ' + this.selectedUser.split(' ')[1].toUpperCase();
            const data = await response1.data;
            const fullNames = data.map(item => `${item.profile.name} ${item.profile.surname}`);
            const index = fullNames.indexOf(fullName);
            const user_id = data[index].id;

            const response2 = await api.get('/api/fixed_sessions/by_user_id/', {params: {user_id: user_id}});
            this.fixed_sessions_info = await response2.data;
            this.$set(this, 'fixed_sessions', this.fixed_sessions_info.reduce((acc, entry) => {
              if (entry.hour === 8 || entry.hour ===9 ) {entry.hour = "0" + entry.hour;}
              acc[entry.day] = `${entry.hour}:00`; return acc;}, {}));

            this.showSessionsClicked2 = true;
          },
          selectFixedDay(day) { this.selectedFixedDay = day; },
          isDisabled(time) {
            const disabled = this.timeButtonColor[time] !== 'green lighten-3' && this.dayButtonColor[this.selectedFixedDay] === 'green lighten-3';
            return disabled;
          },
          async deleteFixedSession() {
            await api.delete(`/api/fixed_sessions/${this.fixedSessionToDelete.fixed_id}/`);
            this.fixed_sessions_info = this.fixed_sessions_info.filter(item => item !== this.fixedSessionToDelete);
            const day = this.days.indexOf(this.selectedFixedDay);
            this.$set(this.fixed_sessions, day, undefined)
            this.dialog = false;
            this.fixedSessionToDelete = null;
          },
          async addFixedSession() {
            if (this.selectedUser) {
              const response1 = await api.get('/api/users/search/', {params: {query: this.selectedUser.split(' ')[1].toUpperCase(),}});
              const fullName = this.selectedUser.split(' ')[0].toUpperCase() + ' ' + this.selectedUser.split(' ')[1].toUpperCase();
              const data = await response1.data;
              const fullNames = data.map(item => `${item.profile.name} ${item.profile.surname}`);
              const index = fullNames.indexOf(fullName);
              const user_id = data[index].id;
              const hour = this.selectedFixedTime.split(':')[0]; 
              const day = this.days.indexOf(this.selectedFixedDay);

              const fixedSessionData = {
                user: user_id,
                hour: parseInt(hour),
                day: parseInt(day),
              };
              
              await api.post('/api/fixed_sessions/', fixedSessionData, {headers: {'Content-Type': 'application/json'}});
              this.$set(this.fixed_sessions, day, hour+':00')
              const response3 = await api.get('/api/fixed_sessions/by_user_id/', {params: {user_id: user_id}});
              this.fixed_sessions_info = await response3.data;
            }
            this.dialog = false;
          },
          async submitForm() {
            if (this.formClicked) {
              let profileData = {};

              if (this.form.next_payment !== '') {
                const [day, month, year] = this.form.next_payment.split('/');
                const dateObject = `${year}-${month}-${day}`;

                profileData = {
                  user: this.form.user_id, name: this.form.name.toUpperCase(),
                  surname: this.form.surname.toUpperCase(), sex: this.form.sex,
                  sessions_per_week: this.form.sessions_per_week, phone: this.form.phone === '' ? null : this.form.phone,
                  pay_plan: this.form.pay_plan, next_payment: dateObject,
                };
              } else {
                profileData = {
                  user: this.form.user_id, name: this.form.name.toUpperCase(),
                  surname: this.form.surname.toUpperCase(), sex: this.form.sex,
                  sessions_per_week: this.form.sessions_per_week, phone: this.form.phone === '' ? null : this.form.phone,
                  pay_plan: this.form.pay_plan,
                };
              }
              
              const userData = {
                username: this.form.username, 
                password: this.form.password, 
                is_active: this.form.sessions_per_week === '0' ? false : true,
              };

              try {
                await api.patch(`/api/admusers/${this.form.user_id}/`, userData, {headers: {'Content-Type': 'application/json'}});
                try {
                  await api.patch(`/api/profiles/${this.form.user_id}/`, profileData, {headers: {'Content-Type': 'application/json'}});
                  alert('Επιτυχημένη τροποποίηση χρήστη!');
                }
                catch (error) {
                  alert('Αποτυχία τροποποίησης χρήστη!\nO συνδυασμός Όνομα-Επώνυμο πρέπει να είναι μοναδικός.');
                }                
              } catch (error) {
                alert('Αποτυχία τροποποίησης χρήστη!\nΤο username πρέπει να είναι μοναδικό.');
              }
            } else {
              const userData = {username: this.form.username, password: this.form.password,};
              const [day, month, year] = this.form.next_payment.split('/');
              const dateObject = `${year}-${month}-${day}`;
              try {
                const response = await api.post('/api/admusers/', userData, {headers: {'Content-Type': 'application/json'}});
                const data = await response.data;
                
                const profileData = {
                  user: data.id, name: this.form.name.toUpperCase(),
                  surname: this.form.surname.toUpperCase(), sex: this.form.sex,
                  sessions_per_week: this.form.sessions_per_week, phone: this.form.phone === '' ? null : this.form.phone,
                  pay_plan: this.form.pay_plan, next_payment: dateObject,
                };

                try {
                  await api.post('/api/profiles/', profileData, {headers: {'Content-Type': 'application/json'}});
                  alert('Επιτυχημένη δημιουργία χρήστη!');
                } catch (error) {
                  await api.delete(`/api/users/${data.id}/`);
                  alert('Αποτυχία δημιουργίας χρήστη!\nO συνδυασμός Όνομα-Επώνυμο πρέπει να είναι μοναδικός.');
                }
              } catch (error) {
                alert('Αποτυχία δημιουργίας χρήστη!\nΤο username πρέπει να είναι μοναδικό.');
              }
            }
            this.form = {user_id: '', username: '', password: '', name: '', surname: '', 
            sex: '', sessions_per_week: '', phone: '', pay_plan: '', pay_day: '', next_payment: '',}
          },
          async displayForm() {
            const response = await api.get('/api/users/search/', {params: {query: this.selectedUser.split(' ')[1].toUpperCase(),}});
            const fullName = this.selectedUser.split(' ')[0].toUpperCase() + ' ' + this.selectedUser.split(' ')[1].toUpperCase();
            const data = await response.data;
            const fullNames = data.map(item => `${item.profile.name} ${item.profile.surname}`);
            const index = fullNames.indexOf(fullName);
            this.form = {
              user_id: data[index].id,
              username: data[index].username,
              password: data[index].password,
              name: data[index].profile.name,
              surname: data[index].profile.surname,
              sex: data[index].profile.sex,
              sessions_per_week: data[index].profile.sessions_per_week,
              phone: data[index].profile.phone,
              pay_plan: data[index].profile.pay_plan,
              next_payment: data[index].profile.next_payment,
            }
            this.formClicked = true;
          },
          calculateNextPayment(day) {
            if (!day) return '';

            const today = new Date();
            today.setDate(day);

            if (this.form.pay_plan === '4WEEK') {
              today.setDate(today.getDate() + 28);
            } else {
              today.setMonth(today.getMonth() + 1);
            }
            const dd = String(today.getDate()).padStart(2, '0');
            const mm = String(today.getMonth() + 1).padStart(2, '0');
            const yyyy = today.getFullYear();

            return `${dd}/${mm}/${yyyy}`;
          },
          generateRandomPassword() {
            const randomPassword = Math.floor(1000 + Math.random() * 9000);
            this.form.password = randomPassword.toString();
          },
        },
        mounted() {
          this.getCurrentWeek();
        },
    };
</script>

<style scoped>
  @import '../styles/AdminEdit.css';
</style>