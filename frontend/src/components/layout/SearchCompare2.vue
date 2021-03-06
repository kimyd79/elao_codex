<template>
<div id="search">
    <ui-container-box :columns="10" vertical>
        <ui-form-box>
            <span class="page-title__2label">Search-2</span>
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

export default {
    name: "Search",

    components: {
        DatePicker
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

    },
    computed: {
        conditions() {
            let rtn = [];
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
        },

        // mapAction
        setSearchCondition() {
            this.$store.dispatch("setFromDate2", this.dateFromValue);
            this.$store.dispatch("setToDate2", this.dateToValue);
            this.$store.dispatch("setFromTime2", this.timeFromValue);
            this.$store.dispatch("setToTime2", this.timeToValue);

            this.$store.dispatch("setCondition2", this.conditionValue);
            this.$store.dispatch("setSearchKeyword2", this.searchValue);
            this.$store.dispatch("setFromTimeTaken2", this.ttFromValue);
            this.$store.dispatch("setToTimeTaken2", this.ttToValue);

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
