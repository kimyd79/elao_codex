<template>
<div id="Register">

    <ui-container-box :columns=9 vertical class="popup-container">

        <div class="popup-header">
            <div class="popup-header__title">
                Register
            </div>
            <div class="popup-header__close">
                <lego-icon small v-on:click="clickCancle">close</lego-icon>
            </div>
        </div>

        <div class="popup-form">

            <ui-form-item :columns=8 label="Username" required left-label :label-width=144 :label-padding=16>
                <lego-text-field v-model="register.username" placeholder="Enter username" />
            </ui-form-item>

            <ui-form-item :columns=8 label="Password" required left-label :label-width=144 :label-padding=16>
                <lego-text-field v-model="register.password1" placeholder="Enter password" password/>
            </ui-form-item>

            <ui-form-item :columns=8 label="Confirm Password" required left-label :label-width=144 :label-padding=16>
                <lego-text-field v-model="register.password2" placeholder="Confirm password" password/>
            </ui-form-item>

            <ui-form-item :columns=8 label="E-mail" required left-label :label-width=144 :label-padding=16>
                <lego-text-field v-model="register.email" v-on:keyup.enter="clickRegister" placeholder="Enter e-mail" />
            </ui-form-item>

        </div>

        <div class="popup-buttons">
            <lego-button v-on:click="clickCancle">Cancel</lego-button>
            <lego-button main v-on:click="clickRegister">Register</lego-button>
        </div>

    </ui-container-box>

</div>
</template>

<script>
import axios from 'axios';

import {
    serverUrl
} from "@/common";

export default {
    name: 'Register',
    data: function () {
        return {
            register: {
                type: Object,
                default: function () {
                    return {
                        username: '',
                        password1: '',
                        password2: '',
                        email: ''
                    }
                }
            },
        }
    },
    methods: {
        clickCancle: function () {
            this.$router.push('/');
        },

        clickRegister: function () {
            axios.post(serverUrl + '/rest-auth/registration/', this.register)
                .then((response) => {
                    // axios.post(serverUrl + '/user/active/', this.register)
                    //     .then((response) => {
                    //         this.$alert("Your account has been successfully created. Administrator approval required for LogIn.", "Notification", "success");
                    //         this.$router.push('/');
                    //     })
                    //     .catch((err) => {
                    //         console.error(err);
                    //     })
                    this.$swal({
                        title: 'Notification',
                        html: 'Your account has been successfully created. You are able to login NOW.',
                        icon: 'success',
                        confirmButtonColor: '#553ca5',                
                        confirmButtonText: 'OK',
                    });
                    this.$router.push('/');
                })
                .catch((err) => {
                    if (err.response.status == "400"){
                        let errMsg = ''

                        // TODO: vue-simple-alert message 줄바꿈 방법 확인 필요.
                        // 우선 error 가 여러개일 경우 마지막 한개만 표시됨.  
                        for (var prop in err.response.data) {
                            console.log(prop, err.response.data[prop]); 
                            errMsg = errMsg + prop+ " "+err.response.data[prop] + "<br>"
                        }
                        this.$swal({
                            title: 'Notification',
                            html: errMsg,
                            icon: 'error',
                            confirmButtonColor: '#553ca5',                
                            confirmButtonText: 'OK',
                        });
                    } else {
                        console.error(err);
                    }  
                })
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

.popup-buttons {
    display: flex;
    justify-content: flex-end;
    margin-top: 16px;
}

.popup-form .ui-form-item {
    margin-top: 32px;
}
</style>
