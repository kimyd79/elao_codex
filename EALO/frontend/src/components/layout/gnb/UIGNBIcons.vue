<template>
    <ui-gnb-item>
        <div v-for="(icon, index) in icons" :key="index" class="ui-gnb-action__icon">
            <lego-icon spacing medium>{{icon}}</lego-icon>
        </div>
    </ui-gnb-item>
</template>

<script>
import UIGNBItem from "./UIGNBItem.vue"

export default {
    name: 'ui-gnb-icons',
    components: {
        'ui-gnb-item' : UIGNBItem
    },
    props: {
        icons: { type : Array, default : [] }
    }
}
</script>

<style lang="scss">
.ui-gnb-action__icon + .ui-gnb-action__icon {
    margin-left: 16px;
}
</style>