<template>
  <div class="pa-10">
    <route-tabs :tabs="tabs" />
    <v-row>
      <v-col class="mx-auto" sm="11" lg="9">
        <router-view />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import RouteTabs from "../../components/RouteTabs"

export default {
  components: { RouteTabs },
  data() {
    return {
      tabs: [
        {
          componentName: "MyGroups",
          text: this.$t("myActivity.activeGroups"),
        },
        {
          componentName: "MyEvents",
          text: this.$t("events.eventsBoard"),
        },
        {
          componentName: "CoordinatorStatistics",
          text: this.$t("myActivity.statistics"),
        },
      ],
    }
  },
}
</script>
