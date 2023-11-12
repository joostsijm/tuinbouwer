<template>
  <div class="list">
    <div v-if="spaces.length == 0">Loading...</div >
    <div v-for="(space, index) in spaces" :key="index" v-on:click="selectedSpace(index)" class="list_item">
      <h2>{{ space.name }}</h2>
      <table>
        <thead>
          <tr>
            <th>avg</th>
            <th>min</th>
            <th>max</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{ space.avg_temperature }}&#176;c</td>
            <td>{{ space.min_temperature }}&#176;c</td>
            <td>{{ space.max_temperature }}&#176;c</td>
          </tr>
          <tr>
            <td>{{ space.avg_humidity }}&#37;</td>
            <td>{{ space.min_humidity }}&#37;</td>
            <td>{{ space.max_humidity }}&#37;</td>
          </tr>
        </tbody>
      </table>
      <div>{{ space.date_time }}</div>
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
    const response = await fetch("http://api.tuinbouwer.joostsijm.nl/api/frontend/spaces/overview")
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
  margin: 0.5em;
  flex-wrap: wrap;
}

.list .list_item
{
  margin: 0.2em;
  padding: 0.4em;
  background-color: var(--primary-color);
  color: #fff;
  cursor: pointer;
  border-radius: 2px;
  width: 100%;
}

@media (min-width: 500px) {
  .list .list_item
  {
    width: 50%;
  }

  .list .list_item:first-child
  {
    margin-left: 0;
  }

  .list .list_item:last-child
  {
    margin-right: 0;
  }
}

@media (min-width: 800px) {
  .list .list_item
  {
    width: calc(100% / 3);
  }
}

.list .list_item h2
{
  margin: 0.2em 0;
}

.list_item table
{
  width: 100%;
}

.list_item table td,
.list_item table th
{
  text-align: left;
  padding: 0.1em 0;
  width: calc(100% / 3);
}

</style>
