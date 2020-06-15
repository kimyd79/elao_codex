<template>

    <LNBPage title="Screen with LNB - Stack 04" class="mg-auto">

        <ui-form-box>
            <ui-form-row>
                <ui-form-item :columns=8 label="Lorem Ipsum" required >
                    <lego-date-picker v-model="dateValue" />
                    <lego-date-picker v-model="dateValue" />
                </ui-form-item>
                <ui-form-item :columns=9 label="Lorem Ipsum" required :label-width=320>
                    <lego-dropdown :items="dropdownItems" v-model="value"/>
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns=7 label="Lorem Ipsum" required >
                    <lego-dropdown :items="dropdownItems" v-model="value"/>
                </ui-form-item>
                <ui-form-item :columns=10 label="Lorem Ipsum" required :label-width=400>
                    <lego-dropdown :items="dropdownItems" v-model="value"/>
                </ui-form-item>
            </ui-form-row>

            <ui-form-buttons divider>
                <template v-slot:items>
                    <ui-form-row>
                        <ui-form-item :columns=18 label="Mechant" :label-width=148>
                            <lego-chip small removable>Seoul</lego-chip>
                            <lego-chip small removable>Paris</lego-chip>
                            <lego-chip small removable>Newyork</lego-chip>
                            <lego-chip small removable>London</lego-chip>
                            <lego-chip small removable>Budapest</lego-chip>
                        </ui-form-item>
                    </ui-form-row>
                    <ui-form-row>
                        <ui-form-item :columns=18 label="Store" :label-width=148>
                            <lego-chip small removable>Bixby</lego-chip>
                            <lego-chip small removable>Hotels.com</lego-chip>
                            <lego-chip small removable>Samsung Pay</lego-chip>
                            <lego-chip small removable>Kakao</lego-chip>
                            <lego-chip small removable>Hotels.com</lego-chip>
                            <lego-chip small removable>Samsung Pay</lego-chip>
                            <lego-chip small removable>Hotels.com</lego-chip>
                            <lego-chip small removable>Samsung Pay</lego-chip>
                            <lego-chip small removable>Bixby</lego-chip>
                            <lego-chip small removable>Kakao</lego-chip>
                            <lego-chip small removable>Samsung Pay</lego-chip>
                        </ui-form-item>
                    </ui-form-row>
                </template>
                <lego-button>Lorem</lego-button>
                <lego-button main>Ipsum</lego-button>
            </ui-form-buttons>

        </ui-form-box>

        <div class="ui-form-divider" />

        <div class="table-title">
            <div class="table-title-header">Lorem Ipsum</div>
            <div class="table-title-sub">Lorem Ipsum is simply dummy text of the printing and typesetting industry.</div>
        </div>

        <img src="../../../assets/img/chart/graph.png" style="padding: 24px;"/>

        <div class="table-title mt24">
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
    name: 'lnb-stack-04',
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