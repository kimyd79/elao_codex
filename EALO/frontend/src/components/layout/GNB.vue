<template>
  <div id="GNB">
    {{ msg }}
    <br />
    <router-link to="/Menu1">Menu1</router-link>
    <router-link to="/Menu2">Menu2</router-link>
    <router-link to="/Menu3">Menu3</router-link>
    <br />
    <b>------------------------------------------</b>
    <router-view></router-view>
    <!-- 여기에 들어가면 안됨
    <router-view name="Info"></router-view> 
     -->
  </div>
</template>

<script>
export default {
  name: "GNB",
  data() {
    return {
      msg: "This page is GNB"
    };
  }
};
</script>

<style scoped></style>
