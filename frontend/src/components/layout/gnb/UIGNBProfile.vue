<template>
    <ui-gnb-item>
        <img src="@/assets/img/thumb/avatar_68x68.png" class="ui-gnb-action__profile-thumb"/>
        <div class="ui-gnb-action__profile-name">
            <slot />
        </div>
    </ui-gnb-item>
</template>

<script>
import UIGNBItem from "./UIGNBItem.vue"

export default {
    name: 'ui-gnb-profile',
    components: {
        'ui-gnb-item' : UIGNBItem
    },
}
</script>

<style lang="scss">
.ui-gnb-action__profile-thumb {
    width: 32px;
    height: 32px;
}
.ui-gnb-action__profile-name {
    margin-left: 8px;
    color: #767676;
}
</style>