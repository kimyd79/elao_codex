<template>
<div class="modal-mask" transition="modal">
    <div class="modal-wrapper">
        <ui-container-box :columns=12 vertical class="modal-container">
            <div class="popup-header">
                <div class="popup-header__title">
                    {{ getPopupHeader }}
                </div>
                <div class="popup-header__close">
                    <lego-icon small v-on:click="clickClose">close</lego-icon>
                </div> 
            </div>

            <!--div class="popup-body" v-html="this.$store.state.popupLog">
            </div-->
            <div class="popup-body" v-html="this.logLine">
            </div>

            <div class="popup-buttons">
                <lego-button main v-on:click="clickClose" v-if="buttonClose">Close</lego-button>
                <lego-button v-on:click="clickCancel" v-if="buttonCancel">Cancel</lego-button>
                <lego-button v-on:click="clickOK" v-if="buttonOK">OK</lego-button>
            </div>
        </ui-container-box>
    </div>
</div>
</template>

<script>
import axios from 'axios';
import EventBus from '../../EventBus';
import store from '@/vuex/store';
import * as types from "@/vuex/mutation_types";
import {
    mapGetters
} from 'vuex';

export default {
    name: 'CommonPopup',
    props: {
        logLine: '',
        popupState: ''
    },

    computed: {
        ...mapGetters(['getPopupHeader']),

        buttonClose: function () {
            if (this.$store.state.popupButton == 'Close') return true;
            else return false;
        },
        buttonCancel: function () {
            if (this.$store.state.popupButton == 'CancelOK') return true;
            else return false;
        },
        buttonOK: function () {
            if (this.$store.state.popupButton == 'CancelOK') return true;
            else return false;
        }
    },

    methods: {
        clickClose: function () {
            //console.log("click Popup Close/Cancel Button");
            this.$emit('popupClose');
        },
        clickOK: function () {
            //console.log("click Popup OK Button");
            this.$emit('popupOK');
        },
    }
};
</script>

<style scoped>
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
</style>
