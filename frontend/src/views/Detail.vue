<template>
<ui-container-box :columns="22" vertical align-center class="page-container">

    <ui-container-box :columns="20" horizontal align-center class="page-title">
        <span class="page-title__label">Detail</span>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
        <info></info>
        <notice></notice>
    </ui-container-box>

    <ui-container-box :columns="20" vertical align-center class="page-form-area">
        <search></search>
    </ui-container-box>

    <ui-container-box :columns="20" vertical align-center class="page-form-area">
        <grid-table></grid-table>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal>
        <ui-container-box :columns="10" vertical class="mt20">
            <font size="4">CI-TEC</font>
        </ui-container-box>
        <ui-container-box :columns="3" vertical class="mt20">
            <img src="@/assets/ico_footer.png" alt="Samsung SDS" />
        </ui-container-box>
    </ui-container-box>

</ui-container-box>
</template>

<script>
import Search from '@/components/layout/Search'
import GridTable from '@/components/layout/GridTable'
import Info from '@/components/layout/Info'
import Notice from '@/components/layout/Notice'

export default {
    name: 'Detail',

    // 컴포넌트 등록
    components: {
        'Info': Info,
        'Notice': Notice,
        'Search': Search,
        'GridTable': GridTable,
    },

    methods: {},
}
</script>

<style scoped>
.page-container {
    margin: 48px 80px 32px;
    padding: 80px 80px;
    background-color: white;
}
</style>
