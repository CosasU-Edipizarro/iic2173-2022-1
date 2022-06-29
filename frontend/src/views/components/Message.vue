<template>
  <div>
    <div class="message" v-for="(message,index) in messages" v-bind:key="index" :class="{own: message.emitter != emitter}">

      <div class="username" v-if="index>0 && messages[index-1].emitter != message.emitter && message.emitter != emitter">
      {{ username }}</div>
      <div class="username" v-if="index == 0 && message.emitter != emitter">{{ username }}</div>

      <div class="username" v-if="index>0 && messages[index-1].emitter != message.emitter && message.emitter == emitter">
      {{emitter_username }}</div>
      <div class="username" v-if="index == 0 && message.emitter == emitter">{{ emitter_username }}</div>

      <div style="margin-top: 5px"></div>
      <div class="content">
        <!-- <div v-html="message.content"></div> -->
        <div > <p v-if="message.sentiment">[{{ message.sentiment }}]</p> {{ message.content }} </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    data () {
      return {}
    },
    props: [
      'messages'
    ],
    computed: {
      emitter () {
        return this.$cookies.get("other_user_uuid")
      },
      username () {
        return this.$cookies.get("username")
      },
      emitter_username() {
        return this.$cookies.get("other_user_username")
      }
    },
    mounted: function() {
      console.log('Messages: ');
      console.log(this.messages);
    }
  }
</script>

<style>
  span.emoji {
    font-size: 20px;
    vertical-align: middle;
    line-height: 2;
  }
</style>