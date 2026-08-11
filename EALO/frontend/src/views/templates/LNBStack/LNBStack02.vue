<template>

    <LNBPage title="Screen with LNB - Stack 02" class="mg-auto">

        <ui-tab box no-action :tabs="tabs" class="mt32" />

        <ui-form-box>

            <ui-form-row>
                <ui-form-item :columns=8 label="Lorem ipsum dilor" >
                    <lego-radio v-model="radioValue" value="1">Lorem</lego-radio>
                    <lego-radio v-model="radioValue" value="2">Lorem</lego-radio>
                    <lego-radio v-model="radioValue" value="3">Lorem</lego-radio>
                    <lego-radio v-model="radioValue" value="4">Lorem Ipsum</lego-radio>
                </ui-form-item>
                <ui-form-item :columns=6 label="Lorem Ipsum" required >
                    <lego-text-field v-model="textValue" placeholder="Lorem" />
                    <lego-text-field v-model="textValue" placeholder="Lorem" />
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns=5 label="Lorem Ipsum" required >
                    <lego-dropdown :items="items" v-model="value"/>
                </ui-form-item>
                <ui-form-item :columns=7>
                    <span>* Lorem Ipsum is simply dummy text of the printing and typesetting industry.</span>
                </ui-form-item>
                <ui-form-item :columns=6 align-left>
                    <lego-button main>Lorem</lego-button>
                </ui-form-item>
            </ui-form-row>

            <div class="ui-form-divider" />

            <div class="table-title">
                <div class="table-title-header">Product</div>
            </div>

            <ui-table checkable :paging-info="pagingInfo" :columns="columns" :items="items">
                <template v-slot:cellview-mode="{ item }" >
                    <lego-badge :badge-color="item.mode.toLowerCase()" badge-type="status-dot">
                        {{item.mode}}
                    </lego-badge>
                </template>
            </ui-table>

        </ui-form-box>

    </LNBPage>

</template>

<script>
import LNBPage from '../_Frame/LNBPage'

export default {
    name: 'lnb-stack-02',
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
            ],
            pagingInfo : {
                rowsPerPage: 10,
                currentPage: 1,
                totalPages: 17,
                totalItems: 163
            },
            columns: [
                {label: 'Name', key: "name", sortable: true, sortValue: "asc", filtable: false, alignRight: false, width: 20 },
                {label: 'Email', key: "email", sortable: true, sortValue: "desc", filtable: true, filterValue:[], alignRight: false, width: 25,
                    filterList: ["@tunivers.com","@samsung.com","Cockatoo","Richard's Pipit"] 
                },
                {label: 'Mode', key: "mode", sortable: false, filtable: true, filterValue:[], alignRight: false, width: 15,
                    filterList: ["Success","Error","Processing"]  },
                {label: 'Gender', key: "gender", sortable: false, filtable: false, alignRight: false, width: 15 },
                {label: 'Registrant', key: "registrant", sortable: true, sortValue: "asc", filtable: true, filterValue:[], alignRight: false, width: 15,
                    filterList: ["Cockatoo","Richard's Pipit"]  },
                {label: 'Size', key: "size", sortable: false, filtable: false, alignRight: true, width: 10 },
            ],
            items: [
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Error', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Error', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Error', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Processing', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
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