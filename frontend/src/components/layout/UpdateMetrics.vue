<template>
<div class="modal-mask" transition="modal">
    <div class="modal-wrapper">
        <ui-container-box :columns=9 vertical class="modal-container">
            <div class="popup-header">
                <div class="popup-header__title">
                    Update Metrics Information
                </div>
                <div class="popup-header__close">
                    <lego-icon small v-on:click="clickCancle">close</lego-icon>
                </div>
            </div>

            <div class="popup-form">
                <ui-form-item :columns=8 label="metric ID" required left-label :label-width=144 :label-padding=16>
                    <lego-text-field disabled v-model="metric.metric_id" />
                </ui-form-item>
                
                <ui-form-item :columns=8 label="metric type" required left-label :label-width=144 :label-padding=16>
                    <lego-dropdown :items="items_types" v-model="metric.metric_type" />
                </ui-form-item>

                <ui-form-item :columns=8 label="metric kind" required left-label :label-width=144 :label-padding=16>
                    <lego-dropdown :items="items_kind" v-model="metric.metric_kind" />
                </ui-form-item>

                <ui-form-item :columns=8 label="metric definition" required left-label :label-width=144 :label-padding=16>
                    <lego-text-field v-model="metric.metric_definition" />
                </ui-form-item>

                <ui-form-item :columns=8 label="metric filter" required left-label :label-width=144 :label-padding=16>
                    <lego-dropdown :items="items_filter" v-model="metric.metric_filter" />
                </ui-form-item>

                <ui-form-item :columns=8 label="metric filter2" required left-label :label-width=144 :label-padding=16 v-if="metric.creator.toLowerCase() == 'leehs'||  metric.creator.toLowerCase() == 'admin'">
                    <lego-text-field v-model="metric.metric_filter2" />
                </ui-form-item>

                <ui-form-item :columns=8 label="metric unit" required left-label :label-width=144 :label-padding=16>
                    <lego-dropdown :items="items_unit" v-model="metric.metric_unit" />
                </ui-form-item>

                <ui-form-item :columns=8 label="metric min" required left-label :label-width=144 :label-padding=16 v-if="metric.metric_kind === 'scope'">
                    <lego-text-field v-model="metric.metric_value1" />
                </ui-form-item>

                <ui-form-item :columns=8 label="metric max" required left-label :label-width=144 :label-padding=16 v-if="metric.metric_kind === 'scope'">
                    <lego-text-field v-model="metric.metric_value2" />
                </ui-form-item>

                <ui-form-item :columns=8 label="metric value" required left-label :label-width=144 :label-padding=16 v-if="metric.metric_kind === 'pattern'">
                    <lego-text-field v-model="metric.metric_value1" />
                </ui-form-item>

                <ui-form-item :columns=8 label="metric pattern" left-label :label-width=144 :label-padding=16 v-if="metric.metric_kind === 'pattern'">
                    <lego-text-field v-model="metric.metric_value2" />
                </ui-form-item>

                <ui-form-item :columns=8 label="metric value" required left-label :label-width=144 :label-padding=16 v-if="metric.metric_kind === 'threshold'">
                    <lego-text-field v-model="metric.metric_value1" />
                </ui-form-item>

                <ui-form-item :columns=8 label="metric static" required left-label :label-width=144 :label-padding=16>
                    <lego-dropdown :items="conditions" v-model="metric.metric_static" />
                </ui-form-item>

                <ui-form-item :columns=8 label="creator" required left-label :label-width=144 :label-padding=16>
                    <lego-text-field disabled v-model="metric.creator" />
                </ui-form-item>

                <ui-form-item :columns=8 label="created" required left-label :label-width=144 :label-padding=16>
                    <lego-text-field disabled v-model="metric.created" />
                </ui-form-item>

            </div>

            <div class="popup-buttons">
                <lego-button v-on:click="clickCancle">Cancel</lego-button>
                <lego-button main v-on:click="clickSave">Save</lego-button>
            </div>

        </ui-container-box>
    </div>
</div>
</template>

<script>
import axios from 'axios';
import EventBus from '../../EventBus';

import {
    serverUrl,
    getMetricskindList,
    getMetricsfilterList,
    getMetricsunitList,
    getMetricsfilterListThreshold,
    getMetricsfilterListPattern,
    getMetricsfilterListScope,
    getMetricsunitListFtime,
    getMetricsunitListFstatus,
    getMetricsunitListFbyte,
    getMetricsunitListFreserve1,
    getMetricsunitListEtc
    

} from "@/common";

var urlStr = serverUrl + "/metrics/";

export default {
    name: 'UpdateMetrics',
    props: {
        metric: {
            type: Object,
            default: function () {
                return {
                    metric_id: '',
                    metric_kind: '',
                    metric_type: '',
                    metric_definition: '',
                    metric_filter: '',
                    metric_filter2: '',
                    metric_unit: '',
                    metric_value1: '',
                    metric_value2: '',
                    creator: '',
                    created: ''
                }
            }
        },
    },
    data: function () {
        return {
            items_kind: [],
            items_filter: [],
            items_unit: [],
            items_types: [{
                value: "Info",
                text: "Information"
            },{
                value: "Warn",
                text: "Warning"
            }],
        }
    },

    created() {
        this.items_kind = getMetricskindList();
        // this.items_filter = getMetricsfilterList();
        // this.items_unit = getMetricsunitList();

        if(this.metric.metric_kind == 'threshold'){
            this.items_filter = getMetricsfilterListThreshold();
        } else if (this.metric.metric_kind == 'pattern'){
            this.items_filter = getMetricsfilterListPattern();
        } else if (this.metric.metric_kind == 'scope'){
            this.items_filter = getMetricsfilterListScope();
        }
        if(this.metric.metric_filter == 'ftime_taken'){
            this.items_unit = getMetricsunitListFtime();
        } else if (this.metric.metric_filter == 'fstatus'){
            this.items_unit = getMetricsunitListFstatus();
        } else if (this.metric.metric_filter == 'fbyte'){
            this.items_unit = getMetricsunitListFbyte();
        } else if (this.metric.metric_filter == 'freserve1'){
            this.items_unit = getMetricsunitListFreserve1();
        } else {
            this.items_unit = getMetricsunitListEtc();
        }
    },
    watch:{
        metric: {
            deep: true,
            handler(){
                if(this.metric.metric_kind == 'threshold'){
                    this.items_filter = getMetricsfilterListThreshold();
                } else if (this.metric.metric_kind == 'pattern'){
                    this.items_filter = getMetricsfilterListPattern();
                } else if (this.metric.metric_kind == 'scope'){
                    this.items_filter = getMetricsfilterListScope();
                }
                if(this.metric.metric_filter == 'ftime_taken'){
                    this.items_unit = getMetricsunitListFtime();
                } else if (this.metric.metric_filter == 'fstatus'){
                    this.items_unit = getMetricsunitListFstatus();
                } else if (this.metric.metric_filter == 'freserve1'){
                    this.items_unit = getMetricsunitListFreserve1();
                } else {
                    this.items_unit = getMetricsunitListEtc();
                }
            }

        }

    },

    computed: {

        conditions() {
            let rtn = [];
            rtn.push({
                value: "Y",
                text: "Y"
            });
            rtn.push({
                value: "N",
                text: "N"
            });
            return rtn;
        }
    },  

    methods: {
        clickCancle: function () {
            //console.log("click Cancel Button");
            this.$emit('popupClose');
        },

        clickSave: function () {
            if(this.metric.metric_kind == 'threshold') {
                this.metric.metric_value2 = this.metric.metric_value1;
            }
            if(this.metric.metric_filter == 'fstatus') {
                if(this.metric.metric_unit == '%_4XX') {
                    this.metric.metric_value2 = '4';
                } else if (this.metric.metric_unit == '%_5XX') {
                    this.metric.metric_value2 = '5';
                }
            }
            EventBus.$emit("updateMetrics", this.metric);
        }
    }
};
</script>

<style scoped>
.modal {
    position: fixed;
    width: 704px;
    left: 50%;
    margin-left: -20%;
    /* half of width */
    height: 500px;
    top: 50%;
    margin-top: -150px;
    /* half of height */
    overflow: auto;
    background-color: rgb(0, 0, 0);
    background-color: rgba(0, 0, 0, 0.4);
}

.modal-mask {
    position: fixed;
    z-index: 9998;
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
    width: 500px;
    margin: 0px auto;
    padding: 30px 30px 30px 30px;
    background-color: #fff;
    border-radius: 2px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
    transition: all .3s ease;
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

.popup-buttons {
    display: flex;
    justify-content: flex-end;
    margin-top: 16px;
}

.popup-form .ui-form-item {
    margin-top: 32px;
}
</style>
