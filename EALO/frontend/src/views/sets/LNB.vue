<template>
    <ui-page-box align-center>

        <ui-container-box :columns=22 :height=1000 horizontal title="Default" class="mt50">

            <ui-lnb>
                <ui-lnb-menus :menus="lv1Menus" @selectMenu="selectMenu"/>
            </ui-lnb>

            <ui-lnb>
                <ui-lnb-menus :menus="lv2Menus" @selectMenu="selectMenu"/>
            </ui-lnb>

            <ui-lnb>
                <ui-lnb-menus :menus="lv3Menus" @selectMenu="selectMenu"/>
            </ui-lnb>

            <ui-lnb>
                <ui-lnb-menus :menus="twoLineMenus" @selectMenu="selectMenu"/>
            </ui-lnb>

            <ui-lnb>
                <ui-lnb-menus :menus="longMenus" @selectMenu="selectMenu"/>
            </ui-lnb>

        </ui-container-box>

        <ui-container-box :columns=22 horizontal class="mt50">

            <ui-container-box :columns=4 :height=1000 horizontal title="Split line">
                <ui-lnb>
                    <ui-lnb-menus :menus="splitLineMenus1" @selectMenu="selectMenu"/>
                    <ui-lnb-menus :menus="splitLineMenus2" @selectMenu="selectMenu"/>
                    <ui-lnb-menus :menus="splitLineMenus3" @selectMenu="selectMenu"/>
                </ui-lnb>
            </ui-container-box>

            <ui-container-box :columns=4 :height=1000 horizontal title="Title">
                <ui-lnb title="Title">
                    <ui-lnb-menus :menus="lv2Menus" @selectMenu="selectMenu"/>
                </ui-lnb>
            </ui-container-box>

            <ui-container-box :columns=4 :height=1000 horizontal title="Search">
                <ui-lnb searchable>
                    <ui-lnb-menus :menus="lv2Menus" @selectMenu="selectMenu"/>
                </ui-lnb>
            </ui-container-box>

            <ui-container-box :columns=8 :height=1000 horizontal title="Tab">

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

                <ui-lnb>
                    <ui-lnb-item>
                        <lego-tab-box :default-idx="1" underline>
                            <lego-tab-label :idx="1">Tab_1</lego-tab-label>
                            <lego-tab-label :idx="2">Tab_2</lego-tab-label>
                        </lego-tab-box>
                    </ui-lnb-item>
                    <ui-lnb-menus :menus="splitLineMenus1" @selectMenu="selectMenu"/>
                    <ui-lnb-menus :menus="splitLineMenus2" @selectMenu="selectMenu"/>
                    <ui-lnb-menus :menus="splitLineMenus3" @selectMenu="selectMenu"/>
                </ui-lnb>

            </ui-container-box>

        </ui-container-box>

        <ui-container-box :columns=22 horizontal class="mt50">

            <ui-container-box :columns=8 :height=1000 horizontal title="Search + Tab">

                <ui-lnb searchable>
                    <ui-lnb-item class="mt24">
                        <lego-tab-box :default-idx="1">
                            <lego-tab-label :idx="1">Tab_1</lego-tab-label>
                            <lego-tab-label :idx="2">Tab_2</lego-tab-label>
                        </lego-tab-box>
                    </ui-lnb-item>
                    <ui-lnb-menus :menus="lv3Menus" @selectMenu="selectMenu"/>
                </ui-lnb>

                <ui-lnb searchable>
                    <ui-lnb-item class="mt24">
                        <lego-tab-box :default-idx="1" underline>
                            <lego-tab-label :idx="1">Tab_1</lego-tab-label>
                            <lego-tab-label :idx="2">Tab_2</lego-tab-label>
                        </lego-tab-box>
                    </ui-lnb-item>
                    <ui-lnb-menus :menus="lv3Menus" @selectMenu="selectMenu"/>
                </ui-lnb>

            </ui-container-box>

            <ui-container-box :columns=4 :height=1000 horizontal title="Badge case">
                <ui-lnb>
                    <ui-lnb-menus :menus="badgeMenus" @selectMenu="selectMenu"/>
                </ui-lnb>
            </ui-container-box>

            <ui-container-box :columns=8 :height=1000 horizontal align-start title="ETC.">
                <ui-lnb expandable>
                    <ui-lnb-item>
                        <lego-tab-box :default-idx="1">
                            <lego-tab-label :idx="1">Tab_1</lego-tab-label>
                            <lego-tab-label :idx="2">Tab_2</lego-tab-label>
                        </lego-tab-box>
                    </ui-lnb-item>
                    <ui-lnb-menus :menus="lv1Menus" @selectMenu="selectMenu"/>
                </ui-lnb>

                <ui-lnb-lite class="ml50">
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
            </ui-container-box>

        </ui-container-box>

    </ui-page-box>
</template>

<script>
export default {
    name: 'lnb',
    data() {
        return {
            lv1Menus: [
                { label:'LNB Menu1', key:'LNB menu1', isSelected: false },
                { label:'LNB Menu2', key:'LNB menu2', isSelected: false },
                { label:'LNB Menu3', key:'LNB menu3', isSelected: true },
                { label:'LNB Menu4', key:'LNB menu4', isSelected: false },
                { label:'LNB Menu5', key:'LNB menu5', isSelected: false }
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
            lv3Menus: [
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
                        {   label:'2depth Menu1', key:'2depthMenu1', isSelected: false,
                            menus: [
                                { label:'3depth Menu1', key:'3depthMenu1', isSelected: false },
                                { label:'3depth Menu2', key:'3depthMenu2', isSelected: false },
                                { label:'3depth Menu3', key:'3depthMenu3', isSelected: false },
                                { label:'3depth Menu4', key:'3depthMenu4', isSelected: false },
                            ]
                        }, 
                        {   label:'2depth Menu2', key:'2depthMenu2', isSelected: true,
                            menus: [
                                { label:'3depth Menu1', key:'3depthMenu1', isSelected: true },
                                { label:'3depth Menu2', key:'3depthMenu2', isSelected: false },
                                { label:'3depth Menu3', key:'3depthMenu3', isSelected: false },
                                { label:'3depth Menu4', key:'3depthMenu4', isSelected: false },
                            ]
                        },
                        {   label:'2depth Menu3', key:'2depthMenu3', isSelected: false,
                            menus: [
                                { label:'3depth Menu1', key:'3depthMenu1', isSelected: false },
                                { label:'3depth Menu2', key:'3depthMenu2', isSelected: false },
                                { label:'3depth Menu3', key:'3depthMenu3', isSelected: false },
                                { label:'3depth Menu4', key:'3depthMenu4', isSelected: false },
                            ] 
                        },
                        {   label:'2depth Menu4', key:'2depthMenu4', isSelected: false,
                            menus: [
                                { label:'3depth Menu1', key:'3depthMenu1', isSelected: false },
                                { label:'3depth Menu2', key:'3depthMenu2', isSelected: false },
                                { label:'3depth Menu3', key:'3depthMenu3', isSelected: false },
                                { label:'3depth Menu4', key:'3depthMenu4', isSelected: false },
                            ]
                        },
                    ]
                },
                { label:'LNB Menu4', key:'LNBmenu4', isSelected: false },
                { label:'LNB Menu5', key:'LNBmenu5', isSelected: false }
            ],
            twoLineMenus: [
                {   label:'LNB Menu1_Andere Cumm-ing Andere', key:'LNBmenu1', isSelected: false },
                {   label:'LNB Menu 2_Acridotheres tristis', key:'LNBmenu2', isSelected: false },
                {   label:'LNB Menu 3_Burhinus grallarius', key:'LNBmenu3', isSelected: true,
                    menus: [
                        {   label:'2depth Menu1_Cacatua galerita', key:'2depthMenu1', isSelected: false },
                        {   label:'2depth Menu2_Corvus coronoides ', key:'2depthMenu2', isSelected: true,
                            menus: [
                                { label:'3depth Menu1_Corvus coronoides', key:'3depthMenu1', isSelected: false },
                                { label:'3depth Menu2_ Calyptorhyn-chus banksii', key:'3depthMenu2', isSelected: true },
                                { label:'3depth Menu3_Dacelo leachii ', key:'3depthMenu3', isSelected: false }
                            ]
                        },
                        {   label:'2depth Menu3', key:'2depthMenu3', isSelected: false },
                        {   label:'2depth Menu4', key:'2depthMenu4', isSelected: false },
                    ]
                },
                { label:'LNB Menu_4 Falco cenchroides', key:'LNBmenu4', isSelected: false },
                { label:'LNB Menu_5 Cacatua galerita', key:'LNBmenu5', isSelected: false }
            ],
            longMenus: [
                {   label:'LNB Menu1', key:'LNBmenu1', isSelected: false },
                {   label:'LNB Menu2', key:'LNBmenu2', isSelected: false },
                {   label:'LNB Menu3', key:'LNBmenu3', isSelected: true,
                    menus: [
                        {   label:'2depth Menu1', key:'2depthMenu1', isSelected: false }, 
                        {   label:'2depth Menu2', key:'2depthMenu2', isSelected: true,
                            menus: [
                                { label:'3depth Menu1', key:'3depthMenu1', isSelected: true },
                                { label:'3depth Menu2', key:'3depthMenu2', isSelected: false },
                                { label:'3depth Menu3', key:'3depthMenu3', isSelected: false },
                                { label:'3depth Menu4', key:'3depthMenu4', isSelected: false },
                            ]
                        },
                        {   label:'2depth Menu3', key:'2depthMenu3', isSelected: false },
                        {   label:'2depth Menu4', key:'2depthMenu4', isSelected: false },
                        {   label:'2depth Menu5', key:'2depthMenu5', isSelected: false },
                        {   label:'2depth Menu6', key:'2depthMenu6', isSelected: false },
                        {   label:'2depth Menu7', key:'2depthMenu7', isSelected: false },
                        {   label:'2depth Menu8', key:'2depthMenu8', isSelected: false },
                    ]
                },
                {   label:'LNB Menu4', key:'LNBmenu4', isSelected: false },
                {   label:'LNB Menu5', key:'LNBmenu5', isSelected: false },
                {   label:'LNB Menu6', key:'LNBmenu6', isSelected: false },
                {   label:'LNB Menu7', key:'LNBmenu7', isSelected: false },
                {   label:'LNB Menu8', key:'LNBmenu8', isSelected: false },
                {   label:'LNB Menu9', key:'LNBmenu9', isSelected: false },
                {   label:'LNB Menu10', key:'LNBmenu10', isSelected: false },
                {   label:'LNB Menu11', key:'LNBmenu11', isSelected: false },
                {   label:'LNB Menu12', key:'LNBmenu12', isSelected: false },
                {   label:'LNB Menu13', key:'LNBmenu13', isSelected: false },
                {   label:'LNB Menu14', key:'LNBmenu14', isSelected: false },
                {   label:'LNB Menu15', key:'LNBmenu15', isSelected: false }
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
            badgeMenus: [
                {   label:'LNB Menu1', key:'LNBmenu1', isSelected: false, badgeLabel: 'N',
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
                { label:'LNB Menu4', key:'LNBmenu4', isSelected: false, badgeLabel: 99 },
                { label:'LNB Menu5', key:'LNBmenu5', isSelected: false, badgeLabel: 'N' }
            ],
            textValue: '',
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