<template>
  <v-container fluid style="padding: 0;">
    <v-row no-gutters>
      <v-col sm="10" style="position: relative;">
        <div class="chat-container" v-on:scroll="onScroll" ref="chatContainer" >
          <message :messages="messages" @imageLoad="scrollToEnd"></message>
        </div>
        <div class="typer">
          <input type="text" placeholder="Escribe aqui..." v-on:keyup.enter="sendMessage" v-model="content">
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import Message from './components/Message.vue'
  export default {
    data () {
      return {
        content: '',
        chatMessages: [],
        emojiPanel: false,
        currentRef: {},
        loading: false,
        totalChatHeight: 0,
        connection: null
      }
    },
    props: [
      'room_id'
    ],
    //mounted () {
      //this.loadChat()
      //this.$store.dispatch('loadOnlineUsers')
    //},
    components: {
      'message': Message
    },
    computed: {
      messages () {
        return this.chatMessages
      },
      username () {
        return "hola"
      },
    },
    created: function() {
      console.log("Starting connection to WebSocket Server")
      //this.connection = new WebSocket("ws://localhost:9229/chat")
      //this.connection.send({"type":"select_room", "room_id": this.room_id});

      // this.connection.onmessage = function(event) {
      //   console.log(event);
      // }

      // this.connection.onopen = function(event) {
      //   console.log(event)
      //   console.log("Successfully connected to the echo websocket server...")
      // }

    },
    methods: {
      async loadChat () {
        var requestOptions = {
          method: 'GET',
          mode: "cors",
          redirect: 'follow'  
        };
        await fetch(`${window.chat_hostname}/room/${this.room_id}`, requestOptions)
          .then(response => response.json())
          .then(data => { this.messages = data; console.log(this.users); })
          .then(() => { this.loaded = true; })
          .catch(error => console.log('error', error));
      },
      onScroll () {
        let scrollValue = this.$refs.chatContainer.scrollTop
        const that = this
        if (scrollValue < 100 && !this.loading) {
          this.totalChatHeight = this.$refs.chatContainer.scrollHeight
          this.loading = true
          let chatID = this.id
          let currentTopMessage = this.chatMessages[0]
          if (currentTopMessage === undefined) {
            this.loading = false
            return
          }
        }
      },
      sendMessage () {
        if (this.content !== '') {
          console.log(this.connection);
          //this.connection.send({"type":"message", "msg": this.content});
          this.messages.push({"user": "hola", "message": this.content})
          this.content = ''
        }
      },
      scrollToEnd () {
        this.$nextTick(() => {
          var container = this.$el.querySelector('.chat-container')
          container.scrollTop = container.scrollHeight
        })
      },
      scrollTo () {
        this.$nextTick(() => {
          let currentHeight = this.$refs.chatContainer.scrollHeight
          let difference = currentHeight - this.totalChatHeight
          var container = this.$el.querySelector('.chat-container')
          container.scrollTop = difference
        })
      }
    }
  }
</script>

<style>
  .scrollable {
    overflow-y: auto;
    height: 90vh;
  }
  .typer{
    box-sizing: border-box;
    display: flex;
    align-items: center;
    bottom: 0;
    height: 4.9rem;
    width: 100%;
    background-color: #fff;
    box-shadow: 0 -5px 10px -5px rgba(0,0,0,.2);
  }
  .typer input[type=text]{
    position: absolute;
    left: 2.5rem;
    padding: 1rem;
    width: 80%;
    background-color: transparent;
    border: none;
    outline: none;
    font-size: 1.25rem;
  }
  .chat-container{
    box-sizing: border-box;
    height: calc(100vh - 9.5rem);
    overflow-y: auto;
    padding: 10px;
    background-color: #f2f2f2;
  }
  .message{
    margin-bottom: 3px;
  }
  .message.own{
    text-align: right;
  }
  .message.own .content{
    background-color: lightskyblue;
  }
  .chat-container .username{
    font-size: 18px;
    font-weight: bold;
  }
  .chat-container .content{
    padding: 8px;
    background-color: lightgreen;
    border-radius: 10px;
    display:inline-block;
    box-shadow: 0 1px 3px 0 rgba(0,0,0,0.2), 0 1px 1px 0 rgba(0,0,0,0.14), 0 2px 1px -1px rgba(0,0,0,0.12);
    max-width: 50%;
    word-wrap: break-word;
    }
  @media (max-width: 480px) {
    .chat-container .content{
      max-width: 60%;
    }
  }
</style>