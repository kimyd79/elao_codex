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

                <ui-form-item :columns=8 
                    label="Username" required left-label :label-width=144 :label-padding=16 >
                    <lego-text-field v-model="register.username" placeholder="enter username" />
                </ui-form-item>

                <ui-form-item :columns=8 
                    label="Password" required left-label :label-width=144 :label-padding=16 >
                    <lego-text-field v-model="register.password1" placeholder="enter password" />
                </ui-form-item>

                <ui-form-item :columns=8 
                    label="Confirm Password" required left-label :label-width=144 :label-padding=16 >
                    <lego-text-field v-model="register.password2" placeholder="confirm password" />
                </ui-form-item>

                <ui-form-item :columns=8 
                    label="email" required left-label :label-width=144 :label-padding=16 >
                    <lego-text-field v-model="register.email" v-on:keyup.enter="clickRegister" placeholder="enter email" />
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

export default {
    name: 'Register',
    data: function() {
        return {
            register : {
                type : Object,
                default : function() {
                    return { username:'', password1:'', password2:'', email:''}
                }
            }
        }
    },
    methods: {
        clickCancle: function() {
            this.$router.push('/');
        },
        
        clickRegister: function() {
            axios.post( 'http://127.0.0.1:8000/rest-auth/registration/', this.register)
            .then((response) => {
            console.log(response);
            this.$router.push('/Login');
            })
            .catch((ex) => {
            console.log('user register failed', ex);
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
