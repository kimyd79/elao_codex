<template>
<div id="search">
    <ui-container-box :columns="20" vertical>

        <!-- class="mb50" -->
        <ui-form-box>
            <span class="page-title__2label">Search</span>
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
                <ui-form-item :columns="8" label="Condition">
                    <lego-dropdown :items="conditions" v-model="conditionValue" />
                    <lego-text-field v-model="searchValue" placeholder="Enter your keyword" searchable />
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns="6" label="TimeTaken">
                    <lego-text-field v-model="ttFromValue" placeholder="ms" />
                    &nbsp;&nbsp;&nbsp;&nbsp;~&nbsp;&nbsp;&nbsp;&nbsp;
                    <lego-text-field v-model="ttToValue" placeholder="ms" />
                </ui-form-item>
                <ui-form-item :columns="8" align-right margin-right>
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
//import { mapGetters } from "vuex";

// Timepicker
import DatePicker from 'vue2-datepicker';
import 'vue2-datepicker/index.css';

export default {
    name: "Search",

    components: {
        DatePicker,
    },
    data() {
        return {

            conditionValue: "",
            searchValue: "",
            dateFromValue: '',
            dateToValue: "",
            timeFromValue: "",
            timeToValue: "",
            ttFromValue: "",
            ttToValue: "",

            projectID: "",

        };
    },
    created() {

        // Initial Value Setting
        this.dateFromValue = this.$store.state.fromDate
        this.dateToValue = this.$store.state.toDate
        this.timeFromValue = this.$store.state.fromTime
        this.timeToValue = this.$store.state.toTime
        this.conditionValue = this.$store.state.condition
        this.searchValue = this.$store.state.searchKeyword
        this.ttFromValue = this.$store.state.fromTimeTaken
        this.ttToValue = this.$store.state.toTimeTaken

        this.projectID = this.$store.state.projectID
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
                text: "Status"
            });
            return rtn;
        }
    },
    methods: {
        initialize() {

            // this.dateFromValue = "";
            // this.dateToValue = "";
            // this.timeFromValue = "";
            // this.timeToValue = "";
            this.conditionValue = "";
            this.searchValue = "";
            this.ttFromValue = "";
            this.ttToValue = "";
        },

        // mapAction
        setSerachCondition() {
            this.$store.dispatch("setFromDate", this.dateFromValue);
            this.$store.dispatch("setToDate", this.dateToValue);
            this.$store.dispatch("setFromTime", this.timeFromValue);
            this.$store.dispatch("setToTime", this.timeToValue);

            this.$store.dispatch("setCondition", this.conditionValue);
            this.$store.dispatch("setSearchKeyword", this.searchValue);
            this.$store.dispatch("setFromTimeTaken", this.ttFromValue);
            this.$store.dispatch("setToTimeTaken", this.ttToValue);

            this.$store.dispatch("setToggleSearch");
        },

        search() {
            // TODO : Validation Check

            // Set Global Variable
            this.setSerachCondition()
        }
    },

    watch: {}
};
</script>

<style scoped>

</style>
