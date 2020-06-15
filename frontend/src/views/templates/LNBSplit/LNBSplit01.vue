<template>

    <LNBPage title="Screen with LNB - Split 01" class="mg-auto">

        <ui-form-row space-between class="search-area">
            <ui-form-item :columns=5 label="Lorem Ipsum" left-label :label-width=144>
                <lego-dropdown :items="dropdownItems" v-model="value"/>
            </ui-form-item>
            <ui-form-item :columns=5 align-right>
                <lego-button>Lorem</lego-button>
            </ui-form-item>
        </ui-form-row>

        <ui-container-box :columns=18 horizontal>

            <ui-container-box :columns=5 vertical>

                <lego-tree v-model="treeData1" class="tree-area"
                    @addButton="addNotify" @moveNode="moveNotify"/>

            </ui-container-box>

            <ui-container-box :columns=13 vertical>

                <ui-form-box class="ml48">

                    <ui-form-row>
                        <ui-form-item :columns=13 label="Menu Name" left-label :label-width=144>
                            <span>Product List</span>
                        </ui-form-item>
                    </ui-form-row>

                    <ui-form-row>
                        <ui-form-item :columns=13 label="Menu Type" left-label :label-width=144>
                            <span>Node</span>
                        </ui-form-item>
                    </ui-form-row>

                    <ui-form-row>
                        <ui-form-item :columns=13 label="Page Name" left-label :label-width=144>
                            <span>50MB</span>
                        </ui-form-item>
                    </ui-form-row>

                    <ui-form-row>
                        <ui-form-item :columns=13 label="Menu Order" left-label :label-width=144>
                            <span>50MB</span>
                        </ui-form-item>
                    </ui-form-row>

                    <ui-form-row>
                        <ui-form-item :columns=13 label="Contact" left-label :label-width=144>
                            <span>samsungsds_design@samsung.com</span>
                        </ui-form-item>
                    </ui-form-row>

                </ui-form-box>

                <div class="mb48 ml80 mt70">
                    <div class="table-title">
                        <div class="table-title-header">Role</div>
                    </div>

                    <ui-table checkable :columns="columns" :items="items" no-action no-info />
                </div>

            </ui-container-box>

        </ui-container-box>

        <ui-form-buttons divider no-margin>
            <lego-button large>Delete</lego-button>
            <lego-button large main>Save</lego-button>
        </ui-form-buttons>

    </LNBPage>

</template>

<script>
import LNBPage from '../_Frame/LNBSearchPage'

export default {
    name: 'lnb-split-01',
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
                {label: 'ID', key: "id", width: 50},
                {label: 'Name', key: "name", filtable: true, filterValue:[], width: 50 },
            ],
            items: [
                {id:'Andere Cummings', name:'Suki', isSelected: false},
                {id:'Scalet', name:'miller.kling@samsung.com', isSelected: false},
                {id:'Andere Cummings', name:'miller.kling@samsung.com', isSelected: false},
                {id:'Andere Cummings', name:'miller.kling@samsung.com', isSelected: false},
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

<style>
.search-area {
    border-bottom: 1px solid #CCCCCC;
    padding: 16px 0 8px;
}
.tree-area.lego-tree {
    width: 100%;
    border: none;
    background-color: #F7F7F7;
}
.tree-area.lego-tree .lego-button {
    background-color: white;
}
.table-title-header {
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 16px;
}
</style>