<template>
    <ui-page-box align-center>

        <ui-container-box :columns=24 vertical title="Type - 1 line" class="mt50 mb50">

            <ui-gnb>
                <template v-slot:lead>
                    <ui-gnb-title>
                        <template v-slot:title>SDS Platform</template>
                        <template v-slot:sub>slogan / full name</template>
                    </ui-gnb-title>
                    <ui-gnb-menus :menus="menus" />
                </template>
                <template v-slot:tail>
                    <ui-gnb-icons :icons="['notification','setting']" />
                    <ui-gnb-profile>Gildong Hong</ui-gnb-profile>
                </template>
            </ui-gnb>

            <ui-gnb class="mt50">
                <template v-slot:lead>
                    <ui-gnb-title>
                        <template v-slot:title>SDS Platform</template>
                        <template v-slot:sub>slogan / full name</template>
                    </ui-gnb-title>
                    <ui-gnb-menus :menus="menus" />
                </template>
                <template v-slot:tail>
                    <ui-gnb-item>
                        <lego-button>Button</lego-button>
                    </ui-gnb-item>
                </template>
            </ui-gnb>

            <ui-gnb class="mt50">
                <template v-slot:lead>
                    <ui-gnb-title>
                        <template v-slot:title>SDS Platform</template>
                        <template v-slot:sub>slogan / full name</template>
                    </ui-gnb-title>
                </template>
                <template v-slot:middle>
                    <ui-gnb-menus :menus="menus" />
                </template>
                <template v-slot:tail>
                    <ui-gnb-item>
                        <lego-button>Button</lego-button>
                    </ui-gnb-item>
                </template>
            </ui-gnb>

            <ui-gnb class="mt50">
                <template v-slot:lead>
                    <ui-gnb-title>
                        <template v-slot:title>SDS Platform</template>
                        <template v-slot:sub>slogan / full name</template>
                    </ui-gnb-title>
                </template>
                <template v-slot:tail>
                    <ui-gnb-item>
                        <lego-text-field v-model="textValue" searchable/>
                    </ui-gnb-item>
                    <ui-gnb-profile>Gildong Hong</ui-gnb-profile>
                </template>
            </ui-gnb>

            <ui-gnb class="mt50">
                <template v-slot:lead>
                    <ui-gnb-title>
                        <template v-slot:title>SDS Platform</template>
                        <template v-slot:sub>slogan / full name</template>
                    </ui-gnb-title>
                </template>
                <template v-slot:middle>
                    <ui-gnb-item>
                        <lego-text-field v-model="textValue" searchable/>
                    </ui-gnb-item>
                </template>
                <template v-slot:tail>
                    <ui-gnb-icons :icons="['notification','setting']" />
                    <ui-gnb-profile>Gildong Hong</ui-gnb-profile>
                </template>
            </ui-gnb>

            <ui-gnb class="mt50">
                <template v-slot:lead>
                    <ui-gnb-menus :menus="shortMenus" />
                </template>
                <template v-slot:tail>
                    <ui-gnb-icons :icons="['notification','setting']" />
                    <ui-gnb-profile>Gildong Hong</ui-gnb-profile>
                </template>
            </ui-gnb>

            <ui-gnb class="mt50">
                <template v-slot:lead>
                    <ui-gnb-menus :menus="shortMenus" />
                </template>
                <template v-slot:middle>
                    <ui-gnb-title align-center>
                        <template v-slot:title>SDS Platform</template>
                        <template v-slot:sub>slogan / full name</template>
                    </ui-gnb-title>
                </template>
                <template v-slot:tail>
                    <ui-gnb-item>
                        <lego-button>Button</lego-button>
                    </ui-gnb-item>
                </template>
            </ui-gnb>

            <ui-gnb class="mt50">
                <template v-slot:lead>
                    <lego-icon large >drawer</lego-icon>
                </template>
                <template v-slot:middle>
                    <ui-gnb-title align-center>
                        <template v-slot:title>SDS Platform</template>
                        <template v-slot:sub>slogan / full name</template>
                    </ui-gnb-title>
                </template>
                <template v-slot:tail>
                    <ui-gnb-icons :icons="['notification','setting']" />
                    <ui-gnb-profile>Gildong Hong</ui-gnb-profile>
                </template>
            </ui-gnb>

            <ui-gnb class="mt50">
                <template v-slot:lead>
                    <lego-icon large >drawer</lego-icon>
                </template>
                <template v-slot:middle>
                    <ui-gnb-title align-center>
                        <template v-slot:title>SDS Platform</template>
                        <template v-slot:sub>slogan / full name</template>
                    </ui-gnb-title>
                </template>
                <template v-slot:tail>
                    <ui-gnb-item>
                        <lego-button>Button</lego-button>
                    </ui-gnb-item>
                </template>
            </ui-gnb>

        </ui-container-box>

        <ui-container-box :columns=24 vertical title="Type - 2 line" class="mb50">

            <ui-gnb two-lines>
                <template v-slot:lead>
                    <ui-gnb-title>
                        <template v-slot:title>SDS Platform</template>
                        <template v-slot:sub>slogan / full name</template>
                    </ui-gnb-title>
                </template>
                <template v-slot:middle>
                    <ui-gnb-item>
                        <lego-text-field v-model="textValue" searchable/>
                    </ui-gnb-item>
                </template>
                <template v-slot:tail>
                    <ui-gnb-icons :icons="['notification','setting']" />
                    <ui-gnb-profile>Gildong Hong</ui-gnb-profile>
                </template>

                <template v-slot:second-lead>
                    <ui-gnb-menus :menus="menus" />
                </template>
            </ui-gnb>

            <ui-gnb two-lines class="mt50">
                <template v-slot:lead>
                    <ui-gnb-title>
                        <template v-slot:title>SDS Platform</template>
                        <template v-slot:sub>slogan / full name</template>
                    </ui-gnb-title>
                </template>
                <template v-slot:tail>
                    <ui-gnb-icons :icons="['notification','setting']" />
                    <ui-gnb-profile>Gildong Hong</ui-gnb-profile>
                </template>

                <template v-slot:second-lead>
                    <ui-gnb-menus :menus="menus" />
                </template>
                <template v-slot:second-tail>
                    <ui-gnb-item>
                        <lego-text-field v-model="textValue" searchable/>
                    </ui-gnb-item>
                </template>
            </ui-gnb>

            <ui-gnb two-lines class="mt50">
                <template v-slot:lead>
                    <ui-gnb-title>
                        <template v-slot:title>SDS Platform</template>
                        <template v-slot:sub>slogan / full name</template>
                    </ui-gnb-title>
                </template>
                <template v-slot:tail>
                    <ui-gnb-item>
                        <lego-button>Button</lego-button>
                    </ui-gnb-item>
                </template>

                <template v-slot:second-lead>
                    <ui-gnb-menus :menus="menus" />
                </template>
                <template v-slot:second-tail>
                    <ui-gnb-item>
                        <lego-text-field v-model="textValue" searchable/>
                    </ui-gnb-item>
                </template>
            </ui-gnb>

            <ui-gnb two-lines class="mt50">
                <template v-slot:lead>
                    <ui-gnb-title>
                        <template v-slot:title>SDS Platform</template>
                        <template v-slot:sub>slogan / full name</template>
                    </ui-gnb-title>
                </template>
                <template v-slot:middle>
                    <ui-gnb-item>
                        <lego-text-field v-model="textValue" searchable/>
                    </ui-gnb-item>
                </template>
                <template v-slot:tail>
                    <ui-gnb-icons :icons="['notification','setting']" />
                    <ui-gnb-profile>Gildong Hong</ui-gnb-profile>
                </template>

                <template v-slot:second-middle>
                    <ui-gnb-menus :menus="menus" />
                </template>
            </ui-gnb>

        </ui-container-box>

    </ui-page-box>
</template>

<script>
export default {
    name: 'gnb',
    data() {
        return {
            menus: [
                { label:'Menu1', key:'menu1', isSelected: true },
                { label:'Menu2', key:'menu2', isSelected: false },
                { label:'Menu3', key:'menu3', isSelected: false },
                { label:'Menu4', key:'menu4', isSelected: false },
                { label:'Menu5', key:'menu5', isSelected: false }
            ],
            shortMenus: [
                { label:'Menu1', key:'menu1', isSelected: true },
                { label:'Menu2', key:'menu2', isSelected: false },
                { label:'Menu3', key:'menu3', isSelected: false }
            ],
            textValue: '',
        }
    }
}
</script>