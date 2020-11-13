<template>
  <div>
    <ul v-if="logs.length != 0">
      <li v-for="(log, index) in logs" :key="index">
        {{ log.date_time }}
        min: {{ log.min_temperature }}
        max: {{ log.max_temperature }}
        avg: {{ log.avg_temperature }}<br>
      </li>
    </ul>
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
      logs: [],
      date_time: null,
    }
  },
  created: async function(){
    const response = await fetch("http://localhost:5000/frontend/spaces/" + this.space_id + "/log/day");
    const object = await response.json();
    console.log(object)
    this.logs = object.logs
  }
}
</script>

<style scoped>
ul {
  list-style-type: none;
  padding: 0;
}
</style>
