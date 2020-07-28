// Use like following in vue files
// import { serverUrl, testGlobal } from '@/common'

import axios from "axios";

export var serverUrl = "http://127.0.0.1:8000"

export function testGlobal() {
    console.log("testGlobal() is invkoed!");
    console.log("testGlobal() serverUrl : ", serverUrl);
}


// Common Chart Area
var bgColors = function (data) {

    var count = data.length;
    var results = [];

    for (var i = 0; i < count; i++) {
        var randomR = Math.floor((Math.random() * 100) + 100);
        var randomG = Math.floor((Math.random() * 120) + 100);
        var randomB = Math.floor((Math.random() * 150) + 100);

        var graphBackground = "rgb(" +
            randomR + ", " +
            randomG + ", " +
            randomB + ", 0.7)";

        results.push(graphBackground);
    }

    return results;
}

export function getPieChartTemplate(x, y) {

    var chartData = {

        labels: x,
        datasets: [{
            data: y,
            backgroundColor: bgColors(y)
        }]
    }

    return chartData;
}

export function getPieChartOptions() {

    var options =  {
        responsive: true,
        maintainAspectRatio: false
      }

    return options;
}

export function getBarChartTemplate(x, y, label) {

    var chartData = {

        labels: x,

        datasets: [{
                label: label,
                fill: true,
                data: y,
                backgroundColor: bgColors(y),
                borderWidth: 1
            },

        ]
    }

    return chartData;
}

export function getBarChartOptions() {

    var options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }

    return options;
}

export function getStackedBarChartTemplate(x, y200, y400, y500) {

    var chartData = {

        labels: x,

        datasets: [{
                label: '20x',
                data: y200,
                backgroundColor: 'rgb(158, 194, 247)',
                borderWidth: 1
            },
            {
                label: '40x',
                data: y400,
                backgroundColor: 'rgb(193, 180, 213)',
                borderWidth: 1
            },
            {
                label: '50x',
                data: y500,
                backgroundColor: 'rgb(194, 157, 180)',
                borderWidth: 1
            }
        ]
    }

    return chartData;
}

export function getStackedBarChartOptions() {

    var options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            xAxes: [{
                stacked: true,
            }],
            yAxes: [{
                stacked: true,
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }

    return options;
}

export function getLineChartTemplate(x, y, label) {

    var chartData = {

        labels: x,

        datasets: [{
            label: label,
            fill: false,
            backgroundColor: '#f87979',
            borderColor: 'rgb(188, 207, 229)',
            data: y
        }, ]
    }

    return chartData;
}

export function getLineChartOptions() {

    var options =  {
        responsive: true,
        maintainAspectRatio: false
      }

    return options;
}