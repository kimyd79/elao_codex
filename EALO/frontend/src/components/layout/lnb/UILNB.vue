<template>
    <div :class="[
            { 'ui-lnb-container' : true },
            { 'ui-lnb-container--white' : !transparent }
        ]"
    >
        <div :class="[
                { 'ui-lnb' : true },
                { 'ui-lnb__expand' : isExpand && !noFixWidth },
                { 'ui-lnb__shrink' : !isExpand },
            ]">
            <div v-if="expandable" @click="changeExpand"
                :class="[
                    { 'ui-lnb-expandable' : true },
                    { 'ui-lnb-expandable__expand' : isExpand },
                    { 'ui-lnb-expandable__shrink' : !isExpand },
                ]">
                <template v-if="isExpand">
                    <lego-icon small spacing>slide_left</lego-icon>
                </template>
                <template v-else>
                    <lego-icon small spacing>slide_right</lego-icon>
                    <div class="ui-lnb-expandable-content">Menu</div>
                </template>
            </div>
            <div v-if="title" class="ui-lnb-title">
                {{title}}
            </div>
            <div v-if="searchable" class="ui-lnb-search">
                <div class="ui-lnb-search-label">
                    Search index
                </div>
                <div class="ui-lnb-search-input">
                    <lego-text-field v-model="searchKeyword" placeholder="Search" searchable />
                </div>
            </div>
            <div class="ui-lnb-menu__container" v-show="isExpand">
                <slot />
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ui-lnb',
    props: {
        title: { type : String, default : undefined },
        searchable: { type : Boolean, default : false },
        expandable: { type : Boolean, default : false },
        noFixWidth: { type : Boolean, default : false },
        transparent: { type : Boolean, default : false },
    },
    data() {
        return {
            searchKeyword : '',
            isExpand: true
        }
    },
    methods: {
        changeExpand() {
            this.isExpand = !this.isExpand;
        }
    }
}
</script>

<style lang="scss">
.ui-lnb-container {
    display: flex;
    flex-direction: column;
    height: inherit;
}
.ui-lnb-container--white {
    background-color: white;
}
.ui-lnb {
    display: flex;
    flex-flow: column nowrap;
    flex-grow: 1;

    overflow-y: auto;
    overflow-x: hidden;

    padding: 32px 0;
    color: #333333;
}
.ui-lnb__expand {
    width: 272px;
}
.ui-lnb__shrink {
    width: 32px;
    overflow-y: hidden;
}
.ui-lnb-title {
    padding: 12px 32px 32px;
    font-size: 24px;
    color: #959595;
}
.ui-lnb-search {
    display: flex;
    flex-flow: column nowrap;
    padding: 0 32px 16px;

    border-bottom: 1px solid #EAEAEA;
}
.ui-lnb-search-label {
    color: #767676;
    font-size: 12px;
}
.ui-lnb-search-input {
    margin-top: 8px;
}
.ui-lnb-expandable {
    background: white;
    color: #A5A5A5;
    padding: 12px 4px;

    display: flex;
    flex-flow: column nowrap;
    justify-content: flex-start;
    align-items: center;
}
.ui-lnb-expandable__expand {
    position: absolute;
    z-index: 9999;

    transform: translateX(272px) translateY(-32px);
    width: 32px;
    height: 48px;
}
.ui-lnb-expandable__shrink {
    transform: translateX(0px) translateY(-32px);
}
.ui-lnb-expandable:hover {
    cursor: pointer;
}
.ui-lnb-expandable-content {
    transform: rotate(270deg);
    margin-top: 16px;
    font-size: 12px;
}

.ui-lnb-item + .ui-lnb-menu {
    margin-top: 24px;
}
.ui-lnb-search + .ui-lnb-menu__container {
    margin-top: 12px;
}
</style>