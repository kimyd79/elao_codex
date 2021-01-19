<template>
<div id="notice" >
    <component :is="currentView" v-on:popupClose="currentView=null" :finding="finding"></component>
    <ui-card :columns="10" :height="200" :padding="9" >
        <ui-card-item header>Findings</ui-card-item>
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
            }],
        }
    },

    created() {
        this.getMetrics()
        //this.getNotice()
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
        getNotice() {

            let postData = {
                project_id: this.projectID,
                threshold: this.threshold,
            };

            // Start Loading Spinner
            this.isActive = true;
            axios
                .post(serverUrl + "/logdetail_dynamic/notice/", postData)
                .then(res => {
                    //console.log(res);
                    this.LongTransactionCount = res.data.timetakenResult

                    // Stop Loading Spinner
                    this.isActive = false;
                })
                .catch(err => {
                    console.error(err);
                    // Stop Loading Spinner
                    this.isActive = false;
                });
        },
        getLongTransactionDetail: function () {
            //alert('LongTransactionCount : ' + this.LongTransactionCount)
            //console.log(this.LongTransactionCount +', ' + this.threshold)
            this.$store.state.popupKind = 'LongTransaction';
            this.$store.state.popupHeader = 'Long Transaction Detail';
            this.$store.state.popupBody = 'threshold : >= ' + this.threshold + 'seconds';
            this.$store.state.popupButton = 'Close';
            this.currentView = 'DetailPopup';
        },
        getMetricList: function () {
            // console.log('getMetricList start: ');
            axios.get( serverUrl + '/logmastermetric/?project=' + this.projectID)
                .then((response) => {
                    console.log('getMetricList result: ', response);
                    this.findingList = response.data.results;
                    return response.data.results;
                })
                .catch((err) => {
                    console.error(err);
                });
        },

        async getMetricDetail(metrics) {
            
            // console.log('getMetricDetail input : ', metrics);
            let items = []
            let descriptionString = ''


            // Start Loading Spinner
            // TODO: 로직 수정해야 함..아래 문제 생김(Loading Bar 관련)
            this.isActive = true; 

            for (let i = 0; i < metrics.length; i++) {
                let postData = {
                    project_id: this.projectID,
                    metric_kind: metrics[i].metric_kind,
                    metric_filter: metrics[i].metric_filter,
                    metric_unit: metrics[i].metric_unit,
                    metric_min: metrics[i].metric_min,
                    metric_max: metrics[i].metric_max,
                };

                await axios
                    .post(serverUrl + "/logdetail_dynamic/findings/", postData)
                    .then(res => {
                        // console.log('getMetricDetail result : [',i ,']', res);
                        if (metrics[i].metric_kind == 'threshold') {
                            descriptionString = "["+metrics[i].metric_kind+"] "+metrics[i].metric_definition+" ["+metrics[i].metric_filter+" <= "+metrics[i].metric_min+" "+metrics[i].metric_unit+"]"
                        } else {
                            descriptionString = "["+metrics[i].metric_kind+"] "+metrics[i].metric_definition+" ["+metrics[i].metric_min+" <= "+metrics[i].metric_filter+" <= "+metrics[i].metric_max+" "+metrics[i].metric_unit+"]"
                        }

                        items.push({
                            description: descriptionString,                            
                            result: res.data.findingsResult,
                            metric_kind: metrics[i].metric_kind,
                            metric_filter: metrics[i].metric_filter,
                            metric_unit: metrics[i].metric_unit,
                            metric_min: metrics[i].metric_min,
                            metric_max: metrics[i].metric_max,
                        });                         
                    })
                    .catch(err => {
                        console.error(err);
                    });
            }

            this.findingListResult = items;
            console.log('this.findingListResult final: ', this.findingListResult);

            //setTimeout("Temp", 1000);
            this.isActive = false;
        },

        async getMetrics() {                    
            
            try {
                let res = await axios.get( serverUrl + '/logmastermetric/?project=' + this.projectID)
                console.log('await getMetricList() result : ', res.data.results);
                this.findingList = res.data.results;
                this.getMetricDetail(res.data.results);
                
                // Stop Loading Spinner
                // this.isActive = false;
            } catch (err) {
                console.error(err);
                // Stop Loading Spinner
                // this.isActive = false;
            } 
        },

        // getMetricDetailSearch(idx, metric_kind,metric_filter, metric_unit, metric_min, metric_max) {
        getMetricDetailSearch(idx, finding) {
            console.log('Findings idx : ', idx, ', ', finding)
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
