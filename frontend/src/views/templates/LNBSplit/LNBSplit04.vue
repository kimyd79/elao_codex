<template>

    <LNBPage title="Screen with LNB - Split 04" class="mg-auto">

        <ui-container-box :columns=20 horizontal class="pt32" >

            <ui-container-box :columns=5 vertical >

                <lego-tree v-model="treeData1" class="tree-area"
                    @addButton="addNotify" @moveNode="moveNotify"/>

            </ui-container-box>

            <ui-container-box :columns=15 vertical style="margin-left: 80px">

                <div class="table-title mb16">
                    <div class="table-title-header">
                        위치: 자동차 헤드램프 조사각 조정
                    </div>
                    <div class="table-title-search">
                        <ui-form-item :columns="5" label="Lorem Ipsum" style="margin-top:0; margin-bottom:0;">
                            <lego-text-field searchable placeholder="Search"></lego-text-field>
                        </ui-form-item>
                    </div>
                </div>

                <ui-table :paging-info="pagingInfo" :columns="columns" :items="items" editable checkable>
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

                <template v-slot:side>
                    <div class="page-side">
                        <div class="page-side-title">
                            <span>SDSAP EAMS</span>
                            <lego-icon small type="picto">setting</lego-icon>
                        </div>
                        <div class="page-side-search">
                            <lego-text-field searchable value="Total 15" />
                        </div>
                        <div class="page-side-list">
                            <div v-for="(item, index) in sideList" :key="index"
                                class="page-side-list__item"
                            >
                                <span>{{item.name}}</span>
                                <span>{{item.position}}</span>
                            </div>
                        </div>
                    </div>
                </template>

            </ui-container-box>

        </ui-container-box>

    </LNBPage>

</template>

<script>
import LNBPage from '../_Frame/LNBLightPage'

export default {
    name: 'lnb-split-04',
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
            defaultTreeNode: {
                treeInfo: {
                    key:'', parentKey:'', name:'', depth:0, seq:0,
                    searched:false, selected:false, checked:false,
                    hasChild:false, expanded:false, inlineEdit:false
                },
                contents: {},
                children: []
            },
            treeData1: [],
        }
    },
    computed : {
        dropdownItems() {
            let rtn = [];
            rtn.push({value:'A',text:'Lorem Ipsum'});
            rtn.push({value:'B',text:'Lorem Ipsum'});
            return rtn;
        }
    },
    mounted() {
        this.treeData1 = this.makeTree(0,'');
    },
    methods: {
        makeTree(depth, pKey) {
            let rtn = [];
                let cnt = 5 - depth;
                for(let i = 0; i< cnt; i++) {
                    let newNode = JSON.parse(JSON.stringify(this.defaultTreeNode));
                    newNode.treeInfo.parentKey = pKey;
                    newNode.treeInfo.key = pKey?pKey+'-'+i:'key-'+i;
                    newNode.treeInfo.name = pKey?pKey+'-'+i:'key-'+i;
                    newNode.treeInfo.depth = depth;
                    newNode.treeInfo.seq = i * 2 + 1;
                    newNode.children = this.makeTree(depth+1, newNode.treeInfo.key);
                    if(newNode.children.length > 0 ) {
                        newNode.treeInfo.hasChild = true;
                    }                    
                    rtn.push(newNode)
                }
            
            return rtn;
        },
        addNotify(e, node, position) {
            let msg = 'addButton triggered. new node will be created under : ';
            console.log(msg + (node.treeInfo?node.treeInfo.name:'root'));
            // 0. show confirm modal or send create request to server
            // this.$refs.refName.appendNode(newNode, position)
        },
        deleteNotify(e, node, position) {
            let msg = 'deleteButton triggered. selected node will be deleted : ';
            console.log(msg + node.treeInfo.name);
            // 0. show confirm modal or send delete request to server
            // this.$refs.refName.deleteNode(node, position)
        },
        editNotify(e, node, position) {
            let msg = 'editButton triggered. you can edit contents of : ';
            console.log(msg + node.treeInfo.name);
            // 0. show edit form -> contents modified,
            // 1. show confirm modal or send update request to server
            // this.$refs.refName.updateNode(node, modifiedNode);
        },
        moveNotify(dragInfo, fromNode, toNode) {
            let msg = 'drag & drop triggered. node will be moved from ';
            console.log(msg + fromNode.treeInfo.name + ' to ' + dragInfo.type + ' of ' + toNode.treeInfo.name);
            // 0. show confirm modal or send update request to server
            // this.$refs.refName.moveNode(dragInfo);
        }
    }
}
</script>

<style scoped>
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
    margin-bottom: 0;
}
.table-title-search {
    margin-left: auto;
}
</style>