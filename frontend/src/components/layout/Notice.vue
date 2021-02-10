<template>
<div id="notice" >
    
    <ui-card :columns="10" :height="170" :padding="4" >
        <ui-card-item header>Findings</ui-card-item>
        <component :is="currentView" v-on:popupClose="currentView=null" :finding="finding"></component>
        <vue-element-loading :active="isActive" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
        <ui-card-item sub class="card_box">                        
            <span style="color:red" v-for="(finding, idx) in findingListResult" :key="idx" v-on:click="getMetricDetailSearch(idx, finding)"> 
                [{{idx+1}}] {{finding.description}} : {{finding.result}}<br>
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
                result: '',
                metric_kind: '',
                metric_filter: '',
                metric_unit: '',
                metric_min: '',
                metric_max: '',
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
        threshold: "getThreshold"
    }),

    methods: {

        async getMetrics() {                    
            
            let items = []
            let descriptionString = ''

            // Start Loading Spinner
            // TODO: 로직 수정해야 함..아래 문제 생김(Loading Bar 관련)
            this.isActive = true; 

            let postData = {
                project_id: this.projectID,
            };

            await axios
                .post(serverUrl + "/logdetail_dynamic/findings/", postData)
                .then(res => {

                    for (let i = 0; i < res.data.findingsResult.length; i++) {
                        if (res.data.findingsResult[i].metric_kind == 'threshold') {
                            descriptionString = "["+res.data.findingsResult[i].metric_kind+"] "+res.data.findingsResult[i].metric_definition+" [static:"+res.data.findingsResult[i].metric_static+"] ["+res.data.findingsResult[i].metric_filter+" <= "+res.data.findingsResult[i].metric_min+" "+res.data.findingsResult[i].metric_unit+"]"
                        } else {
                            descriptionString = "["+res.data.findingsResult[i].metric_kind+"] "+res.data.findingsResult[i].metric_definition+" [static:"+res.data.findingsResult[i].metric_static+"] ["+res.data.findingsResult[i].metric_min+" <= "+res.data.findingsResult[i].metric_filter+" <= "+res.data.findingsResult[i].metric_max+" "+res.data.findingsResult[i].metric_unit+"]"
                        }

                        items.push({
                            description: descriptionString,                            
                            result: res.data.findingsResult[i].result,
                            metric_kind: res.data.findingsResult[i].metric_kind,
                            metric_filter: res.data.findingsResult[i].metric_filter,
                            metric_unit: res.data.findingsResult[i].metric_unit,
                            metric_min: res.data.findingsResult[i].metric_min,
                            metric_max: res.data.findingsResult[i].metric_max,
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

        getMetricDetailSearch(idx, finding) {
            this.finding = finding
            this.$store.state.popupKind = 'FindingsDetail';
            this.$store.state.popupHeader = 'Finding Detail';
            this.$store.state.popupBody = finding.description;
            this.$store.state.popupButton = 'Close';
            this.currentView = 'DetailPopup';
        },
    }
};
</script>

<style scoped>
.card_box {
    max-height: 300px;
    overflow-y: auto;
}
</style>
