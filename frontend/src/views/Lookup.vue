<template>
<ui-container-box :columns="22" vertical class="page-container">

    <ui-container-box :columns="20" horizontal align-center class="page-title">
        <span class="page-title__label">Lookup</span>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
        <info></info>
        <notice></notice>
    </ui-container-box>
    
    <ui-form-box class="page-title-sub">
        <span class="page-title__2label">Conditions</span>
        <ui-form-row>
            <ui-form-item :columns="12" label="Date/Time" required-left>

                <date-picker type="date" value-type="format" format="YYYYMMDD" v-model="dateFromValue" default-value="dateFromValue" placeholder="YYYYMMDD" style="width:140px"></date-picker>&nbsp;&nbsp;
                <date-picker type="time" value-type="format" format="HHmmss" v-model="timeFromValue" default-value="timeFromValue" placeholder="HHmmss" style="width:140px"></date-picker>
                &nbsp;&nbsp;&nbsp;&nbsp;~&nbsp;&nbsp;&nbsp;&nbsp;
                <date-picker type="date" value-type="format" format="YYYYMMDD" v-model="dateToValue" default-value="dateToValue" placeholder="YYYYMMDD" style="width:140px"></date-picker>&nbsp;&nbsp;
                <date-picker type="time" value-type="format" format="HHmmss" v-model="timeToValue" default-value="timeToValue" placeholder="HHmmss" style="width:140px"></date-picker>
            </ui-form-item>
        </ui-form-row>

        <ui-form-row>
            <ui-form-item :columns="8" label="Search Strings">                
                <lego-text-field v-model="searchValue" placeholder="Enter your keyword" searchable />
            </ui-form-item>
        </ui-form-row>

        <ui-form-row>
            <ui-form-item :columns="6" label="Before / After">
                <lego-text-field v-model="beforeLines" placeholder="- lines" />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/<lego-text-field v-model="afterLines" placeholder="+ lines" />
            </ui-form-item>
            <ui-form-item :columns="8" align-right margin-right>
                <lego-button v-on:click="initialize">Initialize</lego-button>
                <lego-button v-on:click="clear">Clear</lego-button>
                <lego-button v-on:click="search" main>Search</lego-button>
            </ui-form-item>
        </ui-form-row>
    </ui-form-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area"> 
    </ui-container-box> 
    Total : {{ totalCount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}    
        
        <div class="page-content card_box">
            <span v-for="(log, idx) in resultLogs" :key="idx">
                <span v-bind:style= " log.is_main == 'true' ? 'color:blue' : 'color:black' " > 
                    [{{idx+1}}] <!--[{{log.id}}]--> <text-highlight :queries="queries"> {{ log.log_line }} </text-highlight>
                </span>
                <br>
                <span v-if="log.is_last == 'true'"> 
                    ---------------------------------------------------------------
                    <br>
                </span>                
            </span>                     
            <infinite-loading spinner="spiral" v-on:infinite="search"></infinite-loading>
        </div>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">        
    </ui-container-box>

    <ui-container-box :columns="20" horizontal>
        <ui-container-box :columns="10" vertical class="mt20">
            <font size="4">CI-TEC</font>
        </ui-container-box>
        <ui-container-box :columns="3" vertical class="mt20">
            <img src="@/assets/ico_footer.png" alt="Samsung SDS" />
        </ui-container-box>
    </ui-container-box>

</ui-container-box>
</template>

<script>
import Search from '@/components/layout/Search'
import Info from '@/components/layout/Info'
import Notice from '@/components/layout/Notice'

import DatePicker from 'vue2-datepicker';
import 'vue2-datepicker/index.css';
import axios from "axios";

import InfiniteLoading from 'vue-infinite-loading';
import TextHighlight from 'vue-text-highlight';

import {
    mapGetters
} from "vuex";

import {    
    getSearchFilter,
    serverUrl
} from "@/common"

export default {
    name: 'Lookup',

    // 컴포넌트 등록
    components: {
        'Info': Info,
        'Notice': Notice,
        'Search': Search,
        'DatePicker': DatePicker,
        'InfiniteLoading': InfiniteLoading,
        'TextHighlight': TextHighlight
    },

    data() {
        return {
            
            dateFromValue: '',
            dateToValue: "",
            timeFromValue: "",
            timeToValue: "",
            projectID: "",
            searchValue: "",

            beforeLines: "",
            afterLines: "",            

            resultLogs: [],            
            scrollLimit: 30,
            scrollCurrentPage: 0,
            totalCount: 0,

            // For Highlighting
            queries: [''],

        };
    },
    created() {

        // Initial Value Setting
        this.dateFromValue = this.$store.state.fromDate
        this.dateToValue = this.$store.state.toDate
        this.timeFromValue = this.$store.state.fromTime
        this.timeToValue = this.$store.state.toTime
        this.searchValue = this.$store.state.searchKeyword
        this.projectID = this.$store.state.projectID
    },
    methods: {
        initialize() {

            this.dateFromValue = this.$store.state.global_fromDate;
            this.dateToValue = this.$store.state.global_toDate;
            this.timeFromValue = this.$store.state.global_fromTime;
            this.timeToValue = this.$store.state.global_toTime;
                        
            this.searchValue = "";
            this.beforeLines = "";
            this.afterLines = "";

            this.resultLogs = [];
            this.scrollCurrentPage = 0;
            this.totalCount = 0;
        },

        clear() {
            this.resultLogs = [];
            this.scrollCurrentPage = 0;
            this.totalCount = 0;
        },

        // mapAction
        setSearchCondition() {
            this.$store.dispatch("setFromDate", this.dateFromValue);
            this.$store.dispatch("setToDate", this.dateToValue);
            this.$store.dispatch("setFromTime", this.timeFromValue);
            this.$store.dispatch("setToTime", this.timeToValue);

            this.$store.dispatch("setToggleSearch1");
        },
        
        async search($state) {
            
            //console.log("this.searchValue : "+this.searchValue);            
            this.setSearchCondition();

            this.queries = [];
            if (this.searchValue != ""){
                this.queries.push(this.searchValue);
            }

            //console.log("this.queries : "+this.queries);

            let filters = getSearchFilter(this.dateFromValue, this.dateToValue, this.timeFromValue, this.timeToValue, "", this.searchValue, "", "", this.projectID);

            this.scrollCurrentPage++;

            //console.log("this.scrollCurrentPage : " +this.scrollCurrentPage);
            //console.log("this.scrollLimit : " +this.scrollLimit);

            let offset = this.scrollLimit * (this.scrollCurrentPage - 1);

            //console.log("offset : " +offset);

            var urlstring = serverUrl + "/logdetail_dynamic/?limit=" + this.scrollLimit + "&offset=" + offset + filters;

            // Test
            //var urlstring = serverUrl + "/logdetail_dynamic/?project_id="+this.projectID;

            //console.log("Lookup : "+urlstring);

            //this.scrollBusy = true;

            // TODO: Result 변수선언            
            // Step1 : log line 가져오기 - Step1 없으면 출력
            // Step2 : Before / After 값 존재여부 확인 
            // Step3 : Before / After 라인값과 같이 범위잡아서 가져오기 - log line 별로
            //         /getBeforeAfterDetail 생성필요
            
            // Step1 : log line 가져오기 - Step1 없으면 출력
            var tempResult = await axios.get(urlstring) 
                .then(res => {                    
                    return res.data;                    
                })
                .catch(err => {
                    console.error(err);                   
                });           
            
            this.totalCount = tempResult.count;

            //console.table(tempResult);

            // Step2 : Before / After 값 존재여부 확인 
            //console.log("this.beforeLines : "+this.beforeLines);
            //console.log("this.afterLines : "+this.afterLines);

            if ( this.beforeLines != "" || this.afterLines != ""){ 
                
                if ( this.beforeLines == ""){
                    this.beforeLines = 0;
                }
                if ( this.afterLines == ""){
                    this.afterLines = 0;
                }

                // Step3 : Before / After 라인값과 같이 범위잡아서 가져오기 - log line 별로 : /getBeforeAfterDetail
                var url = serverUrl + "/logdetail_dynamic/get_before_after_detail/"                

                let postData = {

                    project_id: this.projectID,
                    before: this.beforeLines,
                    after: this.afterLines,
                    logs: tempResult,

                };

                let axiosConfig = {
                    headers: {
                        //'Authorization': 'Token '+ this.token // For Django
                    }
                };

                tempResult = await axios.post(url, postData, axiosConfig)

                    .then(res => {                              

                        return res.data;;

                    })
                    .catch(err => {
                        console.error(err);
                    })                
            }

            //console.table(tempResult);

            if (tempResult.results.length) {
                
                this.resultLogs.push(...tempResult.results);

                $state.loaded();
                
            } else {                

                this.resultLogs.push(...tempResult.results);

                $state.complete();
            }

            
            
        }

    },
}
</script>

<style scoped>
.page-container {
    margin: 48px 80px 32px;
    padding: 80px 80px;
    background-color: white;
}

.page-body-area {
    padding: 48px 80px;
    background-color: white;
}

.page-content {
    margin-top: 16px;
    width: 100%;
    height: 480px;
    background-color: #EAEAEA;
}

.page-title-sub {
    margin-top: 16px;
}
.page-title-sub__label {
    font-size: 28px;
    font-weight: bold;
}

.card_box {
    max-height: 480px;
    overflow-y: auto;
}

</style>
