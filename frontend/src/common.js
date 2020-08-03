// Use like following in vue files
// import { serverUrl, testGlobal } from '@/common'

import axios from "axios";

export var serverUrl = "http://127.0.0.1:8000"

//////////////////////////////////////////////////////////////
// Common Filter
//////////////////////////////////////////////////////////////
export function getSearchFilter(dateFrom, dateTo, timeFrom, timeTo, condition, search, ttFrom, ttTo){
    
    var filters=""

    if ( dateFrom != '') {
      filters = filters + "&dateFromValue="+dateFrom
    }
    if ( dateTo != '') {
      filters = filters + "&dateToValue="+dateTo
    }
    if ( timeFrom != '') {
      filters = filters + "&timeFromValue="+timeFrom
    }
    if ( timeTo != '') {
      filters = filters + "&timeToValue="+timeTo
    }
    if ( condition != '') {
      filters = filters + "&conditionValue="+condition
    }
    if ( search != '') {
      filters = filters + "&searchValue="+search
    }
    if ( ttFrom != '') {
      filters = filters + "&ttFromValue="+ttFrom
    }
    if ( ttTo != '') {
      filters = filters + "&ttToValue="+ttTo
    }

    return filters;
}

//////////////////////////////////////////////////////////////
// Common Chart Data
//////////////////////////////////////////////////////////////
export function getChartDataFromStatistics(type, logfile_id, filter) {

    // Top 5 일때
    // type=1. Status Codes Top5
    // type=2. Requests Top5
    // type=3. 최다 404 발생 URL Top5
    // type=4. Time Taken Top5 
    // type=5. Visitors Top5       

    //this.title = "Top 5"

    var url = serverUrl + "/logdetail/statistics_top5/"

    var label

    switch (type) {
        case 1:
            label = "HTTP Status Codes(count)"
            break;
        case 2:
            label = "Requests URI(count)"
            break;
        case 3:
            label = "404 Requests URI(count)"
            break;
        case 4:
            label = "Requests Time-taken(ms/㎲)"
            break;
        case 5:
            label = "Visitors(count)"
            break;
        default:
    }

    console.log(logfile_id)

    let postData = {
        logfile_id: logfile_id,
        type: type,
        filter: filter
    };

    let axiosConfig = {
        headers: {
            //'Authorization': 'Token '+ this.token // For Django
        }
    };

    // For Await
    return axios.post(url, postData, axiosConfig)
        .then(res => {
            console.log(res)

            var x = []
            var y = []

            for (let i = 0; i < res.data.results.length; i++) {

                x.push(res.data.results[i].result);
                y.push(res.data.results[i].result_count);
            }

            res.x = x
            res.y = y
            res.label = label

            return res
        })
        .catch(err => {
            console.error(err);
        })


}

export function getLineChartData(kind = 1, timeCondition, logfile_id, filter) {
    var url = serverUrl + "/logdetail/chartdata/"

    let postData = {

        logfile_id: logfile_id,

        //Type1 : 시(HH)기준
        //   Kind1 : request(요청) 건수(count)
        //   Kind2 : status code 건수(count)
        //   Kind3 : time-taken 시간(max, min, count)
        //Type2 : 시분(HHMM)기준                    
        //   Kind1 : request(요청) 건수(count)
        //   Kind2 : status code 건수(count)
        //   Kind3 : time-taken 시간(max, min, count)

        type: timeCondition,
        kind: kind,
        filter: filter

    };

    let axiosConfig = {
        headers: {
            //'Authorization': 'Token '+ this.token // For Django
        }
    };

    return axios.post(url, postData, axiosConfig)

        .then(res => {
            console.log(res)

            if (kind == 1) {
                res.x = res.data.resultX
                res.y = res.data.resultY

            } else if (kind == 2) {
                res.sbarX = res.data.resultX
                res.sbarY_200 = res.data.resultY_200
                res.sbarY_300 = res.data.resultY_300
                res.sbarY_400 = res.data.resultY_400
                res.sbarY_500 = res.data.resultY_500
            } else if (kind == 3) {
                
                res.x = res.data.resultX
                res.y = res.data.resultY
                res.yt = res.data.resultY_time
                res.time_unit = res.data.resultY_time_unit
            }

            return res

        })
        .catch(err => {
            console.error(err);
        })

}

//////////////////////////////////////////////////////////////
// Common Chart Area
//////////////////////////////////////////////////////////////
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

    var options = {
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

export function getStackedBarChartTemplate(x, y200, y300, y400, y500) {

    var chartData = {

        labels: x,

        datasets: [{
                label: '20x',
                data: y200,
                backgroundColor: 'rgb(158, 194, 247)',
                borderWidth: 1
            },
            {
                label: '30x',
                data: y300,
                backgroundColor: 'rgb(193, 180, 213)',
                borderWidth: 1
            },
            {
                label: '40x',
                data: y400,
                backgroundColor: 'rgb(222, 157, 213)',
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
            backgroundColor: 'rgb(188, 207, 229)',
            borderColor: 'rgb(188, 207, 229)',
            data: y
        }, ]
    }


    
    return chartData;
}

export function getLineChartOptions() {

    var options = {
        responsive: true,
        maintainAspectRatio: false,

        // TODO: Scale
        
        // TODO: Zooming and Panning - 미완성
        plugins: {
            zoom: {
                // Container for pan options
                pan: {
                    // Boolean to enable panning
                    enabled: true,
        
                    // Panning directions. Remove the appropriate direction to disable
                    // Eg. 'y' would only allow panning in the y direction
                    // A function that is called as the user is panning and returns the
                    // available directions can also be used:
                    //   mode: function({ chart }) {
                    //     return 'xy';
                    //   },
                    mode: 'x',
        
                    rangeMin: {
                        // Format of min pan range depends on scale type
                        x: null,
                        y: null
                    },
                    rangeMax: {
                        // Format of max pan range depends on scale type
                        x: null,
                        y: null
                    },
        
                    // On category scale, factor of pan velocity
                    speed: 20,
        
                    // Minimal pan distance required before actually applying pan
                    threshold: 10,
        
                    // Function called while the user is panning
                    onPan: function({chart}) { console.log(`I'm panning!!!`); },
                    // Function called once panning is completed
                    onPanComplete: function({chart}) { console.log(`I was panned!!!`); }
                },
        
                // Container for zoom options
                zoom: {
                    // Boolean to enable zooming
                    enabled: true,
        
                    // Enable drag-to-zoom behavior
                    drag: true,
        
                    // Drag-to-zoom effect can be customized
                    // drag: {
                    // 	borderColor: 'rgba(180,180,180,0.3)',
                    // 	borderWidth: 5,
                    // 	backgroundColor: 'rgb(180,180,180)',
                    // 	animationDuration: 0
                    // },
        
                    // Zooming directions. Remove the appropriate direction to disable
                    // Eg. 'y' would only allow zooming in the y direction
                    // A function that is called as the user is zooming and returns the
                    // available directions can also be used:
                    //   mode: function({ chart }) {
                    //     return 'xy';
                    //   },
                    mode: 'x',
        
                    rangeMin: {
                        // Format of min zoom range depends on scale type
                        x: null,
                        y: null
                    },
                    rangeMax: {
                        // Format of max zoom range depends on scale type
                        x: null,
                        y: null
                    },
        
                    // Speed of zoom via mouse wheel
                    // (percentage of zoom on a wheel event)
                    speed: 0.1,
        
                    // Minimal zoom distance required before actually applying zoom
                    threshold: 2,
        
                    // On category scale, minimal zoom level before actually applying zoom
                    sensitivity: 3,
        
                    // Function called while the user is zooming
                    onZoom: function({chart}) { console.log(`I'm zooming!!!`); },
                    // Function called once zooming is completed
                    onZoomComplete: function({chart}) { console.log(`I was zoomed!!!`); }
                }
            }
        }
    }

    return options;
}

export function getMultiLineChartTemplate(x, y1, label1, y2, label2) {

    var chartData = {

        labels: x,

        datasets: [{
            label: label1,
            fill: false,
            backgroundColor: 'rgb(188, 207, 229)',
            borderColor: 'rgb(188, 207, 229)',
            data: y1,
            yAxisID: "request"
        }, {
            label: label2,
            fill: false,
            backgroundColor: 'rgb(194, 157, 180)',
            borderColor: 'rgb(194, 157, 180)',
            data: y2,
            yAxisID: "time_taken"
        },]

    }


    
    return chartData;
}

export function getMultiLineChartOptions() {

    var options = {
        responsive: true,
        maintainAspectRatio: false,

        scales:{
            yAxes:[{
                type: 'linear',
                display: true,
                position: 'left',
                id: "request"
            },{
                type: 'linear',
                display: true,
                position: 'right',
                id: "time_taken"
            }]
        }
    }

    return options;
}