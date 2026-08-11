<template>

    <ui-container-box :columns=24 vertical :title="title">

        <ui-gnb>
            <template v-slot:lead>
                <ui-gnb-title>
                    <template v-slot:title>SDS Platform</template>
                    <template v-slot:sub>slogan / full name</template>
                </ui-gnb-title>
                <ui-gnb-menus :menus="menus" />
            </template>
            <template v-slot:tail>
                <ui-gnb-icons :icons="['notification','setting']" />
                <ui-gnb-profile>Gildong Hong</ui-gnb-profile>
            </template>
        </ui-gnb>

        <ui-container-box :columns=24 horizontal class="bg-contents">

            <ui-lnb>
                <ui-lnb-item>
                    <lego-tab-box :default-idx="1">
                        <lego-tab-label :idx="1">Tab_1</lego-tab-label>
                        <lego-tab-label :idx="2">Tab_2</lego-tab-label>
                    </lego-tab-box>
                </ui-lnb-item>
                <ui-lnb-menus :menus="splitLineMenus1" @selectMenu="selectMenu"/>
                <ui-lnb-menus :menus="splitLineMenus2" @selectMenu="selectMenu"/>
                <ui-lnb-menus :menus="splitLineMenus3" @selectMenu="selectMenu"/>
            </ui-lnb>

            <ui-container-box :columns=16 vertical align-center class="bg-white page-content-area" >
                <ui-container-box :columns=14 vertical>
                    <div class="ui-title">
                        <div class="ui-title-label">
                            <div class="ui-title-label__main">
                                Lorem Ipsum
                            </div>
                        </div>
                        <div class="ui-title-side">
                            Menu1 > LNB Menu1 > <em> LNB Sub Menu1</em>
                        </div>
                    </div>
                    <slot />
                </ui-container-box>
            </ui-container-box>

            <div class="bg-white">
                <slot name="side" />
            </div>

        </ui-container-box>

    </ui-container-box>

</template>

<script>
export default {
    props: {
        title: { type: String }
    },
    data() {
        return {
            menus: [
                { label:'Menu1', key:'menu1', isSelected: true },
                { label:'Menu2', key:'menu2', isSelected: false },
                { label:'Menu3', key:'menu3', isSelected: false },
                { label:'Menu4', key:'menu4', isSelected: false },
                { label:'Menu5', key:'menu5', isSelected: false }
            ],
            splitLineMenus1: [
                {   label:'LNB Menu1', key:'LNBmenu1', isSelected: false },
                {   label:'LNB Menu2', key:'LNBmenu2', isSelected: false },
            ],
            splitLineMenus2: [
                {   label:'LNB Menu3', key:'LNBmenu3', isSelected: true,
                    menus: [
                        { label:'2depth Menu1', key:'2depthMenu1', isSelected: false },
                        { label:'2depth Menu2', key:'2depthMenu2', isSelected: true },
                        { label:'2depth Menu3', key:'2depthMenu3', isSelected: false },
                        { label:'2depth Menu4', key:'2depthMenu4', isSelected: false },
                    ]
                },
                {   label:'LNB Menu4', key:'LNBmenu4', isSelected: false,
                    menus: [
                        { label:'2depth Menu1', key:'2depthMenu1', isSelected: false },
                        { label:'2depth Menu2', key:'2depthMenu2', isSelected: false },
                        { label:'2depth Menu3', key:'2depthMenu3', isSelected: false },
                        { label:'2depth Menu4', key:'2depthMenu4', isSelected: false },
                    ]
                },
                {   label:'LNB Menu5', key:'LNBmenu5', isSelected: false,
                    menus: [
                        { label:'2depth Menu1', key:'2depthMenu1', isSelected: false },
                        { label:'2depth Menu2', key:'2depthMenu2', isSelected: false },
                        { label:'2depth Menu3', key:'2depthMenu3', isSelected: false },
                        { label:'2depth Menu4', key:'2depthMenu4', isSelected: false },
                    ]
                }
            ],
            splitLineMenus3: [
                {   label:'LNB Menu6', key:'LNBmenu6', isSelected: false,
                    menus: [
                        { label:'2depth Menu1', key:'2depthMenu1', isSelected: false },
                        { label:'2depth Menu2', key:'2depthMenu2', isSelected: false },
                        { label:'2depth Menu3', key:'2depthMenu3', isSelected: false },
                        { label:'2depth Menu4', key:'2depthMenu4', isSelected: false },
                    ]
                },
                {   label:'LNB Menu7', key:'LNBmenu7', isSelected: false,
                    menus: [
                        { label:'2depth Menu1', key:'2depthMenu1', isSelected: false },
                        { label:'2depth Menu2', key:'2depthMenu2', isSelected: false },
                        { label:'2depth Menu3', key:'2depthMenu3', isSelected: false },
                        { label:'2depth Menu4', key:'2depthMenu4', isSelected: false },
                    ]
                },
            ],
        }
    },
    methods: {
        selectMenu(clickedMenu, clickedMenuSiblings){

            if (clickedMenu.isSelected && clickedMenu.menus) {
                this.releaseMenuSelection(clickedMenuSiblings);
                clickedMenu.isSelected = false;
            } else {
                this.releaseMenuSelection(clickedMenuSiblings);
                clickedMenu.isSelected = true;
            }
        },
        releaseMenuSelection(menus){
            menus.forEach(menu => {
                menu.isSelected = false;
                if(menu.menus) this.releaseMenuSelection(menu.menus);
            });
        }
    }
}
</script>

<style scoped>
.ui-title {
    display: flex;
    flex-flow: row nowrap;

    background-color:white;
    padding-bottom: 16px;

    border-bottom: 1px solid #CCCCCC;
}
.ui-title-label {
    display: flex;
    flex-flow: column nowrap;
}
.ui-title-label__main {
    font-size: 32px;
    font-weight: bold;
}
.ui-title-label__sub {
    color: #5A5A5A;
    font-size: 16px;

    margin-top: 12px;
}
.ui-title-side {
    margin-left: auto;

    display: flex;
    align-items: flex-end;
    color: #767676;
}
.ui-title-side > em {
    color: #333333;
}
.page-content-area {
    margin: 32px auto;
    padding: 48px 0;
}
</style>