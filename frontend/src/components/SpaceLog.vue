<template>
  <div>
    <button @click="logType = 'hour'" :disabled="logType == 'hour'">Hour</button>
    <button @click="logType = 'day'" :disabled="logType == 'day'">Day</button>
    <button @click="logType = 'week'" :disabled="logType == 'week'">week</button>
    <button @click="logType = 'month'" :disabled="logType == 'month'">month</button>
    <br>
    <button @click="temperature = !temperature">Temperature</button>
    <button @click="humidity = !humidity">Humidity</button>
    <button @click="previousTimePosition">&lt;</button>
    <button @click="nextTimePosition" :disabled="timePosition <= 1">&gt;</button>
    <button @click="getLogs">Refesh</button>
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
      maxTemperature: 0
    }
  },
  methods: {
    getLogs: async function() {
      let startDate = new Date()
      startDate.setTime(startDate.getTime() - this.time * this.timePosition)
      let url = 'http://localhost:5000/api/frontend/spaces/' + this.space_id + '/log/' + this.timeUnit
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
table {
  width: 100%;
  max-width: 500px;
}
</style>
