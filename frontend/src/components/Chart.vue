<template>
  <h3>Chart</h3>
  <div id="chart"></div>
</template>

<script>
import * as am4core from "@amcharts/amcharts4/core"
import * as am4charts from "@amcharts/amcharts4/charts"
// import am4themes_animated from "@amcharts/amcharts4/themes/animated"

// am4core.useTheme(am4themes_animated)

export default {
  name: 'Chart',
  props: {
    chartData: Array,
    logType: String,
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

      let dateAxis = chart.xAxes.push(new am4charts.DateAxis())
      dateAxis.baseInterval = {
        'timeUnit': this.timeUnit,
      }
      dateAxis.renderer.grid.template.location = 0

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
      this.generateArc()
      this.generateTemperatureLineSeries()
    },
    temperature: function() {
      if (this.temperature) {
        this.generateTemperatureLineSeries()
      }
      else {
        if (this.logType != 'minute') {
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
        if (this.logType != 'minute') {
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
      if (this.logType == 'day') {
        return 'hour'
      }
      if (this.logType == 'hour') {
        return 'second'
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
