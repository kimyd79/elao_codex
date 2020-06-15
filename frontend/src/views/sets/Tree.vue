<template>
    <ui-page-box align-center>

        <ui-container-box :columns=16 horizontal wrap class="mt50 bg-white">

            <ui-container-box :columns=5 horizontal title="No option" class="pd16">

                <lego-tree v-model="treeData1" 
                    @addButton="addNotify" @moveNode="moveNotify"/>

            </ui-container-box>

            <ui-container-box :columns=5 horizontal title="With checkbox" class="pd16">

                <lego-tree v-model="treeData2" checkbox 
                    @addButton="addNotify" @moveNode="moveNotify"/>

            </ui-container-box>

            <ui-container-box :columns=5 horizontal title="With label action buttons" class="pd16">

                <lego-tree v-model="treeData3" label-action
                    @addButton="addNotify" @moveNode="moveNotify"
                    @deleteButton="deleteNotify" @editButton="editNotify"/>

            </ui-container-box>

            <ui-container-box :columns=5 horizontal title="Inline edit" class="pd16">

                <lego-tree v-model="treeData4" label-action inline-edit :rules="customRules"
                    @addButton="addNotify" @moveNode="moveNotify"
                    @deleteButton="deleteNotify"/>

            </ui-container-box>

            <ui-container-box :columns=5 horizontal title="Change label" class="pd16">

                <lego-tree v-model="treeData5" :node-label="labelInfo"
                    @addButton="addNotify" @moveNode="moveNotify"/>

            </ui-container-box>
            
            <ui-container-box :columns=5 horizontal title="Hide and button" class="pd16">

                <lego-tree v-model="treeData6" hideAdd
                    @addButton="addNotify" @moveNode="moveNotify"/>

            </ui-container-box>

        </ui-container-box>

    </ui-page-box>
</template>

<script>
export default {
    name: 'tree',
    data(){return{
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
        treeData2: [],
        treeData3: [],
        treeData4: [],
        treeData5: [],
        treeData6: [],
        customRules: [
            v => !!v || 'required!',
            v => v.length <= 10 || 'length limit 10!',
            v => /^[a-zA-z0-9-_]*$/.test(v) || 'only alphanumeric & dash allowed'
        ],
        labelInfo: {
            field: ['treeInfo.depth', 'treeInfo.seq'],
            separator: ' > '
        }
    }},
    mounted() {
        this.treeData1 = this.makeTree(1,0,'');
        this.treeData2 = JSON.parse(JSON.stringify(this.treeData1));
        this.treeData3 = JSON.parse(JSON.stringify(this.treeData1));
        this.treeData4 = JSON.parse(JSON.stringify(this.treeData1));
        this.treeData5 = JSON.parse(JSON.stringify(this.treeData1));
        this.treeData6 = JSON.parse(JSON.stringify(this.treeData1));
    },
    methods: {
        makeTree(p, depth, pKey) {
            let rtn = [];
            if(0.3 < p) {
                let cnt = 5 - depth;
                for(let i = 0; i< cnt; i++) {
                    let newNode = JSON.parse(JSON.stringify(this.defaultTreeNode));
                    newNode.treeInfo.parentKey = pKey;
                    newNode.treeInfo.key = pKey?pKey+'-'+i:'key-'+i;
                    newNode.treeInfo.name = pKey?pKey+'-'+i:'key-'+i;
                    newNode.treeInfo.depth = depth;
                    newNode.treeInfo.seq = i * 2 + 1;
                    newNode.children = this.makeTree(p*2/3, depth+1, newNode.treeInfo.key);
                    if(newNode.children.length > 0 ) {
                        newNode.treeInfo.hasChild = true;
                    }                    
                    rtn.push(newNode)
                }
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