<template>

    <LNBPage title="Screen with LNB - Stack 07" class="mg-auto">

        <ui-form-box>

            <ui-form-row>
                <ui-form-item :columns=10 label="Lorem ipsum" required left-label>
                    <span class="fs16">Lorem Ipsum</span>
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns=10 label="Lorem ipsum" required left-label>
                    <lego-checkbox v-model="checkValue" value="1">Lorem Ipsum</lego-checkbox>
                    <lego-checkbox v-model="checkValue" value="2">Lorem Ipsum</lego-checkbox>
                    <lego-checkbox v-model="checkValue" value="3">Lorem Ipsum</lego-checkbox>
                    <lego-checkbox v-model="checkValue" value="4">Lorem Ipsum</lego-checkbox>
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns=7 label="Lorem" required left-label>
                    <lego-text-field v-model="textValue" placeholder="Lorem" />
                    <lego-text-field v-model="textValue" placeholder="Lorem" />
                </ui-form-item>
                <ui-form-item :columns=7 label="Lorem ipsum" required left-label>
                    <lego-text-field v-model="textValue" placeholder="Lorem" />
                    <lego-text-field v-model="textValue" placeholder="Lorem" />
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns=18 label="Ipsum" required left-label>
                    <span class="fs16">Regular Preventive Maintenace in October</span>
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns=18 label="Lorem ipsum" required left-label>
                    <span class="fs16">Regular Preventive Maintenace in October</span>
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns=18 label="Lorem ipsum" required left-label>
                    <span class="fs16">
                        As regular PM causes Korea Billing Checkout System to be interrupted, please note your job.<br>
                        <br>
                        Operations Target<br>
                        -vault.samsung.com<br>
                        <br>
                        Operation date<br>
                        -sat, 27th Oct, 2018:23:00 - Sun, 28th Oct. 05:30(KST)
                    </span>
                </ui-form-item>
            </ui-form-row>

            <ui-form-buttons divider class="page-buttons">
                <lego-button large>Delete</lego-button>
                <lego-button large main>Save</lego-button>
            </ui-form-buttons>

        </ui-form-box>

    </LNBPage>

</template>

<script>
import LNBPage from '../_Frame/LNBPage'

export default {
    name: 'lnb-stack-07',
    components: {
        LNBPage
    },
    data: function() {
        return {
            value: 'A',
            dateValue: '',
            segmentValue: '2',
            radioValue: '1',
            textValue: '',
            checkValue: [],
            tabs: [
                { label: "Tab_1",  isSelected: true },
                { label: "Tab_2",  isSelected: false },
                { label: "Tab_3",  isSelected: false },
                { label: "Tab_4",  isSelected: false }
            ]
        }
    },
    computed : {
        dropdownItems() {
            let rtn = [];
            rtn.push({value:'A',text:'Lorem Ipsum'});
            rtn.push({value:'B',text:'Lorem Ipsum'});
            return rtn;
        }
    }
}
</script>

<style scoped>
.mt0 {
    margin-top: 0px;
}
.ui-form-divider {
    width: 100%;
    height: 1px;
    background-color: #EAEAEA;
    margin: 32px 0;
}
.table-title {
    display: flex;
    flex-flow: row nowrap;
    align-items: flex-end;
    margin-bottom: 16px;
}
.table-title-header {
    font-size: 20px;
    font-weight: bold;
    margin-right: 20px;
}
.table-title-sub {
    font-size: 14px;
}
.table-checkbox {
    display: flex;
    flex-flow: column nowrap;
    align-items: flex-end;
    margin: 20px 0;
}
.page-buttons {
    border-top-color: #cccccc;
    margin: 168px 0 0 0;
}
.fs16 {
    font-size: 16px;
}
</style>