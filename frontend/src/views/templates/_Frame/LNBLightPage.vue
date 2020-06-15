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

            <ui-lnb-lite>
                <template v-slot:menus>
                    <ui-lnb-lite-item icon="word" label="Lorem" selected />
                    <ui-lnb-lite-item icon="powerpoint" label="Lorem" />
                    <ui-lnb-lite-item icon="pdf" label="Lorem" />
                    <ui-lnb-lite-item icon="voice_file" label="Lorem" />
                    <ui-lnb-lite-item icon="hangul" label="Lorem" />
                    <ui-lnb-lite-item icon="calendar" label="Lorem" />
                </template>
                <template v-slot:functions>
                    <ui-lnb-lite-item icon="delete" />
                    <ui-lnb-lite-item icon="setting" />
                </template>
            </ui-lnb-lite>

            <ui-container-box :columns=22 vertical align-center class="bg-white page-content-area" >
                <ui-container-box :columns=20 vertical>
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

        </ui-container-box>

    </ui-container-box>

</template>

<script scoped>
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
            ]
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

<style>
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