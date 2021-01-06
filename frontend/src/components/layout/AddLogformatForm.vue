<template>
<div class="modal-mask" transition="modal">
    <div class="modal-wrapper">
        <ui-container-box :columns=9 vertical class="modal-container">
            <div class="popup-header">
                <div class="popup-header__title">
                    Add Logformat
                </div>
                <div class="popup-header__close">
                    <lego-icon small v-on:click="clickCancle">close</lego-icon>
                </div>
            </div>

            <div class="popup-form">

                <ui-form-item :columns=8 label="format kind" required left-label :label-width=144 :label-padding=16>
                    <!--lego-text-field v-model="format.format_kind" placeholder="enter format kind. ex)apache, nginx, IIS..." /-->
                    <!-- <lego-dropdown :items="conditions" v-model='format.format_kind' /> -->
                    <lego-dropdown :items="items" v-model='format.format_kind' />
                    
                </ui-form-item>

                <ui-form-item :columns=8 label="format name" required left-label :label-width=144 :label-padding=16>
                    <lego-text-field v-model="format.format_name" placeholder="enter format name. ex)common, combined..." />
                </ui-form-item>

                <ui-form-item :columns=8 label="format strings" required left-label :label-width=144 :label-padding=16>
                    <lego-text-field v-model="format.format_strings" placeholder="enter log format. ex)%h %l %u %t \%r\ %>s %b" />
                </ui-form-item>

                <ui-form-item :columns=8 label="creator" required left-label :label-width=144 :label-padding=16>
                    <lego-text-field disabled v-model="format.creator" />
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
import axios from "axios";
import {
    mapGetters
} from "vuex";
import {
    serverUrl,
    getFormatkindLlist
} from "@/common";
import EventBus from '../../EventBus';

export default {
    name: 'AddLogformatFrom',
    data: function () {
        return {
            format: {
                type: Object,
                default: function () {
                    return {
                        format_kind: '',
                        format_name: '',
                        format_strings: '',
                        creator: ''
                    }
                }
            },
            // for format_kind list
            items: [],
        }
    },

    created() {
        this.items = getFormatkindLlist();
        this.format.creator = this.$store.state.userName
    },    

    methods: {
        clickCancle: function () {
            this.$emit('popupClose');
        },

        clickSave: function () {
            EventBus.$emit("addFormat", this.format);
        },
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
</style>
