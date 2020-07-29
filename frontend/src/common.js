// Use like following in vue files
// import { serverUrl, testGlobal } from '@/common'

import axios from "axios";

export var serverUrl = "http://127.0.0.1:8000"

//////////////////////////////////////////////////////////////
// Common Chart Data
//////////////////////////////////////////////////////////////
export function getChartDataFromStatistics(type, logfile_id) {

    // Top 5 일때
    // type=1. Status Codes Top5
    // type=2. Requests Top5
    // type=3. 최다 404 발생 URL Top5
    // type=4. Time Taken Top5        

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
        default:
    }

    //let logfile_id = this.$store.state.logFileID
    console.log(logfile_id)

    let postData = {
        logfile_id: logfile_id,
        type: type
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

export function getLineChartData(kind = 1, timeCondition, logfile_id) {
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
        kind: kind

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
                res.sbarY_400 = res.data.resultY_400
                res.sbarY_500 = res.data.resultY_500
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

    var options = {
        responsive: true,
        maintainAspectRatio: false
    }

    return options;
}