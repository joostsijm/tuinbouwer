<template>
  <h3>Chart |
    <span>{{ chartType }} ago | </span>
    <span>{{ chartData.length }} items | </span>
    <span v-if="temperature">Temperature | </span>
    <span v-if="humidity">Humidity</span>
  </h3>
    
    
  <div id="chart"></div>
</template>

<script>
import * as am4core from "@amcharts/amcharts4/core"
import * as am4charts from "@amcharts/amcharts4/charts"

export default {
  name: 'Chart',
  props: {
    chartType: String,
    chartData: Array,
    temperature: Boolean,
    humidity: Boolean,
  },
  mounted() {
    this.generateArc()
  },
  methods: {
    generateArc() {
      let chart = am4core.create('chart', am4charts.XYChart)

      chart.paddingRight = 20
      chart.data = this.chartData

      // https://www.amcharts.com/docs/v4/concepts/axes/date-axis/
      let dateAxis = chart.xAxes.push(new am4charts.DateAxis())
      dateAxis.baseInterval = {
        'timeUnit': this.timeUnit,
      }
      dateAxis.renderer.grid.template.location = 0
      dateAxis.gridIntervals.setAll([
        { timeUnit: 'minute', count: 1 },
        { timeUnit: 'minute', count: 5 },
        { timeUnit: 'minute', count: 10 },
        { timeUnit: 'minute', count: 30 },
        { timeUnit: 'hour', count: 1 },
        { timeUnit: 'day', count: 1 },
      ]);

      // https://www.amcharts.com/docs/v4/tutorials/wrapping-and-truncating-axis-labels/
      let label = dateAxis.renderer.labels.template;
      label.rotation = -45;
      label.horizontalCenter = 'right';
      label.verticalCenter = 'middle';

      let valueAxis = chart.yAxes.push(new am4charts.ValueAxis())
      valueAxis.tooltip.disabled = true
      valueAxis.renderer.minWidth = 35

      chart.cursor = new am4charts.XYCursor()
      this.chart = chart
    },
    generateTemperatureLineSeries() {
      this.minTemperatureSeries = this.chart.series.push(new am4charts.LineSeries())
      this.minTemperatureSeries.stroke = 'blue'
      this.minTemperatureSeries.dataFields.dateX = 'date'
      this.minTemperatureSeries.dataFields.valueY = 'min_temperature'
      this.minTemperatureSeries.tooltipText = '{valueY.value}'

      this.maxTemperatureSeries = this.chart.series.push(new am4charts.LineSeries())
      this.maxTemperatureSeries.stroke = 'red'
      this.maxTemperatureSeries.dataFields.dateX = 'date'
      this.maxTemperatureSeries.dataFields.valueY = 'max_temperature'
      this.maxTemperatureSeries.tooltipText = '{valueY.value}'

      this.avgTemperatureSeries = this.chart.series.push(new am4charts.LineSeries())
      this.avgTemperatureSeries.stroke = 'black'
      this.avgTemperatureSeries.dataFields.dateX = 'date'
      this.avgTemperatureSeries.dataFields.valueY = 'avg_temperature'
      this.avgTemperatureSeries.tooltipText = '{valueY.value}'
    },
    generateHumidityLineSeries() {
      this.minHumiditySeries = this.chart.series.push(new am4charts.LineSeries())
      this.minHumiditySeries.stroke = 'blue'
      this.minHumiditySeries.dataFields.dateX = 'date'
      this.minHumiditySeries.dataFields.valueY = 'min_humidity'
      this.minHumiditySeries.tooltipText = '{valueY.value}'

      this.maxHumiditySeries = this.chart.series.push(new am4charts.LineSeries())
      this.maxHumiditySeries.stroke = 'red'
      this.maxHumiditySeries.dataFields.dateX = 'date'
      this.maxHumiditySeries.dataFields.valueY = 'max_humidity'
      this.maxHumiditySeries.tooltipText = '{valueY.value}'

      this.avgHumiditySeries = this.chart.series.push(new am4charts.LineSeries())
      this.avgHumiditySeries.stroke = 'black'
      this.avgHumiditySeries.dataFields.dateX = 'date'
      this.avgHumiditySeries.dataFields.valueY = 'avg_humidity'
      this.avgHumiditySeries.tooltipText = '{valueY.value}'
    }
  },
  watch: { 
    chartData: function() {
      this.chart.dispose()
      this.generateArc()
      this.generateTemperatureLineSeries()
    },
    temperature: function() {
      if (this.temperature) {
        this.generateTemperatureLineSeries()
      }
      else {
        if (this.chartType != 'minute') {
          this.chart.series.removeIndex(
            this.chart.series.indexOf(this.minTemperatureSeries)
          ).dispose()
          this.chart.series.removeIndex(
            this.chart.series.indexOf(this.maxTemperatureSeries)
          ).dispose()
        }
        this.chart.series.removeIndex(
          this.chart.series.indexOf(this.avgTemperatureSeries)
        ).dispose()
      }
    },
    humidity: function() {
      if (this.humidity) {
        this.generateHumidityLineSeries()
      }
      else {
        if (this.chartType != 'minute') {
          this.chart.series.removeIndex(
            this.chart.series.indexOf(this.minHumiditySeries)
          ).dispose()
          this.chart.series.removeIndex(
            this.chart.series.indexOf(this.maxHumiditySeries)
          ).dispose()
        }
        this.chart.series.removeIndex(
          this.chart.series.indexOf(this.avgHumiditySeries)
        ).dispose()
      }
    },
  },
  computed: {
    timeUnit: function() {
      if (this.chartType == 'hour') {
        return 'minute'
      }
      if (this.chartType == 'day') {
        return 'hour'
      }
      if (this.chartType == 'week') {
        return 'day'
      }
      if (this.chartType == 'month') {
        return 'day'
      }
      return null
    }
  }
}
</script>

<style scoped>
#chart {
  width: 100%;
  height: 500px;
}
</style>
