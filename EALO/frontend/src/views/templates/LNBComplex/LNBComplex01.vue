<template>

    <LNBPage title="Screen with LNB - Complex 01" class="mg-auto">

        <ui-container-box :columns=18 horizontal class="pt16 mb48" >

            <ui-form-box>

                <ui-form-row>
                    <ui-form-item :columns=6 label="Lorem Ipsum" left-label required >
                        <lego-dropdown :items="dropdownItems" v-model="value"/>
                    </ui-form-item>
                    <ui-form-item :columns=7>
                        <span>* Lorem Ipsum is simply dummy text of the printing and typesetting industry.</span>
                    </ui-form-item>
                </ui-form-row>

                <ui-form-row>
                    <ui-form-item :columns=8 label="Lorem ipsum dilor" left-label >
                        <lego-radio v-model="radioValue" value="1">Lorem</lego-radio>
                        <lego-radio v-model="radioValue" value="2">Lorem</lego-radio>
                        <lego-radio v-model="radioValue" value="3">Lorem</lego-radio>
                        <lego-radio v-model="radioValue" value="4">Lorem Ipsum</lego-radio>
                    </ui-form-item>
                    <ui-form-item :columns=6 label="Lorem Ipsum" required >
                        <lego-text-field v-model="textValue" placeholder="Lorem" />
                        <lego-text-field v-model="textValue" placeholder="Lorem" />
                    </ui-form-item>
                    <ui-form-item :columns=4 align-right>
                        <lego-button main>Lorem</lego-button>
                    </ui-form-item>
                </ui-form-row>

            </ui-form-box>

        </ui-container-box>

        <ui-container-box :columns=18 horizontal class="content-area__border">

            <ui-container-box :columns=4 vertical >

                <lego-tree v-model="treeData1" class="tree-area" checkbox
                    @addButton="addNotify" @moveNode="moveNotify"/>

            </ui-container-box>

            <ui-container-box :columns=14 vertical align-center style="margin-left: 80px; padding-top:32px;">

                <ui-container-box :columns=12 wrap horizontal>

                    <ui-card v-for="(card, index) in cards" :key="index" class="mt16"
                        :columns=3 :height=290 no-top-padding small
                    >
                        <ui-card-item img :height=160 no-margin badge="Retail">
                            <img src="@/assets/img/thumb/thumb_76x76.png"/>
                        </ui-card-item>
                        <ui-card-item header>
                            {{card.title}}
                        </ui-card-item>
                        <ui-card-item body :margin-top=4>
                            {{card.desc}}
                        </ui-card-item>
                        <ui-card-item action>
                            이진호<hr v/>
                            <lego-icon>display_password</lego-icon> 50<hr v/>
                            <lego-icon>recommend</lego-icon> 0<hr v/>
                            <lego-icon>comment</lego-icon> 3
                        </ui-card-item>
                    </ui-card>

                </ui-container-box>

                <lego-pagination :pagination="page" class="mt24"/>

            </ui-container-box>

        </ui-container-box>

    </LNBPage>

</template>

<script>
import LNBPage from '../_Frame/LNBSearchTitlePage'

export default {
    name: 'lnb-complex-01',
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
.content-area__border {
    border-top: 1px solid #EAEAEA;
}
</style>