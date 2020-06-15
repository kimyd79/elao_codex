<template>

    <Page title="Screen without LNB - Stack 05" class="mg-auto">

        <ui-container-box :columns=24 vertical align-center class="page-container">

            <ui-container-box :columns=20 horizontal align-center class="page-title">
                <span class="page-title__label">Lorem Ipsum</span>
                <span class="page-title__sub">
                    Menu1 > LNB Menu1 > <em>LNB Sub Menu1</em>
                </span>
            </ui-container-box>

            <ui-container-box :columns=18 horizontal>

                <ui-form-box>

                    <ui-form-row>
                        <ui-form-item :columns=5 label="Patient Name" required-left>
                            <lego-date-picker v-model="dateValue" />
                        </ui-form-item>
                        <ui-form-item :columns=5 label="Primary ID Type">
                            <lego-dropdown :items="[{value: 'L', text: 'Lorem Ipsum'}]" value="L"/>
                        </ui-form-item>
                        <ui-form-item :columns=5 label="Primary ID">
                            <lego-dropdown :items="[{value: 'L', text: 'Lorem Ipsum'}]" value="L"/>
                        </ui-form-item>
                        <ui-form-item :columns=3 />
                    </ui-form-row>

                    <ui-form-row>
                        <ui-form-item :columns=5 label="Contact No.">
                            <lego-text-field v-model="textValue" placeholder="Enter your keyword" searchable/>
                        </ui-form-item>
                        <ui-form-item :columns=5 label="Name in English">
                            <lego-dropdown :items="[{value: 'L', text: 'Lorem Ipsum'}]" value="L"/>
                        </ui-form-item>
                        <ui-form-item :columns=5 label="Gender" required-left>
                            <lego-segment-wrapper solid primary v-model="segmentValue">
                                <lego-segment-button value="1">Lorem</lego-segment-button>
                                <lego-segment-button value="2">Lorem</lego-segment-button>
                            </lego-segment-wrapper>
                        </ui-form-item>
                        <ui-form-item :columns=3 />
                    </ui-form-row>

                    <ui-form-row>
                        <ui-form-item :columns=5 label="Date of Birth" required-left>
                            <lego-date-picker v-model="dateValue" />
                        </ui-form-item>
                        <ui-form-item :columns=5 label="Age">
                            <lego-dropdown :items="[{value: 'L', text: 'Lorem Ipsum'}]" value="L"/>
                        </ui-form-item>
                        <ui-form-item :columns=8 />
                    </ui-form-row>

                    <ui-form-buttons divider>
                        <lego-button>Lorem</lego-button>
                        <lego-button main>Lorem</lego-button>
                    </ui-form-buttons>

                </ui-form-box>

            </ui-container-box>

            <ui-container-box :columns=18 vertical class="page-table-area">

                <ui-table checkable expandable :paging-info="pagingInfo" :columns="columns" :items="items">
                    <template v-slot:control >Unit&nbsp;<b>KRW</b></template>
                    <template v-slot:expand=" {item} ">
                        <div style="background-color: #F7F7F7;">
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
                        </div>
                    </template>
                </ui-table>

            </ui-container-box>

        </ui-container-box>

    </Page>

</template>

<script>
import Page from '../_Frame/Page'

export default {
    name: 'stack-04',
    components: {
        Page
    },
    data: function() {
        return {
            value: 'A',
            dateValue: '',
            segmentValue: '2',
            radioValue: '1',
            textValue: '',
            checkValue: false,
            perPageItems : [
                {text: '10 Per page', value: 10},
                {text: '20 Per page', value: 20},
                {text: '30 Per page', value: 30}
            ],
            pagingInfo : {
                rowsPerPage: 10,
                currentPage: 1,
                totalPages: 17,
                totalItems: 163
            },
            cardItems : [
                { label: "1" },
                { label: "2" },
                { label: "3" },
                { label: "4" },
            ],
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
    }
}
</script>

<style scoped>
.page-container {
    padding: 48px 0 32px;
    background-color: white;
}
.page-title {
    margin-top: 16px;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid #CCCCCC;
}
.page-title__label {
    font-size: 32px;
    font-weight: bold;
}
.page-table-area {
    margin: 32px 0 24px;
}
</style>