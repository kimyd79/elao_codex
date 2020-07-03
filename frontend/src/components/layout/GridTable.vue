<template>
  <div id="gridtable">
    <!-- This page is GridTable - {{ isSearch }} -->
    <ui-container-box :columns="20" vertical title="Details" class="mb50">
      <ui-container-box :columns="20" vertical>
        <ui-table header-divider no-action :columns="columns" :items="items" class="mt20"></ui-table>
      </ui-container-box>

      <lego-pagination :pagination="pagingInfo" @move="pageChange" class="mt20" />
    </ui-container-box>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";

export default {
  name: "GridTable",

  data: function() {
    return {

      pagingInfo: {
        rowsPerPage: 10,
        currentPage: 1,
        totalPages: 0,
        totalItems: 0
      },
      columns: [
        {label: 'Date', key: "date", sortable: true, sortValue: "asc", filtable: false, alignRight: false, width: 10 },
        {label: 'Time', key: "time", sortable: true, sortValue: "desc", filtable: true, filterValue:[], alignRight: false, width: 10 },
        {label: 'IP', key: "ip", sortable: false, filtable: true, filterValue:[], alignRight: false, width: 10, filterList: ["Success","Error","Processing"] },
        {label: 'Request', key: "request", sortable: false, filtable: false, alignRight: false, width: 40 },
        {label: 'Referrer', key: "referrer", sortable: true, sortValue: "asc", filtable: true, alignRight: false, width: 15 },
        {label: 'UserAgent', key: "useragent", sortable: false, filtable: false, alignRight: false, width: 10 },
        {label: 'Status', key: "status", sortable: false, filtable: false, alignRight: false, width: 10 },
        {label: 'TimeTaken', key: "timetaken", sortable: false, filtable: false, alignRight: false, width: 10 },
      ],

      // Grid Rows
      items: []
    };
  },

  computed: mapGetters({
    isSearch: "getToggleSearch",
    
    dateFromValue: "getFromDate",
    dateToValue: "getToDate",
    timeFromValue: "getFromTime",
    timeToValue: "getToTime",

    conditionValue: "getCondition",
    searchValue: "getSearchKeyword",

    ttFromValue: "getFromTimeTaken",
    ttToValue: "getToTimeTaken",

  }),

  methods: {
    getDateTimeString(str) {
      return str >= 10 ? str : "0" + str;
    },

    setItemList(results) {
      var dateString, timeString;
      this.items = [];

      for (let i = 0; i < results.length; i++) {
        dateString =
          results[i].fyear +
          "" +
          this.getDateTimeString(results[i].fmonth) +
          "" +
          this.getDateTimeString(results[i].fday);
        timeString =
          this.getDateTimeString(results[i].fhour) +
          "" +
          this.getDateTimeString(results[i].fminute) +
          "" +
          this.getDateTimeString(results[i].fsecond);

        this.items.push({
          date: dateString,
          time: timeString,
          ip: results[i].fip,
          request: results[i].frequest,
          referrer: results[i].referrer,
          useragent: results[i].fuser_agent,
          status: results[i].fstatus,
          timetaken: results[i].ftime_taken,
          isSelected: false
        });
      }

      //console.log("results : "+ this.results)
    },

    getLogDetails() {
      
      console.log("dateFromValue(vuex) : " + this.dateFromValue);
      console.log("dateToValue(vuex) : " + this.dateToValue);
      console.log("timeFromValue(vuex) : " + this.timeFromValue);
      console.log("timeToValue(vuex) : " + this.timeToValue);
      console.log("ttFromValue(vuex) : " + this.ttFromValue);
      console.log("ttToValue(vuex) : " + this.ttToValue);

      console.log("conditionValue(vuex) : " + this.conditionValue);
      console.log("searchValue(vuex) : " + this.searchValue);      

      console.log("pagingInfo : " + this.pagingInfo.rowsPerPage);
      console.log("pagingInfo : " + this.pagingInfo.currentPage);

      let offset =
        this.pagingInfo.rowsPerPage * (this.pagingInfo.currentPage - 1);

      // 1 : 0~9, 2 : 10~19,
      console.log("offset :" + offset);

      // Filter String
      let filters=""
      if ( this.dateFromValue != '') {
        filters = filters + "&dateFromValue="+this.dateFromValue
      }
      if ( this.dateToValue != '') {
        filters = filters + "&dateToValue="+this.dateToValue
      }
      if ( this.timeFromValue != '') {
        filters = filters + "&timeFromValue="+this.timeFromValue
      }
      if ( this.timeToValue != '') {
        filters = filters + "&timeToValue="+this.timeToValue
      }
      if ( this.conditionValue != '') {
        filters = filters + "&conditionValue="+this.conditionValue
      }
      if ( this.searchValue != '') {
        filters = filters + "&searchValue="+this.searchValue
      }
      if ( this.ttFromValue != '') {
        filters = filters + "&ttFromValue="+this.ttFromValue
      }
      if ( this.ttToValue != '') {
        filters = filters + "&ttToValue="+this.ttToValue
      }

      console.log("filters : "+filters)

      var urlstring =
        "http://127.0.0.1:8000/logdetail/?limit=" +
        this.pagingInfo.rowsPerPage +
        "&offset=" +
        offset + filters;

      // TODO : Set axiosConfig to set headers
      //let axiosConfig = {
      //  headers: {
      //    'Authorization': 'Token '+ this.token // For Django
      //  }
      //};

      // TODO : Set GET parametes, ex) /logdetail/?limit=10&offset=20
      axios
        .get(urlstring)
        .then(res => {
          //console.log(res.data)       // 전체 Object
          console.log(res.data.count); // 전체건수

          this.pagingInfo.totalItems = res.data.count;

          console.log(this.pagingInfo.totalPages);

          console.log(res.data.results); // 결과(offset)

          //this.tempItems = res.data.results

          // TODO #1 : Data 처리 - Table Row에 맞도록 => items에 매핑
          this.setItemList(res.data.results);
          // TODO #3 : Graph 그리기 - Analysis 화면
        })
        .catch(err => {
          console.error(err);
        });
    },

    pageChange(page) {
      console.log(page);
      this.pagingInfo.currentPage = page;
      this.getLogDetails();
    }
  },

  created() {
    this.getLogDetails();

  },

  watch: {
    isSearch() {
      //alert('This value is changed -- '+ this.isSearch)
      this.getLogDetails();
    }
  }
};
</script>

<style scoped>
</style>