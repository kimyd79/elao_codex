<template>

    <ui-container-box :columns=24 vertical :title="title">

        <ui-gnb>
            <template v-slot:lead>
                <ui-gnb-title>
                    <template v-slot:title>SDS Platform</template>
                </ui-gnb-title>
                <ui-gnb-menus :menus="menus" />
                <ui-gnb-item>
                    <div class="gnb-menu-link">
                        <span class="gnb-menu-link__label">GNB Menu_5</span>
                        <span><lego-icon small>open_in_new</lego-icon></span>
                    </div>
                </ui-gnb-item>
            </template>
            <template v-slot:tail>
                <lego-button icon="download" primary>Design Asset</lego-button>
            </template>
        </ui-gnb>

        <ui-container-box :columns=24 horizontal class="bg-contents">

            <ui-lnb>
                <ui-lnb-menus :menus="splitLineMenus1" @selectMenu="selectMenu"/>
                <ui-lnb-menus :menus="splitLineMenus2" @selectMenu="selectMenu"/>
                <ui-lnb-menus :menus="splitLineMenus3" @selectMenu="selectMenu"/>
            </ui-lnb>

            <ui-container-box :columns=20 vertical align-center class="page-content-area" >
                <ui-container-box :columns=16 vertical>
                    
                    <slot />
                </ui-container-box>
            </ui-container-box>

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
                { label:'GNB Menu_1', key:'menu1', isSelected: true },
                { label:'GNB Menu_2', key:'menu2', isSelected: false },
                { label:'GNB Menu_3', key:'menu3', isSelected: false },
                { label:'GNB Menu_4', key:'menu4', isSelected: false }
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
.ui-title-page {
    display: flex;
    flex-flow: column nowrap;

    padding-bottom: 24px;

    border-bottom: 1px solid #CCCCCC;
}
.ui-title-page-label__main {
    font-size: 32px;
    font-weight: bold;
}
.ui-title-page-label__sub {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
    justify-content: space-between;
    color: #5A5A5A;
    font-size: 16px;

    margin-top: 12px;
}
.page-content-area {
    margin: 32px auto;
    padding: 48px 0;
}
.gnb-menu-link {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
    padding-left: 32px;
    border-left: 1px solid #CCCCCC;
    font-size: 16px;
}
.gnb-menu-link:hover {
    cursor: pointer;
}
.gnb-menu-link__label {
    margin-right: 12px;
}
</style>