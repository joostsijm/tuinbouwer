<template>
  <div>
    <button v-on:click="getLogs">Refesh</button>
    <button v-on:click="log_type = 'day'">Day</button>
    <button v-on:click="log_type = 'hour'">Hour</button>
    <ul>
    </ul>
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
export default {
  name: 'SpaceLog',
  props: {
    space_id: String
  },
  data: function(){
    return {
      logs: null,
      date_time: null,
      log_type: 'day',
    }
  },
  methods: {
    getLogs: async function() {
      this.logs = []
      const response = await fetch("http://localhost:5000/frontend/spaces/" + this.space_id + "/log/" + this.log_type);
      const object = await response.json();
      this.logs = object.logs
    }
  },
  created: function(){
    this.getLogs()
  },
  watch: { 
    space_id: function() {
      this.getLogs()
    },
    log_type: function() {
      this.getLogs()
    },
  }
}
</script>

<style scoped>
ul {
  list-style-type: none;
  padding: 0;
}
</style>
