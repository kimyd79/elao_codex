<template>
    <img src="@/assets/img/thumb/thumb_52x52.png" class="ui-list-thumbnail__img" :style="listThumbnailStyle" />
</template>

<script>
export default {
    name: 'ui-list-thumbnail',
    props: {
            width: { type : Number, required : true },
            height: { type : Number, required : true }
    },
    computed: {
        listThumbnailStyle() {
            var style = {};
            
            style['width']  = this.width + 'px';
            style['height']  = this.height + 'px';

            return style;
        },
    }
}
</script>

<style lang="scss">
.ui-list-thumbnail__img {
    margin-right: 16px;
}
</style>