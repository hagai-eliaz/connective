<template>
  <v-card
    class="my-15 mx-auto px-sm-10 py-sm-10"
    max-width="1000"
    :min-height="$vuetify.breakpoint.mobile ? 350 : 500"
    :elevation="$vuetify.breakpoint.mobile ? 0 : 3"
  >
    <v-card-title
      class="text-sm-h4"
      v-text="$t('events.unsummarizedPastEvents')"
    />
    <v-card-subtitle
      class="text-md-h6 pt-3"
      v-text="$t('events.clickAnEventToSummarizeIt')"
    />
    <click-list
      v-if="formattedEvents.length"
      v-model="selected"
      class="my-12"
      :title="$t('events.eventsToSummarize')"
      :items="formattedEvents"
      @input="onEventClick"
    />
    <div v-else class="text-center text-md-h6 absolute-center text-body-1" v-text="$t('events.eventsToSummarizeWereNotFound')" />
  </v-card>
</template>

<script>
import store from "../vuex/store"
import moment from "moment"
import { mapState } from "vuex"
import ClickList from "../components/ClickList"
export default {
  components: { ClickList },
  data() {
    return {
      selected: [],
      isEventClicked: false,
    }
  },
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("instructorEvent/getPastEvents", { daysAgo: 60, unsummarizedOnly: true })
    next()
  },
  computed: {
    ...mapState("instructorEvent", ["eventList"]),
    formattedEvents() {
      return this.eventList
        .filter(event => !event.hasSummary)
        .map(event => ({
          action: moment(event.startTime).format("DD.MM.YYYY"),
          subtitle: event.activityName,
          title: event.schoolGroupName,
        }))
    },
  },
  methods: {
    onEventClick(e) {
      // extract event slug & route to event summary
      if (this.isEventClicked) return
      this.isEventClicked = true
      const eventPos = e[0]
      this.$router.push({
        name: "InstructorEventSummary",
        params: { slug: this.eventList[eventPos].slug },
      })
    },
  },
}
</script>
