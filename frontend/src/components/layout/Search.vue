<template>
  <div id="search">
    <ui-form-box>
      <ui-form-row>
        <ui-form-item :columns="6" label="Lorem Ipsum">
          <lego-dropdown :items="[{value: 'L', text: 'Lorem Ipsum'}]" value="L" />
        </ui-form-item>
        <ui-form-item :columns="6" label="Lorem Ipsum">
          <lego-dropdown :items="[{value: 'L', text: 'Lorem Ipsum'}]" value="L" />
        </ui-form-item>
        <ui-form-item :columns="6" label="Lorem Ipsum">
          <lego-dropdown :items="[{value: 'L', text: 'Lorem Ipsum'}]" value="L" />
        </ui-form-item>
      </ui-form-row>
      <ui-form-row>
        <ui-form-item :columns="6" label="Lorem Ipsum">
          <lego-dropdown :items="[{value: 'L', text: 'Lorem Ipsum'}]" value="L" />
        </ui-form-item>
        <ui-form-item :columns="6" label="Lorem Ipsum">
          <lego-dropdown :items="[{value: 'L', text: 'Lorem Ipsum'}]" value="L" />
        </ui-form-item>
        <ui-form-item :columns="6" label="Lorem Ipsum">
          <lego-dropdown :items="[{value: 'L', text: 'Lorem Ipsum'}]" value="L" />
        </ui-form-item>
      </ui-form-row>
      <ui-form-row>
        <ui-form-item :columns="6" label="Lorem Ipsum">
          <lego-dropdown :items="[{value: 'L', text: 'Lorem Ipsum'}]" value="L" />
        </ui-form-item>
        <ui-form-item :columns="6" label="TODO : 시간도" required-left>
          <lego-date-picker v-model="dateValue" />
        </ui-form-item>
        <ui-form-item :columns="8" align-right margin-right>
          <lego-button main>Lorem</lego-button>
        </ui-form-item>
      </ui-form-row>
    </ui-form-box>
  </div>
</template>

<script>
export default {
  name: "Search"
};
</script>

<style scoped>
</style>