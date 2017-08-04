<template>
    <div>
        <el-form :model="ruleForm2" :rules="rules2" ref="ruleForm2" label-width="100px" class="demo-ruleForm">
            <el-form-item label="邮箱" prop="email">
                <el-input v-model.number="ruleForm2.email"></el-input>
            </el-form-item>        
            <el-form-item label="密码" prop="pass">
                <el-input type="password" v-model="ruleForm2.pass" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('ruleForm2')">提交</el-button>
                <el-button @click="resetForm('ruleForm2')">重置</el-button>
            </el-form-item>
          </el-form>
    </div>
</template>
<script>
  export default {
      name: 'signin-form',
      data () {
          var validatePass = (rule, value, callback) => {
              if (value === '') {
                  callback(new Error('请输入密码'))
              } else {
                  // if (this.ruleForm2.checkPass !== '') {
                  //     this.$refs.ruleForm2.validateField('checkPass')
                  // }
                  callback()
              }
          }
          return {
              ruleForm2: {
                  email: '',
                  pass: ''
              },
              rules2: {
                  email: [
                      { required: true }
                  ],
                  pass: [
                      { required: true, validator: validatePass, trigger: 'blur' }
                  ]
              }
          }
      },
      methods: {
          submitForm (formName) {
              this.$refs[formName].validate((valid) => {
                  if (valid) {
                      alert('submit!')
                  } else {
                      console.log('error submit!!')
                      return false
                  }
              })
          },
          resetForm (formName) {
              this.$refs[formName].resetFields()
          }
      }
  }
</script>