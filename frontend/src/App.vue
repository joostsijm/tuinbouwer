<template>
<div id="app">
  <header>
    <h1>Tuinbouwer</h1>
    <div class="right">
      <div>
        <a href="https://github.com/joostsijm/tuinbouwer_server_api">Github</a>
      </div>
      <div>
        <span v-on:click="refresh()">Refresh</span>
      </div>
    </div>
  </header>
  <SpacesOverview @select-space="selectSpace" />
  <SpaceLog :space_id="space_id" v-if="space_id != 0"/>
</div>
</template>

<script>
import SpacesOverview from './components/SpacesOverview.vue'
import SpaceLog from './components/SpaceLog.vue'

export default {
  name: 'App',
  components: {
    SpacesOverview,
    SpaceLog,
  },
  data: function(){
    return {
      space_id: 0,
    }
  },
  methods: {
    selectSpace(id) {
      this.space_id = id
    },
    refresh() {
      window.location.reload();
    }
  }
}
</script>

<style scoped>
header
{
  display: flex
}

header .right
{
  width: 100%;
  display: flex;
  justify-content: right;
}

header .right div 
{
  padding: 0 1em;
  display: flex;
  justify-content: center;
  flex-direction: column;
  font-family: sans-serif;
}

header div a,
header div span
{
  color: #000;
  text-decoration: none;
  cursor: pointer;
}
</style>
