import UIPageBox from "./box/UIPageBox.vue";
import UIContainerBox from "./box/UIContainerBox.vue";

import UICard from "./card/UICard.vue";
import UICardItem from "./card/UICardItem.vue";

import UIFormBox from "./form/UIFormBox.vue";
import UIFormRow from "./form/UIFormRow.vue";
import UIFormButtons from "./form/UIFormButtons.vue";
import UIFormItem from "./form/UIFormItem.vue";

import UIGNB from "./gnb/UIGNB.vue"
import UIGNBTitle from "./gnb/UIGNBTitle.vue"
import UIGNBMenus from "./gnb/UIGNBMenus.vue"
import UIGNBIcons from "./gnb/UIGNBIcons.vue"
import UIGNBProfile from "./gnb/UIGNBProfile.vue"
import UIGNBItem from "./gnb/UIGNBItem.vue"

import UIList from "./list/UIList.vue";
import UIListItem from "./list/UIListItem.vue";
import UIListThumbnail from "./list/UIListThumbnail.vue"
import UIListFile from "./list/UIListFile.vue"
import UIListContainer from "./list/UIListContainer.vue"
import UIListGroup from "./list/UIListGroup.vue"

import UILNB from "./lnb/UILNB.vue"
import UILNBMenus from "./lnb/UILNBMenus.vue"
import UILNBItem from "./lnb/UILNBItem.vue"
import UILNBLite from "./lnb/UILNBLite.vue"
import UILNBLiteItem from "./lnb/UILNBLiteItem.vue"

import UIStep from "./step/UIStep.vue"
import UIValidationStep from "./step/UIValidationStep.vue"

import UITab from "./tab/UITab.vue"

import UITable from "./table/UITable.vue"

// LogAnalyzer
import GNB from "./GNB.vue"
import Graph from "./Graph.vue"
import GridTable from "./GridTable.vue"
import Info from "./Info.vue"
import Init from "./Init.vue"
import Notice from "./Notice.vue"
import Search from "./Search.vue"
import Statistics from "./Statistics.vue"

export default {
    install(Vue){

        // LogAnalyzer
        Vue.component(GNB.name, GNB);
        Vue.component(Graph.name, Graph);
        Vue.component(GridTable.name, GridTable);
        Vue.component(Info.name, Info);
        Vue.component(Init.name, Init);
        Vue.component(Notice.name, Notice);
        Vue.component(Search.name, Search);
        Vue.component(Statistics.name, Statistics);


        Vue.component(UIPageBox.name, UIPageBox);
        Vue.component(UIContainerBox.name, UIContainerBox);

        Vue.component(UICard.name, UICard);
        Vue.component(UICardItem.name, UICardItem);

        Vue.component(UIFormBox.name, UIFormBox);
        Vue.component(UIFormRow.name, UIFormRow);
        Vue.component(UIFormButtons.name, UIFormButtons);
        Vue.component(UIFormItem.name, UIFormItem);

        Vue.component(UIGNB.name, UIGNB);
        Vue.component(UIGNBTitle.name, UIGNBTitle);
        Vue.component(UIGNBMenus.name, UIGNBMenus);
        Vue.component(UIGNBIcons.name, UIGNBIcons);
        Vue.component(UIGNBProfile.name, UIGNBProfile);
        Vue.component(UIGNBItem.name, UIGNBItem);

        Vue.component(UIList.name, UIList);
        Vue.component(UIListItem.name, UIListItem);
        Vue.component(UIListThumbnail.name, UIListThumbnail);
        Vue.component(UIListFile.name, UIListFile);
        Vue.component(UIListContainer.name, UIListContainer);
        Vue.component(UIListGroup.name, UIListGroup);

        Vue.component(UILNB.name, UILNB);
        Vue.component(UILNBMenus.name, UILNBMenus);
        Vue.component(UILNBItem.name, UILNBItem);
        Vue.component(UILNBLite.name, UILNBLite);
        Vue.component(UILNBLiteItem.name, UILNBLiteItem);

        Vue.component(UIStep.name, UIStep);
        Vue.component(UIValidationStep.name, UIValidationStep);

        Vue.component(UITab.name, UITab);

        Vue.component(UITable.name, UITable);
    }
};