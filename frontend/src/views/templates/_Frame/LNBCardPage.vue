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
                <ui-lnb-item>
                    <div class="lnb-card-page__title">
                        성인의 식품 섭취빈도<br>
                        유사성에 따른<br>
                        당뇨 유병률 분석 1
                    </div>
                </ui-lnb-item>
                <ui-lnb-item>
                    <div class="lnb-card-page__desc">
                        이 데이터는 신현태 선생님께서 
                        유전체 변이별 약물 반응을 분석하기 
                        위해 만든 데이터 입니다.
                    </div>
                </ui-lnb-item>
                <ui-lnb-menus :menus="lnbMenus" @selectMenu="selectMenu" no-expand>
                    <template v-slot:default="{menu}">
                        <div class="lnb-card-page__item">
                            <div class="lnb-card-page__item-title">
                                <span>Card Information {{menu.label}}</span>
                                <lego-icon small>more</lego-icon>
                            </div>
                            <div class="lnb-card-page__item-info">
                                <lego-badge badge-color="default" badge-type="status-dot">Complete</lego-badge>
                                <span>2018 - 05 - 05</span>
                            </div>
                        </div>
                    </template>
                </ui-lnb-menus>
            </ui-lnb>

            <ui-container-box :columns=20 vertical align-center class="bg-white page-content-area" >
                <slot />
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
            lnbMenus: [
                { label:'TITLE1', key:'TITLE1', isSelected: false },
                { label:'TITLE2', key:'TITLE2', isSelected: false },
                { label:'TITLE3', key:'TITLE3', isSelected: true },
                { label:'TITLE4', key:'TITLE4', isSelected: false },
                { label:'TITLE5', key:'TITLE5', isSelected: false },
                { label:'TITLE6', key:'TITLE6', isSelected: false },
                { label:'TITLE7', key:'TITLE7', isSelected: false }
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
.lnb-card-page__title {
    font-size: 20px;
    margin-top: 32px;
}
.lnb-card-page__desc {
    margin-top: 16px;
    margin-bottom: 52px;
}
.lnb-card-page__item {
    display: flex;
    flex-flow: column nowrap;
    flex-grow: 1;
    padding: 6px 0;
}
.lnb-card-page__item-title,
.lnb-card-page__item-info {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
}
.lnb-card-page__item-title {
    justify-content: space-between;
    font-size: 14px;
    padding-left: 6px;
}
.lnb-card-page__item-info {
    font-size: 12px;
    margin-top: 4px;
}
.lnb-card-page__item-info span {
    margin-left: 8px;
    padding-left: 8px;
    border-left: 1px solid #959595;
}
</style>