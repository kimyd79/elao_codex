<template>
    <div class="ui-gnb">
        <div class="ui-gnb-main">
            <div class="ui-gnb-lead">
                <slot name="lead" />
            </div>
            <div class="ui-gnb-middle">
                <slot name="middle" />
            </div>
            <div class="ui-gnb-tail">
                <slot name="tail" />
            </div>
        </div>
        <div v-if="twoLines" class="ui-gnb-main">
            <div class="ui-gnb-lead">
                <slot name="second-lead" />
            </div>
            <div class="ui-gnb-middle">
                <slot name="second-middle" />
            </div>
            <div class="ui-gnb-tail">
                <slot name="second-tail" />
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ui-gnb',
    props: {
        twoLines : { type : Boolean, default : false }
    }
}
</script>

<style lang="scss">
.ui-gnb {
    background: white;
    display: flex;
    flex-flow: column nowrap;

    border-bottom: 1px solid #707070;
}
.ui-gnb-main {
    display: flex;
    flex-flow: row nowrap;
    height: 72px;
    padding: 0 16px;
    position: relative;
}
.ui-gnb-main + .ui-gnb-main {
    border-top: 1px solid #CCCCCC;
}
.ui-gnb-lead {
    display: flex;
    flex-flow: row nowrap;
}
.ui-gnb-middle {
    position:absolute;
    top: 0;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%); 
    
    display: flex;
    flex-flow: row nowrap;
    justify-content: center;
}
.ui-gnb-tail {
    margin-left: auto;
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
}
</style>