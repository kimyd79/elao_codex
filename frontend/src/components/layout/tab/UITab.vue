<template>
    <div :class="[
        { 'ui-tab-box' : true },
        { 'ui-tab-box--no-bottom-border' : noBottomBorder }
    ]">
        <div class="ui-tab-tabs">
            <template v-for="(tab, index) in tabs">
                <div :key="index"
                    :class="[
                        {'ui-tab-item':true},
                        {'ui-tab-item__box':box},
                        {'ui-tab-item__underline':underline},
                        {'ui-tab-item__removable':removable},
                        {'ui-tab-item__box--selected':box && tab.isSelected},
                        {'ui-tab-item__underline--selected':underline && tab.isSelected},
                        {'ui-tab-item__removable--selected':removable && tab.isSelected},
                    ]"
                >
                    <div v-if="tab.icon" class="ui-tab-item-icon">
                        <lego-icon small spacing>cart</lego-icon>
                    </div>
                    <div class="ui-tab-item-label">
                        {{ tab.label }}
                    </div>
                    <div v-if="removable" class="ui-tab-item-close">
                        <lego-icon small spacing>close</lego-icon>
                    </div>
                </div>
            </template>
        </div>
        <div v-if="!noAction" class="ui-tab-action">
            <div class="ui-tab-action-item">
                <div class="ui-tab-action-forward">
                    <lego-icon small type="picto" v-on:click="tabForward">collapse_menu</lego-icon>
                </div>
            </div>
            <div class="ui-tab-action-item">
                <div class="ui-tab-action-backward">
                    <lego-icon small type="picto"  v-on:click="tabBackward">collapse_menu</lego-icon>
                </div>
            </div>
            <div v-if="removable" class="ui-tab-action-item">
                <lego-icon small type="picto">add</lego-icon>
            </div>
        </div>
    </div>

</template>

<script>
export default {
    name: 'ui-tab',
    props: {
        tabs: { type: Array, required: true },

        box: { type: Boolean, default: false },
        underline : { type: Boolean, default: false },
        removable : { type: Boolean, default: false },

        noAction : { type: Boolean, default: false },
        noBottomBorder : { type: Boolean, default: false },
    },

    methods: {

        tabChange(dir) {
            this.$emit('tabChange', dir)
        },

        tabForward() {
            this.tabChange(1)
        },
        tabBackward() {
            this.tabChange(2)
        },
        

    }
}
</script>

<style>
.ui-tab-box {
    display: flex;
    flex-flow: row nowrap;
    height: 48px;

    position: relative;
    overflow: hidden;
    
    color: #5A5A5A;
    border-bottom: 1px solid #CCCCCC;
}
.ui-tab-box.ui-tab-box--no-bottom-border {
    border-bottom: none;
}
.ui-tab-tabs {
    display: flex;
    flex-flow: row nowrap;
}
.ui-tab-item {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
    justify-content: center;

    padding: 0px 24px;
    min-width: 168px;
}
.ui-tab-item:hover {
    cursor: pointer;
}
.ui-tab-item-label {
    font-size: 14px;
}
.ui-tab-item-close {
    margin-left: auto;
}
.ui-tab-item__box {
    border: 1px solid #CCCCCC;
    background-color: white;
}
.ui-tab-item__removable {
    border: 1px solid #CCCCCC;

    padding: 0px 8px 0 16px;

    justify-content: flex-start;
}


.ui-tab-item__box--selected {
    color: #553CA5;
    border-color: #553CA5;
    background-color: #F3F1F9;
}
.ui-tab-item__underline--selected {
    color: #553CA5;
    border-bottom: 2px solid #553CA5;
}
.ui-tab-item__removable--selected {
    color: #553CA5;
    border-color: #553CA5;
    background-color: #F3F1F9;
}

.ui-tab-action {
    position: absolute;
    right: 0;
    top: 0;

    display: flex;
    flex-flow: row nowrap;
}
.ui-tab-action-item {
    display: flex;
    justify-content: center;
    align-items: center;

    width: 36px;
    height: 48px;
}
.ui-tab-action-item:hover {
    cursor: pointer;
}
.ui-tab-action-forward {
    transform: rotate(-90deg);
}
.ui-tab-action-backward {
    transform: rotate(90deg);
}

</style>