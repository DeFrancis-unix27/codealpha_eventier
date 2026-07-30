from django import forms

from .models import CustomUser,Attendee,Event,CustomField,CustomAnswer

class RegistrationForm(forms.ModelForm):
    conf_pass = forms.CharField(
        # include widget
        widgets = forms.PasswordInput(
            attrs={
                "class":"reg_form"
                "placeholder":"Confirm your Password please"
            }
            
        ) # end of the widget
        label="confirm password"
    )
    class Meta:
        model = CustomUser
        fields = [
            "firstname",
            "lastname",
            "user_email",
            "username",
            "password"
        ]

        labels = [
            "user_email":"email address"
        ]

        widgets = {
            "firstname":forms.TextInput(attrs={
                                            "class":"reg_form",
                                           "placeholder":"Your Firstname Please"
                                        })
            "lastname":forms.TextInput(attrs={
                                          "class":"reg_form",
                                          "placeholder":"Your Lastname Please"
                                      })
            "user_email":forms.EmailInput(attrs={
                                              "class":"reg_form",
                                              "placeholder":"Your Email Address PLease"
                                          })
            "password":forms.PasswordInput(attrs={
                                           "class":"input_form",
                                           "placeholder":"your password here please"
                                         })
        }

    def clean(self):
        cleaned_data = super.clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("conf_pass")
        email = cleaned_data.get("user_email")
        username = cleaned_data.get("username")
        if password and confirm_password:
            if confirm_password != password:
                self.add_error(
                    "confirm_password", "password don't match"
                )
        if email and username:
            if Custom_User.objects.filter(user_email=email).exists():
                self.add_error(
                    "user_email":"email has been registerd before"
                )
            if Custom_User.objects.filter(username=username).exists():
                self.add_error(
                    "username":"username taken"
                )
                
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(
        label="username"
        widgets=TextInput(
            attrs={
                "class":"login_form",
                "placeholder":"mark benson"
            }
        )
    )
    password = forms.CharField(
        label="password"
        widgets=PasswordInput(
            attrs={
                "class":"login_form",
                "placeholder":"***********"
            }
        )
    )

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = [
            "banner",
            "title",
            "description",
            "start_date",
            "end_date"
        ]

        widgets = {
         "banner":forms.FileInput(
             attrs={
                 "class":"event_file",
                 "placeholder":"upload image here"
             }
         )   
        "title":forms.TextInput(
            attrs={
                "class":"event_form",
                "placeholder":"event title"
            }
        )
        "description":forms.Textarea(
            attrs={
                "class":"event_form",
                "placeholder":"event description"
            }
        )
        "start_date":forms.DateTimeInput(
            attrs={
                "class":"event_form"
            }
        )
        "end_date":forms.DateTimeInput(
            attrs={
                "class":"event_form"
            }
        )
        }

class CustomFieldForm(forms.ModelForm):
    class Meta:
        model = CustomField
        fields = [
            "cartegory",
            "question",
            "field_type",
            "choice",
            "required",
            "order"
        ]

        labels = {
            "cartgory":"question type",
            "chioce":"option context"
        }
        help_texts={
            "choice":"use comma (,) to separate option context",
            "cartegory":"choose other to include your own text",
            "field_type":"choose anyone of this text, number, chioce",
            "order":"this help you organise where and how your question is to be displayed"
            
        }
        widgets = {
            "cartegory":forms.Select(
                attrs={
                    "class":"custom_form",
                    "id":"custom_form"
                }
            )

            "question":forms.TextInput(
                attrs={
                    "class":"custom_form",
                    "placeholder":"your questions"
                }
            )

            "field_type":forms.TextInput(
                attrs={
                    "class":"custom_form",
                    "placeholder":"text or chioce or number"
                    "id":"field_type"
                }
            )

            "choice": forms.TextInput(
                attrs={
                    "class":"custom_form",
                    "placeholder":"write down your context here"
                    "id":"choice"
                }
            )


            "required":forms.CheckInput(
                attrs={
                    "class":"custom_form",
                }
            )

            "order":forms.NumberInput(
                attrs={
                    "class":"custom_form"
                }
            )
        }       


class CustomAnswer(models.Model):
    class Meta:
        model = CustomAnswer
        fields = [
            "answer"
        ]

        widget = {
            "answer":forms.Textarea(
                attrs={
                    "class":"answer_form"
                }
            )
        }
