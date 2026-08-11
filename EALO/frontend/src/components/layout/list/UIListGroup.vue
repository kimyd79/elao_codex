<template>
    <div class="ui-list-group">
        <div v-if="title != undefined" class="ui-list-group__title">{{ title }}</div>
        <slot />
    </div>
</template>

<script>
    export default {
        name: 'ui-list-group',
        props: {
            title : { type: String, default: undefined }
        },
        computed: {
            listStyle() {
                var style = {};

                if (this.columns) {
                    var width = this.columns * 80 - (this.columns > 1 ? 16 : 0);
                    style['width']  = width + 'px';
                }

                return style;
            }
        }
    };
</script>

<style lang="scss">
.ui-list-group {
    background: $lego-card__background-color;
    display: flex;
    flex-flow: column nowrap;
}
.ui-list-group > .ui-list {
    border-bottom: 1px solid #EAEAEA;
}
.ui-list-group__title {
    font-size: 12px;
    padding-top: 20px;
    border-top: 1px solid #CCCCCC;
}
</style>