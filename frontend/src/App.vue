<template>
<div id="app">
  <h1>Tuinbouwer</h1>
  <h2>Spacess</h2>
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
      SpaceLog
  },
  data: function(){
    return {
      space_id: 0
    }
  },
  methods: {
    selectSpace(id) {
      this.space_id = id
    }
  }
}
</script>
