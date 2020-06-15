<template>
    <ui-page-box align-center>

        <ui-container-box :columns=11 vertical class="mt50 mb50">

            <ui-container-box title="Single line" :columns=11 vertical>

                <ui-list v-for="(item, index) in list1" :key="index"
                    expandable :class="{ 'mt8' : index > 0 }"
                >
                    <ui-list-item header>{{item.title}}</ui-list-item>
                    <template v-slot:expand>
                        <div class="m24">{{item.content}}</div>
                    </template>
                </ui-list>

            </ui-container-box>

            <ui-container-box title="Multi line" :columns=11 class="mt50">

                <ui-list v-for="(item, index) in list2" :key="index"
                    expandable :selected="item.isChecked" :class="{ 'mt8' : index > 0 }"
                >
                    <template v-slot:control>
                        <lego-checkbox v-model="item.isChecked" />
                    </template>
                    <ui-list-item box>
                        <div>
                            <b>{{item.name}}</b> <br>
                            {{item.level}}
                        </div>
                        <div>
                            {{item.company}} <br>
                            {{item.division}}
                        </div>
                        <div>
                            {{item.eventdate}}
                        </div>
                        <div>
                            {{item.status}}
                        </div>
                    </ui-list-item>
                    <template v-slot:expand>
                        <ui-form-row>
                            <ui-form-item :columns=10 label="Location" left-label>
                                {{item.location}}
                            </ui-form-item>
                        </ui-form-row>

                        <ui-form-row>
                            <ui-form-item :columns=10 label="Event Date/Time" left-label>
                                {{item.eventtime}}
                            </ui-form-item>
                        </ui-form-row>

                        <ui-form-row>
                            <ui-form-item :columns=10 label="Shipper" left-label>
                                {{item.shipper}}
                            </ui-form-item>
                        </ui-form-row>

                        <ui-form-row>
                            <ui-form-item :columns=10 label="Total Loss" left-label>
                                {{item.totalloss}}
                            </ui-form-item>
                        </ui-form-row>

                        <ui-form-row>
                            <ui-form-item :columns=10 label="Event Outline" left-label>
                                {{item.outline}}
                            </ui-form-item>
                        </ui-form-row>

                        <ui-form-row>
                            <ui-form-item :columns=10 label="Event Handling" left-label>
                                {{item.handling}}
                            </ui-form-item>
                        </ui-form-row>
                        
                        <ui-form-buttons divider>
                            <lego-button main>BUTTON</lego-button>
                        </ui-form-buttons>
                    </template>
                </ui-list>

            </ui-container-box>

        </ui-container-box>

    </ui-page-box>
</template>

<script>
export default {
  name: 'accordion',
  data: function() {
      return {
          list1: [],
          list2: [],
          checkValue: false,
      }
  },
  created: function() {
      for(var i = 0; i < 5; i++){
          this.list1.push({
            title: "Samsung SDS UX Design System",
            content: 
`Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna
aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
magna aliqua.`,
            isExpend: false
          });
      }

      for(var j = 0; j < 5; j++){
          this.list2.push({
            isChecked: false,
            name: "HONG KIL-DONG",
            level: "Senior staff / Solution Group",
            company: "Samsung SDS",
            division: "User Experience Design",
            eventdate: "2018-08-01 ~ 2021-07-30",
            status: "Confirm",
            location: "Dallas TX.",
            eventtime: "10/4 ~ 10/5",
            shipper: "SAMSUNG ELECTRONIC (SEA)",
            totalloss: "$ 130,320.24 USD",
            outline: 
`Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna
aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
magna aliqua.`,
            handling: "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
            isExpend: false
          });
      }
  }
}
</script>