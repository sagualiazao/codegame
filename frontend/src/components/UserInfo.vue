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
            <p>{{ this.$store.state.userNickName }}</p>
            <el-button type="text" @click="changeName()" :title="$store.state._const.CLICK_TO_CHANGE_NICKNAME">
                {{ $store.state._const.CHANGE_NICKNAME }}
            </el-button><br>
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
                {{ $store.state._const.REMAINED_LEVELS }}
            </span>
            <p>{{ remainedLevel }}</p>
        </div>
        <el-button type="text" @click="resetPasswordChange()" :title="$store.state._const.CLICK_TO_CHANGE_PASSWORD">
            {{ $store.state._const.RESET_PASSWORD }}
        </el-button>
        <el-dialog :title="$store.state._const.RESET_PASSWORD" :visible.sync="$store.state.changePasswordDialog" size="tiny">
            <reset-password-form></reset-password-form>
        </el-dialog>
    </div>
</div>
</template>

<script>
/**
* UserInfo 用户信息界面
*
* @class UserInfo
*/
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '@/assets/js/store.js'
import ResetPasswordForm from './ResetPasswordForm'
import { simplePost } from '@/assets/js/util.js'
import { Message } from 'element-ui'

export default {
    name: 'user-info',
    store: store,
    components: {
        ResetPasswordForm
    },
    data: function () {
        return {
            /**
            *已经完成的关卡数
            *
            * @property finishedLevel
            * @type {Number}
            */
            finishedLevel: null,
            /**
            *未完成的关卡数
            *
            * @property remainedLevel
            * @type {Number}
            */
            remainedLevel: null,
            /**
            *昵称
            *
            * @property nickname
            * @type {String}
            */
            nickname: null
        }
    },
    /**
    *
    *vue组件的mounted函数, 判断登录状态, 调用初始化函数
    *
    *@method mounted
    */
    mounted: async function () {
        if (this.$store.state.loginStatus === false) {
            await this.$store.dispatch('signin')
            if (await this.$store.state.loginStatus === false) {
                this.$message(this.$store.state._const.LOGIN_FIRST)
                this.$router.push('/')
            } else {
                this.init()
            }
        } else {
            this.init()
        }
    },
    methods: {
        /**
        *初始化函数, 读取当前用户的昵称等信息
        *
        *@method init
        */
        init: function () {
            this.finishedLevel = this.$store.state.userGameProgress
            this.remainedLevel = 15 - this.finishedLevel
            this.nickname = this.$store.state.userNickName
        },
        /**
        *更改昵称
        *
        *@method changeName
        */
        changeName () {
            this.$prompt('请输入昵称', '修改昵称', {
                confirmButtonText: '确定',
                cancelButtonText: '取消'
            }).then(({ value }) => {
                this.nickname = value
                this.nameSubmit()
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '取消输入'
                })
            })
        },
        /**
        *更改昵称提交
        *
        *@method nameSubmit
        */
        nameSubmit: async function () {
            let response = await simplePost('api/change-nickname', {
                'nickname': this.nickname
            })
            let obj = await response.json()
            if (await obj.status === '1') {
                this.$store.commit('changeUserNickName', this.nickname)
                Message.success({message: this.$store.state._const.CHANGE_SUCCESS})
            } else {
                Message.error({message: this.$store.state._const.CHANGE_FALURE})
            }
        },
        /**
        *更改密码响应
        *
        *@method resetPasswordChange
        */
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
    text-align: center;
}
.user-info {
    margin-top: -30px;
    background: url(../assets/img/infobackgro1.png) no-repeat 0px center;
    background-size: cover;
    width: 100%;
    text-align: justify;
}
.el-button {
    font-size: 20px;
}
h2, p, span, i, input, .el-button {
    position: relative;
    left: 10%;
}
.el-button:hover {
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
    width: 15%;
    height: 15%;
}
.base-info p, .game-info p {
    border-radius: 30px;
    border: 18px solid transparent;
    border-image: url(../assets/img/border10.png) 100 120 round;
    /*border: 2px solid #708090;*/
    /*margin-right: 600px;*/
    width: 35%;
}
#img-id {
    float: right;
    margin-right: 10%;
    transition: width 2s,height 2s,transform 2s;
    border: 1px solid #BFBFBF;
    box-shadow: 2px 2px 3px #aaaaaa;
}
#img-id:hover {
    width: 20%;
    height: 20%;
    transform: skewX(30deg),skewY(50deg);
    transform: rotate(360deg);
}
@keyframes myfirst {
    from {background:#F0E6BC;}
    to {background:#7FFFD4;}
}

</style>
