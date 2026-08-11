<template>

    <LNBPage title="Screen with LNB - Stack 01" class="mg-auto">

        <ui-form-box>
            <ui-form-row>
                <ui-form-item :columns=8 label="Lorem Ipsum" required left-label :label-width=144>
                    <lego-dropdown :items="dropdownItems" v-model="value"/>
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns=6 label="Lorem" required left-label :label-width=144>
                    <lego-radio v-model="radioValue" value="1">Lorem</lego-radio>
                    <lego-radio v-model="radioValue" value="2">Lorem</lego-radio>
                </ui-form-item>
            </ui-form-row>

            <ui-form-row space-between>
                <ui-form-item :columns=8 label="Lorem" required left-label :label-width=144>
                    <lego-text-field v-model="textValue" placeholder="Lorem" />
                </ui-form-item>
                <ui-form-item :columns=9 label="Lorem" required left-label :label-width=144>
                    <lego-text-field v-model="textValue" placeholder="Lorem" />
                </ui-form-item>
            </ui-form-row>

            <ui-form-row space-between>
                <ui-form-item :columns=8 label="Lorem Ipsum" required left-label :label-width=144>
                    <lego-text-field v-model="textValue" placeholder="Lorem" searchable/>
                </ui-form-item>
                <ui-form-item :columns=9 label="Lorem Ipsum" required left-label :label-width=144>
                    <lego-text-field v-model="textValue" placeholder="Lorem" searchable/>
                </ui-form-item>
            </ui-form-row>
            
            <ui-form-row>
                <ui-form-item :columns=9 label=" " :label-width=144 class="mt0">
                    <div>
                        <lego-checkbox v-model="checkValue" small>Lorem Ipsum is simply dummy text of the printing and typesetting industry.</lego-checkbox>
                        <lego-checkbox class="mt12" v-model="checkValue" small>Lorem Ipsum is simply dummy text of the printing and typesetting industry.</lego-checkbox>
                    </div>
                </ui-form-item>
            </ui-form-row>

            <ui-form-row space-between>
                <ui-form-item :columns=8 label="Lorem Ipsum" required left-label :label-width=144>
                    <lego-dropdown :items="dropdownItems" v-model="value"/>
                </ui-form-item>
                <ui-form-item :columns=9 label="Lorem Ipsum" required left-label :label-width=144>
                    <lego-dropdown :items="dropdownItems" v-model="value"/>
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns=8 label="Lorem" required left-label :label-width=144>
                    <lego-text-field v-model="textValue" placeholder="Lorem" />
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns=18 label="Lorem" required left-label :label-width=144>
                    <lego-text-field v-model="textValue" placeholder="Lorem" />
                </ui-form-item>
            </ui-form-row>

            <div class="ui-form-divider" />

            <ui-form-row>
                <ui-form-item :columns=18 label="Lorem" required left-label :label-width=144>
                    <lego-text-field v-model="textValue" placeholder="Lorem" textarea rows="4"/>
                </ui-form-item>
            </ui-form-row>

        </ui-form-box>

        <div class="table-title">
            <div class="table-title-header">Contact Person</div>
            <div class="table-title-sub">* Lorem Ipsum is simply dummy text of the printing and typesetting industry.</div>
        </div>

        <ui-table checkable :columns="columns" :items="items" no-action no-info editable>
            <template v-slot:celledit-regdate="{ item }" >
                <lego-text-field v-model="item.regdate" />
            </template>
            <template v-slot:celledit-servicename1="{ item }" >
                <lego-text-field v-model="item.servicename1" />
            </template>
            <template v-slot:celledit-servicename2="{ item }" >
                <lego-text-field v-model="item.servicename2" />
            </template>
            <template v-slot:celledit-servicename3="{ item }" >
                <lego-text-field v-model="item.servicename3" />
            </template>
            <template v-slot:celledit-servicename4="{ item }" >
                <lego-text-field v-model="item.servicename4" />
            </template>
        </ui-table>

        <div class="table-checkbox">
            <lego-checkbox v-model="checkValue" small>Lorem Ipsum is simply dummy text of the printing and typesetting industry.</lego-checkbox>
        </div>

        <ui-form-buttons divider class="page-buttons">
            <lego-button large>Cancel</lego-button>
            <lego-button large main>Confirm</lego-button>
        </ui-form-buttons>

    </LNBPage>

</template>

<script>
import LNBPage from '../_Frame/LNBPage'

export default {
    name: 'lnb-stack-01',
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
            columns: [
                {label: 'Reg. Date', key: "regdate", alignCenter: true, width: 20},
                {label: 'Service name', key: "servicename1", alignCenter: true, width: 20 },
                {label: 'Service name', key: "servicename2", alignCenter: true, width: 20 },
                {label: 'Service name', key: "servicename3", alignCenter: true, width: 20 },
                {label: 'Service name', key: "servicename4", alignCenter: true, width: 20 },
            ],
            items: [
                {regdate:'-', servicename1:'-', servicename2:'-', servicename3:'-', servicename4:'-', isSelected: false}
            ],
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
    margin: 12px 0 0 0;
}
</style>