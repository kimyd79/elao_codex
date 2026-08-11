<template>

    <Page title="Screen without LNB - Stack 01" class="mg-auto">

        <ui-container-box :columns=22 vertical class="mt32">

            <ui-tab box :tabs="tabs" no-action />

        </ui-container-box>

        <ui-container-box :columns=22 vertical class="page-body-area">

            <div class="page-title">
                <span class="page-title__label">Lorem Ipsum</span>
                <span class="page-title__search">
                    <lego-text-field searchable placeholder="Search" />
                </span>
            </div>

            <div class="ui-v-header">
                <div class="ui-v-header__category">
                    <div class="ui-v-header__category-label">
                        News&amp;Event
                    </div>
                    <div class="ui-v-header__category-bookmark">
                        <lego-icon xsmall type="picto">bookmark</lego-icon>
                    </div>
                </div>
                <div class="ui-v-header__title">
                    HPC Managed Services - End-to-end managed high <br>
                    performancecomputing services and solutions 
                </div>
                <div class="ui-v-header__info">
                    <div class="ui-v-header__info-item">
                        <div class="ui-v-header__info-item__label">
                            Writer
                        </div>
                        <div class="ui-v-header__info-item__content">
                            Writer Name
                        </div>
                    </div>
                    <div class="ui-v-header__info-item">
                        <div class="ui-v-header__info-item__label">
                            Upload Time
                        </div>
                        <div class="ui-v-header__info-item__content">
                            2020.04.25  00:00
                        </div>
                    </div>
                    <div class="ui-v-header__info-item">
                        <div class="ui-v-header__info-item__label">
                            <lego-icon>hits</lego-icon>
                        </div>
                        <div class="ui-v-header__info-item__content">
                            184
                        </div>
                    </div>
                    <div class="ui-v-header__info-action">
                        <lego-button small>Edit</lego-button>
                        <lego-button small>Delete</lego-button>
                    </div>
                </div>
            </div>

            <div class="ui-v-body">
                <div class="ui-v-body-content">
                    <strong>Build, manage, and grow your HPC infrastructure</strong> <br>
                    As convention centers continue to innovate and augment their facilities with leading-edge technology, they look for ways to optimize their exhibition halls and meetings rooms with intelligent digitalization technology to provide not only a better customer experience but also opportunity to maximize revenue for every show.
                    <br><br>
                    Convention center business leaders need to understand what technology is available as well as how to implement to create a living, breathing space that visitors will want to keep coming back to. Value added services are increasingly more essential as convention centers face cost and competitive pressures to renovate and keep up with current technology year after year.
                    <br><br>
                    We would like to invite you to join us for a dynamic webinar on March 19th at 2pm ET/11am PT when we’ll cover:
                    <br><br>
                    Understanding digital signage’s role in supporting user friendly dynamic infotainment<br>
                    Geolocation wayfinding to provide optimal traffic routes for show attendees<br>
                    Leveraging smart ad sales to optimally manage advertisements and increase ROI<br>
                    Hear from industry players on how they are innovating to stay competitive<br>
                    <br><br>
                    We will be featuring a panel of executive level convention center leaders to understand how they plan to implement digital technology to enhance the user experience and ROI of their shows.
                </div>
                <div class="ui-v-body-attachment">
                    <div class="ui-v-body-label">
                        Attachment
                    </div>
                    <div class="ui-v-body-attachment__list">
                        <div class="ui-v-body-attachment__list-item">
                            <div class="ui-v-body-attachment__list-item-name">
                                2019.03.04  Samsung SDS HPC infrastructure.pdf
                            </div>
                            <div class="ui-v-body-attachment__list-item-icon">
                                <lego-icon small spacing>download</lego-icon>
                            </div>
                        </div>
                        <div class="ui-v-body-attachment__list-item">
                            <div class="ui-v-body-attachment__list-item-name">
                                2019.03.04  Samsung SDS HPC infrastructure.pdf
                            </div>
                            <div class="ui-v-body-attachment__list-item-icon">
                                <lego-icon small spacing>download</lego-icon>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="ui-v-body-keyword">
                    <div class="ui-v-body-label">
                        Keyword
                    </div>
                    <div class="ui-v-body-items">
                        <lego-chip small>hpc</lego-chip>
                        <lego-chip small>SDS</lego-chip>
                        <lego-chip small>CX</lego-chip>
                    </div>
                </div>
            </div>

            <div class="ui-v-page-nav">
                <div class="ui-v-page-nav-item">
                    <div class="ui-v-page-nav-item__direction">
                        <div class="ui-v-page-nav-item__direction-icon">
                            <lego-icon small spacing>arrow_up</lego-icon>
                        </div>
                        <div class="ui-v-page-nav-item__direction-label">
                            다음
                        </div>
                    </div>
                    <div class="ui-v-page-nav-item__category">
                        News&amp;Event
                    </div>
                    <div class="ui-v-page-nav-item__title">
                        The one-stop service for HPC Managed Services
                    </div>
                    <div class="ui-v-page-nav-item__date">
                        2019 - 02- 02
                    </div>
                </div>
                <div class="ui-v-page-nav-item">
                    <div class="ui-v-page-nav-item__direction">
                        <div class="ui-v-page-nav-item__direction-icon">
                            <lego-icon small spacing>arrow_down</lego-icon>
                        </div>
                        <div class="ui-v-page-nav-item__direction-label">
                            이전
                        </div>
                    </div>
                    <div class="ui-v-page-nav-item__category">
                        Presentation
                    </div>
                    <div class="ui-v-page-nav-item__title">
                        Cost-effectively expand or outsource your HPC infrastructure
                    </div>
                    <div class="ui-v-page-nav-item__date">
                        2019 - 02- 01
                    </div>
                </div>
            </div>

            <div class="page-buttons">
                <lego-button large>List</lego-button>
            </div>

        </ui-container-box>

    </Page>

</template>

<script>
import Page from '../_Frame/Page'

export default {
    name: 'stack-01',
    components: {
        Page
    },
    data: function() {
        return {
            value: 'A',
            dateValue: '',
            segmentValue: '2',
            radioValue: '1',
            textValue: '',
            checkValue: false,
            tabs: [
                { label: "Tab_1",  isSelected: true },
                { label: "Tab_2",  isSelected: false },
                { label: "Tab_3",  isSelected: false },
                { label: "Tab_4",  isSelected: false }
            ],
        }
    }
}
</script>

<style scoped>
.page-body-area {
    padding: 48px 80px;
    background-color: white;
}
.page-title {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
    justify-content: space-between;
    
    padding-bottom: 18px;
    border-bottom: 1px solid #CCCCCC;
}
.page-title__label {
    font-size: 24px;
    font-weight: bold;
}
.page-title__search {
    width: 208px;
}
.page-buttons {
    display: flex;
    flex-flow: row nowrap;
    justify-content: flex-end;

    margin-top: 24px;
}

.ui-v-header {
    display: flex;
    flex-flow: column nowrap;

    padding: 24px 48px;
    background-color: white;
}
.ui-v-header__category {
    color: #047AD5;

    display: flex;
    flex-flow: row nowrap;
    justify-content: flex-start;
    align-items: center;
}
.ui-v-header__category-label {
    font-size: 14px;
}
.ui-v-header__category-bookmark {
    margin-left: auto;
}
.ui-v-header__title {
    color: #333333;
    font-size: 24px;
    font-weight: bold;
}
.ui-v-header__info {
    display: flex;
    flex-flow: row nowrap;
    justify-content: flex-start;
    align-items: center;
}
.ui-v-header__info-item {
    display: flex;
    flex-flow: row nowrap;

    font-size: 14px;
}
.ui-v-header__info-item__label {
    color: #767676;

    display: flex;
    align-items: center;
}
.ui-v-header__info-action {
    margin-left: auto;
}

.ui-v-header__info-item__label + .ui-v-header__info-item__content {
    margin-left: 8px;
}

.ui-v-header__category + .ui-v-header__title {
    margin-top: 14px;
}
.ui-v-header__title + .ui-v-header__info {
    margin-top: 14px;
}
.ui-v-header__info-item + .ui-v-header__info-item::before {
    content: "|";
    margin: 0 16px;
    font-size: 12px;
}


.ui-v-body {
    display: flex;
    flex-flow: column nowrap;

    padding: 32px 48px;
    background-color: white;
}
.ui-v-body-content {
    font-size: 14px;
    line-height: 24px;
}
.ui-v-body-label {
    font-size: 14px;
    margin-bottom: 8px;
}
.ui-v-body-attachment {
    display: flex;
    flex-flow: column nowrap;
}
.ui-v-body-attachment__list {
    display: flex;
    flex-flow: row nowrap;
}
.ui-v-body-attachment__list-item {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;

    border: 1px solid #CCCCCC;
    padding: 8px 16px;
    width: 352px;
}
.ui-v-body-attachment__list-item:hover {
    background-color: #F7F7F7;
    cursor: pointer;
}
.ui-v-body-attachment__list-item-name {
    font-size: 12px;
    color: #5A5A5A;
    border-right: 1px solid #CCCCCC;

    display: flex;
    flex: 1 0 auto;
}
.ui-v-body-attachment__list-item-icon {
    margin-left: 12px;

    display: flex;
    align-items: center;
    justify-content: center;
}
.ui-v-body-keyword {
    margin-top: 16px;
}

.ui-v-body-content + .ui-v-body-attachment {
    margin-top: 68px;
}
.ui-v-body-attachment__list-item + .ui-v-body-attachment__list-item {
    margin-left: 4px;
}


.ui-v-page-nav {
    display: flex;
    flex-flow: column nowrap;
    background-color: white;

    border-bottom: 1px solid #CCCCCC;
}
.ui-v-page-nav-item {
    display: flex;
    flex-flow: row nowrap;
    justify-content: flex-start;
    align-items: center;

    padding: 8px 48px;;
}
.ui-v-page-nav-item + .ui-v-page-nav-item {
    border-top: 1px solid #EAEAEA;
}
.ui-v-page-nav-item:hover {
    background-color: #F7F7F7;
    cursor: pointer;
}
.ui-v-page-nav-item__direction {
    display: flex;
    flex-flow: row nowrap;

    color: #767676;
}
.ui-v-page-nav-item__direction-icon {
    display: flex;
    align-items: center;
}
.ui-v-page-nav-item__direction-label {
    font-size: 14px;
}
.ui-v-page-nav-item__direction-icon + .ui-v-page-nav-item__direction-label {
    margin-left: 4px;
}
.ui-v-page-nav-item__category {
    font-size: 12px;
    color: #767676;
}
.ui-v-page-nav-item__title {
    font-size: 14px;
}
.ui-v-page-nav-item:hover .ui-v-page-nav-item__title {
    font-weight: bold;
}
.ui-v-page-nav-item__date {
    margin-left: auto;
    font-size: 13px;
    color: #767676;
}

.ui-v-page-nav-item__direction + .ui-v-page-nav-item__category {
    margin-left: 24px;
}
.ui-v-page-nav-item__category + .ui-v-page-nav-item__title {
    margin-left: 36px;
}


.ui-v-header + .ui-v-body {
    border-top: 1px solid #CCCCCC;
}
.ui-v-body + .ui-v-page-nav {
    border-top: 1px solid #CCCCCC;
}
</style>