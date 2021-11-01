<template>
  <div>
    <ul>
      <li v-if="spaces.length == 0">Loading...</li>
      <li v-for="(space, index) in spaces" :key="index" v-on:click="selectedSpace(index)">
        naam: {{ space.name }}
        min: {{ space.min_temperature }}
        max: {{ space.max_temperature }}
        avg: {{ space.avg_temperature }}<br>
        update: {{ space.date_time }}
      </li>
    </ul>
  </div>
</template>

<script>

export default {
  name: 'SpacesOverview',
  data: function(){
    return {
      spaces: []
    }
  },
  created: async function(){
    const response = await fetch("http://api.tuinbouwer.ga/api/frontend/spaces/overview")
    this.spaces = await response.json()
  },
  methods: {
    selectedSpace(index) {
      this.$emit('select-space', this.spaces[index].id)
    }
  }
}
</script>

<style scoped>
ul {
  list-style-type: none;
  padding: 0;
}
</style>
