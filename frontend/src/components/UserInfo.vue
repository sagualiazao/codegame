<template>
<div class="user-info">
    <h1>个人主页</h1>
    <div>
        <el-tabs v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="基本信息" name="base-tab" class="base-info">
                <img src="../assets/h1.jpg" id="img-id">
                <i class="el-icon-date"></i>
                <span>昵称</span>
                <p>{{ userNickName }}</p>
                <i class="el-icon-message"></i>
                <span>邮箱地址</span>
                <p>{{ userEmail }}</p>
                <i class="el-icon-date"></i>
                <span>注册日期</span>
                <p>{{ registerDate }}</p>
            </el-tab-pane>
            <el-tab-pane label="游戏信息" name="game-tab" class="game-info">
                <span>已完成的关卡数</span>
                <p>{{ finishedLevel }}</p>
                <span>剩下的关卡数</span>
                <p>{{ remainedLevel }}</p>
            </el-tab-pane>
            <el-tab-pane label="收藏的地图" name="map-tab" class="map-info">
                <img src="../assets/pc1.jpg">
                <img src="../assets/pc2.jpg">
                <img src="../assets/pc3.jpg">
                <img src="../assets/pc4.jpg">
            </el-tab-pane>
            <el-tab-pane label="账号设置" name="set-account-tab" class="set-account">
                <form id="change-name-form" method="post">
                    <p><h2>修改昵称</h2><br>
                        <input type="text" placeholder="请输入昵称" maxlength="16" v-model="nickname">
                        <input type="button" @click="nameSubmit()" value="确认">
                    </p>
                </form>
                <form id="change-password-form" method="post">
                    <p><h2>修改密码</h2><br>
                        <label>现在的密码</label><br>
                        <input type="password" v-model="verifyPassword">
                        <br>
                        <label>新密码</label><br>
                        <input type="password" placeholder="请输入新密码，可使用数字\字母\下划线" maxlength="16" v-model="userPassword">
                        <br>
                        <label>确认密码</label><br>
                        <input type="password" placeholder="请再次输入新密码" maxlength="16" v-model="checkPassword">
                        <input type="button" @click="passwordSubmit()" value="确认">
                    </p>
                </form>
            </el-tab-pane>
        </el-tabs>
    </div>
    <h2>这是用户信息!</h2>
</div>
</template>

<script>
export default {
    name: 'user-info',
    data: function () {
        return {
            finishedLevel: '',
            remainedLevel: '',
            activeName: 'base-tab',
            nickname: '',
            userNickName: this.$parent.$store.state.userNickName,
            userEmail: this.$parent.$store.state.userEmail,
            registerDate: this.$parent.$store.state.registerDate
        }
    },
    methods: {
        handleClick (tab, event) {
        },
        nameSubmit: function () {
            this.$parent.$store.commit('changeUserNickName', this.nickname)
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
    width: 1250px;
    height: 800px;
    left: 100px;
    margin-top: 80px;
    text-align: justify;
}
.user-info {
    margin-top: -30px;
    background-color: #F0E6BC;
    animation: myfirst 3s;
}
h1, p, span, i, form {
    position: relative;
    left: 100px;
}
h2 {
    margin-bottom: -8px;
}
img {
    width: 200px;
    height: 200px;
}
.base-info p, .game-info p{
    border: 2px solid #708090;
    margin-right: 600px;
}
#img-id {
    float: right;
    margin-right: 80px;
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
