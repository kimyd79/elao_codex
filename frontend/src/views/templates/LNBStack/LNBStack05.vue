<template>

    <LNBPage title="Screen with LNB - Stack 05" class="mg-auto">

        <ui-form-box>

            <ui-form-row>
                <ui-form-item :columns=1 />
                <ui-form-item :columns=3 label="Lorem Ipsum" top-label>
                    <lego-dropdown :items="dropdownItems" v-model="value"/>
                </ui-form-item>
                <ui-form-item :columns=3 label="Lorem Ipsum" top-label>
                    <lego-dropdown :items="dropdownItems" v-model="value"/>
                </ui-form-item>
                <ui-form-item :columns=3 label="Lorem Ipsum" top-label>
                    <lego-dropdown :items="dropdownItems" v-model="value"/>
                </ui-form-item>
                <ui-form-item :columns=3 label="Lorem Ipsum" top-label>
                    <lego-dropdown :items="dropdownItems" v-model="value"/>
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns=1 />
                <ui-form-item :columns=6 label="Lorem Ipsum" top-label>
                    <lego-date-picker v-model="dateValue" />
                    <lego-date-picker v-model="dateValue" />
                </ui-form-item>
                <ui-form-item :columns=3 label="Lorem Ipsum" top-label>
                    <lego-text-field v-model="textValue" placeholder="Lorem" />
                    <lego-text-field v-model="textValue" placeholder="Lorem" />
                </ui-form-item>
                <ui-form-item :columns=3 label="Lorem Ipsum" required top-label>
                    <lego-text-field v-model="textValue" placeholder="Lorem" />
                </ui-form-item>
                <ui-form-item :columns=5 label=" " top-label alignRight>
                    <lego-button main>Lorem</lego-button>
                </ui-form-item>
            </ui-form-row>

        </ui-form-box>

        <div class="table-title mt16">
            <div class="table-title-header">Lorem Ipsum</div>
        </div>

        <ui-table :paging-info="pagingInfo" :columns="columns" :items="items" editable>
            <template v-slot:cellview-mode="{ item }" >
                <lego-badge :badge-color="item.mode.toLowerCase()" badge-type="status-dot">
                    {{item.mode}}
                </lego-badge>
            </template>
            <template v-slot:celledit-mode="{ item }" >
                <lego-badge :badge-color="item.mode.toLowerCase()" badge-type="status-dot">
                    {{item.mode}}
                </lego-badge>
            </template>
            <template v-slot:celledit-email="{ item }" >
                <lego-text-field v-model="item.email" />
            </template>
        </ui-table>

    </LNBPage>

</template>

<script>
import LNBPage from '../_Frame/LNBPage'

export default {
    name: 'lnb-stack-05',
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
    margin: 0 0 32px 0;
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