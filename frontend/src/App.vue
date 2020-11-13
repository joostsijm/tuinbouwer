<template>
<div id="app">
  <h1>Tuinbouwer</h1>
  <h2>Spaces</h2>
  <ul>
    <li v-for="(space, index) in spaces" :key="index">
      {{ space.name }}
    </li>
  </ul>
  <Overview />
</div>
</template>

<script>
import Overview from './components/Overview.vue'

export default {
  name: 'App',
  components: {
      Overview
  },
  data: function(){
    return {
      spaces: []
    }
  },
  created: async function(){
    const gResponse = await fetch("http://localhost:5000/frontend/spaces");
    const gObject = await gResponse.json();
    this.flaskSpaces = gObject
  }
}
</script>

<style>
#app {
}
</style>
