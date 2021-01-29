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
                    <th>metric kind</th>
                    <th>metric definition</th>
                    <th>metric filter</th>
                    <th>metric unit</th>
                    <th>metric min</th>
                    <th>metric max</th>
                    <th>metric static</th>
                    <th>creator</th>
                    <th>created</th>
                </tr>
            </thead>
            <tbody id="list">
            <tr v-for="(metric_list, idx) in metric_lists" :key="idx" v-on:click="clickList(metric_list)" :class="{'highlight': (metric_list.metric_id == selected_metric_id) }">
                    <td>{{metric_list.metric_kind}}</td>
                    <td>{{metric_list.metric_definition}}</td>
                    <td>{{metric_list.metric_filter}}</td>
                    <td>{{metric_list.metric_unit}}</td>
                    <td>{{metric_list.metric_min}}</td>
                    <td>{{metric_list.metric_max}}</td>
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
                metric_definition: '',
                metric_filter: '',
                metric_unit: '',
                metric_min: '',
                metric_max: '',
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
        // EventBus.$on("updateOK", (metric) => {
        //     this.currentView = null;
        //     this.currentView = 'UpdateMetrics';
        // });
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
        // EventBus.$off("updateOK");
        EventBus.$off("updateMetrics");
        EventBus.$off("addMetrics");
    },

    methods: {
        getData: function (metric_kind) {
            axios.get(urlStr + '?metric_kind=' + metric_kind)
                .then((response) => {
                    //console.log(response);
                    this.metric_lists = response.data.results;
                    this.selected_metric_id = '';
                    this.metric.metric_id = '';
                    this.metric.metric_kind = '';
                    this.metric.metric_definition = '';
                    this.metric.metric_filter = '';
                    this.metric.metric_unit = '';
                    this.metric.metric_min = '';
                    this.metric.metric_max = '';
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
                    //console.log(response);
                    this.getData("");
                    EventBus.$emit("searchLogmasterMetric","CLEAR");
                })
                .catch((err) => {
                    console.error(err);
                    this.$alert("Delete Metrics failed. Check for required fields.", "Notification", "error");
                })
        },
        updateData: function (metric) {
            axios.put(urlStr + metric.metric_id + '/', metric)
                .then((response) => {
                    //console.log(response);
                    this.getData("");
                })
                .catch((err) => {
                    console.error(err);
                    this.$alert("Update Metrics failed. Check for required fields.", "Notification", "error");
                })
        },
        addData(metric) {
            axios.post(urlStr, metric)
                .then((response) => {
                    //console.log(response);
                    this.getData("");
                })
                .catch((err) => {
                    console.error(err);
                    this.$alert("Add Metrics failed. Check for required fields.", "Notification", "error");
                })
        },
        clickList: function (metric_list) {
            this.selected_metric_id = metric_list.metric_id;
            this.metric.metric_id = metric_list.metric_id;
            this.metric.metric_kind = metric_list.metric_kind;
            this.metric.metric_definition = metric_list.metric_definition;
            this.metric.metric_filter = metric_list.metric_filter;
            this.metric.metric_unit = metric_list.metric_unit;
            this.metric.metric_min = metric_list.metric_min;
            this.metric.metric_max = metric_list.metric_max;
            this.metric.metric_static = metric_list.metric_static;
            this.metric.creator = metric_list.creator;
            this.metric.created = metric_list.created;
            this.$store.dispatch("setMetricId", metric_list.metric_id);
            EventBus.$emit("searchLogmasterMetric", metric_list.metric_id);
            //console.log(this.metric_name);
            //console.log("click ID : " + metric_list.metric_id);

        },
        clickDelete: function () {
            if (this.metric.metric_id != '') {
                this.$confirm("Are you sure want to Delete?", "Confirm Delete", "question").then(() => {
                    //console.log("OK clicked");
                    this.deleteData(this.metric);
                }).catch(() => {
                    //console.log("Cancel clicked");
                });
            } else {
                this.$alert("No Metrics selected", "Confirm Delete", "error");
            }
        },
        clickUpdate: function () {
            if (this.metric.metric_id != '') {
                this.currentView = 'UpdateMetrics';
            } else {
                this.$alert("No Metrics selected", "Confirm Update", "error");
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
