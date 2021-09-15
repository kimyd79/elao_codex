<template>
<div id="search">
    <ui-container-box :columns="10" vertical>
        <ui-form-box>
            <span class="page-title__2label">Search-2</span>

            <ui-form-row>
                <ui-form-item :columns="11" label="Instances" required-left>                
                    <treeselect v-model="selectedInstances" :multiple="true" :options="options" :defaultExpandLevel="1" :disable-branch-nodes="true" />
                    <!-- v-on:select="setInstances" -->
                    <!-- v-on:select="testEvent" -->
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns="8" label="Date/Time" required-left>
                    <date-picker type="date" value-type="format" format="YYYYMMDD" v-model="dateFromValue" default-value="dateFromValue" placeholder="YYYYMMDD" style="width:120px"></date-picker>&nbsp;&nbsp;
                    <date-picker type="time" value-type="format" format="HHmmss" v-model="timeFromValue" default-value="timeFromValue" placeholder="HHmmss" style="width:120px"></date-picker>
                    &nbsp;&nbsp;&nbsp;&nbsp;~&nbsp;&nbsp;&nbsp;&nbsp;
                    <date-picker type="date" value-type="format" format="YYYYMMDD" v-model="dateToValue" default-value="dateToValue" placeholder="YYYYMMDD" style="width:120px"></date-picker>&nbsp;&nbsp;
                    <date-picker type="time" value-type="format" format="HHmmss" v-model="timeToValue" default-value="timeToValue" placeholder="HHmmss" style="width:120px"></date-picker>
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns="8" label="Condition">
                    <lego-dropdown :items="conditions" v-model="conditionValue" />
                    &nbsp;&nbsp;&nbsp;
                    <lego-text-field v-model="searchValue" placeholder="Enter your keyword" searchable />
                    &nbsp;&nbsp;&nbsp;&nbsp;                    
                    <lego-checkbox v-model="excludeSearch" small >Exclude</lego-checkbox>
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns="8" label="TimeTaken">
                    <lego-text-field v-model="ttFromValue" placeholder="ms" />
                    <lego-text-field v-model="ttToValue" placeholder="ms" />
                    &nbsp;&nbsp;&nbsp;
                    <lego-button v-on:click="initialize">Initialize</lego-button>
                    <lego-button v-on:click="search" main>Search</lego-button>
                </ui-form-item>

            </ui-form-row>
        </ui-form-box>
    </ui-container-box>
</div>
</template>

<script>
// @ is an alias to /src
import axios from "axios";

// Timepicker
import DatePicker from 'vue2-datepicker';
import 'vue2-datepicker/index.css';

import Treeselect from '@riophae/vue-treeselect';
import '@riophae/vue-treeselect/dist/vue-treeselect.css';

import { serverUrl } from "@/common";


export default {
    name: "Search",

    components: {
        DatePicker,
        Treeselect,
    },

    data() {
        return {

            conditionValue: "",
            searchValue: "",
            dateFromValue: "",
            dateToValue: "",
            timeFromValue: "",
            timeToValue: "",
            ttFromValue: "",
            ttToValue: "",

            excludeSearch: false,

            // For Tree
            // define the default value
            selectedInstances: null,
            // define options
            options: [ 
                {
                    id: 'server1',
                    label: 'server1',
                    children: [ 
                        {
                            id: 'server1-instance1',
                            label: 'instance1',
                        }, 
                        {
                            id: 'server1-instance2',
                            label: 'instance2',
                        } 
                    ],
                }, {
                    id: 'server2',
                    label: 'server2',
                }, {
                    id: 'server3',
                    label: 'server3',
                }             
            ],

        };
    },
    created() {
        // Initial Value Setting

        this.dateFromValue = this.$store.state.fromDate2
        this.dateToValue = this.$store.state.toDate2
        this.timeFromValue = this.$store.state.fromTime2
        this.timeToValue = this.$store.state.toTime2
        this.conditionValue = this.$store.state.condition2
        this.searchValue = this.$store.state.searchKeyword2
        this.ttFromValue = this.$store.state.fromTimeTaken2
        this.ttToValue = this.$store.state.toTimeTaken2

        this.projectID = this.$store.state.projectID
        this.excludeSearch = this.$store.state.excludeSearch2;

        if ( this.$store.state.projectServers2 == "")
            this.selectedInstances = null;
        else
            this.selectedInstances = this.$store.state.projectServers2;

        // server, instance 목록 가져오기 by project_id
        var url = serverUrl + "/logfile?project=" + this.projectID

        let axiosConfig = {
            headers: {
                //'Authorization': 'Token '+ this.token // For Django
            }
        };

        axios.get(url, axiosConfig)
        .then(res => {
            // console.log(res.data);

            // Tree 구성
            var treeOptions = []
            
            for(var result of res.data.results){
                //console.log(result);
                //console.log(result.server_name);
                //console.log(result.instance_name);

                var nodeServer = {};    // id, label, children
                var nodeInstance = {};  // id, label

                // check node ids
                var isExist = false;
                var nodeIdx = 0;
                for(var node of treeOptions){
                    if (node.id == result.server_name){
                        isExist = true;
                        break;
                    }
                    nodeIdx = nodeIdx + 1;
                }

                if (isExist) {  // Already Exist -> Add children attribute as array

                    nodeInstance.id = result.server_name+"-"+result.instance_name;
                    nodeInstance.label = result.server_name+"-"+result.instance_name;

                    // check instance duplication
                    for(var child of treeOptions[nodeIdx].children){

                        if (child.id != nodeInstance.id) {
                            //console.log("Not duplicate");
                            treeOptions[nodeIdx].children.push(nodeInstance);
                        }                         
                    }

                }else {         // Not Exist -> Add as object
                    nodeServer.id = result.server_name;
                    nodeServer.label = result.server_name;

                    nodeInstance.id = result.server_name+"-"+result.instance_name;
                    nodeInstance.label = result.server_name+"-"+result.instance_name;

                    nodeServer.children = [ nodeInstance ];

                    treeOptions.push(nodeServer);                    
                }

            }

            this.options = treeOptions;
        })
        .catch(err => {
            console.error(err);
            throw err;
        })

    },
    computed: {
        conditions() {
            let rtn = [];
            rtn.push({
                value: "N",
                text: "None"
            });
            rtn.push({
                value: "I",
                text: "IP"
            });
            rtn.push({
                value: "R",
                text: "Request"
            });
            rtn.push({
                value: "E",
                text: "Referrer"
            });
            rtn.push({
                value: "U",
                text: "UserAgent"
            });
            rtn.push({
                value: "S",
                text: "Satus"
            });
            return rtn;
        }
    },
    methods: {
        initialize() {

            this.dateFromValue = this.$store.state.global_fromDate;
            this.dateToValue = this.$store.state.global_toDate;
            this.timeFromValue = this.$store.state.global_fromTime;
            this.timeToValue = this.$store.state.global_toTime;
            
            this.conditionValue = "";
            this.searchValue = "";
            this.ttFromValue = "";
            this.ttToValue = "";

            this.excludeSearch = false;            

         },

        // mapAction
        setSearchCondition() {
            this.$store.dispatch("setFromDate2", this.dateFromValue);
            this.$store.dispatch("setToDate2", this.dateToValue);
            this.$store.dispatch("setFromTime2", this.timeFromValue);
            this.$store.dispatch("setToTime2", this.timeToValue);

            this.$store.dispatch("setCondition2", this.conditionValue);
            this.$store.dispatch("setSearchKeyword2", this.searchValue);
            this.$store.dispatch("setExcludeSearch2", this.excludeSearch);

            this.$store.dispatch("setFromTimeTaken2", this.ttFromValue);
            this.$store.dispatch("setToTimeTaken2", this.ttToValue);

            this.$store.dispatch("setProjectServers2", this.selectedInstances);

            this.$store.dispatch("setToggleSearch2");
        },

        search() {
            // TODO : Validation Check

            // Set Global Variable
            this.setSearchCondition()
        }
    },

    watch: {}
};
</script>

<style scoped>
</style>
