<template>
    <div class="ui-list" :style="listStyle">
        <div v-if="number" class="ui-list-number">
            {{number}}
        </div>
        <div :class="[
                { 'ui-list-main' : true },
                { 'ui-list-main--selected' : selected }
            ]"
            :style="listMainStyle"
        >
            <div class="ui-list-control">
                <slot name="control" />
            </div>
            <div class="ui-list-thumbnail">
                <slot name="thumbnail" />
            </div>
            <div class="ui-list-content">
                <slot />
            </div>
            <div class="ui-list-support">
                <slot name="support">
                    <ui-list-item v-if="expandable" icons @click="toggleExpand" class="ui-list-support__expandable">
                        <lego-icon v-if="isExpend" xsmall type="picto">collapse_menu</lego-icon>
                        <lego-icon v-else xsmall type="picto">expand_menu</lego-icon>
                    </ui-list-item>
                </slot>
            </div>
        </div>
        <div v-if="isExpend" class="ui-list-expand">
            <slot name="expand" />
        </div>
    </div>
</template>

<script>
    export default {
        name: 'ui-list',
        props: {
            columns : { type: Number, default: undefined },
            radio : { default: undefined },
            check : { default: undefined },
            expandable : { type: Boolean, default: false },
            selected : { type: Boolean, default: false },
            number : { type: Number, default: undefined },
        },
        data() { return {
            isExpend : false
        }},
        computed: {
            listStyle() {
                var style = {};

                if (this.columns) {
                    var width = this.columns * 80 - (this.columns > 1 ? 16 : 0);
                    style['width']  = width + 'px';
                }

                return style;
            },
            listMainStyle() {
                var style = {};

                if (this.number) {
                    style['padding-left']  = '12px';
                }

                return style;
            }
        },
        methods: {
            toggleExpand() {
                this.isExpend = !this.isExpend;
            }
        }
    };
</script>

<style lang="scss">
.ui-list {
    position: relative;
    background: white;
    display: flex;
    flex-flow: column nowrap;
}
.ui-list-main > div:first-child {
    margin-left: 24px;
}
.ui-list-main > div:last-child {
    margin-right: 24px;
}
.ui-list-main {
    display: flex;
    flex-flow: row nowrap;
    padding: 16px 0;
}
.ui-list-main:hover {
    background-color: #F7F7F7;
}
.ui-list-main--selected {
    background-color: #F3F1F9;
    color: #553CA5;
}
.ui-list-number {
    position: absolute;
    top: 16px;
    left: 20px;

    font-size: 14px;
    font-weight: bold;
}
.ui-list-control {
    display: flex;
    align-items: center;
    flex-grow: 0;
    flex-shrink: 0;
}
.ui-list-control > * {
    margin-right: 16px;
}
.ui-list-thumbnail {
    display: flex;
    flex-grow: 0;
    flex-shrink: 0;
}
.ui-list-content {
    display: flex;
    flex-flow: column nowrap;
    
    flex-shrink: 1;
    flex-grow: 1;
    overflow: hidden;
    
    justify-content: center;
}
.ui-list-support {
    display: flex;
    flex-grow: 0;
    flex-shrink: 0;
    flex-flow: column nowrap;
    justify-content: center;
}
.ui-list-support > * {
    margin-left: 16px !important;
}
.ui-list-support > button + button {
    margin-top: 8px;
}
.ui-list-support__expandable:hover {
    cursor: pointer;
}
.ui-list-expand {
    margin: 0 24px 24px 24px;
    border-top: 1px solid #EAEAEA;
}
</style>