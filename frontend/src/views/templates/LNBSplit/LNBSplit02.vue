<template>

    <LNBPage title="Screen with LNB - Split 02" class="mg-auto page">

        <ui-container-box :columns=20 vertical align-center>

            <ui-validation-step :steps="['Basic Information', 'Select Data Connection', 'Column Settings', 'Additional Information']" :current-index=2 no-content />

        </ui-container-box>

        <ui-container-box :columns=20 horizontal class="content-area">

            <ui-container-box :columns=4 vertical >

                <ui-lnb searchable class="attr-list">
                    <ui-lnb-menus :menus="attrItems" @selectMenu="selectMenu" class="mt20">
                        <template v-slot:default="{menu}">
                            <div class="attr-item" :class="[{ 'attr-item--selected' : menu.isSelected }]">
                                <lego-icon xsmall>check</lego-icon>
                                <span>{{menu.label}}</span>
                            </div>
                        </template>
                    </ui-lnb-menus>
                </ui-lnb>

            </ui-container-box>

            <ui-container-box :columns=16 vertical class="content-right-area">

                <div class="content-title">
                    <span class="content-title__main">
                        BMI
                    </span>
                    <span class="content-title__sub">
                        변수타입 : 불연속형 | 변수형식/단위 : yrs | 정상구간 : 0~200
                    </span>
                </div>

                <div class="content-main">
                    <div class="content-point">
                        <div class="content-item">
                            <span class="content-item-title">Missing Values</span>
                            <span class="content-item-desc">A specific value or range can be defined as a missing</span>
                            <img src="../../../assets/img/bmi/bmi_img1.png" style="width: 505px; height:210px;"/>
                        </div>
                        <div class="content-item">
                            <span class="content-item-title">Repeated measure</span>
                            <span class="content-item-desc">You can see the graph corresponding to the selected item.</span>
                            <img src="../../../assets/img/bmi/bmi_img1.png" style="width: 505px; height:210px;"/>
                        </div>
                    </div>
                    <div class="content-bottom">
                        <img src="../../../assets/img/bmi/bmi_img2.png" style="width: 362px; height:207px;"/>
                        <img src="../../../assets/img/bmi/bmi_img3.png" style="width: 572px; height:159px;"/>
                    </div>
                </div>

                <ui-form-buttons divider no-margin>
                    <lego-button large>Delete</lego-button>
                    <lego-button large main>Save</lego-button>
                </ui-form-buttons>

            </ui-container-box>

        </ui-container-box>

    </LNBPage>

</template>

<script>
import LNBPage from '../_Frame/LNBCardPage'

export default {
    name: 'lnb-split-02',
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
            attrItems: [
                { label:'gender', key:'gender', isSelected: false },
                { label:'ages', key:'ages', isSelected: false },
                { label:'height', key:'height', isSelected: false },
                { label:'weight', key:'weight', isSelected: false },
                { label:'birth', key:'birth', isSelected: false },
                { label:'BMI', key:'BMI', isSelected: true },
                { label:'Blood Type', key:'Blood', isSelected: false }
            ],
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
.attr-item {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
}
.attr-item .lego-icon {
    color: #CCCCCC;
}
.attr-item.attr-item--selected .lego-icon {
    color: #333333;
}
.attr-item span {
    margin-left: 8px;
}
.attr-item.attr-item--selected {
    color: #333333;
}
.page .content-area {
    border-top: 1px solid #EAEAEA;
}
.page .attr-list {
    border-right: 1px solid #EAEAEA;
    height: 100%;
}
.content-title {
    display: flex;
    flex-flow: row nowrap;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
}
.content-title__main {
    font-size: 28px;
    font-weight: bold;
}
.content-title__sub {
    font-size: 12px;
    color: #333333;    
}

.content-main {
    display: flex;
    flex-flow: column nowrap;
}
.content-point {
    display: flex;
    flex-flow: row nowrap;
    justify-content: space-between;
    background-color: #F7F7F8;
    padding: 32px;
}
.content-item {
    display: flex;
    flex-flow: column nowrap;
}
.content-item-title {
    font-size: 20px;
}
.content-item-desc {
    font-size: 14px;
    color: #767676;
    padding-left: 8px;
    margin-bottom: 50px;
}
.content-bottom {
    display: flex;
    flex-flow: row nowrap;
    justify-content: space-between;
    align-items: flex-start;
    padding: 32px;
}
.content-right-area {
    padding: 48px 80px 48px 48px;
}
</style>