<template>
    <div class="ui-table lego-table"
        :class="[
            { 'ui-table--narrow' : narrow },
            { 'ui-table--expandable' : expandable },
            { 'ui-table--left-header' : leftHeader },
            { 'ui-table--no-bottom-border' : noBottomBorder }
        ]"
    >
        <div v-if="!noInfo || !noAction" class="ui-table-control">
            <div v-if="!noInfo" class="ui-table-control__info">
                <div class="ui-table-control__info-total">
                    <div class="ui-table-control__info-total-label">
                        Total
                    </div>
                    <div class="ui-table-control__info-total-number" >
                        <b>{{items.length}}</b>                                           
                    </div>
                </div>
                <div v-if="pagingInfo" class="ui-table-control__info-size">
                    <lego-dropdown class="lego-table__counter__per-page" 
                        :items="perPageItems" v-model="pagingInfo.rowsPerPage" />
                </div>
                <div class="ui-table-control__info-unit">
                    <slot name="control" />
                </div>
            </div>
            <div v-if="!noAction" class="ui-table-control__action">
                <div v-show="selectedItems.length > 0" class="ui-table-control__action--item-selected">
                    <lego-icon xsmall type="picto">checked</lego-icon>
                    <div class="ui-table-control__action--item-selected-label">
                        {{selectedItems.length}} items selected
                    </div>
                </div>
                <div class="ui-table-control__action-left">
                    <slot name="action-left">
                        <lego-button small>Add</lego-button>
                        <lego-button small>Delete</lego-button>
                        <lego-button small>Modify</lego-button>
                    </slot>
                </div>
                <div class="ui-table-control__action-right">
                    <slot name="action-right">
                        <lego-button small>Download</lego-button>
                        <lego-button small>Print</lego-button>
                        <lego-icon-button small>more</lego-icon-button>
                    </slot>
                </div>
            </div>
        </div>
        <div ref="headerContainer" 
            :class="[
                { 'ui-table-header' : true }
            ]"
        >
            <div v-if="checkable" 
                class="ui-table-header__checkbox">
                <lego-checkbox small v-model="headerChecked"/>
            </div>
            <div class="ui-table-header__list">
                <div 
                    v-for="(column, index) in columns" :key="index" :ref="column.key+'_header'"
                    :class="[
                        { 'ui-table-header__list-item' : true }
                    ]"
                    :style="{ flexBasis: column.width+'%' }"
                >
                    <div :class="[
                            { 'ui-table-header__list-item-title' : true },
                            { 'ui-table-header__list-item-title--divider' : headerDivider && index+1 < columns.length },
                            { 'ui-table-header__list-item-title--right' : column.alignRight },
                            { 'ui-table-header__list-item-title--center' : column.alignCenter}
                        ]"
                    >
                        <div class="ui-table-header__list-item-label">
                            {{column.label}}
                        </div>
                        <div v-if="column.sortable || column.filtable" @click="clickHeaderIcon(column, column.key+'_header')"
                            class="ui-table-header__list-item-icon">
                            <lego-icon v-if="column.sortable && column.filtable" 
                                small spacing type="picto">filter_sort</lego-icon>
                            <lego-icon v-else-if="column.filtable" 
                                small spacing type="picto">filter</lego-icon>
                            <lego-icon v-else-if="column.sortable" 
                                small spacing type="picto">sort</lego-icon>
                        </div>
                    </div>
                    <div v-if="headerFilter" class="ui-table-header__list-item-filter">
                        <lego-text-field small />
                    </div>
                </div>
            </div>
        </div>
        <div class="ui-table-body">
            <!-- log detail popup -->
            <component :is="currentView" :logLine="logLine" v-on:popupClose="currentView=null"></component>
            
            <div class="ui-table-body__list">
                    
                <div v-for="group in groups" class="ui-table-body__list-group" :key="group.key" >

                    <div v-if="group.key != '_default'" @click="toggleGroupOpen(group)"
                        class="ui-table-body__list-group-item"
                    >
                        <div class="ui-table-body__list-group-label">
                            {{group.label}}
                        </div>
                        <div class="ui-table-body__list-group-icon">
                            <lego-icon v-if="group.isOpened" xsmall spacing>arrow_up</lego-icon>
                            <lego-icon v-else xsmall spacing>arrow_down</lego-icon>
                        </div>
                    </div>

                    <div v-for="(item, index) in grouppedItems(group)" :key="group.key+index"
                        :class="[
                            { 'ui-table-body__list-item' : true},
                            { 'ui-table-body__list-item--selected' : item.isSelected }
                        ]"
                        @click="toggleCellEdit(item)"
                    >
                        <div class="ui-tabl-body__list-item-main">
                            <div v-if="checkable"
                                class="ui-table-body__list-item-checkbox"
                            >
                                <lego-checkbox small v-model="item.isSelected"/>
                            </div>
                            
                            <div class="ui-table-body__list-item-cells">
                                <div v-for="column in columns" :key="column.key+group.key+index"
                                    :class="[
                                        { 'ui-table-body__list-item-cell' : true },
                                        { 'ui-table-body__list-item-cell--right' : column.alignRight },
                                        { 'ui-table-body__list-item-cell--center' : column.alignCenter}
                                    ]"
                                    :style="{ flexBasis: column.width+'%' }"
                                >
                                    <div class="ui-table-body__list-item-cell__content" v-on:click="selectedRow(item)">
                                        <slot v-if="editingItem === item" :name="'celledit-'+column.key" :item="item" >
                                            {{item[column.key]}}
                                        </slot>
                                        <slot v-else :name="'cellview-'+column.key" :item="item">
                                            {{item[column.key]}}
                                        </slot>
                                    </div>
                                </div>
                            </div>
                            <div v-if="expandable"
                                :class="[
                                    { 'ui-table-body__list-item-expand-icon' : true },
                                    { 'ui-table-body__list-item-expand-icon--expanded' : expandingItem === item },
                                ]"
                                @click="toggleRowExpand(item)"
                            >
                                <lego-icon v-if="expandingItem === item" xsmall type="picto">expand_menu</lego-icon>
                                <lego-icon v-else xsmall type="picto">collapse_menu</lego-icon>
                            </div>
                        </div>
                        <div v-if="expandingItem === item" class="ui-tabl-body__list-item-expand">
                            <slot name="expand" :item="item">
                                Expand Content
                            </slot>
                        </div>
                    </div>

                </div>

            </div>
        </div>

        <div class="ui-table-summary">
            <slot name="summary" />
        </div>

        <div v-if="pagingInfo && !noPaging" class="ui-table-pagination">
            <lego-pagination :pagination="pagingInfo" @move="pageChange" @change="pageChange"  />
        </div>

        <div v-show="headerToolColumn" class="ui-table-tool"
            :style="[{ top: headerToolTop + 'px' },{ left: headerToolLeft + 'px' }]"
        >
            <div v-if="headerToolColumn && headerToolColumn.sortable" class="ui-table-tool__sort">
                <lego-radio v-model="headerToolColumn.sortValue" value="asc" small>Sort Ascending</lego-radio>
                <lego-radio v-model="headerToolColumn.sortValue" value="desc" small>Sort Descending</lego-radio>
            </div>
            <div v-if="headerToolColumn && headerToolColumn.filtable" class="ui-table-tool__filter">
                <lego-checkbox v-for="(filterItem, index) in headerToolColumn.filterList" :key="index"
                    :value="filterItem" v-model="headerToolColumn.filterValue" small>{{filterItem}}</lego-checkbox>
            </div>
        </div>
        
    </div>

</template>

<script>
import CommonPopup from '../CommonPopup';
import store from '@/vuex/store';

export default {
    name: 'ui-table',
    components: { 
      CommonPopup, 
    },
    props: {
        perPageItems : { type: Array, default: function() {
            return [
                {text: '10 Per page', value: 10},
                {text: '20 Per page', value: 20},
                {text: '30 Per page', value: 30}
            ]}
        },
        pagingInfo : { type: Object, default: undefined },
        columns: { type: Array, default: function() {
            return [];
        }},
        groups: { type: Array, default: function() {
            return [ {
                key: '_default', isOpened: true
            } ];
        }},
        items: { type: Array, default: function() {
            return [];
        }},
        checkable: { type: Boolean, default: false },
        headerDivider : { type: Boolean, default: false },
        narrow: { type: Boolean, default: false },
        editable: { type: Boolean, default: false },
        noAction: { type: Boolean, default: false },
        noPaging: { type: Boolean, default: false },
        noInfo: { type: Boolean, default: false },
        expandable: { type: Boolean, default: false },
        headerFilter: { type: Boolean, default: false },
        leftHeader: { type: Boolean, default: false },
        noBottomBorder: { type: Boolean, default: false },
    },
    data() {
        return {
            unit: 'KRW',
            headerChecked: false,

            headerToolColumn: null,
            headerToolTop: 0,
            headerToolLeft: 0,

            editingItem: null,
            expandingItem: null,

            currentView : null,
            logLine: '',
        }
    },
    computed: {
        selectedItems() {
            return this.items.filter(item => item.isSelected);
        }
    },
    watch: {
        headerChecked: function (newChecked, oldChecked) {
            this.items.forEach(item => {
                item.isSelected = newChecked;
            });
        }
    },
    methods: {
        
        // Leehs
        pageChange(page) {
            this.pagingInfo.currentPage = page
        },

        selectedRow(item){
  
            var selectedCount = 0
            for(let i = 0 ; i< this.items.length; i++){
                if ( this.items[i].isSelected == true ){
                    selectedCount++
                }
            }
            if (selectedCount == 0){
                 item.isSelected == true ? item.isSelected = false : item.isSelected = true
                //  this.$store.dispatch("setToggleSearch");
            }else if (selectedCount == 1 && item.isSelected == true){                
                item.isSelected == true ? item.isSelected = false : item.isSelected = true
            }else {
                item.isSelected = false
            }

            //console.log('item : ', item)

            // TODO : project_id 등 설정 필요 - vuex 사용
            //console.log('item : ', item.projectID)
            //console.log('item : ', item.projectName)
            //console.log('item : ', item.projectDescription)
            //console.log('item : ', item.logline)            
            //console.log('item.viewname : ', item.viewname) 
            // log detail table에서만 Popup 생성
            if( item.viewname == 'detail'){
                //this.$alert(item.logline, "Access Log", "info");
                //this.$store.state.popupLog = item.logline;
                this.logLine = item.logline;
                this.currentView = 'CommonPopup';
            }else {              
                this.$store.dispatch("setProjectName", item.projectName);
                this.$store.dispatch("setProjectDescription", item.projectDescription);
                this.$store.dispatch("setProjectID", item.projectID);
            }
        },

        clickHeaderIcon(column, refId) {
            if (this.headerToolColumn === column) {
                this.headerToolColumn = null;
            } else {
                this.headerToolColumn = column;

                let left = this.$refs[refId][0].offsetLeft;
                let top = this.$refs.headerContainer.offsetTop;
                top += this.$refs.headerContainer.offsetHeight;

                this.headerToolLeft = left;
                this.headerToolTop = top;
            }
        },
        toggleCellEdit(item) {
            if(this.editable) this.editingItem = item;
        },
        toggleRowExpand(item) {
            if (this.expandingItem === item) {
                this.expandingItem = null;
            } else {
                this.expandingItem = item;
            }
        },
        grouppedItems(group) {
            if (group.key === '_default') return this.items;
            else if (group.isOpened) return this.items.filter(item => item.groupKey === group.key);
            else return null;
        },
        toggleGroupOpen(group) {
            group.isOpened = !group.isOpened;
        }
    }
}
</script>

<style>
.ui-table {
    overflow: hidden;
    width: 100%;
}
.ui-table,
.ui-table-control {
    display: flex;
    flex-flow: column nowrap;
}
.ui-table-control__info,
.ui-table-control__info-total,
.ui-table-control__info-size,
.ui-table-control__info-unit,
.ui-table-control__action,
.ui-table-control__action-right,
.ui-table-control__action--item-selected {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
}
.ui-table-control__info-total-label {
    margin-right: 4px;
}
.ui-table-control__info-total-number {
    margin-right: 4px;
}
.ui-table-control__info-total + .ui-table-control__info-size::before {
    display:block;
    content:' ';
    width: 1px;
    height: 14px;
    background-color: #A5A5A5;
}
.ui-table-control__info-unit {
    margin-left: auto;
}
.ui-table-control__info-unit-label {
    margin-right: 4px;
}
.ui-table-control__action--item-selected {
    color: #553CA5;
    padding-right: 16px;
}
.ui-table-control__action--item-selected-label {
    margin-left: 16px;
}
.ui-table-control__action-right {
    margin-left: auto;
}

.ui-table-control__info + .ui-table-control__action {
    margin-top: 16px;
}
.ui-table-control + .ui-table-header {
    margin-top: 16px;
}

.ui-table-header,
.ui-table-header__checkbox,
.ui-table-header__list,
.ui-table-header__list-item,
.ui-table-header__list-item-label,
.ui-table-header__list-item-icon {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
}
.ui-table-header {
    border-top: 1px solid #EAEAEA;
    border-bottom: 1px solid #A5A5A5;
}
.ui-table-header__list {
    flex-grow: 1;
}
.ui-table-header__list-item {
    flex-flow: column nowrap;
    padding: 16px;
}
.ui-table-header__list-item-title {
    display: flex;
    flex-flow: row nowrap;
    align-self: stretch;
}
.ui-table-header__list-item-title--divider {
    border-right: 1px solid #A5A5A5;
}
.ui-table-header__list-item-title--right {
    justify-content: flex-end;
}
.ui-table-header__list-item-title--center {
    justify-content: center;
}
.ui-table-header__list-item-icon {
    color: #A5A5A5;
}
.ui-table-header__list-item-icon:hover {
    cursor: pointer;
}
.ui-table-header__checkbox {
    padding: 16px 0 16px 32px;
}
.ui-table-header__list-item-label + .ui-table-header__list-item-icon {
    margin-left: 4px;
}
.ui-table-header__list-item-filter {
    display: flex;
    align-self: stretch;
    margin-top: 4px;
}
.ui-table--narrow .ui-table-header {
    background-color: #F7F7F7;
}
.ui-table--left-header .ui-table-header {
    font-weight: bold;
    background-color: #F7F7F7;
}
.ui-table--narrow .ui-table-header__list-item {
    padding: 4px 16px 4px 16px;
    font-size: 12px;
}
.ui-table--narrow .ui-table-header__checkbox {
    padding: 4px 0 4px 32px;
}
.ui-table--expandable .ui-table-header__list {
    margin-right: 38px;
}

.ui-table-body,
.ui-table-body__list,
.ui-table-body__list-group,
.ui-table-body__list-item {
    display: flex;
    flex-flow: column nowrap;
}
.ui-table-body {
    flex-grow: 1;
    border-bottom: 1px solid #CCCCCC;
}
.ui-table--no-bottom-border .ui-table-body{
    border-bottom: none;
}
.ui-table-body__list-group-item,
.ui-tabl-body__list-item-main,
.ui-table-body__list-item-checkbox {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
}
.ui-table-body__list-group-item {
    background-color: #F7F7F7;
}
.ui-table-body__list-group-item:hover {
    cursor: pointer;
}
.ui-table-body__list-group-label {
    font-size: 12px;
    padding: 6px 0px 6px 32px;
}
.ui-table-body__list-group-icon {
    margin-left: auto;
    padding: 6px 32px 6px 0px;
}
.ui-table-body__list-item-checkbox {
    padding-left: 32px;
}
.ui-table-body__list-item--selected {
    color: #553CA5 !important;
    background-color: #F3F1F9 !important;
    font-weight: bold;
}
.ui-table-body__list-item-cells,
.ui-table-body__list-item-cell {
    display: flex;
    align-items: center;
    flex: 1 1 auto;
}
.ui-table-body__list-item-cell {
    height: 48px;
    padding: 0 16px;
}
.ui-table-body__list-item-cell--right {
    justify-content: flex-end;
}
.ui-table-body__list-item-cell--center {
    justify-content: center;
}
.ui-table-body__list-item + .ui-table-body__list-item {
    border-top: 1px solid #FFFFFF;
}
.ui-table--narrow .ui-table-body__list-item-cell {
    height: 40px;
    font-size: 12px;
}
.ui-table--narrow .ui-table-body__list-item:nth-child(2n) {
    background-color: #F7F7F7;
}
.ui-table--left-header .ui-table-body__list-item + .ui-table-body__list-item {
    border-top: 1px solid #F7F7F7;
}
.ui-table--left-header .ui-table-body__list-item-cell {
    border-left: 1px solid #F7F7F7;
}
.ui-table--left-header .ui-table-body__list-item-cell:first-child {
    background-color: #F7F7F7;
}
.ui-table-body__list-item-expand-icon {
    cursor: pointer;
    display: flex;
    align-items: center;
    margin-right: 24px;
    color: #CCCCCC;
}
.ui-table-body__list-item-expand-icon--expanded {
    color: #333333;
}
.ui-tabl-body__list-item-expand {
    background-color: #F7F7F7;
    padding: 16px 24px;
}

.ui-table-summary + .ui-table-pagination {
    margin-top: 24px;
}

.ui-table-tool,
.ui-table-tool__sort,
.ui-table-tool__filter {
    display: flex;
    flex-flow: column nowrap;
}
.ui-table-tool {
    position: absolute;
    background-color: white;
    padding: 0 12px;
    min-width: 200px;

    border: 1px solid #959595;
}
.ui-table-tool__sort,
.ui-table-tool__filter {
    padding: 12px 0;
}
.ui-table-tool .lego-radio + .lego-radio,
.ui-table-tool .lego-checkbox + .lego-checkbox {
    margin-left: 0px;
    margin-top: 12px;
}
.ui-table-tool__sort + .ui-table-tool__filter {
    border-top: 1px solid #F7F7F7;
}

.ui-table .lego-checkbox {
    background-color: white;
}
</style>
