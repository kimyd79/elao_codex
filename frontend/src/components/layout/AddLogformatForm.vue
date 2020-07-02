<template>
    <div class="modal">
        <ui-container-box :columns=9 vertical class="popup-container">
            <div class="popup-header">
                <div class="popup-header__title">
                    Logformat 추가
                </div>
                <div class="popup-header__close">
                    <lego-icon small v-on:click="clickCancle">close</lego-icon>
                </div>
            </div>

            <div class="popup-form">

                <ui-form-item :columns=8
                    label="제품명" required left-label :label-width=144 :label-padding=16 >
                    <lego-text-field v-model="format.format_kind" placeholder="제품명을 입력해주세요. apache, nginx, IIS..." />
                </ui-form-item>

                <ui-form-item :columns=8
                    label="포맷명" required left-label :label-width=144 :label-padding=16 >
                    <lego-text-field v-model="format.format_name" placeholder="포맷명을 입력해주세요. 커스텀로그1..." />
                </ui-form-item>

                <ui-form-item :columns=8
                    label="로그포맷" required left-label :label-width=144 :label-padding=16 >
                    <lego-text-field v-model="format.format_strings" placeholder="로그포맷을 입력해주세요." />
                </ui-form-item>
                <ui-form-item :columns=8
                    label="생성자" required left-label :label-width=144 :label-padding=16 >
                    <lego-text-field disabled v-model='samplecreator' />
                </ui-form-item>

            </div>

            <div class="popup-buttons">
                <lego-button v-on:click="clickCancle">취소</lego-button>
                <lego-button main v-on:click="clickSave">저장</lego-button>
            </div>

        </ui-container-box>
    </div>
</template>

<script>
import EventBus from '../../EventBus';

export default {
    name: 'AddLogformatFrom',
    data: function() {
        return {
            samplecreator: 'tester',
            format : {
                type : Object,
                default : function() {
                    return { format_kind:'', format_name:'', format_strings:'', creator:'' }
                }
            }
        }
    },
    methods: {
        clickCancle: function() {
            console.log("click Cancel Button");
            EventBus.$emit("cancel");
        },
        
        clickSave: function() {
            this.format.creator = "tester";
            EventBus.$emit("addFormat", this.format);
        }
    }
};
</script>

<style scoped>
/*
.modal {
    display: balck;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgb(0,0,0);
    background-color: rgba(0,0,0,0.4);
}
*/
.modal {
    position: fixed;
    width: 704px;
    left: 50%;
    margin-left: -20%; /* half of width */
    height: 500px;
    top: 50%;
    margin-top: -150px; /* half of height */
    overflow: auto;
    background-color: rgb(0,0,0);
    background-color: rgba(0,0,0,0.4);
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
