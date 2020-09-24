// Use like following in vue files
// import { serverUrl, testGlobal } from '@/common'

import axios from "axios";
import * as store from "@/vuex/store";

export var serverUrl = "http://127.0.0.1:8000";
//export var serverUrl = "http://172.16.1.109"

//////////////////////////////////////////////////////////////
// Common Popup
//////////////////////////////////////////////////////////////
// export function setPopup(){

//     this.$store.dispatch("setPopupKind", 'Noti');
//     this.$store.dispatch("setPopupHeader", 'Notification');
//     this.$store.dispatch("setPopupBody", 'Create Data completed..!!');
//     this.$store.dispatch("setPopupButton", 'CancelOK');

// }

//////////////////////////////////////////////////////////////
// Common Filter
//////////////////////////////////////////////////////////////
export function getSearchFilter(dateFrom, dateTo, timeFrom, timeTo, condition, search, ttFrom, ttTo, projectID){
    
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
    if ( projectID != '') {
        filters = filters + "&project_id="+projectID
    }

    return filters;
}

export function getDetailSearchFilter(dateFrom, dateTo, timeFrom, timeTo, condition, search, ttFrom, ttTo, projectID, detailcondition, detailsearch){
    
    var filters="";

    filters = getSearchFilter(dateFrom, dateTo, timeFrom, timeTo, condition, search, ttFrom, ttTo, projectID);

    if ( detailcondition != '') {
        filters = filters + "&detailconditionValue="+detailcondition
    }
    if ( detailsearch != '') {
        filters = filters + "&detailsearchValue="+detailsearch
    }

    return filters;
}

//////////////////////////////////////////////////////////////
// Common Chart Data
//////////////////////////////////////////////////////////////

export function setCommonStatisticInfo(type, project_id, filter, N) {
    
    // Top N으로 수정
    // type=1. Status Codes Top N
    // type=2. Requests Top N
    // type=3. 최다 404 발생 URL TopN
    // type=4. Time Taken (s/㎲) Top N
    // type=5. Visitors Top N
    // type=6. Referers Top N
    // type=7. User Agent Top N
    // type=8. Requests URI (Total Bytes) Top N
    // type=9. Static files (count) Top N
    // type=10. Requests URI (Average Bytes) Top N
    // type=11. Requests Average Time-taken (s/㎲)  Top N

    var content = "";

    switch (type) {
        case 1:
            content = "HTTP Status Codes (count)";
            break;
        case 2:
            content = "Requests URI (count)";
            break;
        case 3:
            content = "404 Requests URI (count)";
            break;
        case 4:
            content = "Requests Time-taken (s/㎲)";
            break;
        case 5:
            content = "Visitors (count)";
            break;
        case 6:
            content = "Referers (count)";
            break;
        case 7:
            content = "User Agent (count)";
            break;
        case 8:
            content = "Requests URI (Total Bytes)";
            break;
        case 9:
            content = "Static files (count)";
            break;
        case 10:
            content = "Requests URI (Average Bytes)";
            break;
        case 11:
            content = "Requests Average Time-taken (s/㎲)";
            break;
        default:
    };

    let postData = {
        project_id: project_id,
        type: type,
        N: N,
        filter: filter
    };

    let axiosConfig = {
        headers: {
            //'Authorization': 'Token '+ this.token // For Django
        }
    };

    let url = serverUrl + "/logdetail_dynamic/statistics/";

    // Set result
    let result = {
        content: content,
        url: url,
        postData: postData,
        axiosConfig: axiosConfig,        
    };  

    // return values
    // 1. content
    // 2. url
    // 3. postData
    // 4. axiosConfig

    return result;
    
}

export function getChartDataFromStatistics(type, project_id, filter, N) {

    let commonInfo = setCommonStatisticInfo(type, project_id, filter, N);

    // For Await
    return axios.post(commonInfo.url, commonInfo.postData, commonInfo.axiosConfig)
        .then(res => {
            console.log(res);

            var x = [];
            var y = [];

            for (let i = 0; i < res.data.results.length; i++) {

                x.push(res.data.results[i].result);
                y.push(res.data.results[i].result_count);
            }

            res.x = x;
            res.y = y;
            res.label = commonInfo.content;

            return res;
        })
        .catch(err => {
            console.error(err);
        })
}

export function getLineChartData(kind = 1, timeCondition, project_id, filter) {
    
    var url = serverUrl + "/logdetail_dynamic/chartdata/"
    //var url = serverUrl + "/logdetail/chartdata/"

    let postData = {

        project_id: project_id,

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

var zoom_plugin_config = {
    zoom: {
        // Container for pan options
        pan: {
            // Boolean to enable panning
            enabled: false,

            // Panning directions. Remove the appropriate direction to disable
            // Eg. 'y' would only allow panning in the y direction
            // A function that is called as the user is panning and returns the
            // available directions can also be used:
            //   mode: function({ chart }) {
            //     return 'xy';
            //   },
            mode: 'x',

            // rangeMin: {
            //     // Format of min pan range depends on scale type
            //     x: null,
            //     y: null
            // },
            // rangeMax: {
            //     // Format of max pan range depends on scale type
            //     x: null,
            //     y: null
            // },

            // On category scale, factor of pan velocity
            //speed: 20,

            // Minimal pan distance required before actually applying pan
            //threshold: 10,

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
            drag: {
                // borderColor: 'rgba(180,180,180,0.3)',
                // borderWidth: 5,
                // backgroundColor: 'rgb(180,180,180)',
                animationDuration: 1000
            },

            // Zooming directions. Remove the appropriate direction to disable
            // Eg. 'y' would only allow zooming in the y direction
            // A function that is called as the user is zooming and returns the
            // available directions can also be used:
            //   mode: function({ chart }) {
            //     return 'xy';
            //   },
            mode: 'x',

            // rangeMin: {
            //     // Format of min zoom range depends on scale type
            //     x: null,
            //     y: null
            // },
            // rangeMax: {
            //     // Format of max zoom range depends on scale type
            //     x: null,
            //     y: null
            // },

            // Speed of zoom via mouse wheel
            // (percentage of zoom on a wheel event)
            //speed: 0.5,

            // // Minimal zoom distance required before actually applying zoom
             //threshold: 2,

            // // On category scale, minimal zoom level before actually applying zoom
             //sensitivity: 3,

            // Function called while the user is zooming
            onZoom: function({chart}) { console.log(`I'm zooming!!!`); },
            // Function called once zooming is completed
            onZoomComplete: function({chart}) { 
                console.log(`I was zoomed!!!`); 

            }
        }
    }
}

var zoomTimeOption = {
    parser: 'YYYYMMDDHHmmss',
    //round: 'day',
    tooltipFormat: 'll HH:mm:ss',
    //unit: 'day',
    unitStepSize: 1,

    // displayFormats: {
    //     'millisecond': 'MMM DD',
    //     'second': 'MMM DD',
    //     'minute': 'MMM DD',
    //     'hour': 'MMM DD',
    //     'day': 'MMM DD',
    //     'week': 'MMM DD',
    //     'month': 'MMM DD',
    //     'quarter': 'MMM DD',
    //     'year': 'MMM DD',
    //  }
}

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

export function getPieChartOptions(title) {

    var options = {
        responsive: true,
        maintainAspectRatio: false,

        title: {
            display: true,
            text: title
        },
    }

    return options;
}

export function getBarChartTemplate(x, y, label) {

    var chartData = {

        labels: x,

        datasets: [{
                label: 'label',
                fill: true,
                data: y,
                backgroundColor: bgColors(y),
                borderWidth: 1
            },

        ]
    }

    return chartData;
}

export function getBarChartOptions(title) {

    var options = {
        responsive: true,
        maintainAspectRatio: false,

        title: {
            display: true,
            text: title
        },

        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        },

        plugins: zoom_plugin_config,
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

export function getStackedBarChartOptions(title) {

    var options = {
        responsive: true,
        maintainAspectRatio: false,

        title: {
            display: true,
            text: title
        },

        scales: {
            xAxes: [{
                type: 'time',
                time: zoomTimeOption,
                stacked: true,
            }],
            yAxes: [{
                stacked: true,
                ticks: {
                    beginAtZero: true
                }
            }]
        },

        plugins: zoom_plugin_config,
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
        title: {
            display: true,
            text: 'Request (count)'
        },

        scales: {
            xAxes: [{
                type: 'time',                
                time: zoomTimeOption,

                scaleLabel: {
                    display: true,
                    labelString: 'Date'
                },
                // ticks: {
                //     maxRotation: 0
                // }
            }],
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'value'
                }
            }]
        },

        plugins: zoom_plugin_config,

        // onClick: function(e) {
        //     // eslint-disable-next-line no-alert
        //     alert(e.type);
        // },
        
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

export function getMultiLineChartOptions(title) {

    var options = {
        responsive: true,
        maintainAspectRatio: false,

        title: {
            display: true,
            text: title
        },

        scales:{
            xAxes: [{
                type: 'time',
                time: zoomTimeOption,

                scaleLabel: {
                    display: true,
                    labelString: 'Date/Time'
                },
                // ticks: {
                //     maxRotation: 0
                // }
            }]
            ,yAxes:[{
                    type: 'linear',
                    display: true,
                    position: 'left',
                    id: "request",
                    scaleLabel: {
                        display: true,
                        labelString: 'value(count)'
                    }
                },{
                    type: 'linear',
                    display: true,
                    position: 'right',
                    id: "time_taken",
                    scaleLabel: {
                        display: true,
                        labelString: 'value(㎲/s)'
                    }
            }]
        },

        plugins: zoom_plugin_config,
    }

    return options;
}
