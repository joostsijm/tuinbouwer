<template>
  <div>
    <button @click="temperature = !temperature">Temperature</button>
    <button @click="humidity = !humidity">Humidity</button>
    <button @click="logType = 'day'" :disabled="logType == 'day'">Day</button>
    <button @click="logType = 'hour'" :disabled="logType == 'hour'">Hour</button>
    <button @click="logType = 'minute'" :disabled="logType == 'minute'">Minute</button>
    <input type="number" v-model="timeField" @keydown="timeKeydown($event)" placeholder="time" />
    <button @click="getLogs">Refesh</button>
    <span>{{ logs.length }} items</span>
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
    space_id: String
  },
  data: function() {
    return {
      temperature: true,
      humidity: false,
      logs: null,
      date_time: null,
      logType: 'hour',
      timeField: null,
      startDate: null,
    }
  },
  methods: {
    getLogs: async function() {
      this.logs = []
      let response = null
      if (this.startDate) {
        response = await fetch('http://localhost:5000/frontend/spaces/' + this.space_id + '/log/' + this.logType + '/' + this.startTimestamp)
      }
      else {
        response = await fetch('http://localhost:5000/frontend/spaces/' + this.space_id + '/log/' + this.logType)
      }
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
    this.getLogs()
  },
  watch: {
    space_id: function() {
      this.getLogs()
    },
    logType: function() {
      if (this.logType == 'day') {
        this.time == 31
      }
      this.getLogs()
    },
    timeField: function() {
      var newDate = new Date()
      if (this.logType == 'hour') {
        newDate.setDate(newDate.getDate() - this.timeField)
      }
      if (this.logType == 'minute') {
        newDate.setTime(newDate.getTime() - (this.timeField*60*60*1000))
      }
      this.startDate = newDate
    },
    startDate: function() {
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
    },
    startTimestamp: function() {
      return Math.round(this.startDate.getTime() / 1000)
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
