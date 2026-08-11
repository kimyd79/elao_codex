<template>
    <div :class="[
            { 
                'ui-lnb-lite-item' : true,
                'ui-lnb-lite-item__selected' : selected
            }
        ]"
    >
        <template v-if="label">
            <lego-icon large spacing>{{icon}}</lego-icon>
            <div class="ui-lnb-lite-item__label">{{label}}</div>
        </template>
        <template v-else>
            <lego-icon medium>{{icon}}</lego-icon>
        </template>
    </div>
</template>

<script>
export default {
    name: 'ui-lnb-lite-item',
    props: {
        icon: { type : String, required : true },
        label: { type : String },
        selected: { type : Boolean, default: false }
    },
}
</script>

<style lang="scss">
.ui-lnb-lite-item {
    display: flex;
    flex-flow: column nowrap;
    justify-content: center;
    align-items: center;

    color: #707070;
    width: 80px;
    height: 80px;
}
.ui-lnb-lite-item:hover {
    cursor: pointer;

    background: #F7F7F7;
    cursor: pointer;
}
.ui-lnb-lite-item__selected {
    color: #553CA5;
    background: #F7F5FB;
}
.ui-lnb-lite-item__label {
    font-size: 12px;

    flex: 0 0 auto;
}
</style>