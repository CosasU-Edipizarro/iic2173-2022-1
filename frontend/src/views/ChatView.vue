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
      console.log("This are the saved cookies")
      console.log('chat_token: ', this.$cookies.get('chat_token'));
      console.log('room_id: ', this.$cookies.get('room_id'));
      console.log("Starting connection to WebSocket Server");
      this.connection = new WebSocket(`${window.ws_hostname}/chat`)
    },
    mounted: function() {
      const deez = this;
      this.connection.onmessage = async function(event) {
        let response = (JSON.parse(event.data)).data;
        if (response.emitter) {
          response.sentiment = await deez.getSentiment(response.content);
          deez.chatMessages.push(response);
        }
      }
      const chat_token = this.$cookies.get('chat_token');
      const room_id = this.$cookies.get('room_id');

      this.connection.onopen = function(event) {
        console.log(event)
        console.log("Successfully connected to the echo websocket server...")
        
        this.send(JSON.stringify({"type":"token", "content": chat_token}));
        this.send(JSON.stringify({"type":"select_room", "room_id": room_id}));
      }
    },
    methods: {
      async loadChat () {
        var requestOptions = {
          method: 'GET',
          mode: "cors",
          redirect: 'follow'  
        };
        await fetch(`${window.chat_hostname}/rooms/${this.room_id}`, requestOptions)
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
          this.connection.send(JSON.stringify({"type":"message", "content": this.content}));
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
      },
      async getSentiment (text) {
        let myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        let requestOptions = {
          method: 'GET',
          headers: myHeaders,
          redirect: 'follow',
          mode: 'no-cors'
        };
        let data;
        console.log("ANTES DE REQUEST")
        await fetch(`${window.sentiment}?text=${text}`, requestOptions)
          .then((result) => {
            console.log('getSentiment');
            console.log(result);
            console.log(result.json());
            data = result;
          })
          .catch(error => console.log('error', error));
        return data;
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