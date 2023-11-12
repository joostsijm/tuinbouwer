<template>
  <div class="controls">
    <div @click="decrementTime" :disabled="timePosition <= 1">&minus;</div>
    <span>{{ timePosition }}</span>
    <div @click="incrementTime">&plus;</div>
    <select name="SelectLogType" @change="logType = $event.target.value" v-model="selected">
      <option value="hour" :selected="true">Hour</option>
      <option value="day">Day</option>
      <option value="week">week</option>
      <option value="month">month</option>
    </select>
    <div @click="temperature = !temperature" :class="{ 'active_button' : temperature }">Temperature</div>
    <div @click="humidity = !humidity" :class="{ 'active_button' : humidity }">Humidity</div>
    <div @click="getLogs">Refresh</div>
    <div @click="getAdvice">Advice</div>
  </div>
  <ul v-if="advices.length != 0">
    <li v-for="(advice, index) in advices" :key="index">{{ advice }}</li>
  </ul>
  <Chart :chartType=logType :logs=logs :temperature=temperature :humidity=humidity />
  <table>
    <thead>
      <tr>
        <th>time</th>
        <th :colspan="logs.length && logs[0].min_temperature ? '3' : '1'">temperatuur</th>
        <th :colspan="logs.length && logs[0].min_humidity ? '3' : '1'">Humidity</th>
      </tr>
      <tr>
        <th></th>
        <th v-if="logs.length && logs[0].min_temperature">min</th>
        <th v-if="logs.length && logs[0].max_temperature">max</th>
        <th>avg</th>
        <th v-if="logs.length && logs[0].min_humidity">min</th>
        <th v-if="logs.length && logs[0].max_humidity">max</th>
        <th>avg</th>
      </tr>
    </thead>
    <tbody>
      <tr v-if="logs.length == 0">
        <td>Loading...</td>
      </tr>
      <tr v-for="(log, index) in logs" :key="index">
        <td>{{ log.date_time }}</td>
        <td v-if="log.min_temperature">{{ log.min_temperature }}&#176;c</td>
        <td v-if="log.max_temperature">{{ log.max_temperature }}&#176;c</td>
        <td>{{ log.avg_temperature }}&#176;c</td>
        <td v-if="log.min_humidity">{{ log.min_humidity }}&#37;</td>
        <td v-if="log.max_humidity">{{ log.max_humidity }}&#37;</td>
        <td>{{ log.avg_humidity }}&#37;</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import Chart from './Chart.vue'

export default {
  name: 'SpaceLog',
  components: {
    Chart,
  },
  props: {
    space_id: Number
  },
  data: function() {
    return {
      temperature: true,
      humidity: true,
      logs: [],
      logType: 'hour',
      timeUnit: 'minute',
      timePosition: 1,
      time: 1000 * 60 * 60,
      minTemperature: 0,
      maxTemperature: 0,
      selected: "hour",
      advices: []
    }
  },
  methods: {
    getLogs: async function() {
      let startDate = new Date()
      startDate.setTime(startDate.getTime() - this.time * this.timePosition)
      let url = 'http://api.tuinbouwer.joostsijm.nl/api/frontend/spaces/' + this.space_id + '/log/' + this.timeUnit
      url += '/' + Math.round(startDate.getTime() / 1000)
      let response = await fetch(url)
      const object = await response.json()
      this.logs = object.logs
    },
    getAdvice: async function() {
      let url = 'http://localhost:5000/api/frontend/spaces/' + this.space_id + '/advice'
      let response = await fetch(url)
      this.advices = await response.json()
    },
    decrementTime() {
      this.timePosition -= 1
      this.getLogs()
    },
    incrementTime() {
      this.timePosition += 1
      this.getLogs()
    }
  },
  created: function(){
    this.getLogs()
  },
  watch: {
    space_id: function() {
      this.getLogs()
    },
    logType: function() {
      this.timePosition = 1
      if (this.logType == 'hour') {
        this.time = 1000 * 60 * 60 
        this.timeUnit = 'minute'
      }
      if (this.logType == 'day') {
        this.time = 1000 * 60 * 60 * 24
        this.timeUnit = 'hour'
      }
      if (this.logType == 'week') {
        this.time = 1000 * 60 * 60 * 24 * 7
        this.timeUnit = 'day'
      }
      if (this.logType == 'month') {
        this.time = 1000 * 60 * 60 * 24 * 31
        this.timeUnit = 'day'
      }
      this.getLogs()
    }
  }
}
</script>

<style scoped>
.controls
{
  margin: 0.5em;
  display: flex;
  flex-wrap: wrap;
}

.controls span,
.controls div,
.controls select
{
  margin: 0.1em;
}

.controls span,
.controls select,
.controls div
{
  padding: 0.5em;
  margin: 0.1em;
  font-size: 0.9em;
  font-weight: bold;
  text-transform: uppercase;
  border-radius: 2px;
  border: 2px solid var(--primary-color);
}

.controls select:focus
{
  outline: none;
}

.controls div,
.controls select
{
  cursor: pointer;
  background: var(--primary-color);
  color: #fff;
}

.controls span,
.controls div.active_button
{
  background: #fff;
  color: var(--primary-color);
}

table {
  width: 100%;
  max-width: 800px;
}
</style>
