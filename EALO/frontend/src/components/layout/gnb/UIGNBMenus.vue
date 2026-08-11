<template>
    <div class="ui-gnb-menu">
        <div v-for="menu in menus" 
            :key="menu.key" 
            :class="{ 'ui-gnb-menu__item--selected' : menu.isSelected }"
            class="ui-gnb-menu__item"
        >
            <slot :menu="menu">
                <a>{{menu.label}}</a>
            </slot>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ui-gnb-menus',
    props: {
        menus: { type : Array, default : [] }
    }
}
</script>

<style lang="scss">
.ui-gnb-menu {
    display: flex;
    flex-flow: row nowrap;
    padding: 0 16px;
}
.ui-gnb-menu__item {
    display: flex;
    font-size: 16px;
    border-bottom: 3px solid transparent;

    padding: 0 4px;
}
.ui-gnb-menu__item > a {
    display: flex;
    align-items: center;
    white-space: nowrap;
}
.ui-gnb-menu__item:hover {
    cursor: pointer;
}
.ui-gnb-menu__item--selected {
    font-weight: bold;
    border-bottom: 3px solid #553CA5;
}
.ui-gnb-menu__item + .ui-gnb-menu__item {
    margin-left: 48px;
}
</style>