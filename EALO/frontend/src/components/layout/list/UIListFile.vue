<template>
    <div class="ui-list-content-file">
        <lego-icon small type="picto">html_file</lego-icon>
        <div class="ui-list-content-file__name">
            <slot name="filename">File Name</slot>
        </div>
        <div class="ui-list-content-file__size">
            (<slot name="filesize">000</slot>MB)
        </div>
        <div class="ui-list-content-file__date">
            <slot name="date">2019.02.21</slot>
        </div>
    </div>
</template>

<script>
export default {
  name: 'ui-list-file',
  props: {
  }
}
</script>

<style lang="scss">
.ui-list-content-file {
    display: flex;
    flex-flow: row nowrap;
    flex-grow: 0;
    flex-shrink: 0;

    align-items: center;
}
.ui-list-content-file__name {
    font-size: 16px;
    font-weight: bold;

    margin-left: 8px;
}
.ui-list-content-file__size {
    font-size: 12px;
    font-weight: bold;
    color: #959595;

    margin-left: 9px;
}
.ui-list-content-file__date {
    font-size: 12px;
    color: #959595;

    margin-left: auto;
}
</style>