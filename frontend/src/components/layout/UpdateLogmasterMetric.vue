<template>
<div class="modal-mask" transition="modal">
    <div class="modal-wrapper">
        <ui-container-box :columns=9 vertical class="modal-container">
            <div class="popup-header">
                <div class="popup-header__title">
                    Modify LogmasterMetric Information
                </div>
                <div class="popup-header__close">
                    <lego-icon small v-on:click="clickCancle">close</lego-icon>
                </div>
            </div>

            <div class="popup-form">
                <ui-form-item :columns=8 label="LogmasterMetric ID" required left-label :label-width=144 :label-padding=16>
                    <lego-text-field disabled v-model="logmastermetric.logmastermetric_id" />
                </ui-form-item>

                <ui-form-item :columns=8 label="metric" required left-label :label-width=144 :label-padding=16>
                    <lego-text-field v-model="logmastermetric.metric" />
                </ui-form-item>

                <ui-form-item :columns=8 label="project" required left-label :label-width=144 :label-padding=16>
                    <lego-text-field v-model="logmastermetric.project" />
                </ui-form-item>

                <ui-form-item :columns=8 label="creator" required left-label :label-width=144 :label-padding=16>
                    <lego-text-field disabled v-model="logmastermetric.creator" />
                </ui-form-item>

                <ui-form-item :columns=8 label="created" required left-label :label-width=144 :label-padding=16>
                    <lego-text-field disabled v-model="logmastermetric.created" />
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
    serverUrl
} from "@/common";

var urlStr = serverUrl + "/metrics/";

export default {
    name: 'UpdateLogmasterMetric',
    props: {
        logmastermetric: {
            type: Object,
            default: function () {
                return {
                    logmastermetric_id: '',
                    metric: '',
                    project: '',            
                    creator: '',
                    created: ''
                }
            }
        }
    },

    methods: {
        clickCancle: function () {
            //console.log("click Cancel Button");
            this.$emit('popupClose');
        },

        clickSave: function () {
            EventBus.$emit("updateLogmasterMetric", this.logmastermetric);
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
