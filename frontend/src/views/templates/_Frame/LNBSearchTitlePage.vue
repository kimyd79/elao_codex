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

            <ui-lnb searchable>
                <ui-lnb-menus :menus="lv2Menus" @selectMenu="selectMenu"/>
            </ui-lnb>

            <ui-container-box :columns=20 vertical class="mg-auto">

                <div class="ui-page-title">
                    <div class="ui-page-title-label">
                        <div class="ui-page-title-label__main">
                            Lorem Ipsum
                        </div>
                    </div>
                    <div class="ui-page-title-side">
                        Menu1 > LNB Menu1 > <em> LNB Sub Menu1</em>
                    </div>
                </div>

                <ui-container-box :columns=20 vertical align-center class="bg-white page-content-area" >
                    <ui-container-box :columns=18 vertical>
                        <slot />
                    </ui-container-box>
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
                { label:'Menu1', key:'menu1', isSelected: true },
                { label:'Menu2', key:'menu2', isSelected: false },
                { label:'Menu3', key:'menu3', isSelected: false },
                { label:'Menu4', key:'menu4', isSelected: false },
                { label:'Menu5', key:'menu5', isSelected: false }
            ],
            lv2Menus: [
                {   label:'LNB Menu1', key:'LNBmenu1', isSelected: false,
                    menus: [
                        { label:'2depth Menu1', key:'2depthMenu1', isSelected: false },
                        { label:'2depth Menu2', key:'2depthMenu2', isSelected: false },
                        { label:'2depth Menu3', key:'2depthMenu3', isSelected: false },
                        { label:'2depth Menu4', key:'2depthMenu4', isSelected: false },
                    ]
                },
                {   label:'LNB Menu2', key:'LNBmenu2', isSelected: false,
                    menus: [
                        { label:'2depth Menu1', key:'2depthMenu1', isSelected: false },
                        { label:'2depth Menu2', key:'2depthMenu2', isSelected: false },
                        { label:'2depth Menu3', key:'2depthMenu3', isSelected: false },
                        { label:'2depth Menu4', key:'2depthMenu4', isSelected: false },
                    ]
                },
                {   label:'LNB Menu3', key:'LNBmenu3', isSelected: true,
                    menus: [
                        { label:'2depth Menu1', key:'2depthMenu1', isSelected: false },
                        { label:'2depth Menu2', key:'2depthMenu2', isSelected: true },
                        { label:'2depth Menu3', key:'2depthMenu3', isSelected: false },
                        { label:'2depth Menu4', key:'2depthMenu4', isSelected: false },
                    ]
                },
                { label:'LNB Menu4', key:'LNBmenu4', isSelected: false },
                { label:'LNB Menu5', key:'LNBmenu5', isSelected: false }
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
.ui-page-title {
    display: flex;
    flex-flow: row nowrap;
    margin-top: 32px;
    margin-bottom: 18px;
}
.ui-page-title-label {
    display: flex;
    flex-flow: column nowrap;
}
.ui-page-title-label__main {
    font-size: 32px;
    font-weight: bold;
}
.ui-page-title-label__sub {
    color: #5A5A5A;
    font-size: 16px;

    margin-top: 12px;
}
.ui-page-title-side {
    margin-left: auto;

    display: flex;
    align-items: flex-end;
    color: #767676;
}
.ui-page-title-side > em {
    color: #333333;
}
.page-content-area {
    margin: 0 auto 32px;
    padding: 48px 0;
}
</style>