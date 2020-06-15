<template>

    <LNBPage title="Screen with LNB - Stack 03" class="mg-auto">

        <ui-tab box no-action :tabs="tabs" class="mt32" />

        <ui-form-box>

            <ui-form-row space-between>
                <ui-form-item :columns=8 label="Lorem ipsum" required left-label>
                    <lego-text-field v-model="textValue" placeholder="Lorem" />
                </ui-form-item>
                <ui-form-item :columns=8 label="Lorem Ipsum" required left-label>
                    <lego-text-field v-model="textValue" placeholder="Lorem" />
                </ui-form-item>
            </ui-form-row>

            <ui-form-row space-between>
                <ui-form-item :columns=7 label="Lorem ipsum" required left-label>
                    <lego-dropdown :items="dropdownItems" v-model="value"/>
                </ui-form-item>
                <ui-form-item :columns=8 label="Lorem Ipsum" required left-label>
                    <lego-text-field v-model="textValue" placeholder="Lorem" />
                </ui-form-item>
            </ui-form-row>

            <ui-form-row space-between>
                <ui-form-item :columns=8 label="Lorem ipsum" required left-label>
                    <lego-text-field v-model="textValue" placeholder="Lorem" />
                </ui-form-item>
                <ui-form-item :columns=8 label="Lorem Ipsum" required left-label>
                    <lego-text-field v-model="textValue" placeholder="Lorem" />
                </ui-form-item>
            </ui-form-row>

            <ui-form-row space-between>
                <ui-form-item :columns=7 label="Lorem ipsum" required left-label>
                    <lego-dropdown :items="dropdownItems" v-model="value"/>
                </ui-form-item>
                <ui-form-item :columns=8 label="Lorem Ipsum" required left-label>
                    <lego-text-field v-model="textValue" placeholder="Lorem" searchable />
                </ui-form-item>
            </ui-form-row>

            <ui-form-row space-between>
                <ui-form-item :columns=7 label="Lorem ipsum" required left-label>
                    <lego-dropdown :items="dropdownItems" v-model="value"/>
                </ui-form-item>
            </ui-form-row>

            <ui-form-row space-between>
                <ui-form-item :columns=7 label="Lorem ipsum" required left-label>
                    <lego-radio v-model="radioValue" value="1">Lorem Ipsum</lego-radio>
                    <lego-radio v-model="radioValue" value="2">Lorem Ipsum</lego-radio>
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
    name: 'lnb-stack-03',
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
            checkValue: false,
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
    margin: 252px 0 0 0;
}
</style>