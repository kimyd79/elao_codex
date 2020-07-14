<template>

    <div id="LogIn">

        <ui-container-box :columns=9 vertical class="popup-container">

            <div class="popup-header">
                <div class="popup-header__title">
                    LogIn
                </div>
                <div class="popup-header__close">
                    <lego-icon small>close</lego-icon>
                </div>
            </div>

            <div class="popup-form">

                <ui-form-item :columns=8 
                    label="Username" required left-label :label-width=144 :label-padding=16 >
                    <lego-text-field v-model="login.username" placeholder="enter username" />
                </ui-form-item>

                <ui-form-item :columns=8 
                    label="Password" required left-label :label-width=144 :label-padding=16 >
                    <lego-text-field v-model="login.password" placeholder="enter password" />
                </ui-form-item>

            </div>

            <div class="popup-buttons">
                <lego-button v-on:click="clickCancle">Cancel</lego-button>
                <lego-button main v-on:click="clickLogin">LogIn</lego-button>
            </div>

        </ui-container-box>

    </div>

</template>

<script>
import axios from 'axios';

export default {
    name: 'Login',
    data: function() {
        return {
            login : {
                type : Object,
                default : function() {
                    return { username:'', password:''}
                }
            }
        }
    },
    methods: {
        clickCancle: function() {
            this.show(false);
        },
        
        clickLogin: function() {
            EventBus.$emit("Login", this.login);
        }
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
.popup-buttons {
    display: flex;
    justify-content: flex-end;
    margin-top: 16px;
}
.popup-form .ui-form-item {
    margin-top: 32px;
}
</style>