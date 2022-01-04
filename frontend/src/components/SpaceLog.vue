<template>
  <div>
    <div class="controls">
      <select name="SelectLogType" @change="logType = $event.target.value" v-model="selected">
        <option value="hour" :selected="true">Hour</option>
        <option value="day">Day</option>
        <option value="week">week</option>
        <option value="month">month</option>
      </select>
      <div @click="nextTimePosition" :disabled="timePosition <= 1">&minus;</div>
      <span>{{ timePosition }}</span>
      <div @click="previousTimePosition">&plus;</div>
      <div @click="temperature = !temperature" :class="{ 'active_button' : temperature }">Temperature</div>
      <div @click="humidity = !humidity" :class="{ 'active_button' : humidity }">Humidity</div>
      <div @click="getLogs">Refesh</div>
    </div>
    <Chart :chartType=logType :logs=logs :temperature=temperature :humidity=humidity />
    <table>
      <thead>
        <tr>
          <th>time</th>
          <th colspan="3">temperatuur</th>
          <th colspan="3">Humidity</th>
        </tr>
        <tr>
          <th></th>
          <th>min</th>
          <th>max</th>
          <th>avg</th>
          <th>min</th>
          <th>max</th>
          <th>avg</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="logs.length == 0">
          <td>Loading...</td>
        </tr>
        <tr v-for="(log, index) in logs" :key="index">
          <td>{{ log.date_time }}</td>
          <td>{{ log.min_temperature }}</td>
          <td>{{ log.max_temperature }}</td>
          <td>{{ log.avg_temperature }}</td>
          <td>{{ log.min_humidity }}</td>
          <td>{{ log.max_humidity }}</td>
          <td>{{ log.avg_humidity }}</td>
        </tr>
      </tbody>
    </table>
  </div>
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
      selected: "hour"
    }
  },
  methods: {
    getLogs: async function() {
      let startDate = new Date()
      startDate.setTime(startDate.getTime() - this.time * this.timePosition)
      let url = 'http://api.tuinbouwer.ga/api/frontend/spaces/' + this.space_id + '/log/' + this.timeUnit
      url += '/' + Math.round(startDate.getTime() / 1000)
      let response = await fetch(url)
      const object = await response.json()
      this.logs = object.logs
    },
    nextTimePosition() {
      this.timePosition -= 1
      this.getLogs()
    },
    previousTimePosition() {
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
  display: flex;
}

.controls span,
.controls div,
.controls select
{
  margin: 0.1em;
}

.controls span,
.controls div 
{
  padding: 0.5em;
  margin: 0.1em;
  font-size: 0.9em;
  font-weight: bold;
  text-transform: uppercase;
}

.controls div
{
  cursor: pointer;
  background: var(--primary-color);
  color: #fff;
  border-radius: 2px;
}

.controls div.active_button
{
  background: #fff;
  border: 2px solid var(--primary-color);
  color: var(--primary-color);
}

table {
  width: 100%;
  max-width: 500px;
}
</style>
