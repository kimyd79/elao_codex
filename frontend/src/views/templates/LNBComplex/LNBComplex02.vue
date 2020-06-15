<template>

    <LNBPage title="Screen with LNB - Complex 02" class="mg-auto">

        <ui-container-box :columns=18 horizontal class="pt16" >

            <ui-form-row space-between class="mb16">
                <ui-form-item :columns=6 label="System Type" left-label required >
                    <lego-dropdown :items="dropdownItems" v-model="value"/>
                </ui-form-item>
                <ui-form-item :columns=12 align-right>
                    <lego-button>B</lego-button>
                    <lego-button>B</lego-button>
                </ui-form-item>
            </ui-form-row>

        </ui-container-box>

        <ui-container-box :columns=18 horizontal class="content-area__border">

            <ui-container-box :columns=5 vertical >

                <lego-tree v-model="treeData1" class="tree-area"
                    @addButton="addNotify" @moveNode="moveNotify"/>

            </ui-container-box>

            <ui-container-box :columns=13 vertical style="margin-left: 80px; padding-top:32px;">

                <span class="content-title">BMI</span>

                <img src="../../../assets/img/bmi/graph.png" style="width: 944px; height:368px;"/>

                <img src="../../../assets/img/bmi/graph.png" style="width: 944px; height:368px; margin-top:16px;"/>

            </ui-container-box>

        </ui-container-box>

    </LNBPage>

</template>

<script>
import LNBPage from '../_Frame/LNBSearchTitlePage'

export default {
    name: 'lnb-complex-02',
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
            page : {
                rowsPerPage: 10,
                currentPage: 1,
                totalPages: 17,
                totalItems: 163
            },
            cards: [
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},

                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},

                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
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
            rtn.push({value:'A',text:'2018.11.10 - 2018.12.09'});
            rtn.push({value:'B',text:'2018.12.10 - 2019.01.09'});
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
.content-area__border {
    border-top: 1px solid #EAEAEA;
}
.content-title {
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 16px;    
}
</style>