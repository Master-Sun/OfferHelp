from captcha.fields import CaptchaField
from django import forms

from user.models import UserProfile


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='密码', widget=forms.PasswordInput, min_length=6, max_length=24)
    password2 = forms.CharField(label='再次输入密码', widget=forms.PasswordInput)
    # 在form表单中设置前端的样式属性
    # email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码', error_messages={'invalid': '验证码错误'})    # 图形验证码


    class Meta:
        model = UserProfile
        fields = ('username', 'nick_name', 'password', 'password2', 'captcha')

    # def clean_password(self):
    #     cd = self.cleaned_data    # 拿到表单中所有字段的数据
    #     print(cd)
    #     if cd['password'] != cd['password2']:
    #         raise forms.ValidationError("两次密码不一致")
    #     if len(cd['password']) < 8:
    #         raise forms.ValidationError("密码长度不得小于8位")
    #     return cd['password']

    # 额外增加的字段不会出现在cleaned_data字典中，必须定义了对应字段的clean方法才会出现
    # 因此此处定义了清洗password2的方法，否则拿不到password2的值
    # 另外已经被清洗过的字段会从cleaned_data字典中移除，因此这里将password的清洗动作合并到了password2中
    def clean_password2(self):
        cd = self.cleaned_data
        print(cd)
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("两次密码不一致")
        if len(cd['password']) < 6:
            raise forms.ValidationError("密码长度不得低于6位")
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码', widget=forms.PasswordInput)