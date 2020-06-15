<template>
    <div class="ui-list-container">
        <slot />
    </div>
</template>

<script>
    export default {
        name: 'ui-list-container',
        props: {
            columns : { type: Number, default: undefined }
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
.ui-list-container {
    background: $lego-card__background-color;
    display: flex;
    flex-flow: column nowrap;
    padding: 24px 16px;
}
.ui-list-container > .ui-list {
    border-bottom: 1px solid #EAEAEA;
}
</style>