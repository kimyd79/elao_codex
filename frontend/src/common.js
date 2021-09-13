// Use like following in vue files
// import { serverUrl, testGlobal } from '@/common'

import axios from "axios";
// import * as store from "@/vuex/store";
import store from "@/vuex/store";

export var serverUrl = "http://127.0.0.1:8000/mwla"; 
//export var serverUrl = "http://172.16.1.109"
// webport
//export var serverUrl = "http://182.195.89.147:18080/mwla"    
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
export function getSearchFilter(dateFrom, dateTo, timeFrom, timeTo, condition, search, ttFrom, ttTo, projectID, excludeSearch, projectServers){
    
    var filters="";

    if ( dateFrom != '') {
      filters = filters + "&dateFromValue="+dateFrom;
    }
    if ( dateTo != '') {
      filters = filters + "&dateToValue="+dateTo;
    }
    if ( timeFrom != '') {
      filters = filters + "&timeFromValue="+timeFrom;
    }
    if ( timeTo != '') {
      filters = filters + "&timeToValue="+timeTo;
    }
    if ( condition != '') {
      filters = filters + "&conditionValue="+condition;
    }
    if ( search != '') {
      filters = filters + "&searchValue="+search;
    }
    if ( ttFrom != '') {
      filters = filters + "&ttFromValue="+ttFrom;
    }
    if ( ttTo != '') {
      filters = filters + "&ttToValue="+ttTo;
    }
    if ( projectID != '') {
        filters = filters + "&project_id="+projectID;
    }
    if ( excludeSearch != '') {
        filters = filters + "&excludeSearch="+excludeSearch;
    }
    if ( projectServers != '') {
        filters = filters + "&projectServers="+projectServers;
    }
    
    return filters;
}

export function getDetailSearchFilter(dateFrom, dateTo, timeFrom, timeTo, condition, search, ttFrom, ttTo, projectID, excludeSearch, detailcondition, detailsearch, byteFrom, byteTo, staticYN, statusYN){
    
    var filters="";

    filters = getSearchFilter(dateFrom, dateTo, timeFrom, timeTo, condition, search, ttFrom, ttTo, projectID, excludeSearch);

    if ( detailcondition != '') {
        filters = filters + "&detailconditionValue="+detailcondition;
    }
    if ( detailsearch != '') {
        filters = filters + "&detailsearchValue="+detailsearch;
    }
    if ( byteFrom != '') {
        filters = filters + "&byteFromValue="+byteFrom;
    }
    if ( byteTo != '') {
        filters = filters + "&byteToValue="+byteTo;
    }
    if ( staticYN != '') {
        filters = filters + "&staticValue="+staticYN;
    }
    if ( statusYN != '') {
        filters = filters + "&statusValue="+statusYN;
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
    // type=12. Static file Names (count) Top N    
    // type=13. Nginx Ingress : Domain Top N - Referer에서 Domain만
    // type=14. Nginx Ingress : $proxy_upstream_name/$upstream_addr(<namespace>-<service name>-<service port>/<IP>:<port>) Top N
    // statisticsKind = 30. Defference : Total Number of Requests (count)
    // statisticsKind = 31. Defference : TPS Requests Top N at TPS peak
    // statisticsKind = 32. Defference : TPS Visitors Top N at TPS peak
    // statisticsKind = 33. Defference : timeTaken Requests Top N at TPS peak
    // statisticsKind = 34. Defference : timeTaken Visitors Top N at TPS peak
    // statisticsKind = 35. Defference : status Requests Top N at TPS peak
    // statisticsKind = 36. Defference : status Visitors Top N at TPS peak

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
        case 12:
            content = "Static file Names (count)";
            break;
        case 13:
            content = "Upstream Info (count, K8S Ingress)";
            break;
        case 14:
            content = "Domains (count, K8S Ingress)";            
            break;
        case 30:
            content = "Total Number of Requests (count)";            
            break;
        case 31:
            content = "Requests URI (count)";            
            break;
        case 32:
            content = "Visitors (count)";            
            break;
        case 33:
            content = "Requests URI (count)";            
            break;
        case 34:
            content = "Visitors (count)";            
            break;
        case 35:
            content = "Requests URI (count)";            
            break;
        case 36:
            content = "Visitors (count)";            
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


export function setDetailCondition() {

    switch (store.state.detailcondition) {
        case 1:
            store.dispatch("setPopupHeader", "HTTP Status Codes (count)");            
            store.dispatch("setDetailCondition", "S");
            break;
        case 2:
            store.dispatch("setPopupHeader", "Requests URI (count)");            
            store.dispatch("setDetailCondition", "R");
            store.dispatch("setDetailSearchKeyword", encodeURIComponent(store.state.detailsearchKeyword));
            break;
        case 3:
            store.dispatch("setPopupHeader", "404 Requests URI (count)");            
            store.dispatch("setDetailCondition", "NFR");
            break;
        case 4:
            store.dispatch("setPopupHeader", "Requests Time-taken (s/㎲)");            
            store.dispatch("setDetailCondition", "R");
            store.dispatch("setDetailSearchKeyword", encodeURIComponent(store.state.detailsearchKeyword));
            break;
        case 5:
            store.dispatch("setPopupHeader", "Visitors (count)");            
            store.dispatch("setDetailCondition", "I");
            break;
        case 6:
            store.dispatch("setPopupHeader", "Referers (count)");            
            store.dispatch("setDetailCondition", "E");
            break;
        case 7:
            store.dispatch("setPopupHeader", "User Agent (count)");            
            store.dispatch("setDetailCondition", "U");
            break;
        case 8:
            store.dispatch("setPopupHeader", "Requests URI (Total Bytes)");            
            store.dispatch("setDetailCondition", "R");
            store.dispatch("setDetailSearchKeyword", encodeURIComponent(store.state.detailsearchKeyword));
            break;
        case 9:
            store.dispatch("setPopupHeader", "Static files (count)");            
            store.dispatch("setDetailCondition", "F");
            break;
        case 10:
            store.dispatch("setPopupHeader", "Requests URI (Average Bytes)");            
            store.dispatch("setDetailCondition", "R");
            store.dispatch("setDetailSearchKeyword", encodeURIComponent(store.state.detailsearchKeyword));
            break;
        case 11:
            store.dispatch("setPopupHeader", "Requests Average Time-taken (s/㎲)");            
            store.dispatch("setDetailCondition", "R");
            store.dispatch("setDetailSearchKeyword", encodeURIComponent(store.state.detailsearchKeyword));
            break;
        case 12:
            store.dispatch("setPopupHeader", "Static file Names (count)");            
            store.dispatch("setDetailCondition", "R");
            store.dispatch("setDetailSearchKeyword", encodeURIComponent(store.state.detailsearchKeyword));
            break;
        case 13:
            store.dispatch("setPopupHeader", "Upstream Info (count, K8S Ingress)");            
            store.dispatch("setDetailCondition", "V1");
            break;
        case 14:
            store.dispatch("setPopupHeader", "Domains (count, K8S Ingress)");            
            store.dispatch("setDetailCondition", "V2");
            break;
        // case 30:
        //     store.state.popupHeader = "Total Number of Requests (count)";
        //     store.state.detailcondition = "R"
        //     break;
        case 31:
            store.dispatch("setPopupHeader", "Requests URI (count)");            
            store.dispatch("setDetailCondition", "R");
            store.dispatch("setDetailSearchKeyword", encodeURIComponent(store.state.detailsearchKeyword));
            break;
        case 32:
            store.dispatch("setPopupHeader", "Visitors (count)");            
            store.dispatch("setDetailCondition", "I");
            break;
        case 33:
            store.dispatch("setPopupHeader", "Requests URI (count)");            
            store.dispatch("setDetailCondition", "R");
            store.dispatch("setDetailSearchKeyword", encodeURIComponent(store.state.detailsearchKeyword));
            break;
        case 34:
            store.dispatch("setPopupHeader", "Visitors (count)");            
            store.dispatch("setDetailCondition", "I");
            break;
        case 35:
            store.dispatch("setPopupHeader", "Requests URI (count)");            
            store.dispatch("setDetailCondition", "R");
            store.dispatch("setDetailSearchKeyword", encodeURIComponent(store.state.detailsearchKeyword));
            // this.statusYN = "Y"
            break;
        case 36:
            store.dispatch("setPopupHeader", "Visitors (count)");            
            store.dispatch("setDetailCondition", "I");
            // this.statusYN = "Y"
            break;
        default:
    }
}

export function setFindingDetailCondition() {

    if (store.state.detailcondition == 'fstatus') {
        store.dispatch("setDetailCondition", "S");
    } else if (store.state.detailcondition == 'frequest') {    
        store.dispatch("setDetailCondition", "R");
    } else if (store.state.detailcondition == 'fip') {
        store.dispatch("setDetailCondition", "I");
    } else if (store.state.detailcondition == 'freferer') {
        store.dispatch("setDetailCondition", "E");
    } else if (store.state.detailcondition == 'fuser_agent') {
        store.dispatch("setDetailCondition", "U");
    } else if (store.state.detailcondition == 'fextension') {
        store.dispatch("setDetailCondition", "F");
    } else if (store.state.detailcondition == 'freserve1') {
        store.dispatch("setDetailCondition", "V1");
    } else if (store.state.detailcondition == 'freserve2') {
        store.dispatch("setDetailCondition", "V2");
    }
}

export function getChartDataFromStatistics(type, project_id, filter, N) {

    let commonInfo = setCommonStatisticInfo(type, project_id, filter, N);

    // For Await
    return axios.post(commonInfo.url, commonInfo.postData, commonInfo.axiosConfig)
        .then(res => {
            //console.log(res);

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
        //Type3 : 시분초(HHMMSS)기준                    
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
            //console.log(res)

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

export function getLineChartDataDiff(kind = 1, timeCondition, project_id, filter) {
    
    var url = serverUrl + "/logdetail_dynamic/chartdata_diff/"

    let postData = {

        project_id: project_id,

        //Type1 : 시(HH)기준
        //Type2 : 시분(HHMM)기준                    
        //Type3 : 시분초(HHMMSS)기준                    

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
            // console.log(res)

            // kind = 0 : request 
            // kind = 1 : TPS
            // kind = 2 : timeTaken  
            // kind = 3 : Status code(4XX, 5XX) 
            // kind = 4 : request + timeTaken
            // kind = 5 : Status code(2XX, 3XX, 4XX, 5XX)

            if (kind == 0 || kind == 1 ) {
                res.xy = res.data.resultXY
            } else if (kind == 2) {
                res.xy = res.data.resultXY
                res.time_unit = res.data.resultY_time_unit
            } else if (kind == 3) {
                res.xy_400 = res.data.resultXY_400
                res.xy_500 = res.data.resultXY_500
            } else if (kind == 4) {
                res.xy = res.data.resultXY
                res.xy2 = res.data.resultXY2
            } else if (kind == 5) {
                res.xy_200 = res.data.resultXY_200
                res.xy_300 = res.data.resultXY_300
                res.xy_400 = res.data.resultXY_400
                res.xy_500 = res.data.resultXY_500
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
            onPan: function({chart}) { 
                //console.log(`I'm panning!!!`); 
            },
            // Function called once panning is completed
            onPanComplete: function({chart}) { 
                //console.log(`I was panned!!!`); 
            }
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
            onZoom: function({chart}) { 
                //console.log(`I'm zooming!!!`); 
            },
            // Function called once zooming is completed
            onZoomComplete: function({chart}) { 
                //console.log(`I was zoomed!!!`); 
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
        var randomR = Math.floor((Math.random() * 100) + 155);
        var randomG = Math.floor((Math.random() * 100) + 155);
        var randomB = Math.floor((Math.random() * 100) + 155);

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
        cutoutPercentage: 35,

        title: {
            display: true,
            text: title,
            fontStyle: 'bold',
            fontColor: 'rgb(85,60,165)',
            fontSize: 18,
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

export function getStackedBarChartOptions(title, x_min, x_max, y_max_request) { 

    var options = {
        responsive: true,
        maintainAspectRatio: false,

        title: {
            display: true,
            text: title,
            fontStyle: 'bold',
            fontColor: 'rgb(85,60,165)',
            fontSize: 18,
            padding: 20,
        },

        // TODO: Data 및 Scale 설정 부분
        scales: {
            xAxes: [{
                type: 'time',
                time: zoomTimeOption,
                stacked: true,
                // X axis scale : 
                ticks: {    // YYYYMMDDHHmmss
                    min: x_min,
                    max: x_max
                }
            }],
            yAxes: [{
                stacked: true,
                ticks: {
                    beginAtZero: true,
                    //suggestedMin: 0,
                    //suggestedMax: y_max_request
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

export function getLineChartOptions(title, x_min, x_max, y_max_tps){

    var options = {
        responsive: true,
        maintainAspectRatio: false,
        title: {
            display: true,
            text: title,
            fontStyle: 'bold',
            fontColor: 'rgb(85,60,165)',
            fontSize: 18,
            padding: 20,
        },

        scales: {
            xAxes: [{
                type: 'time',                
                time: zoomTimeOption,

                scaleLabel: {
                    display: true,
                    labelString: 'Date'
                },
                // X axis scale : 
                ticks: {    // YYYYMMDDHHmmss
                    min: x_min,
                    max: x_max
               }
            }],
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'tps'
                },
                ticks: { 
                     suggestedMin: 0,
                     suggestedMax: y_max_tps
                     //min: 0,
                     //max: ''
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

export function getMultiLineChartOptions(title, x_min, x_max, y_max_request, y_max_duration) { 

    var options = {
        responsive: true,
        maintainAspectRatio: false,

        title: {
            display: true,
            text: title,
            fontStyle: 'bold',
            fontColor: 'rgb(85,60,165)',
            fontSize: 18,
            padding: 20,
        },

        scales:{
            xAxes: [{
                type: 'time',
                time: zoomTimeOption,

                scaleLabel: {
                    display: true,
                    labelString: 'Date/Time'
                },
                ticks: {    // YYYYMMDDHHmmss
                    min: x_min,
                    max: x_max
               }
            }]
            ,yAxes:[{
                    type: 'linear',
                    display: true,
                    position: 'left',
                    id: "request",
                    scaleLabel: {
                        display: true,
                        labelString: 'Request(count)'
                    },
                    ticks: { 
                        suggestedMin: 0,
                        suggestedMax: y_max_request
                        //min: 0,
                        //max: ''
                   }
                },{
                    type: 'linear',
                    display: true,
                    position: 'right',
                    id: "time_taken",
                    scaleLabel: {
                        display: true,
                        labelString: 'Duration(s)'
                    },
                    ticks: { 
                        suggestedMin: 0,
                        suggestedMax: y_max_duration
                        //min: 0,
                        //max: ''
                   }
            }]
        },

        plugins: zoom_plugin_config,
    }

    return options;
}

export function getMultiLineChartTemplateDiff(label1, xy1, label2, xy2) {

    var chartData = {

        datasets: [{
            label: label1,
            fill: false,
            backgroundColor: 'rgb(188, 207, 229)',
            borderColor: 'rgb(188, 207, 229)',
            data: xy1,
            xAxisID: 'x-axis-1',
            yAxisID: "y-axis-1"
        },{
            label: label2,
            fill: false,
            backgroundColor: 'rgb(194, 157, 180)',
            borderColor: 'rgb(194, 157, 180)',
            data: xy2,
            xAxisID: 'x-axis-2',
            yAxisID: "y-axis-1"
        }]

    }
    
    return chartData;
}

export function getMultiLineChartTemplateStatusDiff(label1, xy1, label2, xy2, label3, xy3, label4, xy4) {

    var chartData = {

        datasets: [{
            label: label1,
            fill: false,
            backgroundColor: 'rgb(188, 207, 229)',
            borderColor: 'rgb(188, 207, 229)',
            data: xy1,
            xAxisID: 'x-axis-1',
            yAxisID: "y-axis-1"
        },{
            label: label2,
            fill: false,
            backgroundColor: 'rgb(204, 157, 180)',
            borderColor: 'rgb(204, 157, 180)',
            data: xy2,
            xAxisID: 'x-axis-1',
            yAxisID: "y-axis-1"
        },{
            label: label3,
            fill: false,
            backgroundColor: 'rgb(86, 118, 154)',
            borderColor: 'rgb(86, 118, 154)',
            data: xy3,
            xAxisID: 'x-axis-2',
            yAxisID: "y-axis-1"
        },{
            label: label4,
            fill: false,
            backgroundColor: 'rgb(185, 76, 104)',
            borderColor: 'rgb(185, 76, 104)',
            data: xy4,
            xAxisID: 'x-axis-2',
            yAxisID: "y-axis-1"
        }]
    }
    
    return chartData;
}

export function getMultiLineChartTemplateStatus2Diff(label1, xy1, label2, xy2, label3, xy3, label4, xy4, label5, xy5, label6, xy6, label7, xy7, label8, xy8) {

    var chartData = {

        datasets: [{
            label: label1,
            fill: false,
            backgroundColor: 'rgb(158, 194, 247)',
            borderColor: 'rgb(158, 194, 247)',
            data: xy1,
            xAxisID: 'x-axis-1',
            yAxisID: "y-axis-1"
        },{
            label: label2,
            fill: false,
            backgroundColor: 'rgb(193, 180, 213)',
            borderColor: 'rgb(193, 180, 213)',
            data: xy2,
            xAxisID: 'x-axis-1',
            yAxisID: "y-axis-1"
        },{
            label: label3,
            fill: false,
            backgroundColor: 'rgb(222, 157, 213)',
            borderColor: 'rgb(222, 157, 213)',
            data: xy3,
            xAxisID: 'x-axis-1',
            yAxisID: "y-axis-1"
        },{
            label: label4,
            fill: false,
            backgroundColor: 'rgb(194, 157, 180)',
            borderColor: 'rgb(194, 157, 180)',
            data: xy4,
            xAxisID: 'x-axis-1',
            yAxisID: "y-axis-1"
        },{
            label: label5,
            fill: false,
            backgroundColor: 'rgb(051, 102, 153)',
            borderColor: 'rgb(051, 102, 153)',
            data: xy5,
            xAxisID: 'x-axis-2',
            yAxisID: "y-axis-1"
        },{
            label: label6,
            fill: false,
            backgroundColor: 'rgb(153, 102, 204)',
            borderColor: 'rgb(153, 102, 204)',
            data: xy6,
            xAxisID: 'x-axis-2',
            yAxisID: "y-axis-1"
        },{
            label: label7,
            fill: false,
            backgroundColor: 'rgb(204, 051, 204)',
            borderColor: 'rgb(204, 051, 204)',
            data: xy7,
            xAxisID: 'x-axis-2',
            yAxisID: "y-axis-1"
        },{
            label: label8,
            fill: false,
            backgroundColor: 'rgb(102, 051, 000)',
            borderColor: 'rgb(102, 051, 000)',
            data: xy8,
            xAxisID: 'x-axis-2',
            yAxisID: "y-axis-1"
        }]

    }
    
    return chartData;
}

export function getMultiLineChartTemplate2Diff(label1, xy1, label2, xy2, label3, xy3, label4, xy4) {

    var chartData = {

        datasets: [{
            label: label1,
            fill: false,
            backgroundColor: 'rgb(188, 207, 229)',
            borderColor: 'rgb(188, 207, 229)',
            data: xy1,
            xAxisID: 'x-axis-1',
            yAxisID: "y-axis-1"
        },{
            label: label2,
            fill: false,
            backgroundColor: 'rgb(204, 157, 180)',
            borderColor: 'rgb(194, 157, 180)',
            data: xy2,
            xAxisID: 'x-axis-1',
            yAxisID: "y-axis-2"
        },{
            label: label3,
            fill: false,
            backgroundColor: 'rgb(86, 118, 154)',
            borderColor: 'rgb(86, 118, 154)',
            data: xy3,
            xAxisID: 'x-axis-2',
            yAxisID: "y-axis-1"
        },{
            label: label4,
            fill: false,
            backgroundColor: 'rgb(185, 76, 104)',
            borderColor: 'rgb(185, 76, 104)',
            data: xy4,
            xAxisID: 'x-axis-2',
            yAxisID: "y-axis-2"
        }]
    }
    
    return chartData;
}

export function getMultiLineChartOptionsDiff(title, x_min1, x_max1, x_min2, x_max2, y_label, y_max_request) { 

    var options = {
        responsive: true,
        maintainAspectRatio: false,

        title: {
            display: true,
            text: title,
            fontStyle: 'bold',
            fontColor: 'rgb(85,60,165)',
            fontSize: 18,
            padding: 20,
        },
        scales:{
            xAxes: [{
                type: 'time',
                time: zoomTimeOption,
                position: 'bottom',

                scaleLabel: {
                    display: true,
                    labelString: 'Date/Time(Search-1)'
                },
                ticks: {    // YYYYMMDDHHmmss
                    min: x_min1,
                    max: x_max1
               },
               id: "x-axis-1",
            }
            ,{
                type: 'time',
                time: zoomTimeOption,
                position: 'top',

                scaleLabel: {
                    display: true,
                    labelString: 'Date/Time(Search-2)'
                },
                ticks: {    // YYYYMMDDHHmmss
                    min: x_min2,
                    max: x_max2
                },
                id: "x-axis-2",
            }
            ]
            ,yAxes:[{
                type: 'linear',
                display: true,
                position: 'left',
                id: "y-axis-1",
                scaleLabel: {
                    display: true,
                    labelString: y_label
                },
                ticks: { 
                    suggestedMin: 0,
                    suggestedMax: y_max_request
                    // min: 0,
                    // max: 
                }
            }]
        },

        plugins: zoom_plugin_config,
    }

    return options;
}

export function getMultiLineChartOptions2Diff(title, x_min1, x_max1, x_min2, x_max2, y_label1,  y_label2, y_max_request) { 

    var options = {
        responsive: true,
        maintainAspectRatio: false,

        title: {
            display: true,
            text: title,
            fontStyle: 'bold',
            fontColor: 'rgb(85,60,165)',
            fontSize: 18,
            padding: 20,
        },
        scales:{
            xAxes: [{
                type: 'time',
                time: zoomTimeOption,
                position: 'bottom',

                scaleLabel: {
                    display: true,
                    labelString: 'Date/Time(Search-1)'
                },
                ticks: {    // YYYYMMDDHHmmss
                    min: x_min1,
                    max: x_max1
               },
               id: "x-axis-1",
            }
            ,{
                type: 'time',
                time: zoomTimeOption,
                position: 'top',

                scaleLabel: {
                    display: true,
                    labelString: 'Date/Time(Search-2)'
                },
                ticks: {    // YYYYMMDDHHmmss
                    min: x_min2,
                    max: x_max2
                },
                id: "x-axis-2",
            }]
            ,yAxes:[{
                type: 'linear',
                display: true,
                position: 'left',
                id: "y-axis-1",
                scaleLabel: {
                    display: true,
                    labelString: y_label1
                },
                ticks: { 
                    suggestedMin: 0,
                    suggestedMax: y_max_request
                    // min: 0,
                    // max: 
                }
            }
            ,{
                type: 'linear',
                display: true,
                position: 'right',
                id: "y-axis-2",
                scaleLabel: {
                    display: true,
                    labelString: y_label2
                },
                ticks: { 
                    suggestedMin: 0,
                    suggestedMax: y_max_request
                    // min: 0,
                    // max: 
                }
            }]
        },

        plugins: zoom_plugin_config,
    }

    return options;
}

export function getFormatkindList() {

    var url = serverUrl + "/logformatstring/formatkind_list/"

    var items = [];
    let axiosConfig = {
        headers: {
            //'Authorization': 'Token '+ this.token // For Django
        }
    };

    axios.get(url, axiosConfig)
        .then(res => {
            // items.push({
            //     value: "ALL",
            //     text: "ALL"
            // });
            for (let i = 0; i < res.data.list_format_kind.length; i++) {
                let tmp = (res.data.list_format_kind[i] == "jeus") ? "jeus(>= ver7)" : res.data.list_format_kind[i];
                items.push({
                    value: res.data.list_format_kind[i],
                    text: tmp
                });
            }             
        })
        .catch(err => {
            console.error(err);
        });

    return items;
}

export function getMetricskindList() {

    var items = [];
    items.push({
        value: "threshold",
        text: "threshold"
    });
    items.push({
        value: "scope",
        text: "scope"
    });
    items.push({
        value: "pattern",
        text: "pattern"
    });

    return items;
}

export function getMetricsfilterListThreshold() {
    var items = []; 
    items.push({
        value: "frequest",
        text: "frequest"
    });
    items.push({
        value: "fuser_agent",
        text: "fuser_agent"
    });
    items.push({
        value: "ftime_taken",
        text: "ftime_taken"
    });
    items.push({
        value: "fbyte",
        text: "fbyte"
    });
    items.push({
        value: "fip",
        text: "fip"
    });
    items.push({
        value: "fstatus",
        text: "fstatus"
    });
    items.push({
        value: "freferer",
        text: "freferer"
    });
    items.push({
        value: "freserve1",
        text: "freserve1"
    });
    items.push({
        value: "freserve2",
        text: "freserve2"
    });
    items.push({
        value: "log_line",
        text: "log_line"
    });

    return items;
}

export function getMetricsfilterListScope() {
    var items = []; 
    items.push({
        value: "ftime_taken",
        text: "ftime_taken"
    });
    items.push({
        value: "fbyte",
        text: "fbyte"
    });

    return items;
}

export function getMetricsfilterListPattern() {
    var items = []; 
    items.push({
        value: "frequest",
        text: "frequest"
    });
    items.push({
        value: "fuser_agent",
        text: "fuser_agent"
    });
    items.push({
        value: "freferer",
        text: "freferer"
    });
    items.push({
        value: "log_line",
        text: "log_line"
    });

    return items;
}

export function getMetricsunitListFtime() {

    var items = [];
    items.push({
        value: "millis",
        text: "millis"
    });
    items.push({
        value: "micros",
        text: "micros"
    });

    return items;
}

export function getMetricsunitListFstatus() {

    var items = [];
    items.push({
        value: "%_4XX",
        text: "%(4XX CODE)"
    });
    items.push({
        value: "%_5XX",
        text: "%(5XX CODE)"
    });

    return items;
}

export function getMetricsunitListFreserve1() {

    var items = [];
    items.push({
        value: "%_SVC",
        text: "%(Service)"
    });
    items.push({
        value: "%_IPPORT",
        text: "%(IP:PORT)"
    });

    return items;
}

export function getMetricsunitListFbyte() {

    var items = [];
    items.push({
        value: "byte",
        text: "byte"
    });

    return items;
}

export function getMetricsunitListEtc() {

    var items = [];
    items.push({
        value: "%",
        text: "%"
    });

    return items;
}

export function getProjectList(creator) {

    // var url = serverUrl + "/logmaster/"

    var items = [];
    let axiosConfig = {
        headers: {
            //'Authorization': 'Token '+ this.token // For Django
        }
    };

    if (creator == 'Leehs' || creator == 'Admin') {
        var url = serverUrl + "/logmaster/?creator="
    } else {
        var url = serverUrl + "/logmaster/?creator=" + creator
    }

    axios.get(url, axiosConfig)
        .then(res => {
            for (let i = 0; i < res.data.results.length; i++) {
                items.push({
                    value: res.data.results[i].project_id,
                    text: res.data.results[i].project_name
                });
            }             
        })
        .catch(err => {
            console.error(err);
        });

    return items;
}

export function getMetricList() {

    var url = serverUrl + "/metrics/"

    var items = [];
    let axiosConfig = {
        headers: {
            //'Authorization': 'Token '+ this.token // For Django
        }
    };

    axios.get(url, axiosConfig)
        .then(res => {
            for (let i = 0; i < res.data.results.length; i++) {
                items.push({
                    value: res.data.results[i].metric_id,
                    text: res.data.results[i].metric_definition
                });
            }             
        })
        .catch(err => {
            console.error(err);
        });

    return items;
}

export function resetZoom(chart) {

    var comp;

    if (chart == 1) {
        comp = this.$refs.lChart;
    } else if (chart == 2) {
        comp = this.$refs.mlChart;
    } else if (chart == 3) {
        comp = this.$refs.sbChart;
    }    

    // resetZoom 코드
    comp._data._chart.resetZoom();

}