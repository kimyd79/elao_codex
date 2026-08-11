<template>
    <ui-page-box align-center>

        <ui-container-box :columns=20 vertical title="Table Default" class="mt50 mb50" >

            <ui-container-box :columns=18 vertical >

                <ui-table checkable :paging-info="pagingInfo" :columns="columns" :items="items">
                    <template v-slot:control >Unit&nbsp;<b>KRW</b></template>
                    <template v-slot:cellview-mode="{ item }" >
                        <lego-badge :badge-color="item.mode.toLowerCase()" badge-type="status-dot">
                            {{item.mode}}
                        </lego-badge>
                    </template>
                </ui-table>

                <ui-table checkable header-divider :paging-info="pagingInfo" :columns="columns" :items="items" class="mt20">
                    <template v-slot:control >Unit&nbsp;<b>KRW</b></template>
                    <template v-slot:cellview-mode="{ item }" >
                        <lego-badge :badge-color="item.mode.toLowerCase()" badge-type="status-dot">
                            {{item.mode}}
                        </lego-badge>
                    </template>
                </ui-table>

            </ui-container-box>

        </ui-container-box>

        <ui-container-box :columns=20 vertical title="Table Narrow" class="mb50" >

            <ui-container-box :columns=18 vertical >

                <ui-table checkable narrow :paging-info="pagingInfo" :columns="columns" :items="items">
                    <template v-slot:control >Unit&nbsp;<b>KRW</b></template>
                    <template v-slot:mode="{ item }" >
                        <lego-badge :badge-color="item.mode.toLowerCase()" badge-type="status-dot">
                            {{item.mode}}
                        </lego-badge>
                    </template>
                </ui-table>

                <ui-table checkable narrow header-divider :paging-info="pagingInfo" :columns="columns" :items="items" class="mt20">
                    <template v-slot:control >Unit&nbsp;<b>KRW</b></template>
                    <template v-slot:mode="{ item }" >
                        <lego-badge :badge-color="item.mode.toLowerCase()" badge-type="status-dot">
                            {{item.mode}}
                        </lego-badge>
                    </template>
                </ui-table>

                <ui-table checkable narrow :paging-info="pagingInfo" :columns="columns" :items="items" class="mt20">
                    <template v-slot:control >Unit&nbsp;<b>KRW</b></template>
                    <template v-slot:mode="{ item }" >
                        <lego-badge :badge-color="item.mode.toLowerCase()" badge-type="status-dot">
                            {{item.mode}}
                        </lego-badge>
                    </template>
                </ui-table>

            </ui-container-box>

        </ui-container-box>

        <ui-container-box :columns=20 vertical title="Table Editable" class="mb50" >

            <ui-container-box :columns=18 vertical >

                <ui-table checkable editable header-divider :paging-info="pagingInfo" :columns="columns" :items="items" class="mt20">
                    <template v-slot:control >Unit&nbsp;<b>KRW</b></template>
                    <template v-slot:celledit-name="{ item }" >
                        <lego-text-field v-model="item.name" />
                    </template>
                    <template v-slot:celledit-email="{ item }" >
                        <lego-text-field v-model="item.email" />
                    </template>
                    <template v-slot:celledit-mode="{ item }" >
                        <lego-text-field v-model="item.mode" />
                    </template>
                    <template v-slot:celledit-gender="{ item }" >
                        <lego-text-field v-model="item.gender" />
                    </template>
                    <template v-slot:celledit-registrant="{ item }" >
                        <lego-text-field v-model="item.registrant" />
                    </template>
                    <template v-slot:celledit-size="{ item }" >
                        <lego-text-field v-model="item.size" />
                    </template>
                </ui-table>
                
            </ui-container-box>

        </ui-container-box>

        <ui-container-box :columns=20 vertical title="Table Custom Controls" class="mb50" >

            <ui-container-box :columns=18 vertical >

                <ui-table checkable narrow header-divider no-action
                    :paging-info="pagingInfo" :columns="columns" :items="items">
                    <template v-slot:control >
                        <lego-text-field placeholder="Auto-Scaling Group" />
                        <lego-text-field placeholder="Group name" searchable style="margin-left: 8px;"/>
                        <lego-text-field placeholder="Configuration Management" style="margin-left: 8px;"/>
                        <lego-button main style="margin-left: 8px; min-width: 100px;">Apply</lego-button>
                    </template>
                </ui-table>

            </ui-container-box>

        </ui-container-box>

        <ui-container-box :columns=20 vertical title="Table Expandable" class="mb50" >

            <ui-container-box :columns=18 vertical >

                <ui-table checkable expandable :paging-info="pagingInfo" :columns="columns" :items="items">
                    <template v-slot:control >Unit&nbsp;<b>KRW</b></template>
                    <template v-slot:expand=" {item} ">
                        <ui-form-row>
                            <ui-form-item :columns=9 label="Name" left-label >
                                {{ item.name }}
                            </ui-form-item>
                            <ui-form-item :columns=7 label="E-mail" left-label >
                                {{ item.email }}
                            </ui-form-item>
                        </ui-form-row>

                        <ui-form-row>
                            <ui-form-item :columns=9 label="Gender" left-label >
                                {{ item.gender }}
                            </ui-form-item>
                            <ui-form-item :columns=7 label="Company" left-label >
                                DC0293ILOD
                            </ui-form-item>
                        </ui-form-row>

                        <ui-form-row>
                            <ui-form-item :columns=9 label="Department" left-label >
                                CX Team (UX Standars Group)
                            </ui-form-item>
                            <ui-form-item :columns=7 label="Job Description" left-label >
                                UX Design
                            </ui-form-item>
                        </ui-form-row>

                        <ui-form-row>
                            <ui-form-item :columns=9 label="Mobile" left-label >
                                +82-10-1234-5678
                            </ui-form-item>
                            <ui-form-item :columns=7 label="Office Fax" left-label >
                                +82-10-1234-5678
                            </ui-form-item>
                        </ui-form-row>

                        <ui-form-row align-right>
                            <lego-button small >Modify</lego-button>
                        </ui-form-row>
                    </template>
                </ui-table>

                <ui-table checkable expandable :paging-info="pagingInfo" :columns="columns" :items="items" class="mt20">
                    <template v-slot:control >Unit&nbsp;<b>KRW</b></template>
                    <template v-slot:expand=" {item} ">
                        <ui-form-row space-between>
                            <ui-form-item :columns=6 label="Name" left-label >
                                <lego-text-field v-model="item.name" />
                            </ui-form-item>
                            <ui-form-item :columns=8 label="E-mail" left-label >
                                {{ item.email }}
                            </ui-form-item>
                        </ui-form-row>

                        <ui-form-row space-between>
                            <ui-form-item :columns=6 label="Gender" left-label >
                                <lego-radio v-model="item.gender" value="Male">Male</lego-radio>
                                <lego-radio v-model="item.gender" value="Female">Female</lego-radio>
                            </ui-form-item>
                            <ui-form-item :columns=8 label="Company" left-label >
                                DC0293ILOD
                            </ui-form-item>
                        </ui-form-row>

                        <ui-form-row space-between>
                            <ui-form-item :columns=6 label="Department" left-label >
                                <lego-dropdown :items="['CX Team (UX Standars Group)']" value="CX Team (UX Standars Group)"/>
                            </ui-form-item>
                            <ui-form-item :columns=8 label="Job Description" left-label >
                                UX Design
                            </ui-form-item>
                        </ui-form-row>

                        <ui-form-row space-between>
                            <ui-form-item :columns=6 label="Mobile" left-label >
                                <lego-text-field value="+82" />
                                <lego-text-field value="10" />
                                <lego-text-field value="1234" />
                                <lego-text-field value="5678" />
                            </ui-form-item>
                            <ui-form-item :columns=8 label="Office Fax" left-label >
                                +82-10-1234-5678
                            </ui-form-item>
                        </ui-form-row>

                        <ui-form-row align-right>
                            <lego-button small >Cencel</lego-button>
                            <lego-button small main>Save</lego-button>
                        </ui-form-row>
                    </template>
                </ui-table>

            </ui-container-box>

        </ui-container-box>

        <ui-container-box :columns=20 vertical title="Table Header Filter" class="mb50" >

            <ui-container-box :columns=18 vertical >

                <ui-table checkable header-filter
                    :paging-info="pagingInfo" :columns="columns" :items="items">
                </ui-table>

            </ui-container-box>

        </ui-container-box>

        <ui-container-box :columns=20 vertical title="Table Accordion" class="mb50" >

            <ui-container-box :columns=18 vertical >

                <ui-table checkable grouping
                    :paging-info="pagingInfo" :columns="columns" :groups="groups" :items="groupItems">
                </ui-table>

            </ui-container-box>

        </ui-container-box>

        <ui-container-box :columns=20 vertical title="Table Summary" class="mb50" >

            <ui-container-box :columns=18 vertical >

                <ui-table :columns="columns" :items="items" no-paging no-action no-info >
                    <template v-slot:summary>
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
                    </template>
                </ui-table>

            </ui-container-box>

        </ui-container-box>

        <ui-container-box :columns=20 vertical title="Table Left Header" class="mb50" >

            <ui-container-box :columns=18 vertical >

                <ui-table left-header
                    :paging-info="pagingInfo" :columns="leftHeaderColumns" :items="leftHeaderItems"  />

            </ui-container-box>

        </ui-container-box>

    </ui-page-box>

</template>

<script>
export default {
    name: 'tables',
    data() {
        return {
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
            groups: [
                {label:'Group 01', key:'01', isOpened: true},
                {label:'Group 02', key:'02', isOpened: false},
                {label:'Group 03', key:'03', isOpened: true},
                {label:'Group 04', key:'04', isOpened: false},
            ],
            groupItems: [
                {name:'Andere Cummings1', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false, groupKey:'01'},
                {name:'Andere Cummings2', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false, groupKey:'02'},
                {name:'Andere Cummings3', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false, groupKey:'01'},
                {name:'Andere Cummings4', email:'cummings@samsung.com', mode:'Error', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false, groupKey:'02'},
                {name:'Andere Cummings5', email:'cummings@samsung.com', mode:'Error', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false, groupKey:'01'},
                {name:'Andere Cummings6', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false, groupKey:'02'},
                {name:'Andere Cummings7', email:'cummings@samsung.com', mode:'Error', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false, groupKey:'02'},
                {name:'Andere Cummings8', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false, groupKey:'03'},
                {name:'Andere Cummings9', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false, groupKey:'03'},
                {name:'Andere Cummings10', email:'cummings@samsung.com', mode:'Processing', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false, groupKey:'04'},
            ],
            leftHeaderColumns: [
                {label: 'Floor', key: "floor", alignCenter: true, width: 20 },
                {label: '1', key: "one", alignCenter: true, width: 20 },
                {label: '2', key: "two", alignCenter: true, width: 20 },
                {label: '3', key: "three", alignCenter: true, width: 20 },
                {label: '4', key: "four", alignCenter: true, width: 20 },
                {label: '5', key: "five", alignCenter: true, width: 20 },
                {label: '6', key: "six", alignCenter: true, width: 20 },
                {label: '7', key: "seven", alignCenter: true, width: 20 },
                {label: '8', key: "eight", alignCenter: true, width: 20 }
            ],
            leftHeaderItems: [
                {floor:'63F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'},
                {floor:'62F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'},
                {floor:'61F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'},
                {floor:'60F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'},
                {floor:'59F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'},
                {floor:'58F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'},
                {floor:'57F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'},
                {floor:'56F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'},
                {floor:'55F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'},
                {floor:'54F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'}
            ]
        }
    }
}
</script>

<style>
.table-summary {
    display: flex;
    flex-flow: row nowrap;
    justify-content: flex-end;
    align-items: center;

    font-size: 14px;
    padding: 12px 48px;
    background-color: #F6F6F6;
}
.table-summary-title {
    display: flex;
    font-weight: bold;
    margin-right: auto;
}
.table-summary-item {
    display: flex;
    flex-flow: column nowrap;
    align-items: flex-end;
}
.table-summary-item + .table-summary-item {
    margin-left: 48px;
}
</style>