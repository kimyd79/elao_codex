<template>

    <Page title="Popup Small" class="mg-auto">

        <ui-container-box :columns=6 vertical class="popup-container">

            <div class="popup-header">
                <div class="popup-header__title">
                    Title
                </div>
                <div class="popup-header__close">
                    <lego-icon small>close</lego-icon>
                </div>
            </div>

            <div class="popup-content">
                If you are a Samsung employee, please use your company <br>
                Email (Knox ID@samsung.com) as your Samsung Account <br>
                ID. <b>Sign In with Knox ID</b>
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
    name: 'popup-s',
    components: {
        Page
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
    margin-top: 24px;
}
.popup-content {
    margin-top: 16px;
}
</style>