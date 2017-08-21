<template>
<div class="user-info">
    <h1>
        {{ $store.state._const.PERSONAL_INFORMATION }}
    </h1>
    <div>
        <div class="base-info">
            <img src="../assets/img/h1.jpg" id="img-id">
            <i class="el-icon-date"></i>
            <span>
                {{ $store.state._const.NICKNAME }}
            </span>
            <p>
                <input type="text" :placeholder="$store.state._const.NEED_NICKNAME" maxlength="16" v-model="nickname">
                <input type="button" @click="nameSubmit()" :value="$store.state._const.CONFIRM" id="btn">
            </p>
            <i class="el-icon-message"></i>
            <span>
                {{ $store.state._const.EMAIL }}
                </span>
            <p>{{ this.$store.state.userEmail }}</p>
            <i class="el-icon-date"></i>
            <span>
                {{ $store.state._const.REGISTER_DATE }}
            </span>
            <p>
                {{ this.$store.state.registerDate }}
            </p>
        </div>
        <div class="game-info">
            <span>
                {{ $store.state._const.GAME_PROGRESS }}
            </span>
            <p>{{ finishedLevel }}</p>
            <span>
                {{ $store.state._const.REMAIND_LEVELS }}
            </span>
            <p>{{ remainedLevel }}</p>
        </div>
        <a href="#UserInfo" @click="resetPasswordChange()">
            {{ $store.state._const.RESET_PASSWORD }}
        </a>
        <el-dialog :title="$store.state._const.RESET_PASSWORD" :visible.sync="$store.state.changePasswordDialog" size="tiny">
            <reset-password-form></reset-password-form>
        </el-dialog>
    </div>
</div>
</template>

<script>
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '@/assets/js/store.js'
import ResetPasswordForm from './ResetPasswordForm'
import { simplePost } from '@/assets/js/util.js'

export default {
    name: 'user-info',
    store: store,
    components: {
        ResetPasswordForm
    },
    data: function () {
        return {
            finishedLevel: null,
            remainedLevel: null,
            nickname: null
        }
    },
    mounted: async function () {
        if (this.$store.state.loginStatus === false) {
            await this.$store.dispatch('signin')
            if (await this.$store.state.loginStatus === false) {
                alert(this.$store.state._const.LOGIN_FIRST)
                this.$router.push('/')
            } else {
                this.init()
            }
        } else {
            this.init()
        }
    },
    methods: {
        init: function () {
            this.finishedLevel = this.$store.state.userGameProgress
            this.remainedLevel = 15 - this.finishedLevel
            this.nickname = this.$store.state.userNickName
        },
        nameSubmit: async function () {
            let response = await simplePost('api/change-nickname', {
                'nickname': this.nickname
            })
            let obj = await response.json()
            if (await obj.status === '1') {
                this.$store.commit('changeUserNickName', this.nickname)
                alert(this.$store.state._const.OPERATION_SUCCESS)
            } else {
                alert(this.$store.state._const.OPERATION_FAILURE)
            }
        },
        resetPasswordChange: function () {
            this.$store.commit('changePasswordWindow', true)
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

h1 {
    font-weight: normal;
    color: #A0522D;
}
div {
    width: 1500px;
    left: 100px;
    margin-top: 80px;
    text-align: justify;
}
.user-info {
    margin-top: -20px;
    /*background-color: #b4e2f4;*/
    background: url(../assets/img/infobackgro1.png) no-repeat 0px center;
    background-size: contain;
    /*animation: myfirst 3s;*/
}
#btn {
    background-image: url(../assets/img/border3.jpg);
}
h1, h2, p, span, i, a, input {
    position: relative;
    left: 160px;
}
a:hover {
    color: #FF00FF;
    text-decoration: underline;
}
span {
    font-size: 20px;
    color: #FA2D6A;
}
p {
    font-size: 20px;
    color: black;
}
h2 {
    margin-bottom: -8px;
    font-size: 18px;
    color: #FA8072;
}
img {
    width: 200px;
    height: 200px;
}
.base-info p, .game-info p, .base-info input{
    border-radius: 30px;
    /*border: 8px solid black;
    border-image: url(../assets/img/border8.png) repeat;*/
    border: 2px solid #708090;
    margin-right: 600px;
    width: 500px;
}
#img-id {
    float: right;
    margin-right: 200px;
    transition: width 2s,height 2s,transform 2s;
    border: 1px solid #BFBFBF;
    box-shadow: 2px 2px 3px #aaaaaa;
}
#img-id:hover {
    width: 300px;
    height: 300px;
    transform: skewX(30deg),skewY(50deg);
    transform: rotate(360deg);
}
@keyframes myfirst {
    from {background:#F0E6BC;}
    to {background:#7FFFD4;}
}

</style>
