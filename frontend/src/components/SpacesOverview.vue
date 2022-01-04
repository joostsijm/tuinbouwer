<template>
  <div class="list">
    <div v-if="spaces.length == 0">Loading...</div >
    <div v-for="(space, index) in spaces" :key="index" v-on:click="selectedSpace(index)" class="list_item">
      <h2>{{ space.name }}</h2>
      <div class="details">
        <span>min: {{ space.min_temperature }}</span>
        <span>max: {{ space.max_temperature }}</span>
        <span>avg: {{ space.avg_temperature }}</span>
      </div>
      <div>update: {{ space.date_time }}</div>
    </div>
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
.list
{
  display: flex;
  margin-bottom: 0.5em;
}

.list .list_item
{
  margin: 0.2em;
  padding: 0.4em;
  background-color: lightgray;
}

.list .list_item h2
{
  margin: 0.2em 0;
}

.list .list_item .details
{
  display: flex;
}

.list .list_item .details span:not(:first-child)
{
  padding: 0 0.5em;
}
</style>
