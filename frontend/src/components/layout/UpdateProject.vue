<template>
<div class="modal">
    <ui-container-box :columns=9 vertical class="popup-container">
        <div class="popup-header">
            <div class="popup-header__title">
                Modify Project Information
            </div>
            <div class="popup-header__close">
                <lego-icon small v-on:click="clickCancle">close</lego-icon>
            </div>
        </div>

        <div class="popup-form">
            <ui-form-item :columns=8 label="project ID" required left-label :label-width=144 :label-padding=16>
                <lego-text-field disabled v-model="project.project_id" />
            </ui-form-item>

            <ui-form-item :columns=8 label="project name" required left-label :label-width=144 :label-padding=16>
                <lego-text-field v-model="project.project_name" />
            </ui-form-item>

            <ui-form-item :columns=8 label="project description" required left-label :label-width=144 :label-padding=16>
                <lego-text-field v-model="project.project_description" />
            </ui-form-item>

            <ui-form-item :columns=8 label="creator" required left-label :label-width=144 :label-padding=16>
                <lego-text-field disabled v-model="project.creator" />
            </ui-form-item>
            <ui-form-item :columns=8 label="created" required left-label :label-width=144 :label-padding=16>
                <lego-text-field disabled v-model="project.created" />
            </ui-form-item>

        </div>

        <div class="popup-buttons">
            <lego-button v-on:click="clickCancle">Cancel</lego-button>
            <lego-button main v-on:click="clickSave">Save</lego-button>
        </div>

    </ui-container-box>
</div>
</template>

<script>
import axios from 'axios';
import EventBus from '../../EventBus';

import {
    serverUrl
} from "@/common";

var urlStr = serverUrl + "/logmaster/";

export default {
    name: 'UpdateProject',
    props: {
        project: {
            type: Object,
            default: function () {
                return {
                    project_id: '',
                    project_name: '',
                    project_description: '',
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
            EventBus.$emit("updateProject", this.project);
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
