from django import forms

from user.models import UserProfile


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='再次输入密码', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('username', 'nick_name', 'password', 'password2')

    # def clean_password(self):
    #     cd = self.cleaned_data    # 拿到表单中所有字段的数据
    #     print(cd)
    #     if cd['password'] != cd['password2']:
    #         raise forms.ValidationError("两次密码不一致")
    #     if len(cd['password']) < 8:
    #         raise forms.ValidationError("密码长度不得小于8位")
    #     return cd['password']

    # 额外增加的字段不出出现在cleaned_data字典中，必须定义了对应字段的clean方法才会出现
    # 因此此处定义了清洗password2的方法，否则拿不到password2的值
    # 另外已经被清洗过的字段会从cleaned_data字典中移除，因此这里将password的清洗动作合并到了password2中
    def clean_password2(self):
        cd = self.cleaned_data
        print(cd)
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("两次密码不一致")
        if len(cd['password']) < 8:
            raise forms.ValidationError("密码长度不得低于8位")
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码', widget=forms.PasswordInput)