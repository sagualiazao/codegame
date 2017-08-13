<template>
<div>
    <div class="main-page">
        <div id="button-container">
            <button id="start-game" @click="clickTest('BlockBase')">开始游戏</button>
        </div>
    </div>
    <div id="intro">
        <p id="game-wordintro">让孩子在游戏中走进编程世界，没有压力，开启头脑风暴</p>
        <div id="pic-intro">
            <div id="intro1" class="introduction">
                <p>description1</p>
            </div>
            <div id="intro2" class="introduction">
                <p>description2</p>
            </div>
            <div id="intro3" class="introduction">
                <p>description3</p>
            </div>
            <div id="intro4" class="introduction">
                <p>description4</p>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '../assets/js/store'

export default {
    name: 'main-page',
    store: store,
    data: function () {
        return {
            msg: '看到这行字，说明它正常了'
        }
    },
    methods: {
        clickTest (text) {
            this.$router.push('/' + text)
        },
        handleSelect (index) {
            this.$store.commit('changeView', index)
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
    font-weight: normal;
}
.main-page {
    width: 1250px;
    height: 600px;
    margin-top: -22px;
    background: url(../assets/backg.jpg) no-repeat 0px center;
}
#intro {
    width: 1250px;
    height: 400px;
    margin-top: -22px;
    background-color: #F0FFFF;
}
#start-game {
    width: 200px;
    height: 60px;
    border-radius: 50em;
    border-width: 0px;
    background-color: #8FBC8F;
    font-size: 1.7em;
}
#button-container {
    padding-top: 400px;
}

#game-wordintro {
    color: #00CED1;
    font-size: 1.5em;
    padding-top: 50px;
}
#pic-intro {
    width: 1250px;
    height: 300px;
    background-color: grey;
    display: inline-flex;
}
.introduction {
    width: 312.5px;
    height: 200px;
}
#intro1 {
    background: url(../assets/backg.jpg) no-repeat 0px center;
}
#intro2 {
    background: url(../assets/desp1.png) no-repeat 0px center;
}
#intro3 {
    background: url(../assets/desp2.jpg) no-repeat 0px center;
}
#intro4 {
    background: url(../assets/desp3.jpg) no-repeat 0px center;
}
</style>
