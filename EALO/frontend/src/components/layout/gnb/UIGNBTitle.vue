<template>
    <div class="ui-gnb-title" :style="{ width : width + 'px'}" :class="{ 'ui-gnb-title__center' : alignCenter }">
        <div class="ui-gnb-title__main">
            <slot name="title"/>
        </div>
        <div class="ui-gnb-label__sub">
            <slot name="sub"/>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ui-gnb-title',
    props: {
        width: { type : Number, default : 304 },
        alignCenter : { type : Boolean, default : false },
    },
}
</script>

<style lang="scss">
.ui-gnb-title {
    display: flex;
    flex-flow: column nowrap;
    justify-content: center;
    padding: 0 16px;
}
.ui-gnb-title__center {
    align-items: center;
}
.ui-gnb-title__main {
    font-size: 24px;
    font-weight: bold;
}
.ui-gnb-title__sub {
    font-size: 12px;
    color: #767676;
}
</style>