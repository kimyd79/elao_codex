<template>
<div id="metricsresult">

    <div class="page-summary-title">Metrics Result</div>

    <component :is="currentView" v-on:popupClose="currentView=null" :metric="metric"></component>

    <ui-form-item :columns=20 align-right margin-right>
        <lego-button main v-on:click="clickAdd">Add</lego-button>
        <lego-button main v-on:click="clickUpdate">Update</lego-button>
        <lego-button main v-on:click="clickDelete">Delete</lego-button>
    </ui-form-item>
    <div class="tb_box">
        <table class="page-summary-table">
            <thead>
                <tr>
                    <th>metric type</th>
                    <th>metric kind</th>
                    <th>metric definition</th>
                    <th>metric filter</th>
                    <th>metric filter2</th>
                    <th>metric unit</th>
                    <th>metric value1</th>
                    <th>metric value2</th>
                    <th>metric static</th>
                    <th>creator</th>
                    <th>created</th>
                </tr>
            </thead>
            <tbody id="list">
            <tr v-for="(metric_list, idx) in metric_lists" :key="idx" v-on:click="clickList(metric_list)" :class="{'highlight': (metric_list.metric_id == selected_metric_id) }">
                    <td>{{metric_list.metric_type}}</td>
                    <td>{{metric_list.metric_kind}}</td>
                    <td>{{metric_list.metric_definition}}</td>
                    <td>{{metric_list.metric_filter}}</td>
                    <td>{{metric_list.metric_filter2}}</td>
                    <td>{{metric_list.metric_unit}}</td>
                    <td>{{metric_list.metric_value1}}</td>
                    <td>{{metric_list.metric_value2}}</td>
                    <td>{{metric_list.metric_static}}</td>
                    <td>{{metric_list.creator}}</td>
                    <td>{{metric_list.created}}</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
</template>

<script>
import axios from 'axios';
import EventBus from '../../EventBus';
import AddMetrics from './AddMetrics';
import UpdateMetrics from './UpdateMetrics';
import store from '@/vuex/store';
import * as types from "@/vuex/mutation_types";
import {
    mapGetters
} from 'vuex';

import {
    serverUrl
} from "@/common";

var urlStr = serverUrl + "/metrics/";

export default {
    name: 'MetricsResult',
    components: {
        AddMetrics,
        UpdateMetrics,
    },
    data: function () {
        return {
            currentView: null,
            selected_metric_id: null,
            metric_lists: [],
            metric: {
                metric_id: '',
                metric_kind: '',
                metric_type: '',
                metric_definition: '',
                metric_filter: '',
                metric_filter2: '',
                metric_unit: '',
                metric_value1: '',
                metric_value2: '',
                metric_static: '',
                creator: '',
                created: ''
            },
        }
    },
    created() {
        EventBus.$on("searchMetrics", this.getData);
        EventBus.$on("cancelUpdateMetrics", () => {
            this.currentView = null;
        });
        EventBus.$on("updateMetrics", (metric) => {
            this.updateData(metric);
            this.currentView = null;
        });
        EventBus.$on("addMetrics", (metric) => {
            this.addData(metric);
            this.currentView = null;
        });
    },
    beforeDestroy(){
        EventBus.$off("searchMetrics");
        EventBus.$off("cancelUpdateMetrics");
        EventBus.$off("updateMetrics");
        EventBus.$off("addMetrics");
    },

    methods: {
        getData: function (metric_kind) {           

            var url = "";

            if (this.$store.state.userName == 'Leehs' || this.$store.state.userName == 'Admin') {
                url = urlStr + '?metric_kind=' + metric_kind + '&creator='
            } else {
                url = urlStr + '?metric_kind=' + metric_kind + '&creator=' + this.$store.state.userName
            }

            axios.get(url)
                .then((response) => {
                    this.metric_lists = response.data.results;
                    this.selected_metric_id = '';
                    this.metric.metric_id = '';
                    this.metric.metric_kind = '';
                    this.metric.metric_type = '';
                    this.metric.metric_definition = '';
                    this.metric.metric_filter = '';
                    this.metric.metric_filter2 = '';
                    this.metric.metric_unit = '';
                    this.metric.metric_value1 = '';
                    this.metric.metric_value2 = '';
                    this.metric.metric_static = '';
                    this.metric.creator = '';
                    this.metric.created = '';
                })
                .catch((err) => {
                    console.error(err);
                })
        },
        deleteData: function (metric) {
            axios.delete(urlStr + metric.metric_id)
                .then((response) => {
                    this.getData("");
                    EventBus.$emit("searchLogmasterMetric","CLEAR");
                })
                .catch((err) => {
                    this.$swal({
                        title: 'Notification',
                        html: 'Delete Metrics failed.',
                        icon: 'error',
                        confirmButtonColor: '#553ca5',                
                        confirmButtonText: 'OK',
                    });
                })
        },
        updateData: function (metric) {
            axios.put(urlStr + metric.metric_id + '/', metric)
                .then((response) => {
                    this.getData("");
                })
                .catch((err) => {
                    this.$swal({
                        title: 'Notification',
                        html: 'Update Metrics failed. Check for required fields.',
                        icon: 'error',
                        confirmButtonColor: '#553ca5',                
                        confirmButtonText: 'OK',
                    });
                })
        },
        addData(metric) {
            axios.post(urlStr, metric)
                .then((response) => {
                    this.getData("");
                })
                .catch((err) => {
                    this.$swal({
                        title: 'Notification',
                        html: 'Add Metrics failed. Check for required fields.',
                        icon: 'error',
                        confirmButtonColor: '#553ca5',                
                        confirmButtonText: 'OK',
                    });
                })
        },
        clickList: function (metric_list) {
            this.selected_metric_id = metric_list.metric_id;
            this.metric.metric_id = metric_list.metric_id;
            this.metric.metric_kind = metric_list.metric_kind;
            this.metric.metric_type = metric_list.metric_type;
            this.metric.metric_definition = metric_list.metric_definition;
            this.metric.metric_filter = metric_list.metric_filter;
            this.metric.metric_filter2 = metric_list.metric_filter2;
            this.metric.metric_unit = metric_list.metric_unit;
            this.metric.metric_value1 = metric_list.metric_value1;
            this.metric.metric_value2 = metric_list.metric_value2;
            this.metric.metric_static = metric_list.metric_static;
            this.metric.creator = metric_list.creator;
            this.metric.created = metric_list.created;
            this.$store.dispatch("setMetricId", metric_list.metric_id);
            EventBus.$emit("searchLogmasterMetric", metric_list.metric_id);
        },
        clickDelete: function () {
            if (this.metric.metric_id != '') {
                this.$swal({
                    title: 'Are you sure?',
                    text: "Do you want to DELETE Logformat?",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#553ca5',
                    cancelButtonColor: '#dddddd',
                    confirmButtonText: 'OK',
                    reverseButtons: true,
                    }).then((result) => {
                    if (result.isConfirmed) {
                        this.deleteData(this.metric);
                    }
                });
            } else {
                this.$swal({
                        title: 'Notification',
                        html: 'No Metrics selected',
                        icon: 'error',
                        confirmButtonColor: '#553ca5',                
                        confirmButtonText: 'OK',
                    });
            }
        },
        clickUpdate: function () {
            if (this.metric.metric_id != '') {
                this.currentView = 'UpdateMetrics';
            } else {
                this.$swal({
                        title: 'Notification',
                        html: 'No Metrics selected',
                        icon: 'error',
                        confirmButtonColor: '#553ca5',                
                        confirmButtonText: 'OK',
                    });
            }
        },
        clickAdd: function () {
            this.currentView = 'AddMetrics';
        },
    }
};
</script>

<style scoped>
.highlight {
    color: #553CA5;
    background-color: #F3F1F9;
    font-weight: bold;
}

.page-container {
    margin: 48px 0 32px;
    padding: 48px 80px;
    background-color: white;
}

.page-title {
    margin-top: 16px;
    margin-bottom: 32px;
    padding-bottom: 16px;
    border-bottom: 1px solid #cccccc;
}

.page-title__label {
    font-size: 32px;
    font-weight: bold;
}

.page-form-area {
    padding: 16px 0;
    border-bottom: 1px solid #cccccc;
}

.page-summary-area {
    margin-top: 48px;
}

.page-summary-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 24px;
}

.tb_box {
    max-height: 400px;
    overflow-y: auto;
}

.page-summary-table {
    border-spacing: 0;
    width: 100%;
    height: 20px;
}

.page-summary-table thead th {
    height: 28px;
    border-top: 1px solid #eaeaea;
    font-weight: normal;
    background-color: #f7f7f7;
    position: sticky;
    top: 0px;
}

.page-summary-table thead th+th {
    border-left: 1px solid #eaeaea;
}

.page-summary-table tbody td {
    width: 500px;
    height: 44px;
    text-align: center;
    border-bottom: 1px solid #eaeaea;
}

.page-summary-table tbody tr:first-child td {
    border-top: 1px solid #a5a5a5;
}

.page-summary-table tbody td+td {
    border-left: 1px solid #eaeaea;
}

.page-tab-area {
    margin-top: 60px;
    border-bottom: 1px solid #cccccc;
}

.page-table-area {
    margin: 32px 0 24px;
}
</style>
