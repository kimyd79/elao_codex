<template>
<div class="modal-mask" transition="modal">
    <div class="modal-wrapper">      
      <ui-container-box :columns=14 vertical class="modal-container">

        <div class="popup-header">
            <div class="popup-header__title">
                Differences
            </div>
            <div class="popup-header__close">
                <lego-icon small v-on:click="clickClose">close</lego-icon>
            </div>
        </div>

        <!-- Table Area-->
        <div class="popup-body add_scroll">
          <!-- TODO:Paging -->
          <ui-table left-header noInfo noAction :columns="columns" :items="items"/>

          <!-- TODO: -->
        </div>
      
        <!-- Chart Area-->
        <span class="page-title__2label">Charts</span>

        <ui-form-row>
            <ui-form-item :columns="12" label="Timeline" align-left required-left>
                <lego-radio v-model="timeCondition" value="1">HH</lego-radio>
                <lego-radio v-model="timeCondition" value="2">HHMM</lego-radio>
                <lego-radio v-model="timeCondition" value="3">HHMMSS</lego-radio>                
            </ui-form-item>            
        </ui-form-row>
        <ui-form-row>
          <lego-button @click="resetZoom()" small>resetZoom</lego-button>
        </ui-form-row>

        
        <!-- <vue-element-loading :active="isActiveMultiLine" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" /> -->
        <chart-line ref='mlChart' :chart-data="mlChartData" :options="mlOptions"></chart-line>

        <div class="popup-buttons">
            <lego-button main v-on:click="clickClose">Close</lego-button>
        </div>

      </ui-container-box>
    </div>
</div>
</template>

<script>
import {
    // TODO: Remove Others
    getMultiLineChartTemplate,
    getMultiLineChartOptions,
    //setCommonStatisticInfo,
    getChartDataFromStatistics,
    getLineChartData,
    //getSearchFilter
} from "@/common"

import UIFormRow from './form/UIFormRow.vue';
import ChartLine from "@/components/layout/ChartLine";

export default {

  components: {
    UIFormRow,
    ChartLine
        
  },
  
  data() {
      return {

          // For Chart
          resetZoomV: "1",
          timeCondition: "1", // "Hour(시) 기준"

          mlChartData: null,
          mlOptions: getMultiLineChartOptions('- No Data -'),

          columns: [
                {label: 'No', key: "no", alignCenter: true, width: 10 },
                {label: 'Request URI', key: "uri", alignCenter: true, width: 80 },
                {label: 'Count_1', key: "count_1", alignCenter: true, width: 15 },
                {label: '%_1', key: "percent_1", alignCenter: true, width: 15 },
                {label: 'Count_2', key: "count_2", alignCenter: true, width: 15 },
                {label: '%_2', key: "percent_2", alignCenter: true, width: 15 },
            ],
            items: [
                {no:'1', uri:'GET /restservice/ci/company/CP0115/gbm/GB007922?extragbm=GB007928&virtualyn=YES HTTP/1.1', count_1:'97', percent_1:'10', count_2:'97', percent_2:'40',},
                {no:'2', uri:'GET /restservice/ci/company/CP0115/gbm/GB007922?extragbm=GB007928&virtualyn=YES HTTP/1.1', count_1:'97', percent_1:'20', count_2:'97', percent_2:'30',},
                {no:'3', uri:'GET /restservice/ci/company/CP0115/gbm/GB007922?extragbm=GB007928&virtualyn=YES HTTP/1.1', count_1:'97', percent_1:'30', count_2:'97', percent_2:'10',},
                {no:'4', uri:'GET /restservice/ci/company/CP0115/gbm/GB007922?extragbm=GB007928&virtualyn=YES HTTP/1.1', count_1:'97', percent_1:'40', count_2:'0', percent_2:'0',},
                {no:'New', uri:'GET /restservice/ci/company/CP0115/gbm/GB007922?extragbm=GB007928&virtualyn=YES HTTP/1.1', count_1:'0', percent_1:'0', count_2:'97', percent_2:'10',},                
            ]
      }
  },

  methods: {
    resetZoom() {       

      this.$refs.mlChart._data._chart.resetZoom();

    },

    showAlert() {
      
      this.$swal('Hello Vue world!!!');
    },

    clickClose: function () {
            
        this.$emit('popupClose');
        
    },
  },
};
</script>

<style scoped>
.table-summary {
    display: flex;
    flex-flow: row nowrap;
    justify-content: flex-end;
    align-items: center;

    font-size: 14px;
    padding: 12px 48px;
    background-color: #F6F6F6;
}
.table-summary-title {
    display: flex;
    font-weight: bold;
    margin-right: auto;
}
.table-summary-item {
    display: flex;
    flex-flow: column nowrap;
    align-items: flex-end;
}
.table-summary-item + .table-summary-item {
    margin-left: 48px;
}


.popup-container {
    padding: 32px;
    border: 1px solid #D0D0D0;
    background-color: white;
}

.popup-header {
    position: relative;
    display: flex;
    flex-flow: column nowrap;

}

.popup-header__title {
    font-size: 24px;
    font-weight: bold;
}

.popup-header__close {
    position: absolute;
    top: 0;
    right: 0;
}

.popup-header__close:hover {
    cursor: pointer;
}

.popup-body {
    font-size: 18px;
    margin: 20px 0;
    word-break: break-all;
}

.popup-buttons {
    display: flex;
    justify-content: flex-end;
    margin-top: 0px;
}

.popup-form .ui-form-item {
    margin-top: 32px;
}

.modal-mask {
    position: fixed;
    z-index: 9997;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: table;
    transition: opacity .3s ease;
}

.modal-wrapper {
    display: table-cell;
    vertical-align: middle;
}

.modal-container {
    width: 50%;
    height: 80%;
    margin: 0px auto;
    padding: 20px 20px 20px 20px;
    background-color: #fff;
    border-radius: 2px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
    transition: all .3s ease;
    font-family: Helvetica, Arial, sans-serif;
}

.modal-header {
    margin-top: 0;
    color: #42b983;
}

.modal-body {
    margin: 20px 0;
}

.modal-button {
    float: right;
}

.modal-enter,
.modal-leave {
    opacity: 0;
}

.modal-enter .modal-container,
.modal-leave .modal-container {
    transform: scale(1.1);
}

.add_scroll {
    max-height: 600px;
    overflow-y: auto;
}
</style>