<template>
  <div class="container">
    <h3>{{ logs.length }} items</h3>
    <div id="chart"></div>
  </div>
</template>

<script>
import * as am4core from "@amcharts/amcharts4/core"
import * as am4charts from "@amcharts/amcharts4/charts"

export default {
  name: 'Chart',
  props: {
    chartType: String,
    logs: Array,
    temperature: Boolean,
    humidity: Boolean,
  },
  data: function() {
    return {
      minTemperature: -1000,
      maxTemperature: 1000,
      minHumidity: -1000,
      maxHumidity: 1000,
    }
  },
  mounted() {
    this.generateChart()
  },
  methods: {
    generateChart() {
      let chart = am4core.create('chart', am4charts.XYChart)

      chart.paddingRight = 20
      chart.data = this.chartData()

      // https://www.amcharts.com/docs/v4/concepts/axes/date-axis/
      this.dateAxis = chart.xAxes.push(new am4charts.DateAxis())
      this.dateAxis.baseInterval = {
        'timeUnit': this.timeUnit,
      }
      this.dateAxis.renderer.grid.template.location = 0
      this.dateAxis.gridIntervals.setAll([
        { timeUnit: 'minute', count: 1 },
        { timeUnit: 'minute', count: 5 },
        { timeUnit: 'minute', count: 10 },
        { timeUnit: 'minute', count: 30 },
        { timeUnit: 'hour', count: 1 },
        { timeUnit: 'day', count: 1 },
      ]);

      // https://www.amcharts.com/docs/v4/tutorials/wrapping-and-truncating-axis-labels/
      let label = this.dateAxis.renderer.labels.template;
      label.rotation = -45;
      label.horizontalCenter = 'right';
      label.verticalCenter = 'middle';

      this.temperatureAxis = chart.yAxes.push(new am4charts.ValueAxis())
      this.temperatureAxis.title.text = "Temperature";
      this.temperatureAxis.renderer.minWidth = 35
      this.temperatureAxis.renderer.minGridDistance = 40;
      // this.temperatureAxis.extraMin = 0.1;
      // this.temperatureAxis.extraMax = 0.1;
      this.temperatureAxis.min = parseFloat(this.minTemperature) - 1;
      this.temperatureAxis.max = parseFloat(this.maxTemperature) + 1;

      // Second value axis
      this.humidityAxis = chart.yAxes.push(new am4charts.ValueAxis());
      this.humidityAxis.title.text = "Humidity";
      this.humidityAxis.renderer.minWidth = 35
      this.humidityAxis.renderer.minGridDistance = 40;
      this.humidityAxis.renderer.opposite = true;
      this.humidityAxis.min = parseFloat(this.minHumidity) - 1;
      this.humidityAxis.max = parseFloat(this.maxHumidity) + 1;

      chart.cursor = new am4charts.XYCursor()
      this.chart = chart
    },
    generateTemperatureLineSeries() {
      this.minTemperatureSeries = this.chart.series.push(new am4charts.LineSeries())
      this.minTemperatureSeries.dataFields.dateX = 'date'
      this.minTemperatureSeries.dataFields.valueY = 'min_temperature'
      this.minTemperatureSeries.tooltipText = '{valueY.value}'
      this.minTemperatureSeries.stroke = 'blue'

      this.maxTemperatureSeries = this.chart.series.push(new am4charts.LineSeries())
      this.maxTemperatureSeries.dataFields.dateX = 'date'
      this.maxTemperatureSeries.dataFields.valueY = 'max_temperature'
      this.maxTemperatureSeries.tooltipText = '{valueY.value}'
      this.maxTemperatureSeries.stroke = 'red'

      this.avgTemperatureSeries = this.chart.series.push(new am4charts.LineSeries())
      this.avgTemperatureSeries.dataFields.dateX = 'date'
      this.avgTemperatureSeries.dataFields.valueY = 'avg_temperature'
      this.avgTemperatureSeries.tooltipText = '{valueY.value}'
      this.avgTemperatureSeries.stroke = 'black'
    },
    generateHumidityLineSeries() {
      this.minHumiditySeries = this.chart.series.push(new am4charts.LineSeries())
      this.minHumiditySeries.dataFields.dateX = 'date'
      this.minHumiditySeries.dataFields.valueY = 'min_humidity'
      this.minHumiditySeries.tooltipText = '{valueY.value}'
      this.minHumiditySeries.stroke = 'blue'
      this.minHumiditySeries.yAxis = this.humidityAxis;
      this.minHumiditySeries.strokeDasharray = "10,3";

      this.maxHumiditySeries = this.chart.series.push(new am4charts.LineSeries())
      this.maxHumiditySeries.dataFields.dateX = 'date'
      this.maxHumiditySeries.dataFields.valueY = 'max_humidity'
      this.maxHumiditySeries.tooltipText = '{valueY.value}'
      this.maxHumiditySeries.stroke = 'red'
      this.maxHumiditySeries.yAxis = this.humidityAxis;
      this.maxHumiditySeries.strokeDasharray = "10,3";

      this.avgHumiditySeries = this.chart.series.push(new am4charts.LineSeries())
      this.avgHumiditySeries.dataFields.dateX = 'date'
      this.avgHumiditySeries.dataFields.valueY = 'avg_humidity'
      this.avgHumiditySeries.tooltipText = '{valueY.value}'
      this.avgHumiditySeries.stroke = 'black'
      this.avgHumiditySeries.yAxis = this.humidityAxis;
      this.avgHumiditySeries.strokeDasharray = "10,3";
    },
    chartData() {
      let data = []
      this.minTemperature = 1000
      this.maxTemperature = -1000
      this.minHumidity = 1000
      this.maxHumidity = -1000
      var has_min_max = (this.logs[0].min_humidity)
      for (let log of this.logs) {
        var logMinHumidity = log.avg_humidity
        var logMaxHumidity = log.avg_humidity
        var logMinTemperature = log.avg_temperature
        var logMaxTemperature = log.avg_temperature
        if (has_min_max) {
          logMinHumidity = log.min_humidity
          logMaxHumidity = log.max_humidity
          logMinTemperature = log.min_temperature
          logMaxTemperature = log.max_temperature
        }
        if (this.minHumidity > logMinHumidity) {
          this.minHumidity = logMinHumidity
        }
        if (this.maxHumidity < logMaxHumidity) {
          this.maxHumidity = logMaxHumidity
        }
        if (this.minTemperature > logMinTemperature) {
          this.minTemperature = logMinTemperature
        }
        if (this.maxTemperature < logMaxTemperature) {
          this.maxTemperature = logMaxTemperature
        }
        data.push({
          date: Date.parse(log.date_time),
          min_temperature: log.min_temperature,
          max_temperature: log.max_temperature,
          avg_temperature: log.avg_temperature,
          min_humidity: log.min_humidity,
          max_humidity: log.max_humidity,
          avg_humidity: log.avg_humidity,
        })
      }
      return data
    }
  },
  watch: { 
    logs: function() {
      this.chart.dispose()
      this.generateChart()
      this.generateTemperatureLineSeries()
      this.generateHumidityLineSeries()
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
.container
{
  margin: 0.5em;
}
#chart {
  width: 100%;
  height: 500px;
}
</style>
