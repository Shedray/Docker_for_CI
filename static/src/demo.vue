<template>
  <div id="terminal">
    <h1>web socket</h1>
    <div id="terminal"></div>
  </div>
</template>
<script>
import "xterm/dist/xterm.css";
import { Terminal } from "./Xterm";
//import {terminal}from ‘terminal-kit‘

export default {
  name: "terminal",

  data() {
    return {};
  },
  methods: {
    runRealTerminal () {
      console.log('webSocket is finished')
    },
    errorRealTerminal () {
      console.log('error')
    },
    closeRealTerminal () {
      console.log('close')
    }
  },
  updated() {},
  mounted(){

  },
  created() {
    var arrayBuffer = "";
    var webssh = new Terminal();
    webssh.open(document.getElementById("terminal"));
    var websshSocket = new WebSocket('ws://127.0.0.1:8888/ws')
    console.log(websshSocket);
    webssh.attach(websshSocket)
  }
};
</script>

<style rel="stylesheet/css" scoped>
</style>