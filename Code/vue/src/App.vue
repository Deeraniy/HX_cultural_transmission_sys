<script setup>
import router from "@/router.js";
import ReportGeneration from "@/components/ReportGeneration/ReportGeneration.vue";
import test from "@/components/Test.vue"
</script>

<template>
  <div id="app">
    <router-view/>
<!--    <test/>-->
  </div>
</template>

<style scoped>
#app{

}

header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
