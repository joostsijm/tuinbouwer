<template>
  <div class="hello">
    <ul>
      <li v-for="(space, index) in spaces" :key="index">
        naam: {{ space.name }}
        min: {{ space.min_temp }}
        max: {{ space.max_temp }}
        avg: {{ space.max_temp }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'Overview',
  data: function(){
    return {
      spaces: [
        { name: 't', min_temp: 15, max_temp: 30, avg_temp: 20}
      ]
    }
  },
  created: async function(){
    const response = await fetch("http://localhost:5000/frontend/spaces/overview");
    const object = await response.json();
    this.spaces = object
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
