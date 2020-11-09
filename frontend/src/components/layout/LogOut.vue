<template>
<div id="LogOut">

    <ui-container-box :columns=9 vertical class="popup-container">

        <div class="popup-header">
            <div class="popup-header__title">
                LogOut
            </div>
            <div class="popup-header__close">
                <lego-icon small>close</lego-icon>
            </div>
        </div>

        <div class="popup-form">

            <ui-form-item :columns=8 label="Username" required left-label :label-width=144 :label-padding=16>
                <lego-text-field disabled v-model="username" />
            </ui-form-item>

        </div>

        <div class="popup-buttons">
            <lego-button v-on:click="clickCancle">Cancel</lego-button>
            <lego-button main v-on:click="clickLogout">LogOut</lego-button>
        </div>

    </ui-container-box>

</div>
</template>

<script>
import axios from 'axios';
import * as types from "@/vuex/mutation_types";
import {
    mapGetters
} from "vuex";

import {
    serverUrl
} from "@/common";

export default {
    name: 'LogOut',
    data: function () {
        return {
            username: this.$store.state.userName,

        }
    },
    methods: {
        clickCancle: function () {
            this.$router.push('/');
        },

        clickLogout: function () {
            var url = serverUrl + "/rest-auth/logout/"

            let axiosConfig = {
                headers: {
                    'Authorization': 'Token ' + this.$store.state.userToken
                }
            };

            axios.post(url, null, axiosConfig)
                .then((response) => {
                    //console.log(response);
                    localStorage.removeItem("vuex")
                    this.$store.reset()
                    delete axios.defaults.headers.common['Authorization'];
                    this.$router.push('/');
                })
                .catch((err) => {
                    if (err.response.status == "401"){
                        //this.$alert(err.response.data.detail + "Authorization Error. Please Login again.", "Unauthorized", "error");
                        delete axios.defaults.headers.common['Authorization'];
                        this.$store.dispatch("setUserToken", "");
                        this.$store.dispatch("setUserName", "Not logged in");
                        this.$router.push('/');                        
                    } else {
                        console.error(err);
                    }                 
                })
        }
    },
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
