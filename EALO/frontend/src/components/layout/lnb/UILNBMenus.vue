<template>
    <div class="ui-lnb-menu">
        <template v-for="menu in menus" >

            <div :key="menu.key" :class="menuItemClass(menu)">

                <div class="ui-lnb-menu__item-box" @click="clickMenu(menu, menus)">
                    <slot :menu="menu">
                        <a>{{menu.label}}</a>
                        <lego-badge v-if="menu.badgeLabel" :value="menu.badgeLabel" style="margin-left: 12px;"/>
                    </slot>
                    <div v-if="!noExpand"
                        :class="[
                            { 'ui-lnb-menu__item-icon' : true },
                            { 'ui-lnb-menu__item-icon--selected' : menu.isSelected }
                        ]"
                    >
                        <template v-if="menu.menus">
                            <lego-icon v-if="menu.isSelected" small spacing>collapse_menu</lego-icon>
                            <lego-icon v-else small spacing>expand_menu</lego-icon>
                        </template>
                    </div>
                </div>

                <template v-if="menu.menus && menu.isSelected">

                    <ui-lnb-menus :menus="menu.menus" :depth="(depth+1)" @selectMenu="clickMenu">
                        <template v-slot="{ menu }" >
                            <slot :menu="menu">
                                <a>{{menu.label}}</a>
                                <lego-badge v-if="menu.badgeLabel" :value="menu.badgeLabel" style="margin-left: 12px;"/>
                            </slot>
                        </template>
                    </ui-lnb-menus>

                </template>

            </div>

        </template>
    </div>
</template>

<script>
export default {
    name: 'ui-lnb-menus',
    props: {
        menus: { type : Array, default : [] },
        noExpand: { type : Boolean, default : false },
        depth: { type : Number, default : 1 }
    },
    methods: {
        menuItemClass(menu) {
            return [
                {
                    'ui-lnb-menu__item' : true,
                    'ui-lnb-menu__item--selected' : menu.isSelected && !menu.menus,
                    'ui-lnb-menu__item--opened' : menu.isSelected && menu.menus,
                    'ui-lnb-menu__item-depth2' : this.depth === 2,
                    'ui-lnb-menu__item-depth3' : this.depth === 3,
                }
            ]
        },
        clickMenu(menu, menus) {
            this.$emit('selectMenu', menu, menus);
        }
    }
}
</script>

<style lang="scss">
.ui-lnb-menu {
    display: flex;
    flex-flow: column nowrap;
    padding: 0 16px;
}
.ui-lnb-menu + .ui-lnb-menu {
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid #EAEAEA;
}
.ui-lnb-menu__item > .ui-lnb-menu {
    padding: 0;
}
.ui-lnb-menu__item-box {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;

    padding: 10px 8px 10px 16px;
    border-radius: 4px;

    flex-shrink: 1;
    overflow: hidden;
}
.ui-lnb-menu__item-box:hover {
    background: #F7F7F7;
    cursor: pointer;
}
.ui-lnb-menu__item--selected > .ui-lnb-menu__item-box {
    background: #F7F5FB;
    font-weight: bold;
    color: #553CA5;
}
.ui-lnb-menu__item--opened > .ui-lnb-menu__item-box {
    font-weight: bold;
}
.ui-lnb-menu__item .ui-lnb-menu__item-depth2 {
    padding-left: 16px;
    font-size: 12px;
}
.ui-lnb-menu__item .ui-lnb-menu__item-depth3 {
    padding-left: 8px;
    font-size: 12px;
}
.ui-lnb-menu__item-icon {
    display: block;
    flex: 0 0 24px;
    height: 24px;
    margin-left: auto;
    color: #CCCCCC;
}
.ui-lnb-menu__item-icon--selected {
    color: #777777 !important;
}

.ui-lnb-menu__item + .ui-lnb-menu__item {
    margin-top: 4px;
}
</style>