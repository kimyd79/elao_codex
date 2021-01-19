<template>
  <div>
      <ui-gnb style="position: absolute; width: 100%; z-index:999;">
          <template v-slot:lead>
              <ui-gnb-menus :menus="menus">
                <template v-slot="{ menu }" >
                  <div class="template-type">
                    <div class="template-type__label">{{menu.label}}</div>
                    <div class="template-type__menus">
                      <router-link v-for="item in menu.menus" 
                        :key="item.key" :to="item.linkto"
                        :class="[
                          { 'template-type__menus-item' : true },
                          { 'template-type__menus-item--selected' : item.isSelected }
                        ]"
                      >
                        {{item.label}}
                      </router-link>
                    </div>
                  </div>
                </template>
              </ui-gnb-menus>
          </template>
      </ui-gnb>
      
      <router-view class="pt80 pb80" />

  </div>
</template>

<script>
export default {
    data() {
        return {
            menus: [
                { 
                  label: 'Setting' ,
                  menus: [
                    { label:'LogFormat', linkto:'/logformat', key:'logformat', isSelected: false },
                    { label:'Project', linkto:'/project', key:'project', isSelected: false }, 
                    { label:'Metrics', linkto:'/metrics', key:'metrics', isSelected: false },                   
                  ]
                },
                
                { 
                  label: 'User' ,
                  menus: [
                    { label:'Register', linkto:'/register', key:'register', isSelected: false },
                    { label:'LogIn', linkto:'/login', key:'login', isSelected: false }, 
                    { label:'LogOut', linkto:'/logout', key:'logout', isSelected: false },                             
                  ]
                },

            ]
        }
    },
    watch: {
      '$route' (to, from) {
        this.menus.forEach(function(menu){
          menu.menus.forEach(function(item){
            item.isSelected = (to.path.includes(item.linkto));
          })
        })
      }
    }
}
</script>

<style lang="scss" scoped>
.template-type {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}
.template-type__menus {
  position: absolute;
  display: none;
  top: 70px;
  left: 0;
  width: 200px;

  flex-flow: column nowrap;
  background-color: white;
  border: 1px solid #CCCCCC;
}
.template-type:hover .template-type__menus {
  display: flex;
}
.template-type__menus-item {
  padding: 16px 24px;
}
.template-type__menus-item:hover {
  cursor: pointer;
  background-color: #F7F7F7;
}
.template-type__menus-item--selected {
  background: #F7F5FB;
  font-weight: bold;
  color: #553CA5;
}

</style>
