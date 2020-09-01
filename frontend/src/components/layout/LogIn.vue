<template>

    <div id="LogIn">

        <ui-container-box :columns=9 vertical class="popup-container">

            <div class="popup-header">
                <div class="popup-header__title">
                    LogIn
                </div>
                <div class="popup-header__close">
                    <lego-icon small v-on:click="clickCancle">close</lego-icon>
                </div>
            </div>

            <div class="popup-form">

                <ui-form-item :columns=8 
                    label="Username" required left-label :label-width=144 :label-padding=16 >
                    <lego-text-field v-model="login.username" placeholder="enter username" />
                </ui-form-item>

                <ui-form-item :columns=8 
                    label="Password" required left-label :label-width=144 :label-padding=16 >
                    <lego-text-field v-model="login.password" v-on:keyup.enter="clickLogin" placeholder="enter password" />
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
import * as types from "@/vuex/mutation_types";
import { mapGetters } from "vuex";

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
            this.$router.push('/');
        },
        
        clickLogin: function() {
            var url = "http://127.0.0.1:8000/rest-auth/login/"

            axios.post( url, this.login )
            .then((response) => {
            console.log(response);
            //토큰을 로컬스토리지에 저장
            localStorage.setItem('user-token', response.data.key);
            this.$store.dispatch("setUserToken", response.data.key);
            axios.defaults.headers.common['Authorization'] = 'Token '+ response.data.key;
            console.log(this.$store.state.userToken);
            this.getUserInfo();
            })
            .catch((ex) => {
            console.log('user login failed', ex);
            })
        },

        getUserInfo: function() {
            var url = "http://127.0.0.1:8000/rest-auth/user/"

            let axiosConfig = {
                headers: {
                'Authorization': 'Token '+ this.$store.state.userToken
                }
            };
            console.log(this.$store.state.userName);
            console.log(axiosConfig);
            axios.get( url, axiosConfig )
            .then((response) => {
            console.log(response);
            //토큰을 로컬스토리지에 저장
            localStorage.setItem('user-name', response.data.username);
            this.$store.dispatch("setUserName", response.data.username);
            console.log(this.$store.state.userName);
            this.$router.push('/');
            })
            .catch((ex) => {
            console.log('get user info failed', ex);
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
