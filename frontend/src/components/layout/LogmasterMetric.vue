<template>
<div id="LogmasterMetric">
    <div class="page-summary-title">Logmaster Metric</div>
    <component :is="currentView" v-on:popupClose="currentView=null" :logmastermetric="logmastermetric"></component>
    <ui-form-item :columns=20 align-right margin-right>
        <lego-button main v-on:click="clickAdd">Add</lego-button>
        <lego-button main v-on:click="clickUpdate">Update</lego-button>
        <lego-button main v-on:click="clickDelete">Delete</lego-button>
    </ui-form-item>
    <div class="tb_box">
        <table class="page-summary-table">
            <thead>
                <tr>
                    <th>metric name</th>
                    <th>project name</th>
                    <th>logmastermetric creator</th> 
                    <th>logmastermetric created</th> 
                </tr>
            </thead>
            <tbody>
                <tr v-for="(logmastermetric_list, idx) in logmastermetric_lists" :key="idx" v-on:click="clickList(logmastermetric_list)" :class="{'highlight': (logmastermetric_list.logmastermetric_id == selected_logmastermetric_id) }">
                    <td>{{logmastermetric_list.metric_definition}}</td>
                    <td>{{logmastermetric_list.project_name}}</td>
                    <td>{{logmastermetric_list.creator}}</td>
                    <td>{{logmastermetric_list.created}}</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
</template>

<script>
import axios from 'axios';
import EventBus from '../../EventBus';
import AddLogmasterMetric from './AddLogmasterMetric';
import UpdateLogmasterMetric from './UpdateLogmasterMetric';
import CommonPopup from './CommonPopup';
import store from '@/vuex/store';
import * as types from "@/vuex/mutation_types";
import {
    mapGetters
} from 'vuex';
import {
    serverUrl
} from "@/common";

var urlStr = serverUrl + "/logmastermetric/";

export default {
    name: 'LogmasterMetric',
    components: {
        AddLogmasterMetric,
        UpdateLogmasterMetric,
        CommonPopup,
    },
    data: function () {
        return {
            currentView: null,
            selected_logmastermetric_id: null,
            logmastermetric_lists: [],
            logmastermetric: {
                logmastermetric_id: '',
                metric: '',
                project: '',
                creator: '',
                created: ''
            },
        }
    },

    created() {
        EventBus.$on("searchLogmasterMetric", this.getData);
        EventBus.$on("updateLogmasterMetric", (logmastermetric) => {
            this.updateData(logmastermetric);
            this.currentView = null;
        });
        EventBus.$on("addLogmasterMetric", (logmastermetric) => {
            this.addData(logmastermetric);
            this.currentView = null;
        });
    },
     beforeDestroy(){
        EventBus.$off("searchLogmasterMetric");
        EventBus.$off("updateLogmasterMetric");
        EventBus.$off("addLogmasterMetric");
    },

    methods: {
        getData: function (metric) {
            if (metric == 'CLEAR') {
                this.logmastermetric_lists=null;
                return 0;
            }
            if (this.$store.state.userName == 'Leehs' || this.$store.state.userName == 'Admin') {
                var url = urlStr + '?metric=' + metric + '&creator='
            } else {
                var url =urlStr + '?metric=' + metric + '&creator=' + this.$store.state.userName
            }
            axios.get(url)
                .then((response) => {
                    this.logmastermetric_lists = response.data.results;
                    this.selected_logmastermetric_id = '';
                    this.logmastermetric.logmastermetric_id = '';
                    this.logmastermetric.metric = '';
                    this.logmastermetric.project = '';
                    this.logmastermetric.creator = '';
                    this.logmastermetric.created = '';
                })
                .catch((err) => {
                    console.error(err);
                });
        },

        deleteData: function (logmastermetric) {
            axios.delete(urlStr + logmastermetric.logmastermetric_id)
                .then((response) => {
                    //console.log(response);
                    this.getData(logmastermetric.metric);
                    //this.logmastermetric_lists = null;
                })
                .catch((err) => {
                    console.error(err);  
                    this.$alert("Delete LogmasterMetric failed. Check for required fields.", "Notification", "error");                  
                })
        },
        updateData: function (logmastermetric) {
            axios.put(urlStr + logmastermetric.logmastermetric_id + '/', logmastermetric)
                .then((response) => {
                    //console.log(response);
                    this.getData(logmastermetric.metric);
                })
                .catch((err) => {
                    console.error(err);
                    this.$alert("Update LogmasterMetric failed. Check for required fields.", "Notification", "error");
                })
        },
        addData(logmastermetric) {

            // TODO: Check
            console.log("logmastermetric : "+logmastermetric);
            console.table(logmastermetric);

            axios.post(urlStr, logmastermetric)
                .then((response) => {
                    //console.log(response);
                    this.getData(logmastermetric.metric);
                })
                .catch((err) => {
                    console.error(err);
                    this.$alert("Add LogmasterMetric failed. Check for required fields.", "Notification", "error");
                })
        },
        clickList: function (logmastermetric_list) {
            this.selected_logmastermetric_id = logmastermetric_list.logmastermetric_id;
            this.logmastermetric.logmastermetric_id = logmastermetric_list.logmastermetric_id;
            this.logmastermetric.metric = logmastermetric_list.metric;
            this.logmastermetric.project = logmastermetric_list.project;
            this.logmastermetric.creator = logmastermetric_list.creator;
            this.logmastermetric.created = logmastermetric_list.created;
        },
        clickDelete: function () {
            if (this.logmastermetric.logmastermetric_id != '') {
                this.$confirm("Are you sure want to Delete?", "Confirm Delete", "question").then(() => {
                    this.deleteData(this.logmastermetric);
                }).catch(() => {
                    //console.log("Cancel clicked");
                });
            } else {
                this.$alert("No LogmasterMetric selected", "Confirm Delete", "error");
            }
        },
        clickUpdate: function () {
            if (this.logmastermetric.logmastermetric_id != '') {
                this.currentView = 'UpdateLogmasterMetric';
            } else {
                this.$alert("No LogmasterMetric selected", "Confirm Update", "error");
            }
        },
        clickAdd: function () {
            this.currentView = 'AddLogmasterMetric';
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
    max-height: 500px;
    overflow-y: auto;
}

.page-summary-table {
    border-spacing: 0;
    width: 100%;
    height: 20px;
}

.page-summary-table thead th {
    width: 500px;
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
