<template>
<div class="user-info">
    <h1>个人主页</h1>
    <div>
        <div class="base-info">
            <img src="../assets/img/h1.jpg" id="img-id">
            <i class="el-icon-date"></i>
            <span>昵称</span>
            <p>{{ this.$store.state.userNickName }}</p>
            <i class="el-icon-message"></i>
            <span>邮箱地址</span>
            <p>{{ this.$store.state.userEmail }}</p>
            <i class="el-icon-date"></i>
            <span>注册日期</span>
            <p>{{ this.$store.state.registerDate }}</p>
        </div>
        <div class="game-info">
            <span>已完成的关卡数</span>
            <p>{{ finishedLevel }}</p>
            <span>剩下的关卡数</span>
            <p>{{ remainedLevel }}</p>
        </div>
        <p><h2>修改昵称</h2><br>
            <input type="text" placeholder="请输入昵称" maxlength="16" v-model="nickname">
            <input type="button" @click="nameSubmit()" value="确认" id="btn">
        </p>
        <a href="#UserInfo" @click="resetPasswordChange()">修改密码</a>
        <el-dialog title="修改密码" :visible.sync="$store.state.changePasswordDialog" size="tiny">
            <reset-password-form></reset-password-form>
        </el-dialog>
    </div>
    <h2>这是用户信息!</h2>
</div>
</template>

<script>
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '@/assets/js/store.js'
import ResetPasswordForm from './ResetPasswordForm'

export default {
    name: 'user-info',
    store: store,
    components: {
        ResetPasswordForm
    },
    data: function () {
        return {
            finishedLevel: '',
            remainedLevel: '',
            activeName: 'base-tab',
            nickname: ''
        }
    },
    mounted () {
        if (this.$store.state.loginStatus === false) {
            alert('请先登录噢!')
            this.$router.push('/')
        }
    },
    methods: {
        nameSubmit: function () {
            this.$store.commit('changeUserNickName', this.nickname)
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
.base-info p, .game-info p{
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
