<template>
  <div id="search">
    <ui-container-box :columns="10" vertical title="Search-2" class="mb50">
      <ui-form-box>
        <ui-form-row>
          <ui-form-item :columns="8" label="Date/Time" required-left>
            <!--<lego-date-picker v-model="dateFromValue" />-->
            <lego-text-field v-model="dateFromValue" placeholder="YYYYMMDD" />
            <lego-text-field v-model="timeFromValue" placeholder="hhmmss" />
            <!--<lego-date-picker v-model="dateToValue" />-->
            <lego-text-field v-model="dateToValue" placeholder="YYYYMMDD" />
            <lego-text-field v-model="timeToValue" placeholder="hhmmss" />
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

export default {
  name: "Search",
  data: function() {
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
    
    this.dateFromValue = this.$store.state.fromDate
    this.dateToValue = this.$store.state.toDate
    this.timeFromValue = this.$store.state.fromTime
    this.timeToValue = this.$store.state.toTime
    this.conditionValue = this.$store.state.condition
    this.searchValue = this.$store.state.searchKeyword
    this.ttFromValue = this.$store.state.fromTimeTaken
    this.ttToValue = this.$store.state.toTimeTaken

  },
  computed: {
    conditions() {
      let rtn = [];
      rtn.push({ value: "I", text: "IP" });
      rtn.push({ value: "R", text: "Request" });
      rtn.push({ value: "E", text: "Referrer" });
      rtn.push({ value: "U", text: "UserAgent" });
      rtn.push({ value: "S", text: "Satus" });
      return rtn;
    }
  },
  methods: {
    initialize() {

      this.dateFromValue = "";
      this.dateToValue = "";
      this.timeFromValue = "";
      this.timeToValue = "";
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

      this.$store.dispatch("setToggleSearch2");
    },

    search(){
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