<template>

    <Page title="Popup Medium" class="mg-auto">

        <ui-container-box :columns=9 vertical class="popup-container">

            <div class="popup-header">
                <div class="popup-header__title">
                    Title
                </div>
                <div class="popup-header__close">
                    <lego-icon small>close</lego-icon>
                </div>
            </div>

            <div class="popup-form">

                <ui-form-item :columns=8 
                    label="Lorem Ipsum" required left-label :label-width=144 :label-padding=16 >
                    <lego-text-field />
                </ui-form-item>

                <ui-form-item :columns=8 
                    label="Lorem Ipsum" required left-label :label-width=144 :label-padding=16 >
                    <lego-text-field />
                </ui-form-item>

                <ui-form-item :columns=5
                    label="Lorem Ipsum" required left-label :label-width=144 :label-padding=16 >
                    <lego-dropdown :items="[{value: 'L', text: 'Lorem Ipsum'}]" value="L"/>
                </ui-form-item>

                <ui-form-item :columns=5
                    label="Lorem Ipsum" required left-label :label-width=144 :label-padding=16 >
                    <lego-radio v-model="radioValue" value="1">Yes</lego-radio>
                    <lego-radio v-model="radioValue" value="2">No</lego-radio>
                </ui-form-item>

            </div>

            <div class="popup-buttons">
                <lego-button>Cancel</lego-button>
                <lego-button main>Okay</lego-button>
            </div>

        </ui-container-box>

    </Page>

</template>

<script>
import Page from '../_Frame/PopupPage'

export default {
    name: 'popup-m',
    components: {
        Page
    },
    data: function() {
        return {
            radioValue: '1'
        }
    }
}
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
.popup-buttons {
    display: flex;
    justify-content: flex-end;
    margin-top: 16px;
}
.popup-form .ui-form-item {
    margin-top: 32px;
}
</style>