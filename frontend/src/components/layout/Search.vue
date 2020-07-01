<template>
  <div id="search">
    <ui-container-box :columns="20" vertical title="Search" class="mb50">
      <ui-form-box>
        <ui-form-row>
          <ui-form-item :columns="12" label="Date/Time" required-left>
            <lego-text-field v-model="dateFromValue" placeholder="YYYYMMDD" />
            <lego-text-field v-model="timeFromValue" placeholder="hhmmss" />            
            <lego-text-field v-model="dateToValue" placeholder="YYYYMMDD" />
            <lego-text-field v-model="timeToValue" placeholder="hhmmss" />
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

export default {
  name: "Search",
  data: function() {
    return {

      conditionValue: "",
      searchValue: "",
      dateFromValue: '',
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
    // ...mapGetters({
    
    //   // TODO : 초기 조건값 세팅필요(파일 업로드 이후 시작시간, 시작시간+10 등)

    //   dateFromValue: "getFromDate",
    //   ateToValue: "getToDate",
    //   imeFromValue: "getFromTime",
    //   imeToValue: "getToTime",
    //   onditionValue: "getCondition",
    //   earchValue: "getSearchKeyword",
    //   tFromValue: "getFromTimeTaken",
    //   ttToValue: "getToTimeTaken",

    // }),

    conditions() {
      let rtn = [];
      rtn.push({ value: "N", text: "None" });
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
      console.log(this.dateFromValue);
      console.log(this.dateToValue);
      console.log(this.timeFromValue);
      console.log(this.timeToValue);
      console.log(this.conditionValue);
      console.log(this.searchValue);
      console.log(this.ttFromValue);
      console.log(this.ttToValue);

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

      this.$store.dispatch("setToggleSearch");
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