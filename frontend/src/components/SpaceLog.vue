<template>
  <div>
    <button @click="logType = 'hour'" :disabled="logType == 'hour'">Hour</button>
    <button @click="logType = 'day'" :disabled="logType == 'day'">Day</button>
    <button @click="logType = 'week'" :disabled="logType == 'week'">week</button>
    <button @click="logType = 'month'" :disabled="logType == 'month'">month</button>
    <br>
    <button @click="temperature = !temperature">Temperature</button>
    <button @click="humidity = !humidity">Humidity</button>
    <button @click="timePosition += 1">&lt;</button>
    <button @click="timePosition -= 1" :disabled="timePosition <= 1">&gt;</button>
    <button @click="getLogs">Refesh</button>
    <Chart :chartType=logType :chartData=chartData :temperature=temperature :humidity=humidity />
    <table>
      <thead>
        <tr>
          <th>time</th>
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
      humidity: false,
      logs: [],
      logType: 'hour',
      timeUnit: 'minute',
      timePosition: 1,
      time: 1000 * 60 * 60,
      startDate: new Date(),
    }
  },
  methods: {
    getLogs: async function() {
      let url = 'http://localhost:5000/frontend/spaces/' + this.space_id + '/log/' + this.timeUnit
      if (this.startDate) {
        url += '/' + Math.round(this.startDate.getTime() / 1000)
      }
      let response = await fetch(url)
      const object = await response.json()
      this.logs = object.logs
    },
    timeKeydown(e) {
      let number = /[0-9]/.test(e.key)
      if (!number && e.key != 'ArrowLeft' && e.key != 'ArrowRight' && e.key != 'Backspace') {
        e.preventDefault()
      }
    }
  },
  created: function(){
    this.startDate.setTime(new Date().getTime() - this.time * this.timePosition)
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
    },
    timePosition: function() {
      this.startDate.setTime(new Date().getTime() - this.time * this.timePosition)
      this.getLogs()
    }
  },
  computed: {
    chartData: function() {
      let data = []
      for (let log of this.logs) {
        data.push({
          date: Date.parse(log.date_time),
          min_temperature: log.min_temperature,
          max_temperature: log.max_temperature,
          avg_temperature: log.avg_temperature,
          min_humidity: log.min_humidity,
          max_humidity: log.max_humidity,
          avg_humidity: log.avg_humidity,
        })
      }
      return data
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
