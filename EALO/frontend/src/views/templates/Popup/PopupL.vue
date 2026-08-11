<template>

    <Page title="Popup Large" class="mg-auto">

        <ui-container-box :columns=12 vertical class="popup-container">

            <div class="popup-header">
                <div class="popup-header__title">
                    Title
                </div>
                <div class="popup-header__desc">
                    Lorem Ipsum is simply dummy text of the printing and typesetting industry.
                </div>
                <div class="popup-header__close">
                    <lego-icon small>close</lego-icon>
                </div>
            </div>

            <ui-tab box :tabs="tabs" no-action />

            <div class="popup-form">

                <ui-form-item :columns=11 
                    label="Lorem Ipsum" required left-label :label-width=144 :label-padding=16 >
                    <lego-text-field />
                </ui-form-item>

                <ui-form-item :columns=11 
                    label="Lorem Ipsum" required left-label :label-width=144 :label-padding=16 >
                    <lego-text-field textarea rows="3" />
                </ui-form-item>

                <ui-form-item :columns=11 
                    label="Lorem Ipsum" required left-label :label-width=144 :label-padding=16 >
                    Lorem Ipsum is simply dummy text of the printing and typesetting industry.
                </ui-form-item>

                <ui-form-item :columns=11 
                    label="Lorem Ipsum" required left-label :label-width=144 :label-padding=16 >
                    2018.09.21 12:45:30
                </ui-form-item>

                <ui-form-item :columns=11 
                    label="Lorem Ipsum" required left-label :label-width=144 :label-padding=16 >
                    As regular PM causes Korea Billing Checkout System to be interrupted, please note your job.<br>
                    Operations Target
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
    name: 'popup-xl',
    components: {
        Page
    },
    data: function() {
        return {
            tabs: [
                { label: "Tab_1",  isSelected: true },
                { label: "Tab_2",  isSelected: false },
                { label: "Tab_3",  isSelected: false }
            ],
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
    margin-bottom: 32px;
}
.popup-header__title {
    font-size: 24px;
    font-weight: bold;
}
.popup-header__desc {
    color: #767676;
    margin-top: 16px;
}
.popup-header__close {
    position: absolute;
    top: 0;
    right: 0;
}
.popup-header__close:hover {
    cursor: pointer;
}
.popup-step {
    margin-top: 48px;
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