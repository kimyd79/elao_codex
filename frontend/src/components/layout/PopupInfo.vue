<template>
<div class="modal-mask" transition="modal">
    <div class="modal-wrapper">
        <ui-container-box :columns=18 vertical class="modal-container">
            
            <div class="popup-header">
                <div class="popup-header__title">
                    ELAO Information
                </div>
                <div class="popup-header__close">
                    <lego-icon small v-on:click="clickClose">close</lego-icon>
                </div>
            </div>

            <div class="popup-body"> <!-- add_scroll -->
                Version : 
                <br><br>
                Log Formats : 
                <br><br>
                <div class="table-summary">
                    <div class="table-summary-title">Summary</div>
                    <div class="table-summary-item">
                        <div>Female: 0</div>
                        <div>Male: 9</div>
                    </div>
                    <div class="table-summary-item">
                        <div>Y: 4</div>
                        <div>N: 5</div>
                    </div>
                    <div class="table-summary-item">
                        <div>Min: 3</div>
                        <div>Max: 18</div>
                    </div>
                    <div class="table-summary-item">
                        <div>Sum: 4,120,000,000</div>
                        <div>Avg: 5,600,000</div>
                    </div>
                </div>
            </div>

            <div class="popup-buttons">
                <lego-button main v-on:click="clickClose">Close</lego-button>
            </div>
        </ui-container-box>
    </div>
</div>
</template>

<script>

export default {
    name: 'PopupInfo',    
    
    methods:{
        clickClose: function () {
            
            this.$emit('popupClose');
            
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
    margin-top: 0px;
}

.popup-form .ui-form-item {
    margin-top: 32px;
}

.modal-mask {
    position: fixed;
    z-index: 9997;
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
    width: 50%;
    height: 80%;
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

.add_scroll {
    max-height: 600px;
    overflow-y: auto;
}
</style>
