<template>
<div id="notice" >
    
    <ui-card :columns="10" :height="160" :padding="2" >
        <ui-card-item header>Findings</ui-card-item>
        <component :is="currentView" v-on:popupClose="currentView=null" :finding="finding"></component>
        <vue-element-loading :active="isActive" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
        <ui-card-item sub class="card_box">                        
            <span style="color:#553ca5" v-for="(finding, idx) in findingListResult" :key="idx"> 
                <b>[{{idx+1}}] {{finding.description}}</b><br>
                <span style="color:#553ca5" v-for="(result, idx) in finding.results" :key="idx" v-on:click="getMetricDetailSearch(finding, result)"> 
                    > {{result.result}} : {{result.result_value}} <br>
                </span>    
            </span>           
        </ui-card-item>
        <ui-card-item body></ui-card-item>

    </ui-card>

</div>
</template>

<script>
import axios from "axios";
import {
    mapGetters
} from "vuex";
import VueElementLoading from 'vue-element-loading'
import DetailPopup from './DetailPopup';
import {
    serverUrl
} from "@/common";

export default {
    name: "Notice",

    components: {
        // export Loading Spinner components
        VueElementLoading,
        DetailPopup,
    },

    data() {
        return {
            // Loading Spinner data
            isActive: false,
            LongTransactionCount: 0,
            currentView: null,
            findingList: [],
            findingListResult: [],
            finding: [{
                description: '',
                results: [],
                metric_kind: '',
                metric_filter: '',
                metric_unit: '',
                metric_value1: '',
                metric_value2: '',
                metric_static: '',
            }],
        }
    },

    created() {
        this.getMetrics()
    },

    computed: mapGetters({
        projectName: "getProjectName",
        fileNames: "getFileNames",
        logFormat: "getLogFormat",
        logfileID: "getLogFileID",
        projectID: "getProjectID",

        dateFromValue: "getFromDate",
        dateToValue: "getToDate",
        timeFromValue: "getFromTime",
        timeToValue: "getToTime",
        threshold: "getThreshold",

        conditionValue: "getCondition",
        searchValue: "getSearchKeyword",

        ttFromValue: "getFromTimeTaken",
        ttToValue: "getToTimeTaken",

        threshold: "getThreshold",

        isSearch: "getToggleSearch",
        isSearch1: "getToggleSearch1",
    }),

    methods: {

        getFilter() {

            let filter = {
                dateFromValue: this.dateFromValue,
                dateToValue: this.dateToValue,
                timeFromValue: this.timeFromValue,
                timeToValue: this.timeToValue,

                conditionValue: this.conditionValue,
                searchValue: this.searchValue,

                ttFromValue: this.ttFromValue,
                ttToValue: this.ttToValue,

                project_id: this.projectID,
            }

            return filter
        },

        async getMetrics() {                    
            
            let items = []
            let descriptionString = ''

            // Start Loading Spinner
            // TODO: 로직 수정해야 함..아래 문제 생김(Loading Bar 관련)
            this.isActive = true; 

            let postData = {
                project_id: this.projectID,
                
                filter: this.getFilter(),
            };

            await axios
                .post(serverUrl + "/logdetail_dynamic/findings/", postData)
                .then(res => {

                    for (let i = 0; i < res.data.findingsResult.length; i++) {
                        // if (res.data.findingsResult[i].metric_kind == 'threshold') {
                        //     descriptionString = "["+res.data.findingsResult[i].metric_kind+"] "+res.data.findingsResult[i].metric_definition+" [static:"+res.data.findingsResult[i].metric_static+"] ["+res.data.findingsResult[i].metric_filter+" <= "+res.data.findingsResult[i].metric_value1+" "+res.data.findingsResult[i].metric_unit+"]"
                        // } else {
                        //     descriptionString = "["+res.data.findingsResult[i].metric_kind+"] "+res.data.findingsResult[i].metric_definition+" [static:"+res.data.findingsResult[i].metric_static+"] ["+res.data.findingsResult[i].metric_value1+" <= "+res.data.findingsResult[i].metric_filter+" <= "+res.data.findingsResult[i].metric_value2+" "+res.data.findingsResult[i].metric_unit+"]"
                        // }

                        descriptionString = "["+res.data.findingsResult[i].metric_kind+"] "+res.data.findingsResult[i].metric_definition+" [static:"+res.data.findingsResult[i].metric_static+"]"

                        items.push({
                            description: descriptionString,                    
                            results: res.data.findingsResult[i].results,
                            metric_kind: res.data.findingsResult[i].metric_kind,
                            metric_filter: res.data.findingsResult[i].metric_filter,
                            metric_unit: res.data.findingsResult[i].metric_unit,
                            metric_value1: res.data.findingsResult[i].metric_value1,
                            metric_value2: res.data.findingsResult[i].metric_value2,
                            metric_static: res.data.findingsResult[i].metric_static,
                        }); 
                    };                                            
                })
                .catch(err => {
                    console.error(err);
                });

            this.findingListResult = items;

            //setTimeout("Temp", 1000);
            this.isActive = false;
    
        },

        getMetricDetailSearch(finding, result) {            
            this.finding = finding
            if (result.result == 'count') {
                this.$store.state.detailsearchKeyword = '';
            } else{
                this.$store.state.detailsearchKeyword = result.result;                
            }  
            this.$store.state.detailcondition = finding.metric_filter;          
            this.$store.state.popupKind = 'FindingsDetail';
            this.$store.state.popupHeader = 'Finding Detail';
            this.$store.state.popupBody = finding.description;
            this.$store.state.popupButton = 'Close';
            this.currentView = 'DetailPopup';
    
        },
        
    },
    watch: {
        
        isSearch() {
            this.getMetrics();
        },

        isSearch1() {
            this.getMetrics();
        }
    }
};
</script>

<style scoped>
.card_box {
    max-height: 300px;
    overflow-y: auto;
}
</style>
