<template>
    <ui-page-box align-center>

        <ui-container-box :columns=14 vertical class="mt50 mb50">

            <ui-tab box :tabs="tabs" />

            <ui-tab box :tabs="iconTabs" class="mt50"/>

            <ui-tab underline :tabs="tabs" class="mt50"/>

            <ui-tab underline no-action :tabs="iconTabs" class="mt50"/>

            <ui-tab removable :tabs="tabs" class="mt50"/>

            <div class="mt50 ui-tab-lite">
                <div class="ui-tab-lite-item ui-tab-lite-item--selected">Tab_1</div>
                <div class="ui-tab-lite-item">Tab_2</div>
                <div class="ui-tab-lite-item">Tab_3</div>
                <div class="ui-tab-lite-item">Tab_4</div>
            </div>

        </ui-container-box>

    </ui-page-box>

</template>

<script>
export default {
    name: 'tab',
    data() {
        return {
            tabs: [
                { label: "Tab_1",  isSelected: true },
                { label: "Tab_2",  isSelected: false },
                { label: "Tab_3",  isSelected: false },
                { label: "Tab_4",  isSelected: false },
                { label: "Tab_5",  isSelected: false }
            ],
            iconTabs: [
                { label: "Tab_1", icon: "cart", isSelected: true },
                { label: "Tab_2", icon: "cart", isSelected: false },
                { label: "Tab_3", icon: "cart", isSelected: false },
                { label: "Tab_4", icon: "cart", isSelected: false },
                { label: "Tab_5", icon: "cart", isSelected: false }
            ]
        }
    }
}
</script>

<style>
.ui-tab-lite {
    display: flex;
    flex-flow: row nowrap;
}
.ui-tab-lite-item {
    display: flex;
    justify-content: center;
    align-items: center;

    height: 36px;
    width: 92px;

    background-color: white;
    border-radius: 3px;

    font-size: 14px;
}
.ui-tab-lite-item:hover {
    cursor: pointer;
}
.ui-tab-lite-item--selected {
    color: #553CA5;
    font-weight: bold;
    background-color: rgba(85,60,165,0.1);
}
.ui-tab-lite-item + .ui-tab-lite-item {
    margin-left: 8px;
}

</style>